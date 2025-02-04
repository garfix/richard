## Hello world

This basic application says "Hi there!" in response to a user's entry of "Hello world".

Next to that, in order to give you an idea what a simple interaction with a database looks like, it has a stripped down version of the CHAT-80 replication that is able to answer the first question of the dialog: "What rivers are there?"

In order to answer the question, the following steps take place:

* set up the database: `HelloWorldDB` creates a in-memory SQLite database. Use your own database if you have one.
* create a database module: `HelloWorldModule` creates the predicates needed to interact with the database
* define the intents and other inference rules: `inferences.pl` and `intents.pl` define the Prolog-like rules
* create a dialog context for dialog-wide facts that follow from the `dialog` parts of executed read grammar
* create a output buffer to store output atoms used by the generator
* create the model that references all data stores via their modules
* define the input pipeline: the parser, the composer, and the executor. The parser needs a `read_grammar`.
* define the generator. The generator needs to `write_grammar`.
* create the system. The system combines everything.

Next, the demo shows how to execute all tests.

Finally, the demo shows how to use the system by entering "Hello world" and receiving a response.
