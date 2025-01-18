# sentence-level predicates

# teach
sentence_teach(A) :- store(A), store(output_type('understand')).

# part of
sentence_part_of(A, B) :- or(
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
sentence_isa(A, B) :- or(
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
sentence_count(Atoms) :- count(C, Atoms), store(output_type('count'), output_count(C)).

# yes/no
sentence_yn(Atoms) :- or(
    (scoped(Atoms), store(output_type('yes'))),
    store(output_type('no'))
).

# own
# Every fireman owns a pair-of-red-suspenders. A firechief is a fireman. Does a firechief own a pair-of-red-suspenders?
# Alfred owns a log-log-decitrig. A log-log-decitrig is a slide-rule. Does Alfred own a slide-rule?
sentence_own(A, B) :- proper_own(A, B), store(output_type('yes')).

sentence_some_own(A, B) :- or(
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
sentence_claim(Atom, "impossible") :- not(check_claim(Atom)), store(output_type('impossible')).
sentence_claim(Atom) :- check_claim(Atom), store(Atom), store(output_type('understand')).

# where
# sentence_where(A, Answer) :- let(Answer, answer_where(A)).
# sentence_where(A, Answer) :- just_left_of(A, B), let(Answer, just_left_of(A, B)).



# implementations

# isa
proper_isa(A, B) :- isa(A, B).
proper_isa(A, B) :- isa(A, C), proper_isa(C, B).

# isa including identity
full_isa(A, A).
full_isa(A, B) :- proper_isa(A, B).
# equality: John is Jack
full_isa(A, B) :- identical(A, B).
full_isa(A, B) :- identical(B, A).
full_isa(A, B) :- identical(A, C), proper_isa(C, B).
full_isa(A, B) :- identical(C, A), proper_isa(C, B).
full_isa(A, B) :- identical(B, C), proper_isa(A, C).
full_isa(A, B) :- identical(C, B), proper_isa(A, C).

#own
# find generalizations of A, find specializations of B
proper_own(A, B) :- full_isa(A, AA), full_isa(BB, B), own(AA, BB).

# part-of
# find specializations of A, find generalizations of B
proper_part_of(A, B) :- full_isa(AA, A), full_isa(B, BB), part_of(AA, BB).
# part-of is transitive
proper_part_of(A, B) :- full_isa(A, AA), part_of(AA, C), proper_part_of(C, B).

# part-of with number
part_of_number(A, B, N) :- full_isa(AA, A), full_isa(B, BB), part_of(AA, BB), part_of_n(AA, BB, N).
# part-of is transitive
part_of_number(A, B, N) :- full_isa(B, BB), part_of(C, BB), part_of(A, C), part_of_n(C, BB, N1), part_of_number(A, C, N2), multiply(N1, N2, N).

# position
# left_of is transitive
left_of(A, B) :- just_left_of(A, B).
left_of(A, B) :- just_left_of(A, C), left_of(C, B).

check_claim(Atom) :- destructure(Atom, 'just_left_of', A, B), check_just_left_of(A, B).
check_claim(Atom) :- destructure(Atom, 'left_of', A, B), check_left_of(A, B).

# check if the position just left of A is not already occupied
# check if A not to the right of B
check_just_left_of(A, B) :- not(just_left_of(A, C)), not(left_of(B, A)).
# check if A not to the right of B
check_left_of(A, B) :- not(left_of(B, A)).
