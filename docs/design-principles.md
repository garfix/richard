# Design principles

Things to keep in mind when extending the framework

* All entity classes are immutable
* Annotate types
* Don't use archaic terms
* Explain things in a simple way
* Provide simple techniques for simple problems and complex techniques for complex problems
* A block is a processing step that can have multiple possible results or interpretations
* Each block has zero or more steps. Each step can have a implementation that can set via setter-injection. No default steps are set, to ensure backward-compatibility.
