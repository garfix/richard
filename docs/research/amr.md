# AMR

Abstract Meaning Representation

* Wikipedia: https://en.wikipedia.org/wiki/Abstract_Meaning_Representation
* Guidelines: https://github.com/amrisi/amr-guidelines/blob/master/amr.md
* Basic paper: https://web.archive.org/web/20140104125210/http://amr.isi.edu/a.pdf

## syntax

An atom has

* a variable
* a name/type
* arguments

An argument has

* a name: ARG0 / ARG1, or free-form
* a value

A value is

* a scalar value (i.e. `3`)
* a variable (i.e. `p`)
* an atom

How can I model this? For example "John wants Jane to do homework"

    (w / want-01
    :ARG0 (j / person :name "John")
    :ARG1 (d / do-02
                :ARG0 (n / person :name "Jane")
                :ARG1 (h / homework)))

All arguments in a single dict

```py
('want', E1, {
    'ARG1': ('person', E2, {"name": "John"}),
    'ARG2': ('do', E3, {
        'ARG0': ('person', E4, {'name': 'Jane'}), 
        'ARG1': ('homework', E5)})
})
```

or: standard arguments as simple arguments (like before) and a dict for the extra arguments

```py
('want', E1, 
    ('person', E2, {"name": "John"}),
    ('do', E3, 
        ('person', E4, {'name': 'Jane'}), 
        ('homework', E5))
)
```

## syntax: quantification

Now

~~~py
        { "syn": "vp_noobj_sub(E1) -> 'does' np(E2) tv(E2, E1)", "sem": lambda np, tv: apply(np, tv) },

        { "syn": "np(E1) -> nbar(E1)", "sem": lambda nbar:
            SemanticFunction([Body], nbar + Body) },

        { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar:
            SemanticFunction([Body], apply(det, nbar, Body)) },

        { "syn": "det(E1) -> 'a'", "sem": lambda:
            SemanticFunction([Range, Body], Range + Body) },
~~~

Planned

~~~py
        { "syn": "vp_noobj_sub(E1) -> 'does' np(E2) tv(E2, E1)", "sem": lambda np, tv: apply(np, tv) },
~~~

This `np tv` is already a problem. Let's rewrite

~~~py
        { "syn": "vp_noobj_sub(E1) -> 'does' np(E2) verb(E2, E1) np(E1)", "sem": lambda np1, verb, np2: (verb, E1, np1, np2) },
~~~

determiner "the boy"

Now

~~~py

        { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar:
            SemanticFunction([Body], apply(det, nbar, Body)) },

        { "syn": "det(E1) -> 'a'", "sem": lambda:
            SemanticFunction([Range, Body], Range + Body) },
~~~

Planned

~~~py

        { "syn": "np(E1) -> det(E1) nbar(E1)", "sem": lambda det, nbar:
            add_arg(nbar, det) },

        { "syn": "det(E1) -> 'a'", "sem": lambda: {'determiner': 'a'} },
~~~

