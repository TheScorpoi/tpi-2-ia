#encoding: utf8

from venv import main
from semantic_network import *
from bayes_net import *
from collections import Counter


class MySemNet(SemanticNetwork):
    def __init__(self):
        SemanticNetwork.__init__(self)

    def source_confidence(self,user):
        assoc_one_user = []
        all_assoc_one = []
        list = []
        most_common_list = []
        correct = 0
        wrong = 0
        for d in self.declarations:
            if isinstance(d.relation, AssocOne) and d.user == user: 
                assoc_one_user.append(d) #fill list with all relation AssocOne that declaration user is equals to user
            if isinstance(d.relation, AssocOne):
                all_assoc_one.append(d) #fill list with all relation AssocOne
        
        for d_user in assoc_one_user: #for each declaration of assoc_one_user
            list.clear()
            for d_all in all_assoc_one: #for each declaration os all_assoc_one
                if d_all.relation.name == d_user.relation.name and d_all.relation.entity1 == d_user.relation.entity1:
                    list.append(d_all.relation.entity2) #add to list the entity2, the declarations that have the same entity1 and relation name
            
            most_commons = Counter(list).most_common()
            most_common = [declaration[0] for declaration in [d for d in most_commons if most_commons[0][1] == d[1]]]
            most_common_list.append(most_common)

        for i in range(len(assoc_one_user)): #for each declaration of assoc_one_user
            if assoc_one_user[i].relation.entity2 in most_common_list[i]: #if the entity2 of declaration is in the most_common_list correct increment by 1
                correct += 1
            else: #if the entity2 of declaration is not in the most_common_list wrong increment by 1
                wrong += 1
        return (1 - (0.75 ** correct)) * (0.75 ** wrong)

    def query_with_confidence(self,entity,assoc):
        # IMPLEMENT HERE
        T = 0 #relations total
        n = 0 #number each one occour
        # sum(n) = T
        



class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        self.result = dict()
        
    def individual_probabilities(self):
        for v in self.dependencies.keys():
            temp_vars = [k for k in self.dependencies.keys() if k != v]
            self.result[v] = round(sum([ self.jointProb([(v, True)] + c) for c in self._generate_conj(temp_vars)]), 3)
        return self.result

    def _generate_conj(self, variaveis):
        if len(variaveis) == 1:
            return [[(variaveis[0], True)] , [(variaveis[0], False)]]
        
        conj_list = []
        conj_remain = self._generate_conj(variaveis[1:])
        for c in conj_remain:
            conj_list.append([(variaveis[0], True)] + c)
            conj_list.append([(variaveis[0], False)] + c)
        return conj_list
