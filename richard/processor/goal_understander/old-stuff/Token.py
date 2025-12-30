# HUM0
#
# TOKEN: T
# CLASS: (*PERSON*)
# PERSNAME: (John)
# GENDER: (*MASC*)

from richard.processor.goal_understander.data.enums import Gender, TokenClass


class Token:
    tokenClass: TokenClass
    persname: str
    gender: Gender
