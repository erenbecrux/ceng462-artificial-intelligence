import copy

class Rule:
    def __init__(self, conclusion= None, statements= [], count= 0):
        self.conclusion = conclusion
        self.statements = statements
        self.count = count

class Statement:
    def __init__(self, name= None, variables= []):
        self.name = name
        self.variables = variables

    def __eq__(self, other):
        return isinstance(other, Statement) and self.name == other.name and self.variables == other.variables

    def __hash__(self):
        return hash((self.name, tuple(self.variables)))

def parse_statement(stringStatement):
    parsedName = stringStatement.split("(")[0]
    parsedVars = stringStatement.split("(")[1].split(")")[0].split(",")
    parsedStatement = Statement(parsedName, parsedVars)
    return parsedStatement

def isConstant(e):
    if(e[0] == e[0].upper()):
        return True
    else:
        return False

def isVariable(e):
    if(e[0] == e[0].lower()):
        return True
    else:
        return False

def apply_subs(state,subs):
    newStatement = copy.deepcopy(state)
    for i in range(len(state.variables)):
        var = state.variables[i]
        if var in subs:
            newvar = subs[var]
            newStatement.variables[i] = newvar
    return newStatement


def mgu(state1, state2):
    subs = {}
    newState1 = copy.deepcopy(state1)
    newState2 = copy.deepcopy(state2)

    if state1.name == state2.name and len(state1.variables) == len(state2.variables):
        for i in range(len(state1.variables)):
            var1 = newState1.variables[i]
            var2 = newState2.variables[i]

            if isVariable(var1) and not isVariable(var2):
                subs[var1] = var2
                newState1 = apply_subs(state1,subs)
                newState2 = apply_subs(state2, subs)

            elif isVariable(var1) and isVariable(var2):
                subs[var2] = var1
                newState1 = apply_subs(state1, subs)
                newState2 = apply_subs(state2, subs)

            elif not isVariable(var1) and isVariable(var2):
                subs[var2] = var1
                newState1 = apply_subs(state1, subs)
                newState2 = apply_subs(state2, subs)

            elif not isVariable(var1) and not isVariable(var2):
                if var1 == var2:
                    continue
                else:
                    return "FAIL"
        return subs
    else:
        return "FAIL"


def forward_chaining(KB,alpha):
    rules = []
    agenda = []
    knowledge = []
    inferred = []
    goal = parse_statement(alpha)

    for item in KB:
        if "<-" in item:
            splitFromImplication = item.split("<-")
            left = splitFromImplication[0]
            right = splitFromImplication[1]

            conclusionItem = parse_statement(left)
            premisesList = []

            premises = right.split(", ")
            for premise in premises:
                spaceRemovedPremise = premise.replace(" ", "", 1)
                premiseItem = parse_statement(spaceRemovedPremise)
                premisesList.append(premiseItem)

            ruleItem = Rule(conclusionItem, premisesList, len(premisesList))
            rules.append(ruleItem)

        else:

            statementItem = parse_statement(item)
            agenda.append(statementItem)
            knowledge.append(statementItem)

    isInferred = True
    while isInferred:
        isInferred = False

        for i in range(len(rules)):
            currentRule = rules[i]
            currentSubs = {}
            currentCount = currentRule.count

            for j in range(len(agenda)):
                currentStatement = agenda[j]
                isUsedAgendaItem = False

                for premise in currentRule.statements:
                    currentPremise = apply_subs(premise, currentSubs)
                    currentMGU = mgu(currentStatement, currentPremise)
                    if currentMGU != "FAIL":
                        currentSubs.update(currentMGU)
                        for updatingPremise in currentRule.statements:
                            updatedPremise = apply_subs(updatingPremise, currentSubs)
                            if updatedPremise in knowledge:
                                currentCount -= 1
                    if currentCount <= 0:
                        inferredConclusion = apply_subs(currentRule.conclusion, currentSubs)
                        if inferredConclusion not in inferred:
                            isInferred = True
                            inferred.append(inferredConclusion)
                            if inferredConclusion == goal:
                                inferredStringList = []
                                for inferredItem in inferred:
                                    inferredString = inferredItem.name + "("
                                    for variableOfItem in inferredItem.variables:
                                        inferredString += variableOfItem + ","
                                    inferredString = inferredString[:-1] + ")"
                                    inferredStringList.append(inferredString)

                                print(inferredStringList)
                                return
                            if inferredConclusion not in agenda:
                                agenda.append(inferredConclusion)
                            if inferredConclusion not in knowledge:
                                knowledge.append(inferredConclusion)
                            isUsedAgendaItem = True
                            agenda.remove(currentStatement)
                            break

                if isUsedAgendaItem:
                    agenda.append(currentStatement)
                    break
    print("Query cannot be proven.")
    return


def backward_chaining(KB,alpha):
    rules = []
    agenda = []
    knowledge = []
    inferred = []
    goal = parse_statement(alpha)

    for item in KB:
        if "<-" in item:
            splitFromImplication = item.split("<-")
            left = splitFromImplication[0]
            right = splitFromImplication[1]

            conclusionItem = parse_statement(left)
            premisesList = []

            premises = right.split(", ")
            for premise in premises:
                spaceRemovedPremise = premise.replace(" ", "", 1)
                premiseItem = parse_statement(spaceRemovedPremise)
                premisesList.append(premiseItem)

            ruleItem = Rule(conclusionItem, premisesList, len(premisesList))
            rules.append(ruleItem)

        else:

            statementItem = parse_statement(item)
            knowledge.append(statementItem)

    agenda.append(goal)

    isInferred = True
    isAgendaUpdated = True
    while isInferred or isAgendaUpdated:
        isInferred = False
        isAgendaUpdated = False
        for i in range(len(rules)):
            currentRule = rules[i]
            currentSubs = {}
            currentCount = currentRule.count

            lenAgenda = len(agenda)
            for j in range(lenAgenda):
                currentStatement = agenda[j]


                if currentStatement.name == currentRule.conclusion.name:
                    currentMGU = mgu(currentRule.conclusion,currentStatement)
                    currentSubs.update(currentMGU)
                    for k in range(len(currentRule.statements)):
                        currentPremise = currentRule.statements[k]
                        modifiedPremise = apply_subs(currentPremise,currentMGU)
                        if modifiedPremise in knowledge:
                            currentCount -= 1
                            if currentCount <= 0:
                                #inferred
                                inferredConclusion = apply_subs(currentRule.conclusion,currentMGU)
                                agenda.remove(currentStatement)
                                knowledge.append(inferredConclusion)

                                currentRuleConclusionSubstitued = apply_subs(currentRule.conclusion, currentSubs)
                                currentRulePremisesSubstitued = []
                                for premiseWithoutSubstitution in currentRule.statements:
                                    premiseSubstitued = apply_subs(premiseWithoutSubstitution, currentSubs)
                                    currentRulePremisesSubstitued.append(premiseSubstitued)

                                currentRuleSubstitued = Rule(currentRuleConclusionSubstitued,currentRulePremisesSubstitued,len(currentRulePremisesSubstitued))

                                inferred.append(currentRuleSubstitued)
                                isInferred = True
                        else:
                            #check if unified version is in knowledge
                            hasUnifiedInKnowledge = False
                            for knowledgeItem in knowledge:
                                if modifiedPremise.name == knowledgeItem.name:
                                    knowledgeMGU = mgu(modifiedPremise,knowledgeItem)
                                    if knowledgeMGU != "FAIL": #means that we have a substutition that will satisfy in knowledge
                                        currentSubs.update(knowledgeMGU)
                                        currentCount -= 1
                                        hasUnifiedInKnowledge = True
                                        if currentCount <= 0:
                                            inferredConclusion = apply_subs(currentRule.conclusion,currentSubs)
                                            agenda.remove(currentStatement)
                                            knowledge.append(inferredConclusion)

                                            currentRuleConclusionSubstitued = apply_subs(currentRule.conclusion,currentSubs)
                                            currentRulePremisesSubstitued = []
                                            for premiseWithoutSubstitution in currentRule.statements:
                                                premiseSubstitued = apply_subs(premiseWithoutSubstitution, currentSubs)
                                                currentRulePremisesSubstitued.append(premiseSubstitued)

                                            currentRuleSubstitued = Rule(currentRuleConclusionSubstitued,currentRulePremisesSubstitued,len(currentRulePremisesSubstitued))

                                            inferred.append(currentRuleSubstitued)
                                            isInferred = True
                                            break

                            if modifiedPremise not in agenda and not hasUnifiedInKnowledge:
                                agenda.append(modifiedPremise)
                                isAgendaUpdated = True
                if isInferred:
                    break
            if isInferred:
                break


    if goal in knowledge:
        inferredRulesStringList = []
        for inferredRule in inferred:
            inferredRuleString = inferredRule.conclusion.name + "("
            for variableOfConclusion in inferredRule.conclusion.variables:
                inferredRuleString += variableOfConclusion + ","
            inferredRuleString = inferredRuleString[:-1] + ") <- "

            for inferredRulePremise in inferredRule.statements:
                inferredRuleString += inferredRulePremise.name + "("
                for variableOfPremise in inferredRulePremise.variables:
                    inferredRuleString += variableOfPremise + ","
                inferredRuleString = inferredRuleString[:-1] + "), "
            inferredRuleString = inferredRuleString[:-2]
            inferredRulesStringList.append(inferredRuleString)

        print(inferredRulesStringList)
    else:
        print("Query cannot be proven.")
    return

