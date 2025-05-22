import pygame
import random
import sys
import os
from pygame import mixer

class UnoMenu:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("UNO Game - IB Computer Science Final Project Ft. Neil, Jack, Noirit")
        

        self.colors = {
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 128, 0),
            'yellow': (255, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'background': (21, 71, 52)  # Dark green background modeled after balatro bg
        }
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.submenu_font = pygame.font.Font(None, 36)
        





        self.current_menu = "main"
        self.selected_option = 0
        self.menu_options = {
            "main": ["Play Game", "Game Settings", "Player Setup", "Rules", "Statistics", "Quit"],
            "play": ["2 Players", "3 Players", "4 Players", "Back"],
            "settings": ["Difficulty: Easy", "Sound: ON", "Custom Rules", "Back"],
            "players": ["Human vs Computer", "Human vs Human", "Back"],
            "rules": ["Basic Rules", "Special Cards", "Back"],
            "statistics": ["Win Rates", "Card Usage", "Back"]
        }
        




        self.settings = {
            "difficulty": "Easy",
            "sound": True,
            "custom_rules": False
        }
        
        # ASS ets
        self.load_assets()
        
        # lalalalal
        if self.settings["sound"]:
            self.play_music()
    
    def load_assets(self):
        """Load images and sounds for the menu"""
        try:




            self.card_back = pygame.image.load(os.path.join('assets', 'card_back.png'))
            self.card_back = pygame.transform.scale(self.card_back, (120, 180))
            
            # UNO logo
            self.logo = pygame.image.load(os.path.join('assets', 'uno_logo.png'))
            self.logo = pygame.transform.scale(self.logo, (400, 150))
            
            # button sounds
            self.hover_sound = mixer.Sound(os.path.join('assets', 'hover.wav'))
            self.select_sound = mixer.Sound(os.path.join('assets', 'select.wav'))
        except:


            # if assets don't load
            self.card_back = pygame.Surface((120, 180))
            self.card_back.fill(self.colors['red'])
            
            self.logo = pygame.Surface((400, 150))
            self.logo.fill(self.colors['blue'])
            #self.logo.fill('uno_logo.png')
            
            self.hover_sound = mixer.Sound(buffer=bytearray(0))
            self.select_sound = mixer.Sound(buffer=bytearray(0))
    
    def play_music(self):
        """Play background music if enabled"""
        try:
            mixer.music.load(os.path.join('assets', 'menu_music.mp3'))
            mixer.music.set_volume(0.5)
            mixer.music.play(-1)  # inf loop  
        except:
            pass
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.settings["sound"] = not self.settings["sound"]
        self.menu_options["settings"][1] = f"Sound: {'ON' if self.settings['sound'] else 'OFF'}"
        
        if self.settings["sound"]:
            mixer.music.unpause()
            self.play_music()
        else:
            mixer.music.pause()
    
    def toggle_difficulty(self):
        """Cycle through difficulty levels"""
        difficulties = ["Easy", "Medium", "Hard"]
        current_index = difficulties.index(self.settings["difficulty"])
        next_index = (current_index + 1) % len(difficulties)
        self.settings["difficulty"] = difficulties[next_index]
        self.menu_options["settings"][0] = f"Difficulty: {self.settings['difficulty']}"
    
    def toggle_custom_rules(self):
        """Toggle custom rules"""
        self.settings["custom_rules"] = not self.settings["custom_rules"]
        status = "ON" if self.settings["custom_rules"] else "OFF"
        self.menu_options["settings"][2] = f"Custom Rules: {status}"
    
    def draw_menu(self):
        """Draw the current menu"""
        self.screen.fill(self.colors['background'])
        
        logo_rect = self.logo.get_rect(center=(self.screen_width//2, 100))
        self.screen.blit(self.logo, logo_rect)
        



        for i, pos in enumerate([(50, 150), (self.screen_width-170, 150)]):
            self.screen.blit(self.card_back, pos)


            border_color = [self.colors['red'], self.colors['blue'], self.colors['green'], self.colors['yellow']][i % 4]
            pygame.draw.rect(self.screen, border_color, (pos[0]-5, pos[1]-5, 130, 190), 5)
        



        options = self.menu_options[self.current_menu]
        for i, option in enumerate(options):
            color = self.colors['yellow'] if i == self.selected_option else self.colors['white']
            
            if i == self.selected_option:
                pygame.draw.rect(self.screen, self.colors['black'], 
                                (self.screen_width//2 - 200, 250 + i*60 - 5, 400, 50), 
                                border_radius=10)
            
            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen_width//2, 280 + i*60))
            self.screen.blit(text, text_rect)
        
        footer = self.submenu_font.render("IB Computer Science Final Project", True, self.colors['white'])
        footer_rect = footer.get_rect(center=(self.screen_width//2, self.screen_height - 30))
        self.screen.blit(footer, footer_rect)
        
        pygame.display.flip()
    
    def handle_events(self):
        """Handle menu navigation and selection"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options[self.current_menu])
                    if self.settings["sound"]:
                        self.hover_sound.play()
                
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options[self.current_menu])
                    if self.settings["sound"]:
                        self.hover_sound.play()
                
                elif event.key == pygame.K_RETURN:
                    if self.settings["sound"]:
                        self.select_sound.play()
                    self.handle_selection()
                
                elif event.key == pygame.K_ESCAPE:
                    if self.current_menu != "main":
                        self.current_menu = "main"
                        self.selected_option = 0
    
    def handle_selection(self):
        """Handle menu selection based on current menu and selected option"""
        option = self.menu_options[self.current_menu][self.selected_option]
        
        if self.current_menu == "main":
            if option == "Play Game":
                self.current_menu = "play"
            elif option == "Game Settings":
                self.current_menu = "settings"
            elif option == "Player Setup":
                self.current_menu = "players"
            elif option == "Rules":
                self.current_menu = "rules"
            elif option == "Statistics":
                self.current_menu = "statistics"
            elif option == "Quit":
                pygame.quit()
                sys.exit()
            self.selected_option = 0
        
        elif self.current_menu == "play":
            if option == "Back":
                self.current_menu = "main"
            else:


                num_players = int(option.split()[0])
                self.start_game(num_players)
        
        elif self.current_menu == "settings":
            if option.startswith("Difficulty"):
                self.toggle_difficulty()
            elif option.startswith("Sound"):
                self.toggle_sound()
            elif option.startswith("Custom Rules"):
                self.toggle_custom_rules()
            elif option == "Back":
                self.current_menu = "main"
        
        elif self.current_menu == "players":
            if option == "Back":
                self.current_menu = "main"
            else:



                self.set_player_mode(option)
        
        elif self.current_menu in ["rules", "statistics"]:
            if option == "Back":
                self.current_menu = "main"
            else:


                self.display_info_page(option.lower().replace(" ", "_"))
    
    def start_game(self, num_players):
        """Start the UNO game with the given number of players"""
        playGame()
        print(f"Starting game with {num_players} players")  


        #for now sends back bc game not finished 
        self.show_loading_screen()
        self.current_menu = "main"
        self.selected_option = 0
    
    def set_player_mode(self, mode):
        """Set the player mode (human vs computer or human vs human)"""
        print(f"Player mode set to: {mode}")  
        self.current_menu = "main"
        self.selected_option = 0
    
    def display_info_page(self, page):
        """Display an information page (rules or statistics)"""
        print(f"Displaying info page: {page}")  # Replace with actual implementation
        # This would show a new screen with the requested information
        # For now, we'll just return to main menu after a delay
        self.show_info_screen(page)
        self.current_menu = "main"
        self.selected_option = 0
    
    def show_loading_screen(self):
        """Show a loading screen before starting the game"""
        self.screen.fill(self.colors['background'])
        
        loading_text = self.title_font.render("Starting Game...", True, self.colors['white'])
        loading_rect = loading_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(loading_text, loading_rect)
        
        pygame.display.flip()
        pygame.time.delay(1000)  # Show for 1s
    
    def show_info_screen(self, page):
        """Show an information screen for rules or statistics"""
        self.screen.fill(self.colors['background'])
        
        title = self.title_font.render(page.replace("_", " ").title(), True, self.colors['white'])
        title_rect = title.get_rect(center=(self.screen_width//2, 100))
        self.screen.blit(title, title_rect)
        
        # Sample content - replace with actual rules or statistics
        if page == "basic_rules":
            lines = [
                "1. Match the top card of the discard pile by color or value",
                "2. If you can't play, draw a card from the draw pile",
                "3. Call 'UNO' when you have only 1 card left",
                "4. First player to play all their cards wins!"
            ]
        elif page == "special_cards":
            lines = [
                "Skip: Next player misses a turn",
                "Reverse: Changes direction of play",
                "Draw +2: Next player draws 2 cards",
                "Wild: Choose the next color",
                "Wild +4: Choose color and next player draws 4"
            ]
        else:  # Statistics pages
            lines = [
                "Statistics tracking coming soon!",
                "Will track win rates, card usage,",
                "and other interesting metrics."
            ]
        
        #  content lines
        for i, line in enumerate(lines):
            text = self.menu_font.render(line, True, self.colors['yellow'])
            text_rect = text.get_rect(center=(self.screen_width//2, 200 + i*50))
            self.screen.blit(text, text_rect)
        
        # Back prompt
        back_text = self.submenu_font.render("Press any key to return", True, self.colors['white'])
        back_rect = back_text.get_rect(center=(self.screen_width//2, self.screen_height - 50))
        self.screen.blit(back_text, back_rect)
        
        pygame.display.flip()
        
        # Wait for any key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
    
    def run(self):
        """Run the menu system"""
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.draw_menu()
            clock.tick(60)

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

def skip(turn, direction):
  if(direction == "normal"):
    turn=turn+1
    if(turn == 4):
      turn = 0
  else:
    turn=turn-1
    if(turn == -1):
      turn = 3
  return turn
  

def reverse(direction):
  return "reverse" if direction == "normal" else "normal"

def reshuffle(discardPile):
  return random.shuffle(discardPile)

def drawCard(deck, hand, discardPile):
  if(len(deck) == 0):
    deck = reshuffle(discardPile)
  hand.append(deck[0])
  deck.remove(deck[0])
  return hand

def pickColor(player):
  if player == 0:
    color = input("Choose a color (Red, Yellow, Green, Blue): ")
    while color not in ["Red", "Yellow", "Green", "Blue"]:
      print("Invalid color!")
      color = input("Choose a color (Red, Yellow, Green, Blue): ")
  else:
    color = random.choice(["Red", "Yellow", "Green", "Blue"])
  return color

class UnoGame:
    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("UNO Game")
        
        self.colors = {
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 128, 0),
            'yellow': (255, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'background': (21, 71, 52),  # Dark green background
            'card_outline': (200, 200, 200)  # Light gray for card outlines
        }
        
        self.card_font = pygame.font.Font(None, 36)
        self.message_font = pygame.font.Font(None, 48)
        self.status_font = pygame.font.Font(None, 24)
        self.controls_font = pygame.font.Font(None, 20)
        
        # Card dimensions
        self.card_width = 100
        self.card_height = 150
        self.card_back = pygame.Surface((self.card_width, self.card_height))
        self.card_back.fill(self.colors['red'])
        pygame.draw.rect(self.card_back, self.colors['card_outline'], (0, 0, self.card_width, self.card_height), 2)
        
        self.message = ""
        self.message_timer = 0

    def get_relative_position(self, player_index, current_player):
        """Convert absolute player index to relative position (0=bottom, 1=right, 2=top, 3=left)"""
        relative_pos = (player_index - current_player) % 4
        return relative_pos

    def draw_card(self, card, x, y, selected=False, is_top_card=False):
        color = self.colors[card.color.lower()] if card.color.lower() in self.colors else self.colors['black']
        card_surface = pygame.Surface((self.card_width, self.card_height))
        card_surface.fill(self.colors['white'])
        
        # Draw colored background with margin
        margin = 5
        pygame.draw.rect(card_surface, color, (margin, margin, self.card_width-2*margin, self.card_height-2*margin))
        
        # Draw card value
        text = self.card_font.render(str(card.value), True, self.colors['white'])
        text_rect = text.get_rect(center=(self.card_width//2, self.card_height//2))
        card_surface.blit(text, text_rect)
        
        # Draw smaller value in corners
        small_font = pygame.font.Font(None, 24)
        small_text = small_font.render(str(card.value), True, self.colors['white'])
        card_surface.blit(small_text, (margin + 2, margin + 2))
        card_surface.blit(small_text, (self.card_width - small_text.get_width() - margin - 2, 
                                     self.card_height - small_text.get_height() - margin - 2))
        
        # Draw outline
        outline_color = self.colors['yellow'] if selected else self.colors['card_outline']
        outline_width = 3 if selected or is_top_card else 1
        pygame.draw.rect(card_surface, outline_color, (0, 0, self.card_width, self.card_height), outline_width)
        
        # Make top card larger
        if is_top_card:
            card_surface = pygame.transform.scale(card_surface, 
                                               (int(self.card_width * 1.2), 
                                                int(self.card_height * 1.2)))
        
        self.screen.blit(card_surface, (x, y))
        return pygame.Rect(x, y, card_surface.get_width(), card_surface.get_height())

    def draw_game_state(self, hands, current_player, top_card, message=""):
        self.screen.fill(self.colors['background'])
        
        # Draw top card with larger size and centered
        top_card_x = self.screen_width//2 - (self.card_width * 1.2)//2
        top_card_y = self.screen_height//2 - (self.card_height * 1.2)//2
        self.draw_card(top_card, top_card_x, top_card_y, is_top_card=True)
        
        # Draw current player's hand at bottom
        hand = hands[current_player]
        start_x = (self.screen_width - (len(hand) * (self.card_width + 10))) // 2
        card_rects = []
        for i, card in enumerate(hand):
            rect = self.draw_card(card, start_x + i * (self.card_width + 10), self.screen_height - 170)
            card_rects.append((rect, card))
        
        # Draw other players' cards (face down)
        for i in range(4):
            if i != current_player:
                relative_pos = self.get_relative_position(i, current_player)
                num_cards = len(hands[i])
                
                if relative_pos == 2:  # Top
                    y = 20
                    x = self.screen_width//2 - (num_cards * 20)//2
                    for j in range(num_cards):
                        self.screen.blit(self.card_back, (x + j*20, y))
                elif relative_pos == 1:  # Right
                    x = self.screen_width - 120
                    y = self.screen_height//2 - (num_cards * 20)//2
                    for j in range(num_cards):
                        self.screen.blit(self.card_back, (x, y + j*20))
                elif relative_pos == 3:  # Left
                    x = 20
                    y = self.screen_height//2 - (num_cards * 20)//2
                    for j in range(num_cards):
                        self.screen.blit(self.card_back, (x, y + j*20))
        
        # Draw player indicators with relative positions
        for i in range(4):
            relative_pos = self.get_relative_position(i, current_player)
            text = self.status_font.render(f"Player {i+1}" + (" (You)" if i == current_player else ""), 
                                         True, self.colors['white'])
            if relative_pos == 2:  # Top
                self.screen.blit(text, (self.screen_width//2 - text.get_width()//2, 5))
            elif relative_pos == 1:  # Right
                self.screen.blit(text, (self.screen_width - text.get_width() - 5, self.screen_height//2))
            elif relative_pos == 0:  # Bottom
                self.screen.blit(text, (self.screen_width//2 - text.get_width()//2, self.screen_height - 30))
            else:  # Left
                self.screen.blit(text, (5, self.screen_height//2))
        
        # Draw message
        if message:
            text = self.message_font.render(message, True, self.colors['white'])
            self.screen.blit(text, (self.screen_width//2 - text.get_width()//2, 10))
        
        # Draw controls help
        controls = [
            "Controls:",
            "- Click on a card to play it",
            "- Cards must match color or value of top card",
            "- Wild cards can be played anytime",
            "- Click color when prompted for Wild cards"
        ]
        
        for i, control in enumerate(controls):
            text = self.controls_font.render(control, True, self.colors['white'])
            self.screen.blit(text, (10, self.screen_height - 100 + i * 20))
        
        pygame.display.flip()
        return card_rects
    
    def get_clicked_card(self, pos, card_rects):
        for rect, card in card_rects:
            if rect.collidepoint(pos):
                return card
        return None
    
    def show_color_picker(self):
        colors = ["Red", "Blue", "Green", "Yellow"]
        rects = []
        spacing = 20
        total_width = len(colors) * (self.card_width + spacing) - spacing
        start_x = (self.screen_width - total_width) // 2
        start_y = self.screen_height // 2 - self.card_height // 2
        
        # Draw color options
        for i, color in enumerate(colors):
            x = start_x + i * (self.card_width + spacing)
            rect = pygame.Rect(x, start_y, self.card_width, self.card_height)
            pygame.draw.rect(self.screen, self.colors[color.lower()], rect)
            rects.append((rect, color))
        
        pygame.display.flip()
        
        # Wait for color selection
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for rect, color in rects:
                        if rect.collidepoint(pos):
                            return color
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

def playGame():
    game = UnoGame()
    deck = createDeck()
    discardPile = []
    hands = deal(deck)
    playing = True
    discardPile.append(deck[0])
    deck.remove(deck[0])
    topCard = discardPile[0]
    i = 0
    direction = "normal"
    message = f"Game started! Top card is {str(topCard)}"
    
    while playing:
        card_rects = game.draw_game_state(hands, i, topCard, message)
        message = ""
        
        # Check win at the start of the turn
        if len(hands[i]) == 0:
            message = f"Player {i+1} Wins!"
            print("game is over")
            game.draw_game_state(hands, i, topCard, message)
            pygame.time.wait(3000)
            playing = False
            break
        
        possibleMove = False
        for card in hands[i]:
            if checkPlay(topCard, str(card), hands[i]):
                possibleMove = True
                break
                
        if not possibleMove:
            message = "No valid moves, drawing a card..."
            game.draw_game_state(hands, i, topCard, message)
            pygame.time.wait(1000)
            hands[i] = drawCard(deck, hands[i], discardPile)
            message = f"Drew: {str(hands[i][-1])}"
            # Check win after drawing a card
            if len(hands[i]) == 0:
                message = f"Player {i+1} Wins!"
                print("game is over")
                game.draw_game_state(hands, i, topCard, message)
                pygame.time.wait(3000)
                playing = False
                break
            continue
        
        if i == 0:  # Human player
            valid_move = False
            while not valid_move:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        clicked_card = game.get_clicked_card(event.pos, card_rects)
                        if clicked_card and checkPlay(topCard, str(clicked_card), hands[i]):
                            playCard = clicked_card
                            valid_move = True
                            break
                        elif clicked_card:
                            message = "Invalid move!"
                            game.draw_game_state(hands, i, topCard, message)
        else:  # AI player
            pygame.time.wait(1000)  # Add delay for AI moves
            for card in hands[i]:
                if checkPlay(topCard, str(card), hands[i]):
                    playCard = card
                    break
        
        message = f"Played: {str(playCard)}"
        hands[i].remove(playCard)
        discardPile.append(playCard)
        
        # Check win after playing a card
        if len(hands[i]) == 0:
            message = f"Player {i+1} Wins!"
            print("game is over")
            game.draw_game_state(hands, i, topCard, message)
            pygame.time.wait(3000)
            playing = False
            break
        
        if playCard.value == "Skip":
            i = skip(i, direction)
            message = "Skipped!"
        elif playCard.value == "Reverse":
            direction = reverse(direction)
            message = "Reversed!"
        elif playCard.value == "+2":
            i = skip(i, direction)
            for _ in range(2):
                hands[i] = drawCard(deck, hands[i], discardPile)
            message = "Drew 2 cards!"
            # Check win after forced draw
            if len(hands[i]) == 0:
                message = f"Player {i+1} Wins!"
                print("game is over")
                game.draw_game_state(hands, i, topCard, message)
                pygame.time.wait(3000)
                playing = False
                break
        elif playCard.value == "+4":
            color = game.show_color_picker() if i == 0 else pickColor(i)
            playCard.color = color
            playCard.value = "Wild"
            i = skip(i, direction)
            for _ in range(4):
                hands[i] = drawCard(deck, hands[i], discardPile)
            message = f"Drew 4 cards! Color changed to {color}"
            # Check win after forced draw
            if len(hands[i]) == 0:
                message = f"Player {i+1} Wins!"
                print("game is over")
                game.draw_game_state(hands, i, topCard, message)
                pygame.time.wait(3000)
                playing = False
                break
        elif playCard.value == "Card":
            color = game.show_color_picker() if i == 0 else pickColor(i)
            playCard.color = color
            playCard.value = "Wild"
            message = f"Color changed to {color}"
        
        discardPile.insert(0, playCard)
        topCard = playCard
        
        if direction == "normal":
            i += 1
        else:
            i -= 1
        if i == 4:
            i = 0
        if i == -1:
            i = 3

if __name__ == "__main__":
    menu = UnoMenu()
    menu.run()
