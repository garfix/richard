from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.store.Record import Record
from richard.store.MemoryDb import MemoryDb

# fill an in-memory database

db = MemoryDb()
db.insert(Record('river', {'id': 'amazon'}))
db.insert(Record('river', {'id': 'brahmaputra'}))

db.insert(Record('country', {'id': 'afghanistan', 'region': 'indian_subcontinent', 'lat': 33, 'long': -65, 'area': 254.861, 'population': 18.290, 'capital': 'kabul', 'currency': 'afghani'}))
db.insert(Record('country', {'id': 'china', 'region': 'far_east', 'lat': 30, 'long': -110, 'area': 3691.502, 'population': 840.0, 'capital': 'peking', 'currency': 'yuan'}))
db.insert(Record('country', {'id': 'upper_volta', 'region': 'west_africa', 'lat': 12, 'long': 2, 'area': 105.869, 'population': 5.740, 'capital': 'ouagadougou', 'currency': 'cfa_franc'}))       
db.insert(Record('country', {'id': 'rwanda', 'region': 'central_africa', 'lat': -2, 'long':-30, 'area': 10.169, 'population': 3.980, 'capital': 'kigali', 'currency': 'rwanda_franc'}))       
db.insert(Record('country', {'id': 'albania', 'region': 'southern_europe', 'lat': 41, 'long': -20, 'area': 11.100, 'population': 2.350, 'capital': 'tirana', 'currency': 'lek'}))
db.insert(Record('country', {'id': 'united_kingdom', 'region': 'western_europe', 'lat': 54, 'long': 2, 'area': 94.209, 'population': 55.930, 'capital': 'london', 'currency': 'pound'}))

db.insert(Record('country', {'id': 'mozambique', 'region': 'southern_africa', 'lat': -19, 'long': -35, 'area': 303.373, 'population': 8.820, 'capital': 'maputo', 'currency': '?'}))
db.insert(Record('country', {'id': 'thailand', 'region': 'southeast_east', 'lat': 16, 'long': -102, 'area': 198.455, 'population': 39.950, 'capital': 'bangkok', 'currency': 'baht'}))
db.insert(Record('country', {'id': 'congo', 'region': 'central_africa', 'lat': -1, 'long': -16, 'area': 132.46, 'population': 1.1, 'capital': 'brazzaville', 'currency': 'cfa_franc'}))

db.insert(Record('country', {'id': 'united_states', 'region': 'north_america', 'lat': 37, 'long': 96, 'area': 3615.122, 'population': 211.210, 'capital': 'washington', 'currency': 'dollar'}))
db.insert(Record('country', {'id': 'paraguay', 'region': 'south_america', 'lat': -23, 'long': 57, 'area': 157.47, 'population': 2.670, 'capital': 'asuncion', 'currency': 'guarani'}))

db.insert(Record('ocean', {'id': 'indian_ocean'}))    
db.insert(Record('ocean', {'id': 'atlantic'}))    
db.insert(Record('ocean', {'id': 'pacific'}))            
db.insert(Record('ocean', {'id': 'southern_ocean'}))    
db.insert(Record('ocean', {'id': 'arctic_ocean'}))    

db.insert(Record('borders', {'country_id1': 'afghanistan', 'country_id2': 'china'}))    
db.insert(Record('borders', {'country_id1': 'mozambique', 'country_id2': 'indian_ocean'}))    
db.insert(Record('borders', {'country_id1': 'china', 'country_id2': 'indian_ocean'}))    
db.insert(Record('borders', {'country_id1': 'thailand', 'country_id2': 'indian_ocean'}))    
db.insert(Record('borders', {'country_id1': 'congo', 'country_id2': 'atlantic'}))    

# create an adapter for this data source

ds = MemoryDbDataSource(db)

