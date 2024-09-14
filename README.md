A Natural Language Understanding and Execution library for Python

This library turns a question, statement or command from a ordinary human language directly into Python executable code. It is completely rule-based and you as a developer define the code that is to be executed. The executable code can be any Python code, and there is specially suited for database access.

## In development

Note! While still on version 0 I will introduce backward-incompatible changes as I'm looking for the right form. Also, the documentation will not always match the code.

## Features

* A configurable processing pipeline
* An implementation of Earley's parser
* Lists of tuples (logic atoms) as semantic attachments to parsing rules
* An executor that processes logic atoms
* Inference rules (using basic Prolog syntax)
* Interaction with any type of data source
* Predefined data sources for Postgres, MySql, Sqlite, and Sparql
* Implementation of David H.D. Warren's query optimizations
* Code example that mimicks a Chat-80 dialog
* Code example for a Wikidata dialog (proof-of-concept)

## Requires

* Python 3.10 (or higher)

## Setup

To add the project to your virtual environment, use

    pip install richard

## Example code

~~~python

class Test(unittest.TestCase):

    def test(self):

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

Showing part of the grammar that mimics a CHAT-80 dialog:

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

