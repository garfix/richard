![Richard!](richard-logo.png)

A Natural Language Understanding and Execution library for Python

This library is able to turn a sentence in any ordinary human language directly into executable Python code. It can be used as answering engine, a command executor, or to join me in my study to explore what is possible with a natural language interface.

The system is completely rule-based, which means that you as a developer have to write the processing pipeline, the grammar and most of the relations. The prize is complete control over the code that is to be executed. The results are accurate, repeatable, and transparent.

In this project, a successor to my earlier [NLI-GO](https://github.com/garfix/nli-go), I will (attempt to) replicate landmark historical NLI systems in a single architecture. Each system provides a different perspective on the field. The goal is not just to replicate each historical system, but to replicate it in a way that will eventually enable the integration of all these systems. The subject is complicated (to the point of screaming out loud) and quite out of fashion, but the attitude was and will be: don't dwell on what can't be done, find out what can be done, and make it easier and easier.

A good way to get an idea about the system is to look at the demos in the `tests/integration` directory and read the [documentation](https://richard.readthedocs.io/).

## In development

Note! While still on version 0 I will introduce backward-incompatible changes as I'm looking for the right form. Also, the documentation will not always match the code.

## Versions

* 0.4 February 2025
    * storing facts and learning rules
    * integrate tokenizer into parser to enable morphological analysis
    * generator with write grammar
    * use sqlite3 to store data in all examples
    * Cooper's system (1964) demo
    * Bertram Rafael's SIR (1964) demo
* 0.3 September 2024
    * from function based grammar to atom based grammar
    * inference engine
    * adapters for PostgreSQL, MySQL, Sqlite3, and SPARQL
    * parse tree ordering heuristics
    * David H.D. Warren's query optimization techniques
    * Chat-80 (1981) demo
    * Wikidata demo
* 0.2 May 2024
    * set up the pipeline
    * Earley parser
    * function based grammar and execution
* 0.1 May 2024
    * starting up

## Features

* A configurable processing pipeline
* An implementation of Earley's parser
* Lists of tuples (logic atoms) as semantic attachments to parsing rules
* An executor that processes logic atoms
* Inference rules (using basic Prolog syntax)
* Interaction with any type of data source
* Predefined data sources for Postgres, MySql, Sqlite, and Sparql
* Implementation of David H.D. Warren's query optimizations
* Code example that replicates a Chat-80 dialog
* Code example for a Wikidata dialog (proof-of-concept)

## Requires

* Python 3.10 (or higher)

## Setup

To add the project to your virtual environment, use

    pip install richard

## Documentation

Documentation is available at [readthedocs](https://richard.readthedocs.io/).

