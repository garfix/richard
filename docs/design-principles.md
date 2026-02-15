# Design principles

The framework aims to be both expressive and simple. Historical language models are replicated in order to extend the expressiveness of the system as a whole, and the aim is to implement all of these systems sharing the same techniques, minimizing custom code.

Things to keep in mind when extending the framework

* Classes are immutable when possible
* Annotate types
* Don't use archaic terms
* Explain things in a simple way
* Provide simple techniques for simple problems and complex techniques for complex problems
* Keep external dependencies to a minimum. Use optional dependencies when possible.
* Expose shortcomings, rather than to smooth-talk over them (this is a hard one)
