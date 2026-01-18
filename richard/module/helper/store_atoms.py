from richard.interface.SomeSolver import SomeSolver


def store_atoms(atoms: list[tuple], solver: SomeSolver):
    for atom in atoms:

        for argument in atom[1:]:
            # if isinstance(argument, list):


            solver.write_atom(atom)
