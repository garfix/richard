## 2025-05-14

The way PAM works is described in chapter 13 of Wilensky's thesis. Its algorithm has some similarities to Earley's algorithm: it starts with bottom-up reading, then makes top-down predictions. Once there are predictions, further reading must match these predictions.

## 2025-04-23

I did some research on the models of Roger Schank's group. I picked PAM, by Robert Wilensky, because dealing with plan and goal recognition is hard enought by itself and would be an incredible addition to Richard! Also it could provide a more natural way to implement SHRDLU (which also deals with goals and reasons).

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
