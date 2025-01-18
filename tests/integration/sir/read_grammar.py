from richard.core.constants import E1, E2, E3, e1, e2, e3


def get_read_grammar():
    return [
        # sentences
        {
            "syn": "s() -> statement()",
            "sem": lambda statement: statement,
            # "dialog": [("format", "canned"), ("format_canned", "I understand")],
        },
        {
            "syn": "s() -> yes_no()",
            "sem": lambda yes_no: yes_no,
            # "dialog": [("format", "y/n"), ("format_yes", "Yes"), ("format_no", "Insufficient information")],
        },

        # statements

        # every X is a Y, where X and Y not part of the grammar
        # this is uncommon, is defines a new concept in terms of an another unknown concept
        {
            "syn": "statement() -> 'every' common_noun_name() 'is' a() common_noun_name()",
            "sem": lambda common_noun_name1, a, common_noun_name2: [('sentence_claim', [('isa', common_noun_name1, common_noun_name2)])],
        },
        # any X is an example of a Y
        {
            "syn": "statement() -> 'any' common_noun_name() 'is' 'an' 'example' 'of' a() common_noun_name()",
            "sem": lambda common_noun_name1, a, common_noun_name2: [('sentence_claim', [('isa', common_noun_name1, common_noun_name2)])],
        },
        # An IBM-7094 is a computer
        {
            "syn": "statement() -> a() common_noun_name() 'is' a() common_noun_name()",
            "sem": lambda a1, common_noun_name1, a2, common_noun_name2: [('sentence_teach', [('isa', common_noun_name1, common_noun_name2)])],
        },
        # A finger is a part of a hand
        # a statement about classes as entities
        {
            "syn": "statement() -> a() common_noun_name() 'is' 'a'? 'part' 'of' a() common_noun_name()",
            "sem": lambda a1, common_noun_name1, a2, common_noun_name2: [('sentence_teach', [('part_of', common_noun_name1, common_noun_name2)])],
        },
        # A screen is part of every display-device
        {
            "syn": "statement() -> a() common_noun_name() 'is' 'a'? 'part' 'of' 'every' common_noun_name()",
            "sem": lambda a1, common_noun_name1, common_noun_name2: [('sentence_teach', [('part_of', common_noun_name1, common_noun_name2)])],
        },
        # A van-dyke is part of Ferren
        {
            "syn": "statement() -> a() common_noun_name() 'is' 'a'? 'part' 'of' proper_noun(E1)",
            "sem": lambda a1, common_noun_name, proper_noun: proper_noun + [('sentence_teach', [('part_of', common_noun_name, E1)])],
        },
        # There are two hands on each person
        # a statement about classes as quantified entities
        {
            "syn": "statement() -> 'there' 'are' number(E1) common_noun_name() 'on' 'each' common_noun_name()",
            "sem": lambda number, common_noun_name1, common_noun_name2: [('sentence_teach', [('part_of', common_noun_name1, common_noun_name2), ('part_of_n', common_noun_name1, common_noun_name2, number)])],
        },
        # John is a boy
        # Max is an IBM-7094
        # Jack is a dope
        {
            "syn": "statement() -> proper_noun(E1) 'is' a() common_noun_name()",
            "sem": lambda proper_noun, a2, common_noun_name: proper_noun + [('sentence_teach', [('isa', E1, common_noun_name)])],
        },
        # Every hand has 5 fingers
        {
            "syn": "statement() -> 'every' common_noun_name() 'has' number(E1) common_noun_name()",
            "sem": lambda common_noun_name1, number, common_noun_name2: [('sentence_teach', [('part_of', common_noun_name2, common_noun_name1), ('part_of_n', common_noun_name2, common_noun_name1, number)])],
        },
        # John is Jack
        {
            "syn": "statement() -> proper_noun(E1) 'is' proper_noun(E2)",
            "sem": lambda proper_noun1, proper_noun2: proper_noun1 + proper_noun2 + [('sentence_teach', [('identical', E1, E2)])],
        },
        # Every fireman owns a pair-of-red-suspenders
        {
            "syn": "statement() -> 'every' common_noun_name() own() a() common_noun_name()",
            "sem": lambda common_noun_name1, own, a, common_noun_name2: [('sentence_teach', [('own', common_noun_name1, common_noun_name2)])],
        },
        # Alfred owns a log-log-decitrig
        {
            "syn": "statement() -> proper_noun(E1) own() a() common_noun_name()",
            "sem": lambda proper_noun, own, a, common_noun_name: proper_noun + [('sentence_teach', [('own', E1, common_noun_name)])],
        },
        # The telephone is just to the right of the book
        {
            "syn": "s(E3) -> proper_noun(E1) 'is' preposition(E1, E2) proper_noun(E2)",
            "sem": lambda proper_noun1, preposition, proper_noun2: proper_noun1 + proper_noun2 + [('sentence_claim', preposition)],
            # "dialog": [("format", "switch"), ("format_switch", e3, 'Insufficient information'),
            #         ("format_switch_value", 'impossible', 'The above statement is impossible'),
            #         ("format_switch_value", 'ok', 'I understand')
            #     ],
        },


        # questions

        # How many fingers does John have?
        # we don't know John, but all that matters is that it's a boy
        # determine 'how many' not by counting but by calculating
        {
            "syn": "s(E3) -> 'how' 'many' common_noun(E1) 'does' proper_noun(E2) 'have'+'?'",
            "sem": lambda common_noun1, proper_noun: common_noun1 + proper_noun + [('sentence_count', [('have', E2, E1)])],
            # "dialog": [("format", "number"), ("format_number", e3, ''), ('format_canned', 'The answer is {}')],
        },
        # Is a X a Y?
        {
            "syn": "s(E3) -> 'is' a() common_noun_name() a() common_noun_name()~'?'",
            "sem": lambda a1, common_noun_name1, a2, common_noun_name2: [('sentence_isa', common_noun_name1, common_noun_name2)],
            # "dialog": [("format", "switch"), ("format_switch", e3, 'Insufficient information'),
            #         ("format_switch_value", 'sometimes', 'Sometimes'),
            #         ("format_switch_value", 'yes', 'Yes')
            #     ],
        },
        # Is a nostril part of a professor?
        # Is a nostril part of a living-creature?
        # Is a living-creature part of a nose?
        {
            "syn": "s(E1) -> 'is' a() common_noun_name() 'a'? 'part' 'of' a() common_noun_name()~'?'",
            "sem": lambda a1, common_noun_name1, a2, common_noun_name2: [('sentence_part_of', common_noun_name1, common_noun_name2)],
            # "dialog": [("format", "switch"), ("format_switch", e1, 'Insufficient information'),
            #         ("format_switch_value", 'sometimes', 'Sometimes'),
            #         ("format_switch_value", 'reverse_sometimes', 'No, but the reverse is sometimes true'),
            #         ("format_switch_value", 'improper', 'No, part means proper subpart'),
            #         ("format_switch_value", 'yes', 'Yes')
            #     ],
        },
        # Is a beard part of Ferren?
        {
            "syn": "s(E1) -> 'is' a() common_noun_name() 'a'? 'part' 'of' proper_noun(E2)~'?'",
            "sem": lambda a1, common_noun_name, proper_noun: proper_noun + [('sentence_part_of', common_noun_name, E2)],
            # "dialog": [("format", "switch"), ("format_switch", e1, 'Insufficient information'),
            #         ("format_switch_value", 'sometimes', 'Sometimes'),
            #         ("format_switch_value", 'reverse_sometimes', 'No, but the reverse is sometimes true'),
            #         ("format_switch_value", 'improper', 'No, part means proper subpart'),
            #         ("format_switch_value", 'yes', 'Yes')
            #     ],
        },

        # Yes/no questions

        # Is Max a computer?
        # Is John a dope?
        {
            "syn": "s(E3) -> 'is' proper_noun(E1) a() common_noun_name()~'?'",
            "sem": lambda proper_noun, a, common_noun_name: proper_noun + [('sentence_isa', E1, common_noun_name)],
            # "dialog": [("format", "switch"), ("format_switch", e3, 'Insufficient information'),
            #         ("format_switch_value", 'sometimes', 'Sometimes'),
            #         ("format_switch_value", 'improper', 'No, part means proper subpart'),
            #         ("format_switch_value", 'yes', 'Yes')
            #     ],
        },
        # Does Alfred own a slide-rule?
        {
            "syn": "yes_no() -> 'does' proper_noun(E1) own() a() common_noun_name()~'?'",
            "sem": lambda proper_noun, own, a, common_noun_name: proper_noun + [('sentence_own', E1, common_noun_name)],
        },
        # Does a doctor own a pair-of-red-suspenders?
        # Does a firechief own a pair-of-red-suspenders?
        # Does an engineering-student own a log-log-decitrig?
        # Does a pair-of-red-suspenders own a pair-of-red-suspenders?
        {
            "syn": "s(E3) -> 'does' a() common_noun_name() own() a() common_noun_name()~'?'",
            "sem": lambda a1, common_noun_name1, own, a2, common_noun_name2: [('sentence_some_own', common_noun_name1, common_noun_name2)],
            # "dialog": [("format", "switch"), ("format_switch", e3, 'Insufficient information'),
            #         ("format_switch_value", 'improper', 'No, they are the same'),
            #         ("format_switch_value", 'yes', 'Yes')
            #     ],
        },
        # Is the pad just to the right of the book?
        {
            "syn": "s() -> 'is' proper_noun(E1) preposition(E1, E2) proper_noun(E2)~'?'",
            "sem": lambda proper_noun1, preposition, proper_noun2: [('sentence_yn', proper_noun1 + proper_noun2 + preposition)],
            # "dialog": [("format", "y/n"), ("format_yes", "Yes"), ("format_no", "No")],
        },
        # Where is the pad?
        # {
        #     "syn": "s(E1) -> 'where' 'is' proper_noun(E1)~'?'",
        #     "sem": lambda proper_noun: proper_noun + [('sentence_where', E1, E2)],
        #     "dialog": [("format", "free"), ("format_free", e2)],
        # },

        # number
        { "syn": "number(E1) -> 'two'", "sem": lambda: 2 },
        { "syn": "number(E1) -> '5'", "sem": lambda: 5 },

        # article
        { "syn": "a() -> 'a'", "sem": lambda: [] },
        { "syn": "a() -> 'an'", "sem": lambda: [] },

        # verb
        { "syn": "own() -> 'own'", "sem": lambda: [] },
        { "syn": "own() -> 'owns'", "sem": lambda: [] },

        # common noun
        {
            "syn": "common_noun(E1) -> common_noun_name()",
            "sem": lambda common_noun_name: [(common_noun_name, E1)], "dialog": lambda common_noun_name: [('isa', e1, common_noun_name)]
        },

        # preposition
        { "syn": "preposition(E1, E2) -> 'just' 'to' 'the' 'left' 'of'", "sem": lambda: [('just_left_of', E1, E2)] },
        { "syn": "preposition(E1, E2) -> 'just' 'to' 'the' 'right' 'of'", "sem": lambda: [('just_left_of', E2, E1)] },
        { "syn": "preposition(E1, E2) -> 'to' 'the' 'left' 'of'", "sem": lambda: [('left_of', E1, E2)] },
        { "syn": "preposition(E1, E2) -> 'to' 'the' 'right' 'of'", "sem": lambda: [('left_of', E2, E1)] },

        # proper noun
        { "syn": "proper_noun(E1) -> 'the'? name()", "sem": lambda name: [('resolve_name', name, E1)] },

        # introduction of a new common noun
        { "syn": "common_noun_name() -> name()", "sem": lambda name: name },
        { "syn": "common_noun_name() -> common_noun_name()+'s'", "sem": lambda common_noun_name: common_noun_name, 'boost': 1 },

        { "syn": "name() -> /\w[\w\d]+(-[\w\d]+)*/", "sem": lambda token: token },
    ]
