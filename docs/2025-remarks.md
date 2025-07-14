## 2025-07-13

I should start with a simple story. The one I have been parsing so far may not be simple enough. I also should start with a story that was explained in detail by Wilensky.

Another thing: while I could produce a completely flat representation of the story, yesterday, that doesn't mean I can do that in all cases. So it's fragile to base the representation structure on this example. While I could store this example in a relational db, that's not the case with all sentences.

I could use the story in 2.4 which is simple and explained well, or the example in chapter 14.

2.5

    JOHN WANTED BILL’S BICYCLE.
    HE WENT OVER TO BILL AND ASKED HIM IF HE WOULD GIVE IT TO HIM.
    BILL REFUSED.
    JOHN TOLD BILL HE WOULD GIVE HIM FIVE DOLLARS FOR IT, BUT BILL WOULD NOT AGREE.
    THEN JOHN TOLD BILL HE WOULD BREAK HIS ARM IF HE DIDN'T LET HIM HAVE IT.
    BILL GAVE HIM THE BICYCLE.

14

    JOHN WAS LOST.
    HE PULLED OVER TO A FARMER STANDING BY THE SIDE OF THE ROAD.
    HE ASKED HIM WHERE HE WAS.

Chapter 14 seems easiest.

I will keep the existing grammar, and extend it.

## 2025-07-12

This is the current meaning of the first story:

~~~js
('go_through_red_light', $1, $2)
('pull_over', $3, $2, $4)
('summons', $9)
('speeding', $10)
('for', $9, $10)
('cop', $8)
('get', $5, $6, $8, $9)
('previous_week', $5)
('tell', $7, $11, $6, $12)
('if', 
    [
        ('he', $15)
        ('another', $17)
        ('violation', $17)
        ('get', $13, $16, $15, $17)
    ], 
    [
        ('license', $18)
        ('his', $18)
        ('take_away', $14, $18, $19, $20)
    ])
('remember', $21, $23, $22, $24)
('he', $25)
('game', $26)
('poss', $27, $26)
('have_on_oneself', $24, $25, $26)
('ticket', $27)
('for', $27, $28)
('number_of', $27, 2)
('if', 
    [
        ('he', $38)
        ('whole', $40)
        ('incident', $40)
        ('forget', $31, $39, $38, $40)
    ], 
    [
        ('he', $32)
        ('cop', $33)
        ('tell', $30, $32, $33, $34)
        ('he', $35)
        ('them', $37)
        ('he', $36)
        ('give', $34, $35, $36, $37)
    ])
('cop', $42)
('happen', $41, $42, $43)
('terrific', $44)
('football_fan', $44)
('he', $46)
('ticket', $49)
('poss', $50, $49)
('take', $45, $48, $46, $49)
('drive_away', $47, $46, $51, $52)
~~~

Seems to be possible to enter this story in a relational database. But what about the "if" statements?

I can do 

~~~js
{
    "syn": "clause(C1) -> 'if' clause(C2)+','? clause(C3)",
    "sem": lambda clause1, clause2: [('if', C1, C2, C3)] + clause1 + clause2
},
~~~

and get 

~~~js
('go_through_red_light', $1, $2)
('pull_over', $3, $2, $4)
('summons', $9)
('speeding', $10)
('for', $9, $10)
('cop', $8)
('get', $5, $6, $8, $9)
('previous_week', $5)
('tell', $7, $11, $6, $12)
('if', $12, $13, $14)
('he', $15)
('another', $17)
('violation', $17)
('get', $13, $16, $15, $17)
('license', $18)
('his', $18)
('take_away', $14, $18, $19, $20)
('remember', $21, $23, $22, $24)
('he', $25)
('game', $26)
('poss', $27, $26)
('have_on_oneself', $24, $25, $26)
('ticket', $27)
('for', $27, $28)
('number_of', $27, 2)
('if', $29, $31, $30)
('he', $32)
('cop', $33)
('tell', $30, $32, $33, $34)
('he', $35)
('them', $37)
('he', $36)
('give', $34, $35, $36, $37)
('he', $38)
('whole', $40)
('incident', $40)
('forget', $31, $39, $38, $40)
('cop', $42)
('happen', $41, $42, $43)
('terrific', $44)
('football_fan', $44)
('he', $46)
('ticket', $49)
('poss', $50, $49)
('take', $45, $48, $46, $49)
('drive_away', $47, $46, $51, $52)
~~~

## 2025-06-29

I reduced parse time from 375 msecs to 34 msecs by "pruning" the parse trees with many regexps in an early stage.

## 2025-06-28

Pruning the parse trees proves expensive. 0.3 seconds for 8192 trees, and this is just checking if they contain regexp nodes. I guess there are a lot of nodes when each tree is a complete parapraph.

Another option is to prune at the enqueue function. But this still requires many duplicate checks.

What about just after the parse, and prune the chart, just before the trees are generated?

===

Tried it. It's not so easy.

Different approach: what about just trying to parse words that are not in the vocabulary?
Well, for one, there is no vocabulary, remember?

## 2025-06-24

Ambiguity:

    He told the cop that he would give them to him 
    if he would forget the whole incident.

    He told the cop that 
        he would give them to him 
        if he would forget the whole incident.

Don't know how to solve at the moment.

===

Great, I can now parse the first story:

    One day, John went through a red light and was pulled over. John had just gotten a summons for speeding by a cop the previous week, and was told that if he got another violation, his license would be taken away. Then John remembered that he had two tickets for the Giants' game on him. He told the cop that he would give them to him if he would forget the whole incident. The cop happened to be a terrific football fan. He took John's tickets and drove away.

It takes 375 msecs (which is bad) and has 4 parse trees (which is quite good!). Actually there are 8192 parse trees before pruning the ones with more regexps.

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
