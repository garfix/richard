# teach
intent_teach(A) :- store(A), store(output_type('understand')).

# part of
intent_part_of(A, B) :- or(
    # Is a nostril part of a professor?
    (proper_part_of(A, B), store(output_type('yes'))),
    # Is a nostril part of a living-creature?
    (proper_isa(BB, B), proper_part_of(A, BB), store(output_type('sometimes'))),
    # Is a nose part of a nose?
    (equals(A, B), store(output_type('no_subpart'))),
    # Is a living-creature part of a nose?
    (proper_isa(AA, A), proper_part_of(B, AA), store(output_type('reverse_sometimes')))
).

# is a
intent_isa(A, B) :- or(
    # is a girl a person?
    (full_isa(A, B), store(output_type('yes'))),
    # is a person a girl?
    (proper_isa(B, A), store(output_type('sometimes'))),
    # is a person a person?
    (equals(A, B), store(output_type('yes'))),
    # otherwise
    store(output_type('unknown'))
).

# count
# not(output_type(T)) means: no output has been produced yet
intent_count(Atoms) :- count(C, Atoms), not(output_type(T)), store(output_type('count'), output_count(C)).

# yes/no
intent_yn(Atoms) :- or(
    (scoped(Atoms), store(output_type('yes'))),
    store(output_type('no'))
).

# own
# Every fireman owns a pair-of-red-suspenders. A firechief is a fireman. Does a firechief own a pair-of-red-suspenders?
# Alfred owns a log-log-decitrig. A log-log-decitrig is a slide-rule. Does Alfred own a slide-rule?
intent_own(A, B) :- proper_own(A, B), store(output_type('yes')).

intent_some_own(A, B) :- or(
    # own in some cases, but not all
    (proper_own(A, B), store(output_type('yes'))),
    # Alfred is a tech-man
    # A tech-man is an engineering-student
    # Alfred owns a log-log-decitrig
    # Does an engineering-student own a log-log-decitrig?
    (proper_isa(AA, A), own(AA, B), store(output_type('yes'))),
    # Does a pair-of-red-suspenders own a pair-of-red-suspenders?
    (equals(A, B), store(output_type('no_same'))),
    # otherwise
    store(output_type('unknown'))
).

# claim
# NB the order is important, because `store` changes the state
intent_claim(Atom, "impossible") :- not(check_claim(Atom)), store(output_type('impossible')).
intent_claim(Atom) :- check_claim(Atom), store(Atom), store(output_type('understand')).

# where
intent_where(Variable, Body) :-
    find_one(Variable, Body, Object),
    store(output_type('location'), output_location(Object)).
