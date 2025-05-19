import pygame
import random

class Card:
  def __init__(self, color, value):
    self.color = color
    self.value = value

  def __str__(self):
    return self.color + " " + str(self.value)

  def __repr__(self):
    return self.__str__()
  def __eq__(self, other):
    return isinstance(other, Card) and self.color == other.color and self.value == other.value

  def __hash__(self):
    return hash((self.color, self.value))

def createDeck():
  deck = []
  for i in range(10):
    if(i != 0):
      for j in range(2):
        deck.append(Card("Red", str(i)))
        deck.append(Card("Yellow", str(i)))
        deck.append(Card("Green", str(i)))
        deck.append(Card("Blue", str(i)))
    else:
      deck.append(Card("Red", str(i)))
      deck.append(Card("Yellow", str(i)))
      deck.append(Card("Green", str(i)))
      deck.append(Card("Blue", str(i)))
  for i in range(2):
    deck.append(Card("Red", "Skip"))
    deck.append(Card("Yellow", "Skip"))
    deck.append(Card("Green", "Skip"))
    deck.append(Card("Blue", "Skip"))
    deck.append(Card("Red", "+2"))
    deck.append(Card("Yellow", "+2"))
    deck.append(Card("Green", "+2"))
    deck.append(Card("Blue", "+2"))
    deck.append(Card("Red", "Reverse"))
    deck.append(Card("Yellow", "Reverse"))
    deck.append(Card("Green", "Reverse"))
    deck.append(Card("Blue", "Reverse"))
  for i in range(4):
    deck.append(Card("Wild", "+4"))
    deck.append(Card("Wild", "Card"))
  random.shuffle(deck)
  return deck


def deal(deck):
  hands = [[None for _ in range(7)] for _ in range(4)]
  for i in range(7):
    for j in range(4):
      card = deck[0]
      hands[j][i] = card
      deck.remove(card)
  return hands

def checkPlay(topCard, playCard, hand):
  if(len(playCard.split(" ")) != 2):
    return False
  playCard = Card(str(playCard.split(" ")[0]), str(playCard.split(" ")[1]))
  return ((topCard.value == playCard.value or topCard.color == playCard.color or topCard.color == "Wild" or playCard.color == "Wild") and (playCard in hand))

def skip(turn):
  turn=turn+1
  if(turn == 4):
    turn = 0
  return turn

def reverse(direction):
  return "reverse" if direction == "normal" else "normal"

def playGame():
  deck = createDeck()
  hands = deal(deck)
  playing = True
  topCard = deck[0]
  print("Top card is: " + str(topCard))
  i = 0
  direction = "normal"
  while playing:
    print("Player " + str(i+1) + "'s hand: " + str(hands[i]))
    if len(hands[i]) == 0:
      print("Player " + str(i+1) + " wins!")
      playing = False
      break
    else:
      noValidMove = True
      while noValidMove:
        playCard = input("Player " + str(i+1) + ", play a card: ")
        if checkPlay(topCard, playCard, hands[i]):
          playCard = Card(str(playCard.split(" ")[0]), str(playCard.split(" ")[1]))
          hands[i].remove(playCard)
          if(playCard.value == "Skip"):
            i = skip(i)
            print("Skipped")
          if(playCard.value == "Reverse"):
            direction = reverse(direction)
            print("Reversed")
          deck.insert(0, playCard)
          topCard = playCard
          noValidMove = False
        else:
          print("Invalid move!")
    if(direction == "normal"):
      i+=1
    else:
      i-=1
    if(i == 4):
      i = 0
    if(i == -1):
      i = 3

playGame()