from richard.entity.Variable import Variable


class VariableGenerator:

    prefix: str
    number: int


    def __init__(self, prefix: str) -> None:
        self.number = 0
        self.prefix = prefix


    def next(self) -> str:
        self.number += 1
        return self.prefix + str(self.number)
    

    def reset(self):
        self.number = 0


    def isinstance(self, variable: Variable):
        return variable.name.startswith(self.prefix)
