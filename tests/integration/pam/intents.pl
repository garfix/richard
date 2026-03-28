intent_understand(Story) :-
    store(output_type('understood')), reify(Story, Reified), store(Reified), induce_facts(Reified), analyze_plans(Reified).

intent_explanation(Question, C1) :-
    explain(Question, C1, Explanation), store(output_type('question', Explanation)).

