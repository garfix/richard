from richard.entity.Variable import Variable


def format_value(value: any, indent: str = "\n") -> str:
    if isinstance(value, tuple):
        text = indent + "("
        sep = ""
        for element in value:
            text += sep + format_value(element, indent + "    ")
            sep = ", "
        text += ")"
    elif isinstance(value, list):
        text = indent + "["
        for element in value:
            text += format_value(element, indent + "    ")
        text += indent + "]"
    elif isinstance(value, str):
        text = "'" + value + "'"
    else:
        text = str(value)
    return text



class IsolateIndependentParts:
    """
    Based on "Efficient processing of interactive relational database queries in logic" - David H.D. Warren (1981)
    """

    def isolate(self, atoms: list[tuple], root_variables: list[str]) -> list[tuple]:
        if len(atoms) == 0:
            return []


        dependency_graph = self.create_dependency_graph(atoms)

        isolation_graph = self.create_isolation_graph(atoms, root_variables, dependency_graph)

        # print(format_value(atoms))
        # print(dependency_graph)
        # print(isolation_graph)

        iso = self.isolate_atoms_from_graph(atoms, isolation_graph, list(isolation_graph[None]), root_variables)

        # print(format_value(iso))

        # exit()

        return iso

        return atoms


    def create_dependency_graph(self, atoms: list[tuple]):
        graph = {}

        for i, atom in enumerate(atoms):
            indexes = set()
            for arg in atom[1:]:
                if isinstance(arg, Variable):
                    indexes |= set(self.find_atoms_with_variable(atoms, arg.name))

            if i in indexes:
                indexes.remove(i)
            graph[i] = indexes

        return graph


    def create_isolation_graph(self, atoms: list[tuple], root_variables: list[str], dependency_graph: dict):
        isolation_graph = {None: []}

        for i, atom in enumerate(atoms):
            if self.is_first_atom_to_contain_root_variable(atom, atoms[:i], root_variables):
                dependent_atom = None
            elif self.has_dependencies_to_succeeding_atoms(i, atoms, dependency_graph):
                dependent_atom = None
            else:
                dependent_atom = self.find_first_dependent_atom(atom, atoms[:i])

            if not i in isolation_graph:
                isolation_graph[i] = []
            isolation_graph[dependent_atom].append(i)

        return isolation_graph


    def has_dependencies_to_succeeding_atoms(self, atom_index: int, atoms: list[tuple], dependency_graph: dict):

        # print(atom_index, atoms, dependency_graph)

        if not atom_index in dependency_graph:
            # print('No')
            return False

        for i in dependency_graph[atom_index]:
            atom = atoms[i]
            dependent_atom_index = self.find_first_dependent_atom(atom, atoms[:i])
            # print(atom, i, dependent_atom_index)
            if dependent_atom_index is not None and dependent_atom_index > atom_index:
                # print('Yes')
                return True

        # print('No 2')
        return False


    def find_atoms_with_variable(self, atoms: list[tuple], variable: str) -> list[int]:
        indexes = []
        for i, atom in enumerate(atoms):
            for arg in atom[1:]:
                if isinstance(arg, Variable) and arg.name == variable:
                    indexes.append(i)
        return indexes


    def is_first_atom_to_contain_root_variable(self, atom: tuple, preceding_atoms: list[tuple], root_variables: list[str]) -> bool:
        # if atom contains any root variables, check if some atom contained them earlier

        found_root_variables = set()
        for arg in atom[1:]:
            if isinstance(arg, Variable):
                if arg.name in root_variables:
                    found_root_variables.add(arg.name)

        if len(found_root_variables) == 0:
            return False

        is_firsts = []

        # print(preceding_atoms)

        for root_variable in found_root_variables:
            is_first = True
            for an_atom in preceding_atoms:
                for an_arg in an_atom[1:]:
                    # print(an_atom, an_arg, isinstance(an_arg, Variable), root_variable)
                    if isinstance(an_arg, Variable) and an_arg.name == root_variable:
                        # print('First!')
                        is_first = False
            is_firsts.append(is_first)

        # print(atom, is_firsts, not False in is_firsts, found_root_variables, preceding_atoms)

        return True in is_firsts


    def find_first_dependent_atom(self, atom: tuple, preceding_atoms: list[tuple]):
        # for each variable of atom, find the first atom it depends on
        # from all these dependent atoms, pick the last

        firsts = []

        for arg in atom[1:]:
            if isinstance(arg, Variable):
                first = None
                for i, an_atom in enumerate(preceding_atoms):
                    for an_arg in an_atom:
                        if isinstance(an_arg, Variable) and an_arg.name == arg.name:
                            if first is None:
                                first = i
                if first is not None:
                    firsts.append(first)

        if len(firsts) == 0:
            return None
        else:
            return max(firsts)


    def isolate_atoms_from_graph(self, atoms: list[tuple], graph: dict, indexes: list[int|None], root_variables: list[str]):

        isolated = []

        for i, atom in enumerate(atoms):

            # print(i)

            if i in indexes:
                if i in graph[None]:
                    isolated.append(atoms[i])
                    isolated.extend(self.isolate_atoms_from_graph(atoms, graph, graph[i], root_variables))
                else:
                    isolated.append(('isolated', [atom] + self.isolate_atoms_from_graph(atoms, graph, graph[i], root_variables)))

        recursive_isolated = [self.isolate_arguments(atom, root_variables) for atom in isolated]

        return recursive_isolated


    def isolate_arguments(self, atom, root_variables: list[str]):
        isolated_args = []

        extended_root_variables = root_variables.copy()
        for arg in atom:
            if isinstance(arg, Variable):
                extended_root_variables.append(arg.name)

        for arg in atom:
            if isinstance(arg, list):
                isolated_args.append(self.isolate(arg, extended_root_variables))
            else:
                isolated_args.append(arg)

        return tuple(isolated_args)


