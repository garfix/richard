from richard.constants import EXISTS


class BasicQueryOptimizer:
    def optimize(self, composition: list[tuple]) -> list[tuple]:
        composition = self.reduce_exists_finds(composition)
        return composition
    

    def reduce_exists_finds(self, composition: list[tuple]):
        """
        Reduces a 'find' with an exists quant to a simple atom
        """
        reduced = []
        for atom in composition:
            if atom[0] == 'find' and atom[2][2] == EXISTS:
                r = self.reduce_exists_find(atom)
                reduced.extend(r)
            else:
                reduced.append(atom)

        return reduced
    

    def reduce_exists_find(self, atom: tuple):
        find_predicate, find_var, quant, body = atom
        quant_predicate, quant_var, det, nbar = quant

        return self.reduce_exists_finds(nbar) + self.reduce_exists_finds(body)

