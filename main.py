import pygame
import random

def createDeck():
  deck = []
  for i in range(10):
    if(i != 0):
      for j in range(2):
        deck.append("Red " + str(i))
        deck.append("Yellow " + str(i))
        deck.append("Green " + str(i))
        deck.append("Blue " + str(i))
    else:
      deck.append("Red " + str(i))
      deck.append("Yellow " + str(i))
      deck.append("Green " + str(i))
      deck.append("Blue " + str(i))
  for i in range(2):
    deck.append("Red Skip")
    deck.append("Yellow Skip")
    deck.append("Green Skip")
    deck.append("Blue Skip")
    deck.append("Red +2")
    deck.append("Yellow +2")
    deck.append("Green +2")
    deck.append("Blue +2")
    deck.append("Red Reverse")
    deck.append("Yellow Reverse")
    deck.append("Green Reverse")
    deck.append("Blue Reverse")
  for i in range(4):
    deck.append("Wild +4")
    deck.append("Wild card")
  random.shuffle(deck)
  return deck


def deal(deck):
  hands = [[None for _ in range(5)] for _ in range(4)]
  for i in range(5):
    for j in range(4):
      card = deck[0]
      hands[j][i] = card
      deck.remove(card)
  return hands


def checkPlay(topCard, playCard):
    return (topCard.split(" ")[1] == playCard.split(" ")[1] or topCard.split(" ")[0] == playCard.split(" ")[0] or topCard.split(" ")[0] == "Wild" or playCard.split(" ")[0] == "Wild")

def playGame():
    deck = createDeck()
    hands = deal(deck)

playGame()