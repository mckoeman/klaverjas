import klaverjas as kl
import treeSearch as ts
import numpy as np
# testHand=[]
# testHand.append(kl.Card(7,"s"))
# testHand.append(kl.Card(8,"d"))
# testHand.append(kl.Card(11,"d"))
# testHand.append(kl.Card(8,"s"))

# testTrick = [0]*4
# testTrick[0] = kl.Card(7,"c")
# testTrick[1] = kl.Card(8,"c")
# testTrick[2] = kl.Card(9,"c")
# testTrick[3] = kl.Card(14,"c")

# print(kl.Card.roem(testTrick,"s"))
# valid = kl.Card.validCards(testHand, "d", testTrick)
# [card.printCard() for card in valid]
# leadPlayer = 0 
# trump = "s"

# print (kl.Card.stringTrick(testTrick,leadPlayer,kl.Card.trick(testTrick,leadPlayer,trump)))\

# np.random.seed(3)
nrDeals = 1
score = []
for i in range(nrDeals):
    deal = kl.OneDeal(botsSettings = 0,activePlayer = (i%4))
    score.append(deal.play())
    deal.gameRecord()
# oneIt = ts.TreeSearch(randomDeal.players, 0, 's', 0)
# deck = [kl.Card(number, suit) for suit in kl.Card.suits for number in range(7, 15)]
# players = [[]]*4
# players[0] = deck[0:8]
# players[1] = deck[8:16]
# players[2] = deck[16:24]
# players[3] = deck[24:32]

# oneIt = ts.TreeSearch(randomDeal.players, 0, 's', 0)
# oneIt.doNumberIts(10000)
# kl.OneDeal.gameRecord(oneIt.findBestSequence(), 's')
# (card, value)= oneIt.bestCard()
# kl.Card.printHand(oneIt.players[0])
# print(card.stringCard() + "  met als score " + str(value))


# firstTrick = [a,b,c,d]
# print(kl.Card.trick(firstTrick,"c","h"))

# testTrick = [0]*4
# testTrick[0] = kl.Card(7,"h")
# testTrick[1] = kl.Card(9,"h")
# testTrick[2] = kl.Card(8,"h")
# testTrick[3] = 0
# hand = [0]*3
# hand[0] = kl.Card(7,"c")
# hand[1] = kl.Card(11,"s")
# hand[2] = kl.Card(8,"s")
# [card.printCard() for card in kl.Card.validCards(hand,'s', testTrick)]
