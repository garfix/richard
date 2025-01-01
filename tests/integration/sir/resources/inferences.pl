# sentence-level predicates

# part of
# Is a nostril part of a professor?
sentence_part_of(A, B, "yes") :- proper_part_of(A, B).
# Is a nostril part of a living-creature?
sentence_part_of(A, B, "sometimes") :- proper_isa(BB, B), proper_part_of(A, BB).
# Is a nose part of a nose?
sentence_part_of(A, A, "improper").
# Is a living-creature part of a nose?
sentence_part_of(A, B, "reverse_sometimes") :- proper_isa(AA, A), proper_part_of(B, AA).

# is a
# is a girl a person?
sentence_isa(A, B, 'yes') :- full_isa(A, B).
# is a person a girl?
sentence_isa(A, B, 'sometimes') :- proper_isa(B, A).
# is a person a person?
sentence_isa(A, A, 'yes').

# own
# Every fireman owns a pair-of-red-suspenders. A firechief is a fireman. Does a firechief own a pair-of-red-suspenders?
# Alfred owns a log-log-decitrig. A log-log-decitrig is a slide-rule. Does Alfred own a slide-rule?
sentence_own(A, B) :- proper_own(A, B).
# own in some cases, but not all
sentence_some_own(A, B, 'yes') :- proper_own(A, B).
# Alfred is a tech-man
# A tech-man is an engineering-student
# Alfred owns a log-log-decitrig
# Does an engineering-student own a log-log-decitrig?
sentence_some_own(A, B, 'yes') :- proper_isa(AA, A), own(AA, B).
# Does a pair-of-red-suspenders own a pair-of-red-suspenders?
sentence_some_own(A, A, 'improper').



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

