from richard.Model import Model
from richard.entity.Instance import Instance
from richard.semantics.commands import avg, create_np, exists, negate


def get_grammar(model: Model):
    return [

        { "syn": "s -> 'what' 'is' 'the' 'average' 'area' 'of' np preposition 'each' nbar '?'", "sem": lambda np, preposition, nbar: 
            lambda: model.group_by(nbar, 
                                   lambda e1: avg(model.find_attribute_values(lambda: 'size-of', 
                                                                                lambda: np(lambda e2: preposition(e2)(e1.id))))) 
        },
        { "syn": "s -> 'what' 'is' 'the' 'total' 'area' 'of' np '?'", "sem": lambda np: lambda: sum(model.find_attribute_values(lambda: 'size-of', np)) },
        { "syn": "s -> 'what' 'are' np '?'", "sem": lambda np: lambda: np() },
        { "syn": "s -> 'what' 'are' 'the' attr 'of' np '?'", "sem": lambda attr, np: lambda: model.create_attribute_map(np, attr) },
        { "syn": "s -> 'what' 'is' np '?'", "sem": lambda np: lambda: np() },
        { "syn": "s -> 'what' nbar 'are' 'there' '?'", "sem": lambda nbar: lambda: nbar() },
        { "syn": "s -> 'where' 'is' np '?'", "sem": lambda np: lambda: model.find_attribute_values(lambda: 'location-of', np) },
        { "syn": "s -> 'which' nbar 'are' adjp '?'", "sem": lambda nbar, adjp: lambda: adjp(nbar) },
        { "syn": "s -> 'which' nbar 'are' tv_no_obj '?'", "sem": lambda nbar, tv_no_obj: lambda: create_np(exists, nbar)(tv_no_obj) },
        { "syn": "s -> 'which' 'is' np '?'", "sem": lambda np: lambda: np() },
        { "syn": "s -> 'which' 'country' \''\' 's' attr 'is' np '?'", "sem": lambda attr, np: 
            lambda: model.find_attribute_objects(attr, np) },
        { "syn": "s -> 'does' np tv_no_sub '?'",  "sem": lambda np, tv_no_sub: lambda: np(tv_no_sub) },
        { "syn": "s -> 'how' 'large' 'is' np '?'",  "sem": lambda np: lambda: model.find_attribute_values(lambda: 'size-of', np) },
        { "syn": "s -> 'how' 'many' nbar 'does' np tv_passive '?'", "sem": lambda nbar, np, tv_passive:
            lambda: len(create_np(exists, nbar)(lambda object: np(tv_passive(object))))
        },

        { "syn": "tv_no_sub -> tv np", "sem": lambda tv, np: lambda subject: np(tv(subject)) },
        { "syn": "tv_no_obj -> tv_passive 'by' np", "sem": lambda tv_passive, np: lambda object: np(tv_passive(object)) },

        { "syn": "tv_passive -> tv", "sem": lambda tv: lambda object: lambda subject: tv(subject)(object) },

        { "syn": "tv -> 'flow' 'through'", "sem": lambda: 
            lambda subject: lambda object: model.find_relation_values('flows-through', [subject, object]) },
        { "syn": "tv -> 'border'", "sem": lambda: 
            lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True) },
        { "syn": "tv -> 'borders'", "sem": lambda: 
            lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True) },
        { "syn": "tv -> 'bordering'", "sem": lambda: 
            lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True) },
        { "syn": "tv -> 'bordered'", "sem": lambda: 
            lambda subject: lambda object: model.find_relation_values('borders', [subject, object], two_ways = True) },

        { "syn": "np -> nbar", "sem": lambda nbar: create_np(exists, nbar) },
        { "syn": "np -> det nbar", "sem": lambda det, nbar: create_np(det, nbar) },
        { "syn": "np -> np relative_clause", "sem": lambda np, relative_clause: create_np(exists, lambda: np(relative_clause)) },
        { "syn": "np -> np relative_clause 'and' relative_clause", "sem": lambda np, rc1, rc2: create_np(exists, lambda: np(rc1) & np(rc2)) },
        { "syn": "np -> np pp", "sem": lambda np, pp: create_np(exists, lambda: np(pp)) },
        { "syn": "np -> np pp 'and' pp", "sem": lambda np, pp1, pp2: create_np(exists, lambda: np(pp1) & np(pp2)) },

        { "syn": "pp -> preposition np", "sem": lambda preposition, np: lambda subject: np(preposition(subject)) },
        { "syn": "pp -> 'not' preposition np", "sem": lambda preposition, np: lambda subject: negate(np(preposition(subject))) },

        { "syn": "preposition -> 'south' 'of'", "sem": lambda: 
            lambda e1: lambda e2: model.find_relation_values('south-of', [e1, e2]) },
        { "syn": "preposition -> 'in'", "sem": lambda: 
            lambda e1: lambda e2: model.find_relation_values('in', [e1, e2]) },

        { "syn": "relative_clause -> 'that' tv_no_sub", "sem": lambda tv_no_sub: lambda subject: tv_no_sub(subject) },
        { "syn": "relative_clause -> tv_no_sub", "sem": lambda tv_no_sub: lambda subject: tv_no_sub(subject) },

        { "syn": "nbar -> noun", "sem": lambda noun: lambda: noun() },
        { "syn": "nbar -> adj noun", "sem": lambda adj, noun: lambda: adj(noun) },
        { "syn": "nbar -> attr 'of' np", "sem": lambda attr, np: lambda: model.find_attribute_values(attr, np) },
        { "syn": "nbar -> superlative nbar", "sem": lambda superlative, nbar: lambda: superlative(nbar) },

        { "syn": "superlative -> 'largest'", "sem": lambda: lambda range: model.find_entity_with_highest_attribute_value(range, 'size-of') },
        { "syn": "superlative -> 'smallest'", "sem": lambda: lambda range: model.find_entity_with_lowest_attribute_value(range, 'size-of') },

        { "syn": "det -> 'the'", "sem": lambda: exists },
        { "syn": "det -> 'two'", "sem": lambda: lambda result_count, range_count: result_count == 2 },

        { "syn": "adjp -> adj", "sem": lambda adj: lambda range: adj(range) },

        { "syn": "adj -> 'european'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'european') },
        { "syn": "adj -> 'african'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'african') },
        { "syn": "adj -> 'american'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'american') },
        { "syn": "adj -> 'asian'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'asian') },

        { "syn": "noun -> proper_noun", "sem": lambda proper_noun: lambda: proper_noun() },
        { "syn": "noun -> 'rivers'", "sem": lambda: lambda: model.get_instances('river') },
        { "syn": "noun -> 'country'", "sem": lambda: lambda: model.get_instances('country') },
        { "syn": "noun -> 'countries'", "sem": lambda: lambda: model.get_instances('country') },
        { "syn": "noun -> 'ocean'", "sem": lambda: lambda: model.get_instances('ocean') },
        { "syn": "noun -> 'seas'", "sem": lambda: lambda: model.get_instances('sea') },
        { "syn": "noun -> 'continent'", "sem": lambda: lambda: model.get_instances('continent') },

        { "syn": "attr -> 'capital'", "sem": lambda: lambda: 'capital-of' },
        { "syn": "attr -> 'capitals'", "sem": lambda: lambda: 'capital-of' },

        # todo
        { "syn": "proper_noun -> 'afghanistan'", "sem": lambda: lambda: set([Instance('country', 'afghanistan')]) },
        { "syn": "proper_noun -> 'china'", "sem": lambda: lambda:  set([Instance('country', 'china')]) },
        { "syn": "proper_noun -> 'upper_volta'", "sem": lambda: lambda:  set([Instance('country', 'upper_volta')]) },
        { "syn": "proper_noun -> 'london'", "sem": lambda: lambda:  set([Instance('city', 'london')])  },
        { "syn": "proper_noun -> 'baltic'", "sem": lambda: lambda:  set([Instance('sea', 'baltic')])  },
        { "syn": "proper_noun -> 'danube'", "sem": lambda: lambda:  set([Instance('river', 'danube')])  },
        { "syn": "proper_noun -> 'equator'", "sem": lambda: lambda:  set([Instance('circle_of_latitude', 'equator')])  },
        { "syn": "proper_noun -> 'australasia'", "sem": lambda: lambda:  set([Instance('region', 'australasia')])  },
    ]