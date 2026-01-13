class BindingResult:

    base_binding: list[tuple]
    new_bindings: int
    index: int

    def __init__(self, base_binding: dict, new_bindings: list[dict]) -> None:
        self.base_binding = base_binding
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

        return self.base_binding | self.new_bindings[self.index-1]
