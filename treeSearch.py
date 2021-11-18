from math import sqrt
from random import choice

import klaverjas as kl
import numpy as np
import tree as tr


class TreeSearch(tr.Tree):
    def __init__(self, players, playerID, trump, leadingPlayer, trickSoFar=None, log=None, cardPlayed=0):
        super().__init__([])
        if log is None:
            log = []
        if trickSoFar is None:
            trickSoFar = [0] * 4
        self.players = players
        self.trump = trump
        self.log = log
        self.trickSoFar = trickSoFar
        self.playerID = playerID
        self.visits = 0
        self.resulteList = []
        self.result = 0
        self.playerWinning = -1
        self.leadingPlayer = leadingPlayer
        self.meanResult = 0
        self.meanAbsResult = 0
        self.cardPlayed = cardPlayed

    def makeChildren(self):
        for play in kl.Card.validCards(self.players[self.playerID], self.trump, self.trickSoFar):
            newPlayers = []
            newTrickSoFar = [card for card in self.trickSoFar]
            newTrickSoFar[self.playerID] = play
            for i, player in enumerate(self.players):
                if i == self.playerID:
                    newPlayers.append([card for card in self.players[i] if card != play])
                else:
                    newPlayers.append(self.players[i])
            if len([card for card in newTrickSoFar if type(card) is kl.Card]) == 4:
                playerWinning = kl.Card.trick(newTrickSoFar, self.leadingPlayer, self.trump)
                newLeadingPlayer = playerWinning
                roem = kl.Card.roem(newTrickSoFar, self.trump)
                trickRecord = (newTrickSoFar, self.leadingPlayer, playerWinning, roem)
                newLog = [logEntry for logEntry in self.log]
                newLog.append(trickRecord)
                nextToPlay = playerWinning
                newTrickSoFar = [0] * 4
            else:
                nextToPlay = (self.playerID + 1) % 4
                newLeadingPlayer = self.leadingPlayer
                newLog = self.log
            self.add(TreeSearch(newPlayers, nextToPlay, self.trump, newLeadingPlayer, newTrickSoFar, newLog, play))

    def doNumberIts(self, N):
        for i in range(N):
            self.doIteration()

    def doIteration(self):
        if not self.isFinished():
            if super().isLeaf():
                self.makeChildren()
            ucbValues = [(self.ucb(child)) for child in self.children]
            maxiOfChoice = -1
            if sum([ucbVal == - float('inf') for ucbVal in ucbValues]) > 0:
                firstAttempts = self.firstGuessAI()
                if firstAttempts:
                    cardToAttempt = choice(firstAttempts)
                    firstAttemptIndex = [index for (index, child) in enumerate(self.children) if
                                         child.cardPlayed == cardToAttempt]
                    maxiOfChoice = firstAttemptIndex[0]
            if maxiOfChoice == -1:
                maxiOfChoice = choice([i for (i, ucbValue) in enumerate(ucbValues) if ucbValue == min(ucbValues)])
            self.children[maxiOfChoice].doIteration()
            self.result = self.children[maxiOfChoice].result * (-1) ** (
                        self.playerID + self.children[maxiOfChoice].playerID)
        else:
            points = kl.OneDeal.parseRecord(self.log, self.trump)
            self.result = (points[0] - points[1]) * ((-1) ** (self.playerID))
        self.update()
        return self.result

    def update(self):
        self.visits += 1
        self.resulteList.append(self.result)
        self.meanResult = ((len(self.resulteList) - 1) * self.meanResult + self.result) / (len(self.resulteList))
        self.meanAbsResult = ((len(self.resulteList) - 1) * self.meanAbsResult + abs(self.result)) / (
            len(self.resulteList))

    def ucb(self, child):
        exploreParam = 2
        if child.isLeaf():
            return - float('inf')
        else:
            return child.meanResult / (self.meanAbsResult + 1) - exploreParam * sqrt(2) * sqrt(
                np.log(self.visits) / child.visits)
            # return (-1)**(self.playerID - child.playerID)*child.meanResult/(self.meanAbsResult +1)  + exploreParam*sqrt(2)*sqrt(np.log(self.visits)/child.visits) 

    def findBestSequence(self):
        if self.childn(0).isFinished():
            return self.childn(0).log
        else:
            (_, child) = min([(child.meanResult, child) for child in self.children if not child.isLeaf()],
                             key=lambda elem: elem[0])
            return child.findBestSequence()

    def isFinished(self):
        return self.players == [[]] * 4

    def bestCard(self):
        (mini, child) = min([(child.meanResult, child) for child in self.children], key=lambda elem: elem[0])
        return (child.cardPlayed, mini)

    def firstGuessAI(self):
        cardsPossible = [child.cardPlayed for child in self.children if child.visits == 0]

        playedSoFar = []
        for entry in self.log:
            playedSoFar.extend(entry[0])
        remainingCards = [card for card in kl.OneDeal.deck if card not in playedSoFar]
        cardsToPlay = []
        for suit in kl.Card.suits:
            viableCardsValue = [(card, card.orderForTrickTaking(suit, suit == self.trump)) for card in remainingCards if
                                card.suit == suit and card in remainingCards]
            if viableCardsValue:
                (card, _) = max(viableCardsValue, key=lambda elem: elem[1])
                if card and card in cardsPossible:
                    cardsToPlay.append(card)

        if not cardsToPlay:
            for cardNr in range(7, 8):
                cardsToPlay = [card for card in cardsPossible if card.number == cardNr]
                if cardsToPlay:
                    return cardsToPlay
        return cardsToPlay
