# sentence-level predicates

# part of
# Is a nostril part of a professor?
sentence_part_of(A, B, "yes") :- proper_part_of(A, B).
# Is a nostril part of a living-creature?
sentence_part_of(A, B, "sometimes") :- proper_isa(BB, B), proper_part_of(A, BB).
# Is a nose part of a nose?
sentence_part_of(A, A, "improper").

# is a
# is a girl a person?
sentence_isa(A, B, 'yes') :- proper_isa(A, B).
# equality: John is Jack
sentence_isa(A, B, "yes") :- equals(A, C), proper_isa(C, B).
sentence_isa(A, B, "yes") :- equals(C, A), proper_isa(C, B).
# is a person a girl?
sentence_isa(A, B, 'sometimes') :- proper_isa(B, A).
# is a person a person?
sentence_isa(A, A, 'yes').

# own
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

# part-of
proper_part_of(A, B) :- part_of(A, B).
proper_part_of(A, B) :- part_of(A, C), proper_part_of(C, B).
proper_part_of(A, B) :- proper_isa(A, AA), proper_part_of(AA, B).
proper_part_of(A, B) :- proper_isa(B, BB), proper_part_of(A, BB).

# part-of with number
part_of_number(A, B, N) :- part_of(A, B), part_of_n(A, B, N).
part_of_number(A, B, N) :- part_of(C, B), part_of_n(C, B, N1), part_of_number(A, C, N2), multiply(N1, N2, N).
part_of_number(A, B, N) :- proper_isa(A, AA), part_of_number(AA, B, N).
part_of_number(A, B, N) :- proper_isa(B, BB), part_of_number(A, BB, N).

# isa
proper_isa(A, B) :- isa(A, B).
proper_isa(A, B) :- isa(A, C), proper_isa(C, B).

#own
proper_own(A, B) :- own(A, B).
# Every fireman owns a pair-of-red-suspenders. A firechief is a fireman. Does a firechief own a pair-of-red-suspenders?
proper_own(A, B) :- proper_isa(A, AA), proper_own(AA, B).
# Alfred owns a log-log-decitrig. A log-log-decitrig is a slide-rule. Does Alfred own a slide-rule?
proper_own(A, B) :- proper_isa(BB, B), proper_own(A, BB).

