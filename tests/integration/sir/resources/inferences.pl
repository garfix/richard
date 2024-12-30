# number objects involved in a part-of relationship
part_of_number(A, B, N) :- part_of(A, B), part_of_n(A, B, N).
part_of_number(A, B, N) :- part_of(C, B), part_of_n(C, B, N1), part_of_number(A, C, N2), multiply(N1, N2, N).
part_of_number(A, B, N) :- instance_of_proper(A, AA), part_of_number(AA, B, N).
part_of_number(A, B, N) :- instance_of_proper(B, BB), part_of_number(A, BB, N).

# is a person a person?
instance_of(A, A).

# set-membership and set-inclusion
instance_of(A, B) :- instance_of_proper(A, B).
# equality: John is Jack
instance_of(A, B) :- equals(A, C), instance_of_proper(C, B).
instance_of(A, B) :- equals(C, A), instance_of_proper(C, B).

# direct isa
instance_of_proper(A, B) :- isa(A, B).
# indirect isa
instance_of_proper(A, B) :- isa(A, C), instance_of_proper(C, B).

# is a girl a person?
two_way_instance_of(A, B, 'yes') :- instance_of(A, B).
# is a person a girl?
two_way_instance_of(A, B, 'sometimes') :- instance_of_proper(B, A).

# Every fireman owns a pair-of-red-suspenders. A firechief is a fireman. Does a firechief own a pair-of-red-suspenders?
one_way_own(A, B) :- instance_of_proper(A, AA), own(AA, B).
# Alfred owns a log-log-decitrig. A log-log-decitrig is a slide-rule. Does Alfred own a slide-rule?
one_way_own(A, B) :- instance_of_proper(BB, B), own(A, BB).
# Alfred is a tech-man
# A tech-man is an engineering-student
# Alfred owns a log-log-decitrig
# Does an engineering-student own a log-log-decitrig?

two_way_own(A, B) :- one_way_own(A, B).
two_way_own(A, B) :- instance_of_proper(AA, A),  own(AA, B).
two_way_own(A, B) :- instance_of_proper(BB, B),  own(A, BB).
