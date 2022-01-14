#encoding: utf8

from venv import main
from semantic_network import *
from bayes_net import *
from collections import Counter


class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)
        # IMPLEMENT HERE (if needed)
        pass

    def source_confidence(self,user):
        assoc_one_list = []
        correct = 0
        wrong = 0
        list = []
        most_commom_one = None
        for d in self.declarations:
            if isinstance(d.relation, AssocOne):
                assoc_one_list.append(d)
        
        dict
        
        for d in assoc_one_list:
                relation = d.relation
                ent1 = d.relation.entity1
                for decla in assoc_one_list:
                    if decla.relation == relation and decla.relation.entity1 == ent1:
                        list.append(decla)
                    
        assoc_values = [d.relation.entity2 for d in list]
        for c, _ in Counter(assoc_values).most_common(1):
            most_commom_one = c
            #print(most_commom_one)
            
        for d in assoc_one_list:
            if d.relation.entity2 == most_commom_one:
                correct += 1
            else:
                wrong += 1
            
        confidence = (1 - (0.75 ** correct)) * (0.75 ** wrong)
        return confidence

    def query_with_confidence(self,entity,assoc):
        # IMPLEMENT HERE
        pass



class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        # IMPLEMENT HERE (if needed)
        pass

    def individual_probabilities(self):
        # IMPLEMENT HERE
        pass
