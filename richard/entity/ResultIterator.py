class ResultIterator:
    """
    A relation needs to produce a list of results. Sometimes the number of results is very large, and you're not interested in the
    inidividual results, but only in their number. This object provides a solution for this situation.
    """

    single_result: list[tuple]
    number: int
    index: int

    def __init__(self, single_result: list[tuple], number: int) -> None:
        self.single_result = single_result
        self.number = number
        self.index = 0

    def __iter__(self):
        return self

    def __len__(self):
        return self.number

    def __next__(self):
        self.index += 1
        if self.index > self.number:
            raise StopIteration
        return self.single_result


