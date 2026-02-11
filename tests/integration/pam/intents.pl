intent_understand(Story) :-
    store(output_type('understood')), induce_facts(Story), analyze_plans(Story).

intent_explanation(Question) :-
    store(output_type('question')).

