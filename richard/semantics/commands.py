
from dataclasses import dataclass

from richard.entity.Range import Range


"""
Determined Noun Phrase
"""
@dataclass(frozen=True)
class dnp:
    # determiner
    determiner: callable
    # nbar phrase
    range: Range
   

def exists(result_count, range_count):
    return result_count > 0


def accept(result_count, range_count):
    return True


def range_and(range1: Range, range2: Range) -> Range:
    if range1.entity != range2.entity:
        raise Exception("Operator AND requires that the ranges have same entity")
    
    x= Range(range1.entity, list(set(range1) & set(range2)))
    # print("and", range1, range2, x)
    return x
    
