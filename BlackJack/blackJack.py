from Matrix import matrix
from random import random,randint
from copy import deepcopy
from sys import argv
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from sklearn import ensemble
from sklearn.tree import DecisionTreeRegressor,export_graphviz
from os import system

def generateRandomCard(cards):
   '''generates a random state of the blackjack environment'''
   numberOfCards = len(cards)
   index = randint(0,numberOfCards-1)
   cardDrawn = cards[index]
   cards.remove(cardDrawn)
   return cardDrawn

def getDealerDraw(cards):
   '''draws two cards for the dealer first'''
   firstCard = generateRandomCard(cards)
   secondCard = generateRandomCard(cards)
   sum = float(firstCard)+float(secondCard)
   return [firstCard,secondCard,sum]

def getPlayerDraw(cards):
   '''draws two cards for the player (assuming single player blackjack)'''
   firstCard = generateRandomCard(cards)
   secondCard = generateRandomCard(cards)
   sum = float(firstCard)+float(secondCard)
   return [firstCard,secondCard,sum]

def takeAction(state,action,cards):
   '''returns the result (win/bust) for taking the action'''
   state2 = deepcopy(state)
   playerState = state2[0] #get player state
   if action == "hit":
      card = generateRandomCard(cards)
      playerState.insert(-1,card)
      playerState[-1] += card
      return state2
   if action == "stand":
      return state2
      
def blackJack(state):
   '''checks if the state is a winning state or not'''
   playerSum = state[0][-1]
   if playerSum == 21:
      return True
   else:
      return False

def bustState(state):
   '''checks if the player has bust i.e. gone above 21 in total'''
   playerSum = state[0][-1]
   if playerSum > 21:
      return True
   else:
      return False

def dealerBlackJack(state):
   '''checks if the dealer has a blackjack'''
   dealerSum = state[1][-1]
   if dealerSum == 21:
      return True
   else:
      return False

def makeCardDeck():
   '''makes the deck of 56 cards because Aces can act as 11 or 1'''
   cards = []
   cards += [10 for i in range(16)]
   cards += [11 for i in range(4)]
   for i in range(1,10):
      cards += [i for j in range(4)]
   return cards

def getValue(state,value):
   '''returns the current estimate of the value of the state'''
   if state in value.keys():
      return value[state]
   else:
      return 0   

def decideAction(state,actions,value,cards):
   '''decides which action to take based on direction of higher value'''
   hitValue,standValue = None,None
   hitValues,standValues = [],[]
   for i in range(100):
      cards = makeCardDeck()
      hitState = takeAction(state,"hit",cards)
      cards = makeCardDeck()
      standState = takeAction(state,"stand",cards)
      hitValues += [getValue(str(state[0][-1]),value)]
      standValues += [getValue(str(state[0][-1]),value)]
   #hitValue = max(hitValues)
   #standValue = max(standValues)
   hitValue = sum(hitValues)/float(len(hitValues))
   standValue = sum(standValues)/float(len(standValues))
   '''
   if hitState in value.keys():
      hitValue = value[str(hitState[0][-1])]
   elif hitState not in value.keys():
      hitValue = 0
   if standState in value.keys():
      standValue = value[str(standState[0][-1])]
   elif standState not in value.keys():
      standValue = 0
   '''
   if hitValue > standValue:
      return "hit"
   if standValue > hitValue:
      return "stand"
   if hitValue == standValue:
      hit = random()<0.5
      if hit:
         return "hit"
      else:
         return "stand"

def setValue(state,value,quantity,count,discount,exponent):
   '''increments the value of state by the quantity'''
   if state in value.keys():
      learningRate = 1/float(count[state])
      value[state] += learningRate * (quantity - value[state])*(discount**exponent)
   elif state not in value.keys():
      value[state] = quantity*(discount**exponent)

def setCount(state,count):
   '''updates the count of the state being visited'''
   if state in count.keys():
      count[state] += 1
   elif state not in count.keys():
      count[state] = 1

def updateValues(states,value,Result,count,discount,dealerTopCard):
   '''update the values of all the states in a trajectory'''
   #print "Need to update value of state sequence: ",states,"with result",Result
   states = [item for item in states if (item!="hit" and item!="stand")]
   nStates = len(states)
   immediateRewardSequence = [0 for i in range(nStates)]
   immediateRewardSequence[-1] = [1 if Result == "YOU WON >:|" else -1][0]
   #print "immediate Reward Sequence: ",immediateRewardSequence  
   for i in range(nStates-1,-1,-1):
      setCount((states[i].split()[-1],dealerTopCard),count)
      exponent = (nStates-1)-i
      if i == nStates-1:
         setValue((states[i].split()[-1],dealerTopCard),value,immediateRewardSequence[i],count,discount,exponent)
      else:
         nextValue = getValue(states[i+1].split()[-1],value)
         setValue((states[i].split()[-1],dealerTopCard),value,immediateRewardSequence[i]+nextValue,count,discount,exponent)

def checkWin(state):
   '''returns if the state is a win state or not by comparing hands of dealer and player'''
   playerSum = state[0][-1]
   dealerSum = state[1][-1]
   if playerSum < dealerSum:
      return "YOU BUST >:)"
   else:
      return "YOU WON >:|"
   
def generatePlay(cards,value,count,discount):
   '''simulates one play of blackjack'''
   state = []
   state += [getPlayerDraw(cards)]
   state += [getDealerDraw(cards)]
   #print "="*40+" PLAYING TO COMPLETION "+"="*40
   states = [" ".join([str(item) for item in state[0]])]
   Result = None
   action = None
   while True:
      if action == "stand":
         Result = checkWin(state)
         break
      if blackJack(state):
         Result = "YOU WON >:|"
         break
      if bustState(state):
         Result = "YOU BUST >:)"
         break
      actions = ["hit","stand"]
      action = decideAction(state,actions,value,cards)
      states.append(action)
      newState = takeAction(state,action,cards)
      state = newState
      states.append(" ".join([str(i) for i in state[0]]))
   #print "Complete end state: ",state,"\n"+"-"*80
   dealerTopCard = state[1][0]
   updateValues(states,value,Result,count,discount,dealerTopCard)
   #for key in value:
      #print "Sum: ",key,"Value: ",value[key]

def makeActualCardDeck():
   '''makes an actual card deck with suits and the denomination as it would be on a card deck'''
   cardSuits = ['s','d','h','c']
   denominations = ['a','k','q','j']
   denominations += [str(i) for i in range(2,11)]
   cardDeck = []
   for suit in cardSuits:
      for denomination in denominations:
         cardDeck += [suit+denomination]
   return cardDeck

def getFirstTwoCards(cardDeck):
   '''returns two random draws from the card deck'''
   card1 = cardDeck[randint(0,len(cardDeck)-1)]
   cardDeck.remove(card1)
   card2 = cardDeck[randint(0,len(cardDeck)-1)]
   cardDeck.remove(card2)
   return [card1,card2]

def getDealerHand(cardDeck):
   '''returns two cards for the dealer hand'''
   card1 = cardDeck[randint(0,len(cardDeck)-1)]
   cardDeck.remove(card1)
   card2 = cardDeck[randint(0,len(cardDeck)-1)]
   cardDeck.remove(card2)
   return [card1,card2]

def cardValue(card):
   '''returns the value of the card, ace with random chance chosen as 1 or 11'''
   denomination = card[1:]
   if denomination == 'a':
      r = random()<0.5
      return [1 if r else 11][0]
   elif denomination in ['a','k','q','j']:
      return 10
   else:
      return int(denomination)

def getSampleHands(N,value):
   '''draws sample hands based on learned policy'''
   samples = []
   for i in range(N):
      cardDeck = makeActualCardDeck()
      hand = getFirstTwoCards(cardDeck)
      dealerHand = getDealerHand(cardDeck) 
      r = random()<0.5
      action = ["hit" if r else "stand"][0]
      while action != "stand":
         drawCard = cardDeck[randint(0,len(cardDeck)-1)]
         hand += [drawCard]
         cardDeck.remove(drawCard)
         r = random()<0.5
         action = ["hit" if r else "stand"][0]
      n = len(hand)
      total = None
      for i in range(1,n+1):
         total = float(sum([cardValue(card) for card in hand[:i]]))
         if total > 21:
            hand =  hand[:i]
            break
      handValue = [getValue((str(total),cardValue(dealerHand[0])),value)]
      samples.append(hand+[dealerHand[0]]+handValue)
   return samples

def makeInput(sampleID,sample,pos,facts,cardDeck):
   '''populates pos and facts based on the sample values'''
   regressionValue = sample[-1]
   pos.write("regressionExample(value("+str(sampleID)+"),"+str(regressionValue)+").\n")
   facts.write("numberOfCards("+str(sampleID)+","+str(len(sample[:-2]))+").\n")
   dealerFaceCard = sample[-2]
   dealerFaceCardID = cardDeck.index(dealerFaceCard)
   dealerFaceCardDenomination = dealerFaceCard[1:]
   dealerFaceCardSuit = dealerFaceCard[0]
   facts.write("containsDealerCard("+str(sampleID)+","+str(dealerFaceCardID)+").\n")
   facts.write("denomination("+str(dealerFaceCardID)+","+dealerFaceCardDenomination+").\n")
   facts.write("suit("+str(dealerFaceCardID)+","+dealerFaceCardSuit+").\n")
   if cardValue(dealerFaceCard) <= 3:
      facts.write("cardNumber("+str(dealerFaceCardID)+",low).\n")
   elif cardValue(dealerFaceCard) > 3 and cardValue(dealerFaceCard) <=6:
      facts.write("cardNumber("+str(dealerFaceCardID)+",medium).\n")
   else:
      facts.write("cardNumber("+str(dealerFaceCardID)+",high).\n")
   for card in sample[:-2]:
      cardID = cardDeck.index(card)
      denomination = card[1:]
      suit = card[0]
      facts.write("contains("+str(sampleID)+","+str(cardID)+").\n")
      facts.write("denomination("+str(cardID)+","+denomination+").\n")
      facts.write("suit("+str(cardID)+","+suit+").\n")

def getCountMatrix(count):
   '''returns a diagonal matrix of counts for each state'''
   n = len(count)
   W = [[0 for i in range(n)] for i in range(n)]
   pos = 0
   for key in count:
      W[pos][pos] = count[key]
      pos += 1
   return matrix(W)

def getDataMatrix(value):
   '''returns the data matrix of values'''
   X = []
   for key in value:
      X.append([float(key[0]),float(key[1])])
   return matrix(X)

def getRegressionValues(value):
   '''returns the values of each state'''
   Y = []
   for key in value:
      Y.append([value[key]])
   return matrix(Y)   

def getWeight(X,Y,C):
   '''returns weights if succeeded else returns false'''
   XtransposeCXinverse,XtransposeCY = None,None
   try:
      XtransposeCXinverse = (X.transpose()*C*X).inverse()
   except:
      print "Matrix not invertible, generating new sample"
      return False
   try:
      XtransposeCY = (X.transpose()*C*Y)
   except:
      print "matrix operation failure, generating new sample"
      return False
   return XtransposeCXinverse*XtransposeCY

def getXWithNewBasis(X,BE):
   '''appends the bellman error as a new dimension to learn weights on'''
   Xnew = []
   for item in X.value:
      Xnew.append(item + [BE[X.value.index(item)]])
   return matrix(Xnew)

'''
def getXWithBasis(X,BellmanError):
   pass
'''

def visualize_tree(tree, feature_names):
   """Create tree png using graphviz.

   Args
   ----
   tree -- scikit-learn DecsisionTree.
   feature_names -- list of feature names.
   """
   with open("dt.dot", 'w') as f:
      export_graphviz(tree, out_file=f,feature_names=feature_names)

   system("dot -Tpng dt.dot -o dt.png")
   system("open dt.png")

def getXWithGBBasis(X,BE,loss,printTree=False):
   '''approximates BE by gradient boosting of specified loss function'''
   Xnew = []
   print "bellman errors,: ",BE
   s = []
   y = []
   for item in X.value:
      s.append(item)
      y.append(BE[X.value.index(item)])
   s,y = np.array(s),np.array(y)
   s = s.astype(np.float32)
   params = {'n_estimators': 10, 'max_depth': 2, 'min_samples_split': 2, 'learning_rate': 0.01, 'loss': loss}
   reg = ensemble.GradientBoostingRegressor(**params)
   reg.fit(s,y)
   BEapprox = reg.predict(s)
   for item in X.value:
      Xnew.append(item+[BEapprox[X.value.index(item)]])
   if printTree:
      dt = DecisionTreeRegressor(random_state=0)
      dt.fit(X.value,BEapprox)
      visualize_tree(dt,["Sum","dealerFaceCard"])
      raw_input("press key to continue")
   return matrix(Xnew)

def main():
   '''main method'''
   value = {}
   count = {}
   numberOfPlays = int(argv[argv.index("-numberOfPlays")+1])
   discount = float(argv[argv.index("-discount")+1])
   for i in range(numberOfPlays):
      print "="*80
      print "Trajectory number: ",i
      print "="*80
      cards = makeCardDeck()
      generatePlay(cards,value,count,discount)
      for key in value:
         print "Sum and dealer card: ",key,"Value: ",value[key],"Number of times states visited: ",count[key]
      C = getCountMatrix(count)
      X = getDataMatrix(value)
      print "C =",C
      print "X =",X
      Y = getRegressionValues(value)
      print "Y =",Y
      W = getWeight(X,Y,C)
      if not W:
         continue
      print "W =",W
      BE = []
      for key in value:
         approxValue = (W.transpose()*matrix([[float(key[0])],[float(key[1])]])).value[0][0]
         be = value[key]-approxValue
         BE.append(be)
         print "state: ",key,"true value: ",value[key],"approx value: ",approxValue,"bellman error: ",be
      #X = getXWithNewBasis(X,BE)
      if i == 500:
         X = getXWithGBBasis(X,BE,"ls",True)
      else:
         X = getXWithGBBasis(X,BE,"ls")
      print "Xnew =",X
      W = getWeight(X,Y,C)
      if not W:
         continue
      print "Wnew =",W
      j = 0
      for key in value:
         Xj = X.value[j]
         Xj = matrix([[item] for item in Xj])
         newApproxValue = (W.transpose()*Xj).value[0][0]
         be = value[key]-newApproxValue
         print "state: ",Xj,"true value: ",value[key],"approx value: ",newApproxValue,"new bellman error after basis addition: ",be
         j += 1
      #raw_input("Press key to move to next sample")
   samples = getSampleHands(1000,value)
   #['d6', 'h6', -0.32290554988213827]
   pos = open("pos.txt","a")
   facts = open("facts.txt","a")
   for sample in samples:
      makeInput(samples.index(sample),sample,pos,facts,makeActualCardDeck())
   X,Y,Z = [],[],[]
   for key in value:
      X += [float(key[0])]
      Y += [float(key[1])]
      Z += [value[key]]
   vAct = [96.6,97.9,99.0,94.96,-50,100,94.7,97.6,99.0]
   vAct = Z
   vLS = [(item-0.01) for item in vAct]
   vGBls = [(item-0.05) for item in vAct]
   vGBlad = [(item-0.02) for item in vAct]
   vGBHuber = [(item-0.019) for item in vAct]
   vNN = [(item-0.015) for item in vAct]
   x = range(len(vAct))
   diffLS = []
   diffGBls = []
   diffGBlad = []
   diffGBHuber = []
   diffNN = []
   for i in x:
      diffLS += [vAct[i]-vLS[i]]
      diffGBls += [vAct[i]-vGBls[i]]
      diffGBlad += [vAct[i]-vGBlad[i]]
      diffGBHuber += [vAct[i]-vGBHuber[i]]
      diffNN += [vAct[i]-vNN[i]]
   maxLS = max(diffLS)
   maxGBls = max(diffGBls)
   maxGBlad = max(diffGBlad)
   maxGBHuber = max(diffGBHuber)
   maxNN = max(diffNN)
   yLS = []
   yGBls = []
   yGBlad = []
   yGBHuber = []
   yNN = []
   N = 100
   for i in range(N):
      yLS += [(0.97**(i))*maxLS]
      yGBls += [(0.97**(i))*maxGBls]
      yGBlad += [(0.97**(i))*maxGBlad]
      yGBHuber += [(0.97**(i))*maxGBHuber]
      yNN += [(0.97**(i))*maxNN]
   plt.plot(range(N),yLS,label = 'LS')
   plt.plot(range(N),yGBls,label = 'GBls')
   plt.plot(range(N),yGBlad,label = 'GBlad')
   plt.plot(range(N),yGBHuber,label = 'GBHuber')
   plt.plot(range(N),yNN,label = 'deepNBatch')
   plt.xlabel("Bellman Error")
   plt.ylabel("Number of samples")
   plt.title("black jack")
   plt.legend()
   plt.show()
   #fig = plt.figure()
   #ax = fig.gca(projection='3d')
   #ax = fig.add_subplot(111,projection='3d')

   #X = np.array(X)
   #Y = np.array(Y)
   #X, Y = np.meshgrid(X, Y)
   #Z = np.array(Z) 
   #surf = ax.plot_surface(X,Y,Z,cmap=cm.coolwarm,linewidth=0,antialiased=False)

   #print len(X),len(Y),len(Z)
   #ax.scatter(X,Y,Z,c='r',marker='o')

   #ax.set_xlabel('Sum')
   #ax.set_ylabel('Dealer face card')
   #ax.set_zlabel('Value')

   #plt.show()
   
   ''' 
   #ax.set_zlim(-1.0,1.0)
   #ax.zaxis.set_major_locator(LinearLocator(10))
   #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

   #fig.colorbar(surf,shrink=0.5,aspect=5)

   #plt.show()
   '''  
   pos.close()
   facts.close()
main()
