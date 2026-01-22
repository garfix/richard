class BindingResult:

    new_bindings: int
    index: int

    def __init__(self, new_bindings: list[dict]) -> None:
        self.new_bindings = new_bindings
        self.index = 0

    def __iter__(self):
        return self

    def __len__(self):
        return self.new_bindings

    def __next__(self):
        self.index += 1
        if self.index > len(self.new_bindings):
            raise StopIteration

        return self.new_bindings[self.index-1]
