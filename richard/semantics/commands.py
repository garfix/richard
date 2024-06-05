from richard.type.OrderedSet import OrderedSet
from richard.type.Simple import Simple


def exists(result_count, range_count):
    return result_count > 0


def accept(result_count, range_count):
    return True
 

def create_np(determiner: callable, range: callable):

    def np(vp = None):
        elements = range()
        range_count = len(elements)

        if vp:
            result = OrderedSet()
            for element in elements:
                for _ in vp(element.id):
                    result.add(element)
        else:
            result = elements

        result_count = len(result)

        if determiner(result_count, range_count):
            return result
        else:
            return []

    return np


def negate(range: list[Simple]) -> list[Simple]:
    elements = range
    if len(elements) > 0:
        return []
    else:
        return [True]


def avg(range: list[Simple]) -> Simple:
    elements = range
    if len(elements) > 0:
        return sum(elements) / len(elements)
    else:
        return -1
        # raise Exception('Cannot average over zero elements')
