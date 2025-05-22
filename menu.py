import pygame
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

if __name__ == "__main__":
    menu = UnoMenu()
    menu.run()