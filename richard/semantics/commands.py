
def find(np: tuple[callable, callable], vp: callable) -> list:
    """
    Result consists of all elements in np.nbar that satisfy vp
    If the number of results agrees with qp, results are returned. If not, an empty list
    """
    qp, nbar = np
    elements = nbar()
    range_count = len(elements)

    result = []
    for element in elements:
        for e2 in vp(element):
            result.append(element)

    result = list(set(result))
    result_count = len(result)
    
    if qp(result_count, range_count):
        return result
    else:
        return []
    