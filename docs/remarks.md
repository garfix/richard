## 2024-06-15

Looking for other semantics parsers, I checked Sippycup once more ( https://github.com/wcmac/sippycup ). I know I have seen this before, so it must have influenced this library, but it probably was in a time that I didn't program in Python yet.

Anyway, seeing it again came as a huge shock. Not so much that its approach is largely similar to the one this library takes, but the fact that it presents multiple ways to deal with semantics. Each of its tutorial pages has a different semantic representation. 

In its third unit that deals with geographic queries https://nbviewer.org/github/wcmac/sippycup/blob/master/sippycup-unit-3.ipynb it takes the approach I have used here as well. The semantics of a rule consists of lambda functions, and these are combined to create the complete semantics.  So far so good.

The last few weeks I kept noticing how much easier it was to write semantics in NLI-GO, which uses a relational rather than a functional approach. And that previous approach had more advantages:

- as it iss declarative, it is data (atoms) and can be manipulated
- it can be used to store learned information. If the system has to learn a rule "all men are mortal", how is this knowledge to be persisted if it is in functional form?
- the atoms can be used to do generation
- the atoms can also be used to reorganize the semantics, as may be needed for scope resolution
- the atoms can be used to optimize the semantics for performance

At the same time I was rethinking my approach to database access. So far I worked with toy domains, and performance was not an issue. But one of the things I want the library to be able to do is answer questions like "How many customers have bought more than 2 products in the last month?" As this is about customers (let's say 10.000 and products (let's say 100.000), such a simple query would run my library to the ground immediately). The consequence is simple: I need my library to produce SQL / Sparql queries. It's the only way to reach any kind of performance. It's not all it should do, but it should be able to do it. And it should not produce SQL directly, it should do this based on the age old logical form: `(predicate arg arg)`, with nested arguments. It that possible?

===

It seems like that is very hard to do.

There are means of optimization. In stead of 10.000 x 100.000 queries, it's possible to do one query that leaves the relevant id's open. So this line of thought may not be as hopeless as it seems.

## 2024-06-09

What an impossible question ...

What are the continents no country in which contains more than two cities whose population exceeds 1 million?

What is the parse tree?

Let's check what Chat-80 itself produces...

~~~
whq
   B
   s
      np
         3+plu
         wh(B)
         []
      verb(be,active,pres+fin,[],pos)
      arg
         dir
         np
            3+plu
            np_head
               det(the(plu))
               []
               continent
            rel
               C
               s
                  np
                     3+sin
                     np_head
                        det(no)
                        []
                        country
                     pp
                        prep(in)
                        np
                           3+plu
                           wh(C)
                           []
                  verb(contain,active,pres+fin,[],pos)
                  arg
                     dir
                     np
                        3+plu
                        np_head
                           quant(more,nb(2))
                           []
                           city
                        rel
                           D
                           s
                              np
                                 3+sin
                                 np_head
                                    det(the(sin))
                                    []
                                    population
                                 pp
                                    poss
                                    np
                                       3+plu
                                       wh(D)
                                       []
                              verb(exceed,active,pres+fin,[],pos)
                              arg
                                 dir
                                 np
                                    3+sin
                                    np_head
                                       quant(same,nb(1))
                                       []
                                       million
                                    []
                              []
                  []
      []


~~~


## 2024-06-08

What are the countries from which a river flows into the Black_Sea?

This is a ditransitive verb phrase with subject and object reversed. I created a notation for the verb phrase that expresses both the order of the arguments and which ones are missing.

~~~python
    { "syn": "s -> 'what' 'are' np vp_noobj_sub_iob '?'", "sem": lambda np, vp_noobj_sub_iob: lambda: np(vp_noobj_sub_iob) },
    { "syn": "vp_noobj_sub_iob -> 'from' 'which' np vp_noobj_nosub_iob", "sem": lambda np, vp_noobj_nosub_iob: lambda obj: np(vp_noobj_nosub_iob(obj)) },
    { "syn": "vp_noobj_nosub_iob -> vp_noobj_nosub_noiob np", "sem": lambda vp_noobj_nosub_noiob, np: lambda obj: lambda sub: np(vp_noobj_nosub_noiob(obj)(sub)) },
    { "syn": "vp_noobj_nosub_noiob -> dtv", "sem": lambda dtv: lambda obj: lambda sub: lambda iob: dtv(sub, obj, iob) },
    { "syn": "dtv -> 'flows' 'into'", "sem": lambda: lambda sub, obj, iob: model.find_relation_values('flows-from-to', [sub, obj, iob]) },
~~~

To resume the semantics:

~~~python
lambda: np(vp_noobj_sub_iob)
lambda obj: np(vp_noobj_nosub_iob(obj))
lambda obj: lambda sub: np(vp_noobj_nosub_noiob(obj)(sub))
lambda obj: lambda sub: lambda iob: dtv(sub, obj, iob)
lambda sub, obj, iob: model.find_relation_values('flows-from-to', [sub, obj, iob])
~~~

There's beauty in this.

## 2024-06-05

Wow @ 

> Is there more than one country in each continent?

- per continent
    - find the countries in the continent
    - count them
    - more than one? yes / no
- are all of them yes?

The latter clause makes this sentence essentially different from the previous one. In stead of answering:

    Europe: yes
    America: yes
    Antartica: no

The expected answer is simply:

    No

===

These questions can benefit from the technique that an aggregate that fails is left out of the group by. In the previous question "Antarctica" was left out of Chat-80's results as it has no countries. If I leave don't add the continents to the group by that have no countries, I can answer the question by comparing the number of group-by elements with the number of continents. Not equal => "no".

The custom aggregation function could return `False` if it failed, or produced no results.

## 2024-06-04

An interesting sentence in Chat-80's dialog: 

> What is the average area of the countries in each continent?

It expects an answer like

    Europe: 500.000
    North America: 700.000
    Australia: 400.000

It is what would be a GROUP BY in SQL: `SELECT continent.name, AVG(country.area) OF country JOIN continent GROUP BY continent.id`. 

What does take to process it?

- in each continent
- collect the areas of the countries
- take the average of these areas

or

- collect all countries
- look up each country's area
- group by continent and average

Chat-80 does this:

- collect the continents
- collect the area per country
- average over the countries per continent

## 2024-05-31

The executionable meaning of the sentence "What is the ocean that borders African countries and that borders Asian countries?"

~~~python
lambda np: lambda: np()
    lambda det, nbar: create_np(det, nbar)
        lambda: exists
        lambda np, rc1, rc2: create_np(exists, lambda: range_and(np(rc1), np(rc2)))
            lambda: lambda: model.get_instances('ocean')
            lambda vp_no_sub: lambda subject: vp_no_sub(subject)
                lambda tv, np: lambda subject: np(tv(subject))
                    lambda: lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True)
                    lambda nbar: create_np(exists, nbar)
                        lambda adj, noun: lambda: adj(noun)
                            lambda: lambda range: model.filter_by_modifier(range, 'african')
                            lambda: lambda: model.get_instances('country')
            lambda vp_no_sub: vp_no_sub
                lambda tv, np: lambda subject: np(tv(subject))
                    lambda: lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True)
                    lambda nbar: create_np(exists, nbar)
                        lambda adj, noun: lambda: adj(noun)
                            lambda: lambda range: model.filter_by_modifier(range, 'asian')
                            lambda: lambda: model.get_instances('country')
~~~

## 2024-05-30

The big question was:

    np or np()

When creating grammar rules, should one use `np` (use the function) or `np()` (use the result of the function). I came up with the following rule:

1. If it is returned directly, use `np()`
2. If it is passed as an argument to a function, use `np`

## 2024-05-23

A relation is a combination of two or more entities of equivalent status. An attribute is a combination of two entities with subordinate status.

===

It _is_ possible to define a relation "of" without asserting an _attr_ category. And this involves en emphasis on the entities of the arguments:

    of(capital, country)

But going through all capitals just to find the capital of Greece is very inefficient, since it can be done with a simple lookup.

===

When looking for a relation, we can use the known entities as a retriction:

    capital of => of(capital, country)
    capital of => of(capital, state)

If `country` is known, this restricts the relations.

===

I think I'll introduce Range

    class Range:
        entity: str
        ids: list[str]

a combination of the entity ids with the name of the entity. I can use the entity to restrict things.

## 2024-05-22

I need to start thinking about events.

At some time you want to be able the question

    What was the capital of Greece in 1830?

===

I think I will leave events for the advanced section. Many projects can be done without events, and would complicate them. If you do events, you must do them everywhere, so this is something to consider at the start of a project. If will name this in the hints.

===

Think of deictic centers as contexts. If I could inject the current contexts (of time, place etc) into the dialog context, then I can inject it into the interpretation function as well. The advantage is that the grammar can stay simple, does not have to deal with time. Only the interpretation function then add time to the db query. Would that work?

## 2024-05-20

    What is the capital of Greece?
    Of which city is Athens the capital?

Relations between things. No good to iterate over all capitals.

I need a query that can be modified based on the context:

"capital of"

    select country_id, capital_id from country cn inner join city ci on ci.country_id = cn.id [where cn.id = 15]

"whose capital is"    

    select country_id, capital_id from country cn inner join city ci on ci.country_id = cn.id [where ci.id = 15]

A relation expressing a verb, used by `find`, will need both where clauses    

Only the where-clause changes.

## 2024-05-19

I added control blocks and release version 0.2.0. I'm renaming the good old `quantifier phrase` to `determiner` (not `dp`, because this has a different connotation).

## 2024-05-16

The database has an insert and a delete.
The domain has a select, but not insert and delete.

~~~python
domain = MyDomain([
    db1, db2
])
domain.select('has_child', {child=2}, 'parent')

class MyDomain
    def select(self, relation, where_clause, select_clause):
        if (relation == 'has_child')
            return self.db1.select()
~~~            

or

~~~python
domain = Domain([
    { 'relation': 'has_child', fields: ['parent', 'child'], 'db': db1, 'map': "(parent, child) -> parent(parent, child) gender(child, 'male')"}
])

grammar = [
    { "syn": "child -> 'children'", "sem": lambda: lambda: domain.select('has_child', ['child']) },
    { 
        "syn": "vp_no_sub -> aux qp child", 
        "sem": lambda aux, qp, child:
                lambda subject: find(
                    (qp, child),
                    lambda object: domain.select('has_child', [subject, object])))
    },

]
~~~

what about this:

~~~python
mem_db = MemoryDb()

domain = Domain([
    Relation("has_child", ['parent', 'child'], lambda parent, child: mem_db.fetch_column('select 1 from has_child where parent_id = %s and child_id = %s')),
],
[
    EntityType("father", lambda: mem_db.fetch_column('select parent_id from has_child hc inner join gender g on ...')),
])
~~~


## 2024-05-15

I need a way to express a noun or adjective in a way that doesn't depend on a specific database or table, as in

    db.select(Record('has_child'))

It needs to be a separate level of abstraction, in order to

- make the grammar more reusable

I can add a new object Domain that accepts databases. One of the challenges is the mapping of knowledge level to db level. Most mappings are simple but here's a mapping that requires 2 relations:

    dom:has_son(A, B) :- parent(B, A) gender(B, 'male');

This code may be do the job:

    domain = Domain()
    domain.add(MemoryDb(), [
        { "rel": "has_child", "map": lambda r: r },
        
        { "rel": "has_son", "map": lambda r, db: 
            db.select(Record('parent', {'parent_id': r.values['parent'], 'child_id': r.values['child']})).
            join(db.select(Record('gender', {'g': 'male'}), ['parent', 'person_id'])) }
    ])


## 2024-05-12

Passing `node` to the semantic functions made the semantics code __much__ more verbose. And more complicated too, because now the user needed to choose between using a function or a node. The benefit would mainly be handling the np.

When I found another way to handle the np I switched back to semantic composition. I don't execute the `qp` and `nbar` of the `np`, I just group them and pass the group as a value to the parent semantic. The semantics code is much shorter and readable for it.

I created a proof of concept using the sentence "each parent has two children". I needed a database-like structure for the sentence so I created a little in-memory "database".

This is now a typical parsing rule:

    { 
        "syn": "s -> np vp_no_sub", 
        "sem": lambda np, vp_no_sub: lambda: find(np(), vp_no_sub) 
    },

The "syn" (for syntax) is the rewrite rule. "sem" is a plain Python function that takes the semantic functions of its (non-word) children as inputs and returns a function that acts on these child functions. The outer function declares the dependencies (the child semantics) and is executed by the composer to get to the inner function. The inner function then has access to the child semantics in its closure. It is the inner function that is passed as depenency to the parent semantic function.

Seeing this proof-of-concept work made me so enthousiastic that I set up a documentation repository `richard-readthedocs` and website https://richard.readthedocs.io/. I also created a package on the official Python repository PyPi. So we're now on version 0.1.0.

Note that I'm using a term like "vp_no_sub", rather than just "vp". I'm not sure about the wording, but creating variants of `vp` seems like a very good idea, if only because the semantic function of "vp" would take a different number of arguments than the "vp_no_sub", and use them differently.

Now I need to write documentation and work on testing and error handling.

## 2024-05-09

To handle quantification, have a look at this simplified representation

    S - check(np, vp)
    - np - quant(qp, nbar)
        - qp - every
        - nbar - parent
    - vp - has two children

The problem is that the function `check` needs direct access to the sem of `qp` as it needs to check if `vp` applies to (in this case) _all_ np's. `qp` however is not a direct child of `s`, but it's a _grandchild_`. Where NLI-GO could access the grandchild because of its declarative nature, Richard could not (at this moment).

Would it be possible to arrange the syntax so that it becomes a direct child?

    S - check(np, vp)
    - qp - every
    - nbar - parent
    - vp - has two children

In theory, yes, but it would split the NP over two nodes, which complicates things, and further, it seems that no linguistic theory has ever done that. 

Giving a node access to the semantics of it's grandchild can be handled in a ridiculously simple way, by passing the parse tree node to the semantic function.

    sem: lambda node: check(
                        node.child_sem('np').child_sem('qp'), 
                        node.child_sem('np').child_sem('np'), 
                        node.child_sem('vp')
                    )

Note that this is a special case. Quantification is the only application that needs access to a grandchild that I know of.

Giving semantics access to the parse tree node, and hence to a bit of its syntactic and word form basis, can have added benefits. SHRDLU for example contains the interaction

    H: How many things are on top of green cubes?
    C: I'M NOT SURE WHAT YOU MEAN BY "ON TOP OF" IN THE PHRASE "ON TOP OF GREEN CUBES" .

Where the quoted phrases are taken literally from the input sentence, and would not be readily available to semantics in NLI-GO, for example. I'm not saying this is important, but it crossed my mind.

The other _big_ advantage of this method is that it requires no composition step.

## 2024-05-05

I started a new Github repository for this project and another one to create the "Github Pages" documentation site for it. I didn't know about this Github service but this is a good time to try it out.

## 2024-04-23

I started this new project because NLI-GO was too much bogged down in its self-created dual-aspect programming language. It caused hard problems every time and conflicted too much with the goal of being simple.

After some months of idling I had the idea of implementing semantics in the host programming language directly, as functions. In this case it's Go, but it should be any language that allows functions as terms and hence as arguments to other functions. This holds true for most modern languages. It seems to me the simple consequence of Richard Montague's writings, but strangly I can't find any example of such direct implementation of semantics when searching the web. 

A few days ago I managed to manually create a single function, representing the meaning of the sentence "add 2 to 5" by combining the meaning-functions of the phrases of a sentence. That was an important proof-of-concept, but I need some more cases to be confident that this approach works.

One point of concern are long-term dependencies. I've used this sentence before and I will use it now:

    Which babies were the toys easiest to take from?

    s                                       sense: check($np, $dep_vp)
        which
        np(E1)                              sense: quant(_, some(_), E1, $nbar)
            nbar(E1)
                noun(E1) - babies
        dep_vp(P1, E1)                      sense: check($np, $advp $vp)
            be() - were
            np(E1)                          sense: quant(Q1, $qp, E1, $nbar)
                qp() - the
                noun(E1) - toys
            adv(P1) - easiest
            vp(P1, E1, E2) - to take from   sense: take_from(P1, E2, E1)

The core of this sentence's meaning is the `check($np, $dep_vp)` from `s`. It first collects all `$np` ("all babies"), then feeds these as arguments to `$dep_vp` ("were the toys easiest to take from"). 

I can do that also in the new system. Find all `np()`, then pass these as argument to `dep_vp()`. The result of the function would then be a list of baby-ids. But I'm wondering if it is okay that a `dep_vp` always returns the missing `np`. Could it be possible that the newly found `P1` is needed as well? Should the `dep_vp` return a list of bindings?

Where NLI-GO was like Prolog that relied on multiple variable bindings, Richard! uses function return values as meaning. This makes it quite a bit different, and I can't yet see all the consequences.

Next to being functional semantic, the new approach also uses intersection to form meaning (a "red car" is the set of cars that is the intersection of all red objects and all car objects).

Another point of concern: quants, consider:

    Do at least 5 babies play with a ball?

    s                                       sense: check($np, $dep_vp)
        np(E1)                              sense: quant(_, $qp, E1, $nbar)
            qp()                            sense: at least 5(E1)
            nbar(E1)
                noun(E1) - babies
        vp(P1, E2)                          sense: play(P1, E2)

To process `check($np, $dep_vp)`, the system needs to go through all `np`'s and then check if the requirement `qp` ("at least five") is met. In the `do()` variant, it needs to try the `np()`'s until `qp()` is met. Perhaps `np` should deliver an iterator?

    {
        /* "... I told you to pick up" */
        rule: vp_without_np(P1, L1) -> np(E1) meta_verb(P1, E1, E2, P2) np(E2) vp_without_nps(P2, E2, L1),
        sense: go:check($np1, go:check($np2, $vp_without_nps $meta_verb))
    }

`meta_verb` returns a set of bindings?

    "Does every parent have 4 children?"

    for every parent
        for exactly 4 children
            the parent has the child

    s
        does
        some_vp : check(np1(), check(np2, verb))
            np1
                qp1 : go:quantifier(Result, Range, $quantifier)
                    quantifier - every : [Result == Range]
                nbar parent
            verb
            np2
                qp1 : go:quantifier(Result, Range, $quantifier)  
                    quantifier - 4 : [Result == 4]

                nbar children


    func check()
            

Richard! doesn't translate from syntax to logic, instead it just uses functions for semantic composition, and adds custom code to each node. This custom code executes the sentence (imperative) rather than just forms a logical expression. The parsing is functional, but the semantics is imperative.

