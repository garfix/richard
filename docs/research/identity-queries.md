The problem as I posed it to several LLM's:

> I am building a system modelling the semantics of natural language in predicate logic. Now I want to store this meaning as tuples in a relational database. But the identity of a person in one sentence, say $2, may be the same in another sentence as $4. So the same entity has two identifiers in the database. Now I want to query this database with a query that has one clause that would match the entity with $2, and another clause that matches the entity with $4. Do you understand? Has some system made this work? What are my options?

The LLM's (Claude Sonnet 4.6, Gemini 3, ChatGPT 5.2, LeChat) gave similar answers. I'll combine these here:

## Skolem-style identifiers

*Skolem-style identifiers* or *Skolem constants* (*logical variables*, *discourse referents*) is a term i hadn't heard of, but seems to be the thing I have been looking for. A skolem constant replaces an existentially bound variable with a constant `∃x` => `c`. Also *mention*.

## Co-reference resolution

The name for having two references to the same entity. "The core issue is that your logical form uses discourse referents (in the DRT/DRS tradition — Kamp & Reyle), and those referents are sentence-local. Stitching them together across sentences is the "merge" problem." (Claude)

You’ve hit on a classic challenge in Natural Language Processing (NLP) and Knowledge Representation: the problem of Entity Resolution (or Coreference Resolution) and how it maps to a Relational Schema. (Gemini)

## Systems that have tackled the problem

* **DRT/DRS** Kamp's DRS boxes use discourse referents, and merging boxes requires unifying co-referring referents. Implementations like Boxer (Bos et al.) produce logical forms and do co-reference resolution (Claude)
* **Cyc** stored propositions in a large relational-ish KB and dealt with this via a canonical entity ID layer — every surface-introduced referent got mapped to a GUID before assertion. (Claude)
* **Neo-Davidsonian event semantics systems** (e.g. in the Boeing/SRI Gemini lineage) stored eventuality and entity tuples and maintained a separate entity resolution table.
* *Knowledge graphs* Systems like Freebase (now part of Google), DBpedia, and YAGO use "Canonical URIs. (Gemini)
* *Reasoning Engines* Description Logic reasoners (like Pellet or HermiT) handle this using the `owl:sameAs` predicate, which explicitly tells the system that two different identifiers are functionally identical. (Gemini)

## Possible solutions

## Canonical entity table / The Union-Find Algorithm (Preprocessing) / Mentions

Maintain a separate table `entity_identity(local_id, canonical_id)`. Before inserting, run co-reference resolution and rewrite all local IDs to canonical ones. (Claude)

If you want to resolve these identities before they hit the database, you can use a Disjoint-set data structure. As you parse sentences, if you encounter a rule or a coreference model that says $2 = $4, you perform a Union operation. When inserting into the DB, you only insert the "Representative" of that set. (Gemini)

Not possible, because I don't know the canonical id at insert-time

Each variable ($2, $4) maps to a shared entity ID once you detect they refer to the same thing.

mention_id | entity_id | sentence_id | variable
-----------+-----------+-------------+---------
M1         | E17       | S1          | $2
M2         | E17       | S5          | $4

This is essentially how knowledge graphs like DBpedia Wikidata handle identity. (ChatGPT)

## The Mapping Table (The "SameAs" Approach)

Instead of trying to merge the rows physically (which is destructive), you maintain a Linkage Table. This allows you to keep the linguistic context of how the entity was referred to while querying across them. (Gemini)

How to query:
When you query, you JOIN your fact tables through this mapping table. This allows a query for $2 to "see" facts associated with $4 because they both share Canonical ID 1001. (Gemini)

Maybe. Sounds complicated, but possible.

Instead of replacing IDs, store equivalence between variables.

same_as
-------
id1 | id2
----+----
$2  | $4

SELECT *
FROM predicates p1
JOIN predicates p2
ON same_entity(p1.arg1, p2.arg1)

Systems that work this way include:
* Soufflé Datalog
* LogicBlox

(ChatGPT)

## Equality assertions as first-class tuples

Store `same_as($2, $4)` as a fact in your database, then write queries that chase equality. This is essentially what OWL's `owl:sameAs` does, and RDF triple stores (Jena, Stardog) handle it via same-as reasoning. Your query planner needs to treat same_as as an equivalence relation and unify across it — expensive without indexing, but very flexible. (Claude)

Think in three layers:

* Mention = one variable/token in one sentence ($2 in sentence 17).
* Entity = latent discourse individual you ultimately want to reason about.
* same_as = growing evidence that two mentions (or entities) refer to the same entity.

CREATE TABLE same_as_mention (
  m1 BIGINT NOT NULL REFERENCES mention(mention_id),
  m2 BIGINT NOT NULL REFERENCES mention(mention_id),
  source TEXT,            -- rule/model name, human annotation, etc.
  confidence REAL,        -- 0..1
  created_at TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (m1, m2)
);

(Perplexity)

## Union-Find structure alongside the DB

Maintain a union-find (disjoint set) structure over all identifiers. A query against $2 is first looked up in the union-find to get the root representative, and all DB lookups use the root. This is efficient and works well if co-reference is established incrementally (sentence by sentence). (Claude)

Not possible, I think, because I don't know which identifiers to query up front.

## Query rewriting

Leave the DB as-is with both $2 and $4, but at query time rewrite the query to include all known aliases. If you know `$2 ≡ $4`, a clause mentioning $2 becomes `$2 OR $4`. This is how some deductive databases (Datalog with equality) handle it. (Claude)

## Datalog with equality (most principled)

Use a Datalog engine that supports equality reasoning natively (e.g. Soufflé supports equivalence classes). You assert `eq($2, $4)` and define eq as an equivalence relation, then the engine handles unification transparently during query evaluation. This is arguably the most theoretically clean option for your use case. (Claude)

## Graph Databases (RDF / Triple Stores)

Since you are already working with predicate logic (essentially triples like $Relationship(Subject, Object)$), a Graph Database (like Neo4j or GraphDB) is often more natural than a Relational DB (SQL).In a graph, you simply draw an EQUIVALENT_TO edge between the two nodes.Queries can then use "Transitive Closure" to traverse these identity links automatically. (Gemini)

## View-Based Resolution

If you want to stay in SQL, you can create a Recursive Common Table Expression (CTE) or a View that collapses these identities on the fly. `Query(x) <- Fact(ID_1, ...) and SameAs(ID_1, ID_2) and Fact(ID_2, ...)` (Gemini)

    name(E1, 'Willa'), same_as(E1, E1alt) michelin_guide(E2), plan(pick_up(E1alt, E2))
    name(E1, 'Willa') # E1 yields $2, then postprocess the solve1 by creating an additional binding with $4

