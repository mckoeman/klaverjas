from functools import partial

import numpy as np
import treeSearch as ts
import sys


class Card:
    suits = ["s", "h", "d", "c"]

    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        # todo fix constructor to check for iligal cards etc

    def __eq__(self, other):
        return self.suit == other.suit and self.number == other.number

    def __hash__(self):
        return hash((self.suit, self.number))

    def toindex(self):
        return Card.suits.index(self.suit) * 8 + self.number - 7

    @staticmethod
    def suitIndex(suit):
        return Card.suits.index(suit)

    def printCard(self):
        print(self.suit, self.number)

    def stringCard(self):
        if self.number == 10:
            numberString = "T"
        elif self.number == 11:
            numberString = "B"
        elif self.number == 12:
            numberString = "Q"
        elif self.number == 13:
            numberString = "K"
        elif self.number == 14:
            numberString = "A"
        else:
            numberString = str(self.number)
        return self.suit + numberString

    def stringTrick(trick, lead=-1, winner=-1, roem=0):
        stringTrick = ""
        for i in range(len(trick)):
            if i == lead and i == winner:
                stringTrick += "[(" + trick[i].stringCard() + ")] "
            elif i == lead:
                stringTrick += " [" + trick[i].stringCard() + "]  "
            elif i == winner:
                stringTrick += " (" + trick[i].stringCard() + ")  "
            else:
                stringTrick += "  " + trick[i].stringCard() + "   "
        if roem != 0:
            stringTrick += str(roem) + " Roem!"
        return stringTrick

    def pointValue(self, trump=False):
        if trump:
            if self.number == 11:
                return 20
            elif self.number == 9:
                return 14
        if self.number == 10:
            return 10
        elif self.number == 11:
            return 2
        elif self.number == 12:
            return 3
        elif self.number == 13:
            return 4
        elif self.number == 14:
            return 11
        else:
            return 0

    def orderForTrickTaking(self, requestedSuit="noSuit", trump=False):
        if self.suit != requestedSuit and not (trump):
            return 0
        if trump:
            if self.number == 11:
                return 100
            elif self.number == 9:
                return 90
            else:
                return Card.orderForTrickTaking(self, self.suit) + 20
        if self.number == 14:
            return 16
        elif self.number == 10:
            return 15
        else:
            return self.number

    @staticmethod
    def validCards(hand, trump, trickSoFar):
        notYetPlayed = [type(x) is int for x in trickSoFar]
        if all(notYetPlayed):
            return hand
        leadingPlayer = notYetPlayed.index(True)
        requestedSuit = []
        while not requestedSuit:
            leadingPlayer = (leadingPlayer + 1) % 4
            if not notYetPlayed[leadingPlayer]:
                requestedSuit = trickSoFar[leadingPlayer].suit
                activePlayer = (leadingPlayer + sum([not x for x in notYetPlayed])) % 4

        trumpsInTrick = [card for card in trickSoFar if type(card) is Card and card.suit == trump]
        if trumpsInTrick:
            cardValues = [card.orderForTrickTaking(trump=True) for card in trumpsInTrick]
            highesttrumpInTrick = trumpsInTrick[cardValues.index(max(cardValues))]

        if requestedSuit != trump:
            cardsValid = [card for card in hand if card.suit == requestedSuit]
            if cardsValid:
                return cardsValid
            positionAlly = (activePlayer + 2) % 4
            if not notYetPlayed[positionAlly] and Card.trick(trickSoFar, leadingPlayer, trump) == positionAlly:
                cardsValid = [card for card in hand if
                              card.suit != trump or card.orderForTrickTaking(trump=True) > trickSoFar[
                                  positionAlly].orderForTrickTaking(trump=trickSoFar[positionAlly].suit == trump)]
                if cardsValid:
                    return cardsValid
                else:
                    return hand
            cardsValid = [card for card in hand if card.suit == trump and (
                    (not trumpsInTrick) or card.orderForTrickTaking(
                trump=True) > highesttrumpInTrick.orderForTrickTaking(trump=True))]
            if cardsValid:
                return cardsValid

            cardsValid = [card for card in hand if card.suit != trump]
            if cardsValid:
                return cardsValid
            return hand
        else:
            cardsValid = [x for x in hand if x.suit == trump and x.orderForTrickTaking(
                trump=True) > highesttrumpInTrick.orderForTrickTaking(trump=True)]
            if cardsValid:
                return cardsValid
            cardsValid = [x for x in hand if x.suit == trump]
            if cardsValid:
                return cardsValid
            else:
                return hand

    def trick(cards, leadingPlayer, trump):
        highest = [(card.orderForTrickTaking(cards[leadingPlayer].suit, card.suit == trump), indi) for indi, card in
                   enumerate(cards) if type(card) is Card]
        _, maxi = max(highest)
        return maxi

    def roem(cards, trump):
        if all([(cards[0].number == card.number and card.number >= 10) for card in cards]):
            if cards[0].number == 11:
                return 200
            else:
                return 100

        for suit in Card.suits:
            sameSuitNumbers = [card.number for card in cards if suit == card.suit]
            if len(sameSuitNumbers) < 2 or (len(sameSuitNumbers) < 3 and suit != trump):
                continue
            if suit == trump and all([x in [card.number for card in cards if card.suit == trump] for x in [12, 13]]):
                return Card.roem(cards, "0") + 20
            diffList = np.diff(np.sort(sameSuitNumbers)).tolist()
            if diffList.count(1) == 2 and np.diff(
                    [ind for ind, difference in enumerate(diffList) if difference == 1]).tolist() == [1]:
                return 20
            elif diffList.count(1) == 3:
                return 50
        return 0

    @staticmethod
    def printHand(hand):
        toPrint = ""
        sortedHand = [otherCard for (_, otherCard) in sorted(zip([(card.suit, card.number) for card in hand], hand))]
        for card in sortedHand:
            toPrint += (card.stringCard()) + " "
        print(toPrint)

    @staticmethod
    def updatePossibilities(trickSoFar, trump, cardPlayed, activePlayer, possibilities):
        trickWithoutLastCard = [maybeCard for maybeCard in trickSoFar]
        trickWithoutLastCard[activePlayer] = 0
        maybePlayable = [card for card in OneDeal.deck if possibilities[activePlayer][card.toindex()] == 1]
        notPlayable = []

        while True:
            tryToPlayCards = Card.validCards(maybePlayable, trump, trickWithoutLastCard)
            if cardPlayed in tryToPlayCards:
                for card in notPlayable:
                    possibilities[activePlayer, card.toindex()] = 0
                break
            else:
                maybePlayable = [card for card in maybePlayable if card not in tryToPlayCards]
                notPlayable.extend(tryToPlayCards)
        for player in range(4):  # removing cardPlayed from possibilities
            possibilities[player, cardPlayed.toindex()] = 0
        return possibilities


class OneDeal:
    deck = [Card(number, suit) for number in range(7, 15) for suit in Card.suits]

    def __init__(self, botsSettings=0, activePlayer=0):
        self.activePlayer = activePlayer
        self.players = [[]] * 4
        self.pointsCollected = [0] * 2
        self.shuffleDeck()
        self.trump = []
        self.determineTrump()
        self.log = []
        if botsSettings == 0:
            self.trump = mikeBotDetermineTrump(self.players[activePlayer], activePlayer)
            self.playerStrat = [partial(mikeBot, trump=self.trump)] * 4
        else:
            self.playerStrat = [None]*4
            self.trump = mikeBotDetermineTrump(self.players[activePlayer], activePlayer,
                                               botsSettings[activePlayer][0] // 4, botsSettings[activePlayer][1])
            for indi, setting in enumerate(botsSettings):
                ('jjjoi')
                self.playerStrat[indi] = partial(mikeBot, trump=self.trump, numberItsDistri=setting[0],
                                                 numberItsTreesearch=setting[1])

    def determineTrump(self):
        self.trump = "s"

    def play(self):
        # todo NAT
        record = []
        possibilities = np.ones((4, 32))
        for i in range(8):
            #print(i)
            trick = [0] * 4
            for j in range(4):
                whoNext = (j + self.activePlayer) % 4
                if not self.players[whoNext]:
                    continue
                trick[whoNext] = self.playerStrat[whoNext](self.players[whoNext], trick, record, whoNext,
                                                           self.activePlayer, possibilities)
                self.players[whoNext].remove(trick[whoNext])
                possibilities = Card.updatePossibilities(trick, self.trump, trick[whoNext], whoNext, possibilities)

            winningPlayer = Card.trick(trick, self.activePlayer, self.trump)
            roem = Card.roem(trick, self.trump)
            trickRecord = (trick, self.activePlayer, winningPlayer, roem)
            record.append(trickRecord)
            self.activePlayer = winningPlayer
        self.log = record
        return OneDeal.parseRecord(record, self.trump)

    @staticmethod
    def parseRecord(log, trump):
        points = [0, 0]
        for (trick, _, winningPlayer, roem) in log:
            points[winningPlayer % 2] += sum([card.pointValue(card.suit == trump) for card in trick]) + roem
        points[log[-1][2] % 2] += 10
        return points

    def gameRecord(self):
        # MK TODO: NAT en PIT
        pointsCollected = OneDeal.parseRecord(self.log, self.trump)
        for entry in self.log:
            print(Card.stringTrick(entry[0], entry[1], entry[2], entry[3]))
        if pointsCollected:
            print("team A: " + str(pointsCollected[0]) + "   team B " + str(pointsCollected[1]))

    @staticmethod
    def randomBot(hand, trickSoFar, log, playerID, leadingPlayer, trump):
        cardsPossible = Card.validCards(hand, trump, trickSoFar)
        return np.random.choice(cardsPossible)

    def shuffleDeck(self):
        shuffledDeck = np.random.permutation(self.deck).tolist()
        self.players[0] = shuffledDeck[0:8]
        self.players[1] = shuffledDeck[8:16]
        self.players[2] = shuffledDeck[16:24]
        self.players[3] = shuffledDeck[24:32]

    @staticmethod
    def naiveValidCards(hand, log, playerID, trickSoFar):
        players = [[] for _ in range(4)]
        tricks = [trick for (trick, _, _, _) in log]
        cardsInTrick = [card for cards in tricks for card in cards]
        filteredCards = [card for card in OneDeal.deck if not (
                card in hand or card in cardsInTrick or card in [card for card in trickSoFar if
                                                                 type(card) is Card])]
        shuffledCards = np.random.permutation(filteredCards).tolist()
        toWhom = playerID
        for card in shuffledCards:
            toWhom = (toWhom + 1) % 4
            if toWhom == playerID:
                toWhom = (toWhom + 1) % 4
            players[toWhom].append(card)
        players[playerID] = hand
        return players

    @staticmethod
    def forcedCardsFromPos(possibilities):
        forcedCards = []
        for card in OneDeal.deck:
            if possibilities[:, card.toindex()].sum() == 1:
                forcedCards.append((card, np.where(possibilities[:, card.toindex()] == 1)))
        return forcedCards

    @staticmethod
    def divideCards(hand, log, playerID, trickSoFar, possibilities):
        possibilitiesUpdated = possibilities.copy()
        possibilitiesUpdated[:, [card.toindex() for card in hand]] = 0  # remove player hand from COPY of possibilities
        forcedCards = OneDeal.forcedCardsFromPos(possibilitiesUpdated)  # determine which cards are forced
        players = [[] for _ in range(4)]
        tricks = [trick for (trick, _, _, _) in log]
        cardsSoFar = [card for cards in tricks for card in cards]
        cardsInTrick = [card for card in trickSoFar if type(card) is Card]
        filteredCards = [card for card in OneDeal.deck if
                         not (card in hand or card in cardsSoFar or card in cardsInTrick)]

        cardsRemaining = len(filteredCards)
        cardsPerPlayer = 4 * [cardsRemaining // 3]
        for player in range(cardsRemaining % 3):
            cardsPerPlayer[(playerID + player + 1) % 4] += 1

        for (card, playerArray) in forcedCards:
            playerIndex = int(playerArray[0])
            players[playerIndex].append(card)
            filteredCards.remove(card)
            cardsPerPlayer[playerIndex] += -1

        cardsPerPlayer[playerID] = 0
        for attempt in range(500):

            playersAttempt = [[] for _ in players]
            for index, onePlayer in enumerate(playersAttempt):
                onePlayer.extend(players[index])
            shuffledCards = iter(np.random.permutation(filteredCards).tolist())

            for playerNr, player in enumerate(playersAttempt):
                for nr in range(cardsPerPlayer[playerNr]):
                    player.append(next(shuffledCards))

            fault = False
            for whichplayer, handforWhichPlayer in enumerate(playersAttempt):
                for card in handforWhichPlayer:
                    if possibilities[whichplayer][card.toindex()] == 0:
                        fault = True
                        break
                if fault:
                    break
            if not fault:
                break

        if fault:
            print('No correct random deal found. Working with incorrect one instead.')
        playersAttempt[playerID] = hand

        return playersAttempt  # returns either a correct version when it's made or an incorrect version when the iterations end


def mikeBot(hand, trickSoFar, log, playerID, leadingPlayer, possibilities, trump, numberItsDistri=10,
            numberItsTreesearch=400):
    #print(trump)
    resultList = []
    possibleCards = Card.validCards(hand, trump, trickSoFar)
    values = [0] * len(possibleCards)

    for _ in range(numberItsDistri):
        resultList.append(
            doSimulation(hand, trickSoFar, log, playerID, leadingPlayer, trump, possibilities, numberItsTreesearch))

    for result in resultList:
        scores = [(child.meanResult, child.cardPlayed) for child in result.children]
        visits = [child.visits for child in result.children]
        UCB = [result.ucb(child) for child in result.children]
        for (score, card) in scores:
            values[possibleCards.index(card)] += score
        # for (score, card), visit, ucb in zip(scores, visits,UCB):
        #     print(card.stringCard() + ' score = ' + str(score) + ' visits = ' + str(visit))    #+ ' USB = ' + str(ucb)
        # pause()
    return possibleCards[values.index(min(values))]


def doSimulation(hand, trickSoFar, log, playerID, leadingPlayer, trump, possibilities, numberItsTreesearch):
    possibleDistri = OneDeal.divideCards(hand, log, playerID, trickSoFar, possibilities)
    searchObj = ts.TreeSearch(possibleDistri, playerID, trump, leadingPlayer, trickSoFar, log)
    searchObj.doNumberIts(numberItsTreesearch)
    return searchObj


def mikeBotDetermineTrump(hand, playerID, numberItsDistri=10, numberItsTreesearch=100):
    resultList = []
    values = [0] * 4
    trickSoFar = [0] * 4
    for _ in range(numberItsDistri):
        possibleDistri = OneDeal.naiveValidCards(hand, [], playerID, trickSoFar)
        for suit in Card.suits:
            searchObj = (ts.TreeSearch(possibleDistri, playerID, suit, playerID, trickSoFar, []))
            searchObj.doNumberIts(numberItsTreesearch)
            resultList.append(searchObj)
    for result in resultList:
        values[Card.suits.index(result.trump)] += result.meanResult
    return Card.suits[values.index(max(values))]  # meanResult wordt in treesearch al geflipt van teken


def pause():
    programPause = input("Press the <ENTER> key to continue...")
