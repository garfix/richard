from richard.core.Model import Model
from richard.core.constants import RESOLVE_NAME
from richard.entity.Variable import Variable


class FrontResolveName:

    def sort(self, composition: list[tuple]):
        name_resolvers, others = self.extract_list(composition)
        return name_resolvers + others


    def extract_list(self, composition: list[tuple]):
        name_resolvers = []
        rest_composition = []

        for atom in composition:
            if isinstance(atom, list):
                child_name_resolvers, child = self.extract_list(atom)
                name_resolvers.extend(child_name_resolvers)
                rest_composition.append(child)
            elif isinstance(atom, tuple):
                if atom[0] == RESOLVE_NAME:
                    name_resolvers.append(atom)
                else:
                    child_name_resolvers, child = self.extract_tuple(atom)
                    name_resolvers.extend(child_name_resolvers)
                    rest_composition.append(child)
            else:
                rest_composition.append(atom)

        return name_resolvers, rest_composition


    def extract_tuple(self, terms: tuple):
        name_resolvers = []
        rest_composition = []

        for term in terms:
            if isinstance(term, list):
                child_name_resolvers, child = self.extract_list(term)
                name_resolvers.extend(child_name_resolvers)
                rest_composition.append(child)
            else:
                rest_composition.append(term)

        return name_resolvers, tuple(rest_composition)

