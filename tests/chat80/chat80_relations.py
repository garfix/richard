from richard.type.Simple import Simple


def south_of(ds, values: list[Simple]):
    # this implementation could be done in SQL like "SELECT id FROM country WHERE lat < (SELECT lat FROM country WHERE id = %s)"
    id1 = values[0]
    id2 = values[1]
    lat1 = None
    lat2 = None
    latitudes = ds.select('country', ['id', 'lat'], [None, None])
    latitudes.append(['equator', 0])
    for id, lat in latitudes:
        if id == id1:
            lat1 = lat
        if id == id2:
            lat2 = lat
    if id1 and id2:
        if lat1 < lat2:
            return [[id1, id2]]
        else:
            return []
    if id2 and not id1:
        return [[id, id2] for id, lat in latitudes if lat < lat2]
    raise Exception("Unhandled case")


def continental(ds, modifier, country_id: int):
    table = "country"
    columns = ["id", "region"]
    regions = {
        "european": ['southern_europe', 'western_europe', 'eastern_europe', 'scandinavia'],
        "asian": ['middle_east', 'indian_subcontinent', 'southeast_east', 'far_east', 'northern_asia'],
        "american": ['north_america', 'central_america', 'caribbean', 'south_america'],
        "african": ['north_africa', 'west_africa', 'central_africa', 'east_africa', 'southern_africa']
    }

    ids = []
    for region in regions[modifier]:
        ids += ds.select_column(table, columns, [country_id, region])
    return ids       
