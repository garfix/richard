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
