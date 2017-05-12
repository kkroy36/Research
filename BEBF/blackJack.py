from random import random,randint
from copy import deepcopy
from sys import argv

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
      
def winState(state):
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
   dealerSum = state[0][-1]
   if dealerSum == 21:
      return True
   else:
      return False

def decideAction(state,actions,value,cards):
   '''decides which action to take based on direction of higher value'''
   hitState = takeAction(state,"hit",cards)
   standState = takeAction(state,"stand",cards)
   hitValue,standValue = None,None
   if hitState in value.keys():
      hitValue = value[str(hitState[0][-1])]
   elif hitState not in value.keys():
      hitValue = 0
   if standState in value.keys():
      standValue = value[str(standState[0][-1])]
   elif standState not in value.keys():
      standValue = 0
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

def getValue(state,value):
   '''returns the current estimate of the value of the state'''
   if state in value.keys():
      return value[state]
   else:
      return 0

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

def updateValues(states,value,Result,count,discount):
   '''update the values of all the states in a trajectory'''
   print "Need to update value of state sequence: ",states,"with result",Result
   states = [item for item in states if (item!="hit" and item!="stand")]
   nStates = len(states)
   immediateRewardSequence = [0 for i in range(nStates)]
   immediateRewardSequence[-1] = [1 if Result == "YOU WON >:|" else -1][0]
   print "immediate Reward Sequence: ",immediateRewardSequence  
   for i in range(nStates-1,-1,-1):
      setCount(states[i].split()[-1],count)
      exponent = (nStates-1)-i
      if i == nStates-1:
         setValue(states[i].split()[-1],value,immediateRewardSequence[i],count,discount,exponent)
         #value[states[i].split()[-1]] += immediateRewardSequence[i]
      else:
         nextValue = getValue(states[i+1].split()[-1],value)
         setValue(states[i].split()[-1],value,immediateRewardSequence[i]+nextValue,count,discount,exponent)
	 #value[states[i].split()[-1]] += immediateRewardSequence[i] + nextValue
   
def generatePlay(cards,value,count,discount):
   '''simulates one play of blackjack'''
   state = []
   state += [getPlayerDraw(cards)]
   state += [getDealerDraw(cards)]
   print "="*40+" PLAYING TO COMPLETION "+"="*40
   states = [" ".join([str(item) for item in state[0]])]
   Result = None
   while True:
      if winState(state):
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
   updateValues(states,value,Result,count,discount)
   for key in value:
      print "Sum: ",key,"Value: ",value[key]

def makeCardDeck():
   '''makes the deck of 56 cards because Aces can act as 11 or 1'''
   cards = []
   cards += [10 for i in range(16)]
   cards += [11 for i in range(4)]
   for i in range(1,10):
      cards += [i for j in range(4)]
   return cards

def main():
   value = {}
   count = {}
   numberOfPlays = int(argv[argv.index("-numberOfPlays")+1])
   discount = float(argv[argv.index("-discount")+1])
   for i in range(numberOfPlays):
      cards = makeCardDeck()
      generatePlay(cards,value,count,discount)
main()
