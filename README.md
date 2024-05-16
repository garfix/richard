A Natural Language Understanding and Execution library for Python

This library turns a question, statement or command from a ordinary human language directly into Python executable code. It is completely rule-based and you as a developer define the code that is to be executed. The executable code can be any Python code, and there is special support for database access.

## Features

* Python code as semantic attachments to parse rules
* Interaction with databases (In-memory, PostgreSQL)

## Requires

* Python 3.10 (or higher)

## Setup

To add the project to your virtual environment, use

    pip install richard

If you want the system to interact with a PostgreSQL database, add one of these packages:

    pip install psycopg2
    pip install psycopg2-binary

## Documentation

Documentation is available at [readthedocs](https://richard.readthedocs.io/).

