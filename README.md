A Natural Language Understanding and Execution library for Python

This library turns a question, statement or command from a ordinary human language directly into Python executable code. It is completely rule-based and you as a developer define the code that is to be executed. The executable code can be any Python code, and there is specially suited for database access.

## In development

Note! While still on version 0 I will introduce backward-incompatible changes as I'm looking for the right form. Also, the documentation will not always match the code.

## Features

* A configurable processing pipeline
* Python code as semantic attachments to parsing rules
* Inference rules (using basic Prolog syntax)
* Interaction with any type of data source
* Predefined data sources for Postgres, MySql, Sqlite, Sparql
* Code examples mimicking Chat-80, Wikidata access

## Requires

* Python 3.10 (or higher)

## Setup

To add the project to your virtual environment, use

    pip install richard

## Documentation

Documentation is available at [readthedocs](https://richard.readthedocs.io/).

