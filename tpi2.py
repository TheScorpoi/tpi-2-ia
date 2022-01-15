#encoding: utf8

from venv import main
from semantic_network import *
from bayes_net import *
from collections import Counter
from itertools import product


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
        predecessors =  {d.relation.entity2 for d in self.query_local(e1=entity) if isinstance(d.relation, (Member, Subtype))}
        assocs:list[AssocOne] = [d.relation.entity2 for d in self.query_local(e1=entity, relname=assoc) if isinstance(d.relation, AssocOne)]

        counter = Counter(assocs)
        T = len(assocs) #total number of declations from assoc
        local_assoc= {a : (counter[a]/(2*T))+(1-(counter[a]/(2*T)))*(1-(0.95**counter[a]))*(0.95**(T-counter[a])) for a in assocs} #counter[a] -> n
        
        predecessors_confidence = {}
        for predecessor in predecessors:
            prede_confidence = self.query_with_confidence(predecessor, assoc)
            for decl in prede_confidence:
                if decl not in predecessors_confidence:
                    predecessors_confidence[decl] = prede_confidence[decl]
                else:
                    predecessors_confidence[decl] += prede_confidence[decl]
        
        #calculate avg confidence
        predecessor_confidence_avg = {}
        for p in predecessors_confidence:
            predecessor_confidence_avg[p] = predecessors_confidence[p]/len(predecessors)
            
        if not predecessors: #if there is no predecessors return the local assoc
            return local_assoc

        if not local_assoc: #if local_assoc is empty return the predecessors_confidence_avg with a discount of 0.1
            return {c : predecessor_confidence_avg[c] * 0.9 for c in predecessor_confidence_avg}

        all_entity2 = set(local_assoc.keys()) | set(predecessor_confidence_avg.keys())
        if not all_entity2: #if all_entity2 is empty return the local_assoc
            return local_assoc

        ninty_percent = 0.9
        ten_percent = 0.1
        confidence = 0
        result = dict(local_assoc)
        #final calculations for the confidence,update value on local_assoc
        for entity2 in all_entity2: 
            if entity2 in result:
                confidence += result[entity2]
                result[entity2] = confidence
            elif entity2 in result and entity2 in predecessor_confidence_avg:
                confidence += result[entity2] *  ninty_percent
                confidence += predecessor_confidence_avg[entity2] * ten_percent
                result[entity2] = confidence
            elif entity2 in predecessor_confidence_avg:
                confidence += predecessor_confidence_avg[entity2] * ten_percent
                result[entity2] = confidence                
            confidence = 0
        return result
                
class MyBN(BayesNet):
    def __init__(self):
        BayesNet.__init__(self)
        self.result = dict()
    def individual_probabilities(self):
        for var in [v for v in self.dependencies.keys()]:
            mothers = self._gen_conj(self.mothers(var))
            self.result[var] = sum([self.jointProb([(var, True)] + conj) for conj in mothers])           
        return self.result
    def _gen_conj(self, variables):
        l = product([True,False], repeat=len(variables))
        return list(map(lambda c : list(zip(variables, c)),l))
    def mothers(self, var):
        local_variables  = [v for (v,x) in list(self.dependencies[var].keys())[0]]
        for varibales in local_variables:
            local_variables += self.mothers(varibales)
        return set(local_variables)