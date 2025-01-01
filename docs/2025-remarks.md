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