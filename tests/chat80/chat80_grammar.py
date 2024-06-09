from richard.Model import Model
from richard.entity.Instance import Instance
from richard.semantics.commands import avg, count, create_np, exists, negate
from richard.type.OrderedSet import OrderedSet


def get_grammar(model: Model):
    return [

        # sentences

        { 
            "syn": "s -> 'is' 'there' np preposition 'each' nbar '?'", 
            "sem": lambda np, preposition, nbar: 
                        lambda: model.test_all(nbar, 
                                   lambda e1: count(np(lambda e2: preposition(e2)(e1))))
        },
        { 
            "syn": "s -> 'what' 'is' 'the' 'average' 'area' 'of' np preposition 'each' nbar '?'", 
            "sem": lambda np, preposition, nbar: 
                        lambda: model.group_by(nbar, 
                                   lambda e1: avg(model.find_attribute_values(lambda: 'size-of', 
                                                                                lambda: np(lambda e2: preposition(e2)(e1))))) 
        },
        { "syn": "s -> 'what' 'is' 'the' 'total' 'area' 'of' np '?'", "sem": lambda np: lambda: sum(model.find_attribute_values(lambda: 'size-of', np)) },
        { "syn": "s -> 'what' 'are' np '?'", "sem": lambda np: lambda: np() },
        { "syn": "s -> 'what' 'are' 'the' attr 'of' np '?'", "sem": lambda attr, np: lambda: model.create_attribute_map(np, attr) },
        { "syn": "s -> 'what' 'is' np '?'", "sem": lambda np: lambda: np() },
        { "syn": "s -> 'what' nbar 'are' 'there' '?'", "sem": lambda nbar: lambda: nbar() },
        { "syn": "s -> 'where' 'is' np '?'", "sem": lambda np: lambda: model.find_attribute_values(lambda: 'location-of', np) },
        { "syn": "s -> 'is' 'there' np '?'", "sem": lambda np: lambda: np() },
        { "syn": "s -> 'which' nbar 'are' adjp '?'", "sem": lambda nbar, adjp: lambda: adjp(nbar) },
        { "syn": "s -> 'which' 'is' np '?'", "sem": lambda np: lambda: np() },
        { "syn": "s -> 'which' 'country' \''\' 's' attr 'is' np '?'", "sem": lambda attr, np: 
            lambda: model.find_attribute_objects(attr, np) },
        { "syn": "s -> 'does' np vp_nosub_obj '?'",  "sem": lambda np, vp_nosub_obj: lambda: np(vp_nosub_obj) },
        { "syn": "s -> 'how' 'large' 'is' np '?'",  "sem": lambda np: lambda: model.find_attribute_values(lambda: 'size-of', np) },
        { "syn": "s -> 'how' 'many' nbar 'does' np vp_noobj_nosub '?'", "sem": lambda nbar, np, vp_noobj_nosub:
            lambda: len(create_np(exists, nbar)(lambda obj: np(vp_noobj_nosub(obj))))
        },

        { "syn": "s -> 'which' nbar 'are' vp_noobj_sub '?'", "sem": lambda nbar, vp_noobj_sub: lambda: create_np(exists, nbar)(vp_noobj_sub) },
        { "syn": "s -> 'what' 'are' np vp_noobj_sub_iob '?'", "sem": lambda np, vp_noobj_sub_iob: lambda: np(vp_noobj_sub_iob) },

        # vp

        # active transitive: sub obj
        { "syn": "vp_nosub_obj -> vp_nosub_noobj np", "sem": lambda tv, np: lambda sub: np(tv(sub)) },
        { "syn": "vp_nosub_obj -> 'does' 'not' vp_nosub_noobj np", "sem": lambda tv, np: lambda sub: negate(np(tv(sub))) },
        { "syn": "vp_nosub_noobj -> tv", "sem": lambda tv: lambda sub: lambda obj: tv(sub, obj) },

        # passive transitive: obj sub
        { "syn": "vp_noobj_sub -> vp_noobj_nosub 'by' np", "sem": lambda vp_noobj_nosub, np: lambda obj: np(vp_noobj_nosub(obj)) },
        { "syn": "vp_noobj_nosub -> tv", "sem": lambda tv: lambda obj: lambda sub: tv(sub, obj) },

        # passive ditransitive: obj sub iob
        { "syn": "vp_noobj_sub_iob -> 'from' 'which' np vp_noobj_nosub_iob", "sem": lambda np, vp_noobj_nosub_iob: lambda obj: np(vp_noobj_nosub_iob(obj)) },
        { "syn": "vp_noobj_nosub_iob -> vp_noobj_nosub_noiob np", "sem": lambda vp_noobj_nosub_noiob, np: lambda obj: lambda sub: np(vp_noobj_nosub_noiob(obj)(sub)) },
        { "syn": "vp_noobj_nosub_noiob -> dtv", "sem": lambda dtv: lambda obj: lambda sub: lambda iob: dtv(sub, obj, iob) },

        # transitive verbs
        { "syn": "tv -> 'flow' 'through'", "sem": lambda: 
            lambda sub, obj: model.find_relation_values('flows-through', [sub, obj]) },
        { "syn": "tv -> 'border'", "sem": lambda: 
            lambda sub, obj: model.find_relation_values('borders', [sub, obj], two_ways = True) },
        { "syn": "tv -> 'borders'", "sem": lambda: 
            lambda sub, obj: model.find_relation_values('borders', [sub, obj], two_ways = True) },
        { "syn": "tv -> 'bordering'", "sem": lambda: 
            lambda sub, obj: model.find_relation_values('borders', [sub, obj], two_ways = True) },
        { "syn": "tv -> 'bordered'", "sem": lambda: 
            lambda sub, obj: model.find_relation_values('borders', [sub, obj], two_ways = True) },

        # ditransitive verbs
        { "syn": "dtv -> 'flows' 'into'", "sem": lambda: 
            lambda sub, obj, iob: model.find_relation_values('flows-from-to', [sub, obj, iob]) },

        # np            

        # noun phrases
        { "syn": "np -> nbar", "sem": lambda nbar: create_np(exists, nbar) },
        { "syn": "np -> det nbar", "sem": lambda det, nbar: create_np(det, nbar) },
        { "syn": "np -> np relative_clause", "sem": lambda np, relative_clause: create_np(exists, lambda: np(relative_clause)) },
        { "syn": "np -> np relative_clause 'and' relative_clause", "sem": lambda np, rc1, rc2: create_np(exists, lambda: np(rc1) & np(rc2)) },
        { "syn": "np -> np pp", "sem": lambda np, pp: create_np(exists, lambda: np(pp)) },
        { "syn": "np -> np pp 'and' pp", "sem": lambda np, pp1, pp2: create_np(exists, lambda: np(pp1) & np(pp2)) },

        # prepositional phrases
        { "syn": "pp -> preposition np", "sem": lambda preposition, np: lambda e1: np(preposition(e1)) },
        { "syn": "pp -> 'not' preposition np", "sem": lambda preposition, np: lambda e1: negate(np(preposition(e1))) },

        { "syn": "preposition -> 'south' 'of'", "sem": lambda: lambda e1: lambda e2: model.find_relation_values('south-of', [e1, e2]) },
        { "syn": "preposition -> 'in'", "sem": lambda: lambda e1: lambda e2: model.find_relation_values('in', [e1, e2]) },

        # relative clauses
        { "syn": "relative_clause -> 'that' vp_nosub_obj", "sem": lambda vp_nosub_obj: lambda e1: vp_nosub_obj(e1) },
        { "syn": "relative_clause -> vp_nosub_obj", "sem": lambda vp_nosub_obj: lambda e1: vp_nosub_obj(e1) },

        # nbars
        { "syn": "nbar -> noun", "sem": lambda noun: lambda: noun() },
        { "syn": "nbar -> adj noun", "sem": lambda adj, noun: lambda: adj(noun) },
        { "syn": "nbar -> attr 'of' np", "sem": lambda attr, np: lambda: model.find_attribute_values(attr, np) },
        { "syn": "nbar -> superlative nbar", "sem": lambda superlative, nbar: lambda: superlative(nbar) },

        # superlatives
        { "syn": "superlative -> 'largest'", "sem": lambda: lambda range: model.find_entity_with_highest_attribute_value(range, 'size-of') },
        { "syn": "superlative -> 'smallest'", "sem": lambda: lambda range: model.find_entity_with_lowest_attribute_value(range, 'size-of') },

        # determiners
        { "syn": "det -> 'a'", "sem": lambda: exists },
        { "syn": "det -> 'the'", "sem": lambda: exists },
        { "syn": "det -> 'some'", "sem": lambda: exists },
        { "syn": "det -> 'any'", "sem": lambda: exists },
        { "syn": "det -> number", "sem": lambda number: lambda result_count, range_count: result_count == number() },
        { "syn": "det -> 'more' 'than' number", "sem": lambda number: lambda result_count, range_count: result_count > number() },

        { "syn": "number -> 'one'", "sem": lambda: lambda: 1 },
        { "syn": "number -> 'two'", "sem": lambda: lambda: 2 },

        # adjective phrases
        { "syn": "adjp -> adj", "sem": lambda adj: lambda range: adj(range) },

        { "syn": "adj -> 'european'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'european') },
        { "syn": "adj -> 'african'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'african') },
        { "syn": "adj -> 'american'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'american') },
        { "syn": "adj -> 'asian'", "sem": lambda: lambda range: model.filter_by_modifier(range, 'asian') },

        # nouns
        { "syn": "noun -> proper_noun", "sem": lambda proper_noun: lambda: proper_noun() },
        { "syn": "noun -> 'river'", "sem": lambda: lambda: model.get_instances('river') },
        { "syn": "noun -> 'rivers'", "sem": lambda: lambda: model.get_instances('river') },
        { "syn": "noun -> 'country'", "sem": lambda: lambda: model.get_instances('country') },
        { "syn": "noun -> 'countries'", "sem": lambda: lambda: model.get_instances('country') },
        { "syn": "noun -> 'ocean'", "sem": lambda: lambda: model.get_instances('ocean') },
        { "syn": "noun -> 'seas'", "sem": lambda: lambda: model.get_instances('sea') },
        { "syn": "noun -> 'continent'", "sem": lambda: lambda: model.get_instances('continent') },

        # attributes
        { "syn": "attr -> 'capital'", "sem": lambda: lambda: 'capital-of' },
        { "syn": "attr -> 'capitals'", "sem": lambda: lambda: 'capital-of' },

        # todo
        { "syn": "proper_noun -> 'afghanistan'", "sem": lambda: lambda: OrderedSet([Instance('country', 'afghanistan')]) },
        { "syn": "proper_noun -> 'china'", "sem": lambda: lambda:  OrderedSet([Instance('country', 'china')]) },
        { "syn": "proper_noun -> 'upper_volta'", "sem": lambda: lambda:  OrderedSet([Instance('country', 'upper_volta')]) },
        { "syn": "proper_noun -> 'london'", "sem": lambda: lambda:  OrderedSet([Instance('city', 'london')])  },
        { "syn": "proper_noun -> 'baltic'", "sem": lambda: lambda:  OrderedSet([Instance('sea', 'baltic')])  },
        { "syn": "proper_noun -> 'danube'", "sem": lambda: lambda:  OrderedSet([Instance('river', 'danube')])  },
        { "syn": "proper_noun -> 'equator'", "sem": lambda: lambda:  OrderedSet([Instance('circle_of_latitude', 'equator')])  },
        { "syn": "proper_noun -> 'australasia'", "sem": lambda: lambda:  OrderedSet([Instance('region', 'australasia')])  },
        { "syn": "proper_noun -> 'black_sea'", "sem": lambda: lambda:  OrderedSet([Instance('sea', 'black_sea')]) },
    ]