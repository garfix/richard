resolve_name(Name, Id) :- wikidata_label(Id, Name), wikidata_person(Id).
place_of_birth(PersonId, Place) :- wikidata_place_of_birth(PersonId, PlaceId), wikidata_label(PlaceId, Place).
