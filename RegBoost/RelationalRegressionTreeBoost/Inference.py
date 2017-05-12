from os import system
from Utils import Utils
class rulePredicate(object):
    '''class for rulePredicate'''
    def __init__(self,predicate):
        '''constructor for rulePredicate class'''
        self.arity = Utils.getArity(predicate)
        self.relation = predicate.split('(')[0].strip()
        if self.arity == 1:
            self.variables = [predicate.split('(')[1][:-1]]
        if self.arity == 2:
            self.variables = predicate.split('(')[1][:-1].split(',')
                
class Rule(object):
    '''class for rule object'''
    def __init__(self,bodyPredicates,score):
        '''class constructor for rule class'''
        self.bodyPredicates = [rulePredicate(predicate) for predicate in bodyPredicates]
        self.score = score
        
class Inference(object):
    '''class for inference based on question asked'''
    people = None
    question = None
    Rules = []
    variableBindings = {'X':"unbound",'Y':"unbound"}
    query = None
    
    @staticmethod
    def parseRule(ruleline):
        '''parse the rule into body predicates and score'''
        rule = ruleline.split("score:")[0].strip()
        rulescore = float(ruleline.split("score:")[1].strip())
        ruleBody = rule.split(":-")[1].strip()
        if '^' in ruleBody:
            bodyPredicates = ruleBody.split('^')
        else:
            bodyPredicates = [ruleBody]
        Inference.Rules.append(Rule(bodyPredicates,rulescore))

    @staticmethod
    def readRulesandScores():
        '''reads the rules and the scores'''
        with open("rules.txt") as ruleFile:
            rules = ruleFile.read().splitlines()
        for rule in rules:
            Inference.parseRule(rule)

    @staticmethod
    def cleanQuestion(question):
        '''removes stop words, makes lower case and remove question mark'''
        return question.lower().replace(" the "," ").replace(" a "," ").replace(" is ","").replace('?',"").replace("  "," ")
    
    @staticmethod
    def parseQuestion(question,bindings):
        '''parses the question and creates and binds variables'''
        question = Inference.cleanQuestion(question)
        partsOfQuestion = question.split("father of")
        if "who" in question and "whom" not in question:
            bindings['Y'] = partsOfQuestion[1].strip()
        elif "whom" in question:
            bindings['X'] = partsOfQuestion[0].strip().split(' ')[-1]
        else:
            bindings['X'] = partsOfQuestion[0].strip().split(' ')[-1]
            bindings['Y'] = partsOfQuestion[1].strip()
        return "father("+bindings['X']+","+bindings['Y']+")."

    @staticmethod
    def getStrongestRule():
        '''returns the rule with the highest score'''
        score = -100
        bestRule = None
        for rule in Inference.Rules:
            if rule.score >= score:
                score = rule.score
                bestRule = rule
        Inference.Rules.remove(bestRule)
        return bestRule

    @staticmethod
    def answerQuestion():
        '''answers the question asked by the user'''
        answerOkay = False
        while not answerOkay:
            print "-"*80
            if len(Inference.Rules) == 0:
                break
            bestRule = Inference.getStrongestRule()
            satisfied = True
            for predicate in bestRule.bodyPredicates:
                arity = predicate.arity
                relation = predicate.relation
                variables = predicate.variables
                answer = "unknown"
                if arity == 1:
                    variable = variables[0]
                    if Inference.variableBindings[variable] != "unbound":
                        questionString = "is "+Inference.variableBindings[variable]+" "+relation.replace("!","")+"?: "
                        answer = raw_input(questionString).lower()
                        print "You answered: "+answer
                elif arity == 2:
                    unbound = False
                    for variable in variables:
                        if Inference.variableBindings[variable] == "unbound":
                            unbound = True
                    if not unbound:
                        questionString = "is "+Inference.variableBindings[variables[0]]+" "+relation.replace("!","")+" of "+Inference.variableBindings[variables[1]]+"?: "
                        answer = raw_input(questionString).lower()
                        print "You answered: "+answer
                if '!' not in relation:
                    if answer == "no":
                        satisfied = False
                        break
                elif '!' in relation:
                    if answer == "yes":
                        satisfied = False
            if satisfied:
                print "The answer to your question: \""+Inference.question+"\" is yes"
                print "The confidence on this answer is: "+str(Utils.sigmoid(bestRule.score)*100)+" percent"
                okay = raw_input("Is this answer acceptable?: ")
                if okay == "yes":
                    answerOkay = True
                else:
		    print "Trying another approach..."
            else:
                print "The answer to your question: \""+Inference.question+"\" is no"
                print "The confidence on this answer is: "+str(Utils.sigmoid(bestRule.score)*100)+" percent"
                okay = raw_input("Is this answer acceptable?: ")
                if okay == "yes":
                    answerOkay = True
                else:
	            print "Trying another approach..."
        if not answerOkay:
            print "Sorry, I do not have an answer you your question"
                    
    @staticmethod
    def promptQuestion():
        '''prompts the user to ask a question'''
        Inference.question = raw_input("Please enter your question: ")
        print "Your question: "+Inference.question
        Inference.readRulesandScores()
        Inference.query = Inference.parseQuestion(Inference.question,Inference.variableBindings)
    #@staticmethod
    
    
