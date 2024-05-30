
def exists(result_count, range_count):
    return result_count > 0


def accept(result_count, range_count):
    return True


def range_and(range1: list, range2: list) -> list:  
    return list(set(range1) & set(range2))
    

def create_np(determiner: callable, range: callable):

    def np(vp = None):
        elements = range()
        range_count = len(elements)

        result = []
        if vp:
            for element in elements:
                for e2 in vp(element.id):
                    result.append(element)
        else:
            result = elements

        result = list(set(result))
        result_count = len(result)

        if determiner(result_count, range_count):
            return result
        else:
            return []

    return np
