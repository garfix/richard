## 2025-06-22

    John had just gotten a summons for speeding by a cop the previous week, and was told that

this is

    S -> np clause and clause

but they share an *object* (John).

So can't just say

    s -> np(E1) clause_sub(E1) 'and' clause_sub(E1)

because in this passive sentence it's an object.    

===

The skeletel clause works much better. 2 sentences parsed in 16 msecs. Ambiguity still too high (not for proper functioning, but for speed).

Processing all sentences of a paragraph in one is possible, but each next sentence multiplies the number of possible parses.

It would be better to parse as much as possible, followed by a check if all text is covered. One problem would be that regexp constructs will win the parse.

===

I want to prune unnecessary parse trees as soon as possible. Parse trees with less reg exp nodes are better than ones with more. I will only keep parse trees with the least amount of reg exps. And I think I can do that in the parse tree extracter.

## 2025-06-18

Just an idea: use thes constructs for main nodes:

    vp(C1, E1, E2, E3)

then do rewrites:    

    vp(C1, E1, E2, E3) -> vp(C1)
    vp(C1, E1, E2, E3) -> vp(C1, E1)
    vp(C1, E1, E2, E3) -> vp(C1, E1, E2)

this is to reduce the number of rules.

Use one of them like this:

    vp(C1, E1, _, E3)

===

I tried this out, and it makes for less rules, but it makes the parsing process very inefficient and the time it takes quickly goes from 0.008 seconds to multiple seconds.

===

I also tried to replace all vp's with `vp(C1, E1, E2, E3)` but this also made the parsing process very very slow. This is the first time, in fact, that the slowness of the parsing process plays any role at all. The structure of the grammar starts to matter.

The reason for the slowness is that the sentences become highly ambiguous with hundred of alternative parse trees.

===

The problem is that the grammar doesn't provide a "skeleton" for the sentence. The main reason for the ambiguity turns out to be that any word can be a pronoun (due to the pronoun being a very accepting regexp `/\w+/`) and that the np can be placed anywhere `vp -> vp np`.

The solution is to provide skeletons for clauses:

    clause -> np vp np by np
    clause -> clause adverb
    vp -> 'had' vp
    vp -> adverb vp
    vp -> verb
    np -> \w+\ \w+\ \w+\
    adverb -> the previous week

    John had just gotten a summons for speeding by a cop the previous week

## 2025-06-17

I'm attempting to write a grammar that rewrites an n-argument clause into an n+1 argument clause, like this:

        {
            "syn": "past_participle_phase_sub(C1, Sub) -> past_participle_phase_sub_obj(C1, Sub, Obj) np(Obj)",
            "sem": lambda past_participle, np: apply(np, past_participle),
        },

There are rules for 1 -> 2 arguments, and 2 -> 3 arguments.

A big problem turns out to be that the second argument may be known before the third argument is added.

    John had just gotten a summons for speeding by a cop the previous week.

Here: John is the object, a summons is the indirect object, and a cop is the subject.    

Writing out the full rules with all arguments at once will probably result in less rules and is much easier to understand.

===

Now trying to solve the grammar without any _sub_ or _obj_ affixes to the predicates. If that works, it will dramatically decrease the number of rules needed. It will allow about any sentence possible, and will not be the fastest, but if it's fast enough, the simplicity gained will be worth it.

## 2025-06-08

PAM doesn't work with dialogues like the other systems. This forms a problem that needs to be solved. Do I force the examples into a dialogue, or do I change the form of interaction?

Forcing the examples into a dialogue will make it look something like this: "I will tell you a story and then I will ask you to answer questions about it. <insert story> <insert questions>" or this "I will tell you a story and then I will ask you to make a summary. <insert story> Summarize this story".

The alternative would be to create special Python functions for question-answering, story-question-answering and story-summarizing. While this could be interesting for some purposes. It defeats the purpose of having an NLI in the long run. One want the system to understand your text without explicitly having to define the parts of it. It's part of understanding.

Before LLM's came along both would have been reasonable, but now the bar is raised. These LLM's don't need any of this scaffolding. They allow any form of interaction and get along with it very well. I even admit to being discouraged by the advent of LLMs. Nothing I can do on PAM will make the result even come close to their power. Story understanding is the topic where they shine.

I will take this approach for the interactions:

    H: Answer questions about a story
    C: OK

    H: <story>
    C: OK
    
    H: Questions
    C: OK

    H: <question>
    C: <answer>

    H: <question>
    C: <answer>

The command "Answer questions about a story" takes the system in story answering mode. For the moment this will be implemented with a simple state variable. Later we may do something with an actual context.

===

There's another problem: what is a story? Where does it begin and where does it end? Which sentences are part of it? When the system reads the lines of the story it accepts the facts therein, but it doesn't link them to a story object as such.

## 2025-05-14

The way PAM works is described in chapter 13 of Wilensky's thesis. Its algorithm has some similarities to Earley's algorithm: it starts with bottom-up reading, then makes top-down predictions. Once there are predictions, further reading must match these predictions.

## 2025-04-23

I did some research on the models of Roger Schank's group. I picked PAM, by Robert Wilensky, because dealing with plan and goal recognition is hard enough by itself and would be an incredible addition to Richard! Also it could provide a more natural way to implement SHRDLU (which also deals with goals and reasons).

For now I just extracted the stories from Wilensky's PhD thesis that have questions added to them. These make story understanding testable. 

I asked some current employees from Yale and Berkeley's computer science departements if they could try to locate some of the source code of the model.

## 2025-02-05

Thinking about contexts. At the moment I need contexts only for this sentence:

    Is the pad just to the right of the book?

What's meant here is not just the relation right_of(A, B) but also the chained application `right_of(A, C) right_of(C, B)` and further.

In order "contexts" we *don't* want the transitive version, but just the simple one. The distinction is like the "broad meaning" and the "narrow meaning".

I think a sentence can

* be executed in a context `in_context('question', body-atoms)`
* start a context `start_context('question')`
* end a context `end_context('question')`

Contexts are stored in the dialog context.

A sentence like "What did you pick up when you started building the tower?" starts a context `at event E`. Following questions may presume this time from the context.
Emotional expressions may also be different depending on the context of emotional feeling.

Inferences may be dependent on context. Even on nested contexts.

===

Okee, starting with the next one. Something based on Roger Schank's work. This stuff is beyond fascinating. But how to approach it?

## 2025-02-04

I finished the SIR dialog.

Renamed sentence context to output buffer, as this it as yet its only purpose. And it is cleared when the output is read by the client.

## 2025-01-01

Inferences using both part-of and isa.

    A van-dyke is part of Ferren
    A van-dyke is a beard
    Is a beard part of Ferren?

Main predicate: `part-of`

    part-of('beard', 'Ferren')
    part-of(Part, Whole)

In order to determine `part-of`, we should consider the specializations of `van-dyke`.

supersets/generalizations
