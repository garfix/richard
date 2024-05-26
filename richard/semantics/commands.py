
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
   

def exists(result_count, range_count):
    return result_count > 0

