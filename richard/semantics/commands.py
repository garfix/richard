
from dataclasses import dataclass


"""
Determined Noun Phrase
"""
@dataclass(frozen=True)
class dnp:
    # determiner
    determiner: callable
    # nbar phrase
    nbar: callable


def filter(dnp: dnp, vp: callable = None) -> list:
    """
    Result consists of all elements in dnp.nbar that satisfy vp
    If the number of results agrees with dnp.determiner, results are returned. If not, an empty list
    """
    elements = dnp.nbar()
    range_count = len(elements)

    result = []
    if vp:
        for element in elements:
            for e2 in vp(element):
                result.append(element)
    else:
        result = elements

    result = list(set(result))
    result_count = len(result)
    
    if dnp.determiner(result_count, range_count):
        return result
    else:
        return []
    

def exists(result_count, range_count):
    return result_count > 0

