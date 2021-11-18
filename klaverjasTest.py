import klaverjas as kl
import treeSearch as ts
import numpy as np

# testHand=[]
# testHand.append(kl.Card(7,"s"))
# testHand.append(kl.Card(8,"d"))
# testHand.append(kl.Card(11,"d"))
# testHand.append(kl.Card(8,"s"))
#
# testTrick = [0]*4
# testTrick[0] = kl.Card(14,"c")
# testTrick[1] = kl.Card(9,"s")
# testTrick[2] = kl.Card(7,'h')
# testTrick[3] = 0
#
# hand =[]
# hand.append(kl.Card(11,'s'))
# hand.append(kl.Card(7,'s'))
# hand.append(kl.Card(14,'h'))
#
# output = kl.Card.validCards(hand,'s',testTrick)
#
#
# for card in output:
#     card.printCard()

# testTrick[2] = kl.Card(9,"c")
# testTrick[3] = kl.Card(14,"c")

# print(kl.Card.roem(testTrick,"s"))
# valid = kl.Card.validCards(testHand, "d", testTrick)
# [card.printCard() for card in valid]
# leadPlayer = 0 
# trump = "s"


nrDeals = 100

score = []

botSetting = [[25, 250], [5, 50], [25, 250],[5, 50]]

botSetting2 = [[10,100]]*4
randomSeedOffset = 400

deal1Dif = []
deal2Dif = []
for i in range(nrDeals):
    np.random.seed(i + randomSeedOffset)
    print(i)
    deal1 = kl.OneDeal(botsSettings=botSetting, activePlayer=(i % 4))
    np.random.seed(i + randomSeedOffset)

    deal2 = kl.OneDeal(botsSettings=botSetting2, activePlayer=(i % 4))
    score1 = deal1.play()
    score2 = deal2.play()
    deal1Dif.append(score1[0]-score1[1])
    deal2Dif.append(score2[0]-score2[1])
    #deal.gameRecord()
team1 = team2 = 0


print(sum(deal1Dif))
print(sum(deal2Dif))

# botSetting = [[20,250]]*4


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
