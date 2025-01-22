from richard.entity.ReifiedVariable import ReifiedVariable
from richard.entity.Variable import Variable


TERMINAL = "terminal"
GAMMA = "gamma"
DELTA = "delta"
ROOT_CATEGORY = "s"

NAME_NOT_FOUND = "Name not found: %s"
SORT_CONFLICT = "It doesn't make sense"
WHICH_ONE = "Which one?"
UNKNOWN_WORD = "Unknown word:"
NO_SENTENCE = "No sentence given"
NOT_UNDERSTOOD = "Sorry, I don't understand"
NO_RESULTS = "No results"

POS_TYPE_RELATION = "relation"
POS_TYPE_WORD_FORM = "word-form"
POS_TYPE_REG_EXP = "reg-exp"

CATEGORY_TEXT = "text"
CATEGORY_VALUE = "value"
CATEGORY_FORMAT = "format"
CATEGORY_PROPER_NOUN = "proper_noun"

E1 = Variable('E1')
E2 = Variable('E2')
E3 = Variable('E3')
E4 = Variable('E4')
E5 = Variable('E5')

e1 = ReifiedVariable('E1')
e2 = ReifiedVariable('E2')
e3 = ReifiedVariable('E3')
e4 = ReifiedVariable('E4')
e5 = ReifiedVariable('E5')

Range = ['__$Range$__']
Body = ['__$Body$__']

ONE = 1
SMALL = 10
MEDIUM = 100
LARGE = 1000
VERY_LARGE = 10000
INFINITE = 1000000000000
UNKNOWN = 500
IGNORED = 'ignored'

RESOLVE_NAME = 'resolve_name'