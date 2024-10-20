from dataclasses import dataclass
from richard.core.atoms import get_atom_variables


@dataclass(frozen=True)
class AtomBatch:
    atoms: list[tuple]
    variables: set[str]


class IsolateIndependentParts:
    """
    Based on "Efficient processing of interactive relational database queries in logic" - David H.D. Warren (1981)

    "Once the first goal has been solved, the rest of the body breaks down in ... independent parts, neither of which share uninstantiated
    variables with each other or with the head of the clause"

    The `root_variables` are the variables that play a role in the answer, and can therefore not be isolated.
    """

    def isolate(self, atoms: list[tuple], root_variables: list[str]) -> list[tuple]:
        if len(atoms) == 0:
            return []

        head = atoms[0]
        head_variables = set(get_atom_variables(head))
        new_atoms = [head]

        batches = self.collect_batches(atoms[1:], head_variables)

        for batch in batches:
            # the batch contains root variables?
            if len(batch.variables & set(root_variables)) > 0:
                # make all atoms top level
                new_atoms.extend(batch.atoms)
            else:
                # do the same for the atoms in this batch
                recursed = self.isolate(batch.atoms, [])
                # isolate the batch
                new_atoms.append(('$isolated', recursed))

        return new_atoms


    def collect_batches(self, atoms, excluded_variables: list[str]):

        # create a batch for each atom
        collection: list[AtomBatch] = []
        for atom in atoms:
            # note that the top level variables are excluded, they may occur in any batch
            variables = set(get_atom_variables(atom)) - excluded_variables
            collection.append(AtomBatch([atom], variables))

        # combine batches until the result is stable
        while True:
            new_batches: list[AtomBatch] = []
            for batch in collection:
                found = None
                for i, new_batch in enumerate(new_batches):
                    if len(batch.variables & new_batch.variables) > 0:
                        found = i
                        break
                if found == None:
                    new_batches.append(batch)
                else:
                    found_batch = new_batches[found]
                    new_batches[found] = AtomBatch(found_batch.atoms + batch.atoms, found_batch.variables | batch.variables)

            if len(new_batches) == len(collection):
                break

            collection = new_batches

        restored = [self.restore_atom_order(atoms, batch) for batch in collection]

        return restored


    def restore_atom_order(self, atoms: list[tuple], batch: AtomBatch) -> AtomBatch:
        """
        creates a new batch, based on `batch`, with the atoms in the order of `atoms`
        """
        ordered_atoms = []

        for atom in atoms:
            for batch_atom in batch.atoms:
                if batch_atom == atom:
                    ordered_atoms.append(batch_atom)
                    break

        ordered_batch = AtomBatch(ordered_atoms, batch.variables)
        return ordered_batch
