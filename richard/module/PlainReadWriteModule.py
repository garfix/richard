from richard.core.functions.atoms import create_argument_binding, has_variables
from richard.entity.ExecutionContext import ExecutionContext
from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface.SomeModule import SomeModule


class PlainReadWriteModule(SomeModule):
    """
    A flexible storage that accepts any relation, and no relation needs to be specified
    """

    atoms: list[tuple]

    def __init__(self, atoms: list[tuple] = []) -> None:
        super().__init__()

        self.atoms = []
        for atom in atoms:
            self.add_atom(atom)


    def add_atom(self, atom: tuple):

        self.atoms.append(atom)

        predicate = atom[0]
        if predicate not in self.relations:
            arguments = atom[1:]
            formal_parameters = [Variable(f"E{i}") for i in enumerate(arguments)]
            self.add_relation(Relation(predicate, formal_parameters=formal_parameters, query_function=self.query, write_function=self.write))


    def query(self, arguments: list, context: ExecutionContext) -> list[list]:
        predicate = context.relation.predicate
        formal_parameters = context.relation.formal_parameters

        results = []
        for atom in self.atoms:
            if atom[0] == predicate:
                if create_argument_binding(formal_parameters, arguments, {}) is not None:
                    results.append(atom[1:])

        return results


    def write(self, arguments: list, context: ExecutionContext):
        if has_variables(arguments):
            raise Exception(f"Atom should be bound: {arguments}")

        self.atoms.append(tuple([context.relation.predicate] + arguments))


    def get_relation(self, predicate: str) -> Relation|None:
        if not predicate in self.relations:
             self.add_relation(Relation(predicate, query_function=self.query, write_function=self.write))

        return self.relations[predicate]


    def clear(self):
        self.atoms = []


