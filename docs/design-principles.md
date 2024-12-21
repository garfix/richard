# Design principles

The framework aims to be both expressive and simple. Historical language models are replicated in order to extend the expressiveness of the system as a whole, and the aim is to implement all of these systems sharing the same techniques, minimizing custom code.

Things to keep in mind when extending the framework

* All entity classes are immutable
* Annotate types
* Don't use archaic terms
* Explain things in a simple way
* Provide simple techniques for simple problems and complex techniques for complex problems
* A block is a processing step that can have multiple possible results or interpretations
* Each block has zero or more steps. Each step can have a implementation that can set via setter-injection. No default steps are set, to ensure backward-compatibility.
* Keep external dependencies to a minimum. Use optional dependencies when possible.
* Expose shortcomings, rather than to smooth-talk over them (this is a hard one)


