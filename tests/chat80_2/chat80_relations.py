from richard.interface.SomeDataSource import SomeDataSource
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


def flows_from_to(ds, values: list[Simple]):
    query_river = values[0]
    query_from = values[1]
    query_to = values[2]
    flows = ds.select('river', ['id', 'flows_through'], [None, None])
    results = []
    for id, flows_through in flows:
        db_to = flows_through[0]
        db_from = flows_through[1:]
        if not id or id == query_river:
            if not query_to or query_to == db_to:
                if not query_from or query_from in db_from:
                    for f in db_from:
                        results.append([id, f, db_to])

    return results

    
def continental(ds, relation, db_values: list):
    country_id = db_values[0]
    table = "country"
    columns = ["id", "region"]
    regions = {
        "european": ['southern_europe', 'western_europe', 'eastern_europe', 'scandinavia'],
        "asian": ['middle_east', 'indian_subcontinent', 'southeast_east', 'far_east', 'northern_asia'],
        "american": ['north_america', 'central_america', 'caribbean', 'south_america'],
        "african": ['north_africa', 'west_africa', 'central_africa', 'east_africa', 'southern_africa']
    }

    rows = []
    for region in regions[relation]:
        ids = ds.select_column(table, columns, [country_id, region])
        for id in ids:
            rows.append([id])
    return rows       


def resolve_name(ds: SomeDataSource, values: list) -> tuple[list[list], list[list]]:
    # todo many other entities
    name = values[0].lower()
    types = []
    db_values = ds.select("country", ["id", "id"], [name, None])
    if len(db_values) > 0:
        types = [None, 'country']
        return db_values, types

    db_values = ds.select("city", ["id", "id"], [name, None])
    if len(db_values) > 0:
        types = [None, 'city']
        return db_values, types
