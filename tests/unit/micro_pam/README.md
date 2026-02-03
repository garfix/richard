MicroPAM (McPAM) captures the essential flavor of Robert Wilensky's PAM. It can be found in the book "Inside computer understanding", by Roger C. Schank and Christopher K. Riesbeck (1981)

This repository contains a Python port of the original Lisp code

Basic use of the code:

~~~python
micro_pam = MicroPAM(init_rules, sub_for, plans_for, instance_of, isa_props)

story = [
    # Willa was hungry
    ['is', ['actor', ['person', ['name', ['Willa']]]], ['state', ['hunger', ['val', [5]]]]],
    # She picked up the Michelin guide
    ['grasp', ['actor', ['person', ['name', ['Willa']]]], ['object', ['book', ['type', ['restaurant-guide']]]]],
    # She got into her car
    ['ptrans', ['actor', ['person', ['name', ['Willa']]]], ['object', ['person', ['name', ['Willa']]]], ['to', ['car']]]
]

log = []
for cd in story:
    micro_pam.justify(cd, log)

print(log)
~~~

The file `test.py` contains a test:

~~~sh
python3 -m unittest test.py 
~~~

Some remarks:

* MicroPAM bindings are in the form [ [name, value], [name, value], ...], but we'll just use a dict in the Python port

