resolve_name(Name, Id) :- wikidata_label(Id, Name).
place_of_birth(PersonId, Place) :- wikidata_place_of_birth(PersonId, PlaceId), wikidata_label(PlaceId, Place).
