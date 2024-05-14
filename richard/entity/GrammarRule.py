from dataclasses import dataclass

from richard.constants import POS_TYPE_RELATION, POS_TYPE_WORD_FORM
from richard.entity.RuleConstituent import RuleConstituent


@dataclass(frozen=True)
class GrammarRule:
    
    antecedent: RuleConstituent
    consequents: list[RuleConstituent]
    sem: callable


    def equals(self, other_rule) -> bool:

        if not self.antecedent.equals(other_rule.antecedent):
            return False

        if len(self.consequents) != len(other_rule.consequents):
            return False
        
        for i, consequent in enumerate(self.consequents):
            if not consequent.equals(other_rule.consequents[i]):
                return False
            
        return True
    

    def basic_form(self):

        s = self.antecedent.predicate #+ "("
        # sep2 = ""
        # for variable in self.antecedent.arguments:
        #     s += sep2 + variable
        #     sep2 = ", "
        # s += ")"

        s += " -> "

        sep = ""
        for i in range(len(self.consequents)):
            if self.consequents[i].position_type == POS_TYPE_RELATION:
                s += sep + self.consequents[i].predicate # + "("
                # sep2 = ""
                # for variable in self.consequents[i].arguments :
                #     s += sep2 + variable
                #     sep2 = ", "
                # s += ")"
            elif self.consequents[i].position_type == POS_TYPE_WORD_FORM:
                s += sep + "'" + self.consequents[i].predicate + "'"
            else:
                s += sep + "/" + self.consequents[i].predicate + "/"
            sep = " "

        return s

