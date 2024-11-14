![Richard!](richard-logo.png)

A Natural Language Understanding and Execution library for Python

This library is able to turn a sentence in any ordinary human language directly into executable Python code. It can be used as answering engine, a command executor, or to join me in my study to explore what is possible with a natural language interface.

The system is completely rule-based, which means that you as a developer have to write the processing pipeline, the grammar and most of the relations. The prize is complete control over the code that is to be executed. The results are accurate, repeatable, and transparent.

In this project, a successor to my earlier [NLI-GO](https://github.com/garfix/nli-go), I will (attempt to) replicate landmark historical NLI systems in a single architecture. Each system provides a different perspective on the field. The subject is complicated (to the point of screaming out loud) and quite out of fashion, but the attitude was and will be: don't dwell on what can't be done, find out what can be done, and make it easier and easier.

A good way to get an idea about the system is to look at the demos in the `tests/integration` directory and read the [documentation](https://richard.readthedocs.io/).

## In development

Note! While still on version 0 I will introduce backward-incompatible changes as I'm looking for the right form. Also, the documentation will not always match the code.

## Versions

* 0.4 ?
    * storing facts and learning rules
    * Cooper's system (1964) demo
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

## Example code

Here's part of the setup that replicates the famous historical CHAT-80 system. You can see that the processing pipeline is built up from just the blocks needed to do the job. The model is built from modules, each of which implements a number of relations in Python code. The test code is tells the system to run the questions and compare them with the answers.

~~~python

class Chat80Test(unittest.TestCase):

    def test_chat80(self):

        facts = Chat80Module(MemoryDbDataSource(db))

        inferences = InferenceModule()
        sentence_context = BasicSentenceContext()
        dialog_context = Chat80DialogContext()

        model = Model([
            facts,
            inferences,
            sentence_context,
            dialog_context
        ])

        tokenizer = BasicTokenizer()
        parser = BasicParser(get_grammar(), tokenizer)
        composer = SemanticComposer(parser)
        composer.query_optimizer = BasicQueryOptimizer(model)
        composer.sentence_context = sentence_context
        executor = AtomExecutor(composer, model)
        responder = SimpleResponder(model, executor)

        pipeline = Pipeline([
            FindOne(tokenizer),
            FindOne(parser),
            FindOne(composer),
            TryFirst(executor),
            FindOne(responder)
        ])

        tests = [
            ["Does Afghanistan border China?", "yes"],
            ["Which is the largest african country?", "sudan"],
            ["What is the ocean that borders African countries and that borders Asian countries?", "indian_ocean"],
            ["What percentage of countries border each ocean?", [
                ['arctic_ocean', "2"],
                ['atlantic', "36"],
                ['indian_ocean', "14"],
                ['pacific', "20"],
                ['southern_ocean', "0"],
            ]],
        ]

        logger = Logger()
        tester = DialogTester(self, tests, pipeline, logger)
        tester.run()

        print(logger)
~~~

## Example grammar

Showing part of the grammar that mimics a CHAT-80 dialog. Each rule has a syntactic rewrite part, a semantic attachment, and a set of inferences that create facts in the sentence context.

~~~python
def get_grammar():

    return [

        # sentence
        {
            "syn": "s(E1) -> 'does' np(E1) vp_nosub_obj(E1) '?'",
            "sem": lambda np, vp_nosub_obj: apply(np, vp_nosub_obj),
            "inf": [("format", "y/n")],
        },
        {
            "syn": "s(E1) -> 'which' 'is' np(E1) '?'",
            "sem": lambda np: apply(np, []),
            "inf": [("format", "list"), ("format_list", e1)],
        },
        {
            "syn": "s(E1) -> 'what' 'is' np(E1) '?'",
            "sem": lambda np: apply(np, []),
            "inf": [("format", "list"), ("format_list", e1)],
        },
        {
            "syn": "s(E2, E3) -> 'what' 'percentage' 'of' np(E1) tv(E1, E2) 'each' nbar(E2) '?'",
            "sem": lambda np, tv, nbar: nbar + [('percentage', E3, apply(np, tv), apply(np, []))],
            "inf": [("format", "table"), ("format_table", [e2, e3], [None, None])],
        },


        # active transitive: sub obj
        { "syn": "vp_nosub_obj(E1) -> tv(E1, E2) np(E2)", "sem": lambda tv, np: apply(np, tv) },
        { "syn": "vp_nosub_obj(E1) -> 'does' 'not' vp_nosub_obj(E1)", "sem": lambda vp_nosub_obj: [('not', vp_nosub_obj)] },

        # transitive verbs
        { "syn": "tv(E1, E2) -> 'border'", "sem": lambda: [('borders', E1, E2)] },
        { "syn": "tv(E1, E2) -> 'borders'", "sem": lambda: [('borders', E1, E2)] },
        { "syn": "tv(E1, E2) -> 'flow' 'through'", "sem": lambda: [('flows_through', E1, E2)] },
        { "syn": "tv(E1, E2) -> 'exceeds'", "sem": lambda: [('>', E1, E2)] },

        # nbar
        { "syn": "nbar(E1) -> adj(E1) nbar(E1)", "sem": lambda adj, nbar: adj + nbar },
        { "syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun },
        { "syn": "nbar(E1) -> nbar(E1) pp(E1)", "sem": lambda nbar, pp: nbar + pp },

        # relative clauses
        { "syn": "relative_clause(E1) -> 'that' vp_nosub_obj(E1)", "sem": lambda vp_nosub_obj: vp_nosub_obj },

        # np
        { "syn": "np(E1) -> nbar(E1)", "sem": lambda nbar:
            SemanticTemplate([Body], nbar + Body) },
        { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar:
            SemanticTemplate([Body], apply(det, nbar, Body)) },

        # determiner
        { "syn": "det(E1) -> 'some'", "sem": lambda:
            SemanticTemplate([Range, Body], Range + Body) },
        { "syn": "det(E1) -> 'no'", "sem": lambda:
            SemanticTemplate([Range, Body], [('none', Range + Body)]) },
        { "syn": "det(E1) -> number(E1)", "sem": lambda number:
            SemanticTemplate([Range, Body], [('det_equals', Range + Body, number)]) },
        { "syn": "det(E1) -> 'more' 'than' number(E1)", "sem": lambda number:
            SemanticTemplate([Range, Body], [('det_greater_than', Range + Body, number)]) },

        # number
        { "syn": "number(E1) -> 'one'", "sem": lambda: 1 },
        { "syn": "number(E1) -> 'two'", "sem": lambda: 2 },
        { "syn": "number(E1) -> token(E1)", "sem": lambda token: int(token), "if": lambda token: re.match('^\d+$', token) },
        { "syn": "number(E1) -> number(E1) 'million'", "sem": lambda number: number * 1000000 },

        # adjective phrases
        { "syn": "adjp(E1) -> adj(E1)", "sem": lambda adj: adj },
        { "syn": "adj(E1) -> 'european'", "sem": lambda: [('european', E1)] },
        { "syn": "adj(E1) -> 'african'", "sem": lambda: [('african', E1)] },

        # noun
        { "syn": "noun(E1) -> 'river'",         "sem": lambda: [('river', E1)],         "inf": [('isa', e1, 'river')] },
        { "syn": "noun(E1) -> 'rivers'",        "sem": lambda: [('river', E1)],         "inf": [('isa', e1, 'river')] },

        { "syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [('resolve_name', proper_noun, E1)] },

        # proper noun
        { "syn": "proper_noun(E1) -> token(E1)", "sem": lambda token: token },
    ]
~~~

## Documentation

Documentation is available at [readthedocs](https://richard.readthedocs.io/).

