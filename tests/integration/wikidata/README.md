[Wikidata](https://www.wikidata.org/) is a free, collaborative, multilingual, secondary knowledge base, collecting structured data to provide support for Wikipedia, Wikimedia Commons, the other wikis of the Wikimedia movement, and to anyone in the world.


## Mapping domain predicates to Wikidata predicates

The rules in `mapping.pl` map domain predicates to Wikidata predicates. The wikidata predicates are implemented in WikidataModule.

## User manual

User manual for the Query Service

https://www.mediawiki.org/wiki/Wikidata_Query_Service/User_Manual

## Query limitations

You are responsible for making limiting the number of queries to Wikidata.

From the documentation:

There is a hard query deadline configured which is set to 60 seconds. There are also following limits:

One client (user agent + IP) is allowed 60 seconds of processing time each 60 seconds
One client is allowed 30 error queries per minute
