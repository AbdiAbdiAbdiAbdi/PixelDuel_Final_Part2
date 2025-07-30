import pygame
from fighter import Fighter, BehaviorTracker
from pygame import mixer
import sys
import random
from collections import defaultdict, deque

pygame.init()
mixer.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

#load background image
bg_img = pygame.image.load("assets/background/backdrop.jpg").convert_alpha()
victory_img = pygame.image.load("assets/background/victory.png").convert_alpha()

#load fighters spritesheet
P1spritesheet = pygame.image.load("assets/fighters/Martial_Hero/Player1Redone.png").convert_alpha()
P2spritesheet = pygame.image.load("assets/fighters/Martial_Hero3/Player2Redone.png").convert_alpha()

#number of steps for each animation
P1_STEPS = [8, 8, 4, 6, 6, 4, 6] #second to last must be skipped
P1_SIZE = 200
P1_SCALE = 4
P1_OFFSET = [90, 80]
P1_DATA = [P1_SIZE, P1_SCALE, P1_OFFSET]
P2_STEPS = [10, 8,6,7,6,3,11]
P2_SIZE = 126
P2_SCALE = 4.3
P2_OFFSET = [55, 43]
P2_DATA = [P2_SIZE, P2_SCALE, P2_OFFSET]
#scale background to screen
scale_bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
#Set up clock
clock = pygame.time.Clock()

#define colors (some might not be used)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#load sounds
pygame.mixer.music.load("assets/sounds/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1,0,5000)
sword_fx = pygame.mixer.Sound("assets/sounds/sword.wav")
sword_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound("assets/sounds/jump.mp3")
jump_fx.set_volume(0.5)
menu_fx = pygame.mixer.Sound("assets/sounds/SFX_UI_MenuSelections.mp3")
confirm_fx = pygame.mixer.Sound("assets/sounds/SFX_UI_Confirm.mp3")
menu_fx.set_volume(0.5)
confirm_fx.set_volume(0.5)

#define font
count_font = pygame.font.Font("assets/background/turok.ttf", 150)
score_font = pygame.font.Font("assets/background/turok.ttf", 30)
menu_font = pygame.font.Font("assets/background/turok.ttf", 80)
start_font = pygame.font.Font("assets/background/turok.ttf", 40)
ai_font = pygame.font.Font("assets/background/turok.ttf", 20)
victory_menu_font = pygame.font.Font("assets/background/turok.ttf", 60)


controls_font = pygame.font.Font("assets/background/turok.ttf", 30)
controls_text_font = pygame.font.Font("assets/background/turok.ttf", 25)

start_bg_img = pygame.image.load("assets/background/backdrop.jpg").convert_alpha()
start_bg_scaled = pygame.transform.scale(start_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

#define game count
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#[P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
WINS_TO_WIN = 3  # Number of wins needed to win the match

 
# Player action tracking for AI learning - more sensitive

# Player action tracking for AI learning

player_action_tracker = {
    'last_action': 'idle',
    'last_position': 0,
    'last_keys': set(),
    'action_start_time': 0,

    'action_duration_threshold': 100,  # Reduced from implicit 1000ms
    'movement_threshold': 5 ,           # More sensitive movement detection

    'action_duration_threshold': 100,
    'movement_threshold': 5
}

class CPUFighter(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, attack_fx, jump_fx):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, attack_fx, jump_fx)
        
        # Enhanced AI state management with MORE AGGRESSIVE neutral spacing
        self.ai_state = "neutral"
        self.state_timer = 0
        self.decision_cooldown = 300  # Faster decision making (was 400)
        self.last_decision_time = 0
        
        # Behavior tracking
        self.behavior_tracker = BehaviorTracker()
        
        # Aggressive distance-based strategy - 1/3 screen length neutral distance
        self.neutral_distance = 333  # 1/3 of 1000 pixel screen width
        self.attack_range = 200      # Range where CPU will attack
        self.close_distance = 150    # Distance considered "too close"
        self.spacing_tolerance = 40  # How precise the spacing needs to be
        
        # Aggression timers
        self.patience_timer = 0
        self.max_patience = 2000     # 2 seconds before getting impatient
        self.attack_commitment_timer = 0
        
        # Movement state
        self.movement_pattern = "neutral"
        self.last_player_distance = 0
        self.player_approaching = False

    def make_decision(self, target, distance):
        """Simplified aggressive decision making"""
        current_time = pygame.time.get_ticks()
        
        # Track if player is approaching
        if distance < self.last_player_distance:
            self.player_approaching = True
        else:
            self.player_approaching = False
        
        self.last_player_distance = distance
        
        # Priority 1: Attack if player is in range
        if distance <= self.attack_range and not self.attacking and self.attack_cooldown == 0:
            return "attack_player"
        
        # Priority 2: Counter attack if player is attacking and close
        if target.attacking and distance < self.attack_range + 50:
            if random.random() < 0.8:  # High counter chance
                return "counter_attack"
        
        # Priority 3: Move away if player is too close
        if distance < self.close_distance:
            return "create_space"
        
        # Priority 4: Close distance if player is too far and we're impatient
        if distance > self.neutral_distance + self.spacing_tolerance:
            self.patience_timer += 16  # Increase patience timer
            if self.patience_timer > self.max_patience:
                self.patience_timer = 0  # Reset timer
                return "close_distance_aggressive"
        else:
            self.patience_timer = max(0, self.patience_timer - 8)  # Decrease patience when at good distance
        
        # Priority 5: Maintain neutral distance
        if distance > self.neutral_distance + self.spacing_tolerance:
            return "close_distance"
        elif distance < self.neutral_distance - self.spacing_tolerance:
            return "maintain_distance"
        
        # Default: Stay ready at neutral distance
        return "neutral_ready"

    def execute_action(self, decision, target, surface, screen_width):
        """Execute aggressive actions"""
        dx = 0
        current_distance = abs(self.rect.centerx - target.rect.centerx)
        
        if decision == "attack_player":
            # Attack aggressively
            if not self.attacking and self.attack_cooldown == 0:
                # Choose attack based on distance
                if current_distance < 170:
                    self.attack_type = 2  # Heavy attack for close range
                else:
                    self.attack_type = 1  # Light attack for medium range
                self.attack(surface, target)
                self.movement_pattern = "attacking"
                
        elif decision == "counter_attack":
            # Quick counter attack
            if not self.attacking and self.attack_cooldown == 0:
                self.attack_type = 1  # Quick light attack for counter
                self.attack(surface, target)
                self.movement_pattern = "countering"
                
        elif decision == "create_space":
            # Move away quickly
            retreat_speed = 6
            dx = -retreat_speed if self.rect.centerx < target.rect.centerx else retreat_speed
            self.running = True
            self.movement_pattern = "retreating"
            
        elif decision == "close_distance_aggressive":
            # Aggressively close distance when impatient
            approach_speed = 8  # Faster approach when impatient
            dx = approach_speed if self.rect.centerx < target.rect.centerx else -approach_speed
            self.running = True
            self.movement_pattern = "aggressive_approach"
            
        elif decision == "close_distance":
            # Normal approach to ideal distance
            approach_speed = 5
            dx = approach_speed if self.rect.centerx < target.rect.centerx else -approach_speed
            self.running = True
            self.movement_pattern = "approaching"
            
        elif decision == "maintain_distance":
            # Small adjustments to maintain ideal distance
            adjust_speed = 3
            dx = -adjust_speed if self.rect.centerx < target.rect.centerx else adjust_speed
            self.running = True
            self.movement_pattern = "maintaining"
            
        elif decision == "neutral_ready":
            # Stay ready at neutral distance with small movements
            if random.random() < 0.2:  # Occasional small movements
                dx = random.choice([-1, 0, 1])
                self.running = dx != 0
            self.movement_pattern = "ready"
            
        return dx

    def move(self, screen_width, screen_height, surface, target, round_over):
        if round_over or not self.life:
            self.running = False
            return

        current_time = pygame.time.get_ticks()
        distance = abs(self.rect.centerx - target.rect.centerx)
        
        # Face the target
        self.flip = self.rect.centerx > target.rect.centerx
        
        # Make decisions quickly
        if current_time - self.last_decision_time >= self.decision_cooldown:
            self.ai_state = self.make_decision(target, distance)
            self.last_decision_time = current_time
            
        # Execute the current decision
        dx = self.execute_action(self.ai_state, target, surface, screen_width)
        
        # Physics
        GRAVITY = 2
        dy = 0
        
        # Jump physics
        if self.jump or self.vel_y != 0:
            self.vel_y += GRAVITY
            dy = self.vel_y
            
            # Landing logic
            ground_level = screen_height - 21
            if self.rect.bottom + dy >= ground_level:
                self.rect.bottom = ground_level
                self.vel_y = 0
                self.jump = False
                dy = 0
        
        # Apply movement with screen bounds checking
        if dx != 0:
            new_x = self.rect.x + dx
            self.rect.x = max(0, min(screen_width - self.rect.width, new_x))
        
        if dy != 0:
            self.rect.y += dy
        
        # Cooldown management
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

#draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#starting screen
def show_start_screen():
    selected_option = 0
    options = ["Single Player Mode", "Versus Mode", "Controls"]
    waiting = True

    while waiting:
        screen.blit(start_bg_scaled, (0, 0))
        draw_text("PIXAL DUEL : SHADOW FIGHT", menu_font, RED, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 4)
        
        # Add subtitle
        draw_text("Single Player Mode: Fight against aggressive CPU!", ai_font, YELLOW, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 4 + 100)

        for i, option in enumerate(options):
            color = YELLOW if i == selected_option else WHITE
            draw_text(option, start_font, color, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + i * 60)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_fx.play()  # Play menu sound when navigating
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    menu_fx.play()  # Play menu sound when navigating
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    confirm_fx.play()  # Play confirm sound when selecting
                    if selected_option == 2:  # Controls option
                        show_controls_screen()
                    else:
                        return selected_option  # 0 for single, 1 for versus

def show_controls_screen():
    """Show controls screen with player controls and return to main menu option"""
    waiting = True
    
    while waiting:
        screen.blit(start_bg_scaled, (0, 0))
        
        # Title
        draw_text("CONTROLS", controls_font, RED, SCREEN_WIDTH // 2 - 100, 50)
        
        # Player 1 Controls
        draw_text("PLAYER 1", controls_text_font, YELLOW, 100, 150)
        draw_text("Move Left: A", controls_text_font, WHITE, 100, 190)
        draw_text("Move Right: D", controls_text_font, WHITE, 100, 220)
        draw_text("Jump: W", controls_text_font, WHITE, 100, 250)
        draw_text("Light Attack: Q", controls_text_font, WHITE, 100, 280)
        draw_text("Heavy Attack: E", controls_text_font, WHITE, 100, 310)
        
        # Player 2 Controls
        draw_text("PLAYER 2", controls_text_font, YELLOW, 550, 150)
        draw_text("Move Left: LEFT ARROW", controls_text_font, WHITE, 550, 190)
        draw_text("Move Right: RIGHT ARROW", controls_text_font, WHITE, 550, 220)
        draw_text("Jump: UP ARROW", controls_text_font, WHITE, 550, 250)
        draw_text("Light Attack: N", controls_text_font, WHITE, 550, 280)
        draw_text("Heavy Attack: M", controls_text_font, WHITE, 550, 310)
        
        # Instructions
        draw_text("Press ENTER to return to main menu", start_font, GREEN, SCREEN_WIDTH // 2 - 250, 450)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    confirm_fx.play()  # Play confirm sound when returning
                    waiting = False  # Return to main menu

def show_victory_menu(winner):
    """Show victory menu after someone reaches 3 wins"""
    selected_option = 0
    options = ["Rematch", "Return to Main Menu", "Exit Game"]
    waiting = True
    
    while waiting:
        screen.blit(start_bg_scaled, (0, 0))
        
        # Display winner
        winner_text = f"Player {winner} Wins!"
        draw_text(winner_text, victory_menu_font, YELLOW, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 4)
        
        # Display final score
        score_text = f"Final Score: P1: {score[0]} - P2: {score[1]}"
        draw_text(score_text, start_font, WHITE, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 4 + 80)
        
        # Display options
        for i, option in enumerate(options):
            color = YELLOW if i == selected_option else WHITE
            draw_text(option, start_font, color, SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 50 + i * 60)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    menu_fx.play()  # Play menu sound when navigating
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    menu_fx.play()  # Play menu sound when navigating
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    confirm_fx.play()  # Play confirm sound when selecting
                    if selected_option == 0:  # Rematch
                        return "rematch"
                    elif selected_option == 1:  # Return to Main Menu
                        return "main_menu"
                    else:  # Exit Game
                        pygame.quit()
                        sys.exit()

#draw background image func
def draw_bg():
    screen.blit(scale_bg, (0, 0))

#func to draw health bars
def draw_health_bar(health, x, y):
    ratio_of_vitality = health / 100
    pygame.draw.rect(screen, GREY, (x-5, y+2, 410, 35))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio_of_vitality, 30))

def detect_player_action(fighter, keys):
    """Detect and categorize player actions"""
    current_time = pygame.time.get_ticks()
    
    # Determine current action
    if fighter.attacking:
        if fighter.attack_type == 1:
            action = "attack_1"
        elif fighter.attack_type == 2:
            action = "attack_2"
        else:
            action = "attack"
    elif fighter.jump:
        action = "jump"
    elif fighter.running:
        action = "move"
    elif fighter.hit:
        action = "hit"
    else:
        action = "idle"
    
    # Check for action changes
    position_change = abs(fighter.rect.centerx - player_action_tracker['last_position'])
    time_since_last = current_time - player_action_tracker['action_start_time']
    
    # Log if action changed OR significant time passed OR significant movement
    should_log = (
        action != player_action_tracker['last_action'] or 
        time_since_last > player_action_tracker['action_duration_threshold'] or
        position_change > player_action_tracker['movement_threshold']
    )
    
    if should_log:
        distance = abs(fighter.rect.centerx - player_action_tracker['last_position'])
        
        player_action_tracker['last_action'] = action
        player_action_tracker['last_position'] = fighter.rect.centerx
        player_action_tracker['action_start_time'] = current_time
        
        return action, distance, current_time
    
    return None, None, None

def reset_fighters(selected_mode, preserve_ai_learning=False, old_cpu_data=None):
    """Reset fighters for a new round/match"""
    global fighter_1, fighter_2
    
    if selected_mode == 0:  # Single Player Mode
        fighter_1 = Fighter(1, 200, 400, False, P1_DATA, P1spritesheet, P1_STEPS, sword_fx, jump_fx)
        fighter_2 = CPUFighter(2, 700, 400, True, P2_DATA, P2spritesheet, P2_STEPS, sword_fx, jump_fx)
        
        # Preserve AI learning if requested
        if preserve_ai_learning and old_cpu_data:
            fighter_2.behavior_tracker = old_cpu_data['behavior_tracker']
    else:  # Versus Mode
        fighter_1 = Fighter(1, 200, 400, False, P1_DATA, P1spritesheet, P1_STEPS, sword_fx, jump_fx)
        fighter_2 = Fighter(2, 700, 400, True, P2_DATA, P2spritesheet, P2_STEPS, sword_fx, jump_fx)
    
    return fighter_1, fighter_2

def main_game_loop():
    global run, selected_mode, fighter_1, fighter_2, score, round_over, intro_count, last_count_update, player_action_tracker
    
    run = True
    selected_mode = show_start_screen()
    
    # Initialize fighters based on mode
    fighter_1, fighter_2 = reset_fighters(selected_mode)
    
    while run:
        #Caps framerate at 60FPS
        clock.tick(60)

        #event handeler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_bg()

        #show players health
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, WHITE, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, WHITE, 580, 60)

        #updates countdown
        if intro_count <= 0:
            # Move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
            
            # AI Learning in single player mode
            if selected_mode == 0 and isinstance(fighter_2, CPUFighter):
                # Track player actions
                keys = pygame.key.get_pressed()
                action, distance, timestamp = detect_player_action(fighter_1, keys)
                
                if action and not round_over:
                    fighter_2.behavior_tracker.log_action(action, distance, timestamp)
            
        else:
            #display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            if(pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        #update fighters
        fighter_1.update()
        fighter_2.update()

        #draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        #check for player defeat
        if round_over == False:
            if fighter_1.life == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                print(f"Score: P1={score[0]}, P2={score[1]}")
            elif fighter_2.life == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                print(f"Score: P1={score[0]}, P2={score[1]}")
        else:
            #display victory
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                # Check for match victory (first to 3 wins)
                if score[0] >= WINS_TO_WIN or score[1] >= WINS_TO_WIN:
                    winner = 1 if score[0] >= WINS_TO_WIN else 2
                    
                    # Show victory menu
                    result = show_victory_menu(winner)
                    
                    if result == "rematch":
                        # Reset everything for rematch
                        score = [0, 0]
                        round_over = False
                        intro_count = 3
                        
                        # Reset fighters - preserve AI learning in single player
                        old_cpu_data = None
                        if selected_mode == 0 and isinstance(fighter_2, CPUFighter):
                            old_cpu_data = {
                                'behavior_tracker': fighter_2.behavior_tracker
                            }
                        
                        fighter_1, fighter_2 = reset_fighters(selected_mode, True, old_cpu_data)
                        
                        # Reset player action tracker
                        player_action_tracker['last_action'] = 'idle'
                        player_action_tracker['last_position'] = 0
                        player_action_tracker['action_start_time'] = pygame.time.get_ticks()
                        
                    elif result == "main_menu":
                        # Return to main menu
                        score = [0, 0]
                        round_over = False
                        intro_count = 3
                        
                        # Reset player action tracker
                        player_action_tracker['last_action'] = 'idle'
                        player_action_tracker['last_position'] = 0
                        player_action_tracker['action_start_time'] = pygame.time.get_ticks()
                        
                        # Show start screen again and reinitialize
                        selected_mode = show_start_screen()
                        fighter_1, fighter_2 = reset_fighters(selected_mode)
                        
                else:
                    # Regular round end - continue the match
                    round_over = False
                    intro_count = 3
                    
                    # Reset fighters for next round
                    old_cpu_data = None
                    if selected_mode == 0 and isinstance(fighter_2, CPUFighter):
                        old_cpu_data = {
                            'behavior_tracker': fighter_2.behavior_tracker
                        }
                    
                    fighter_1, fighter_2 = reset_fighters(selected_mode, True, old_cpu_data)
                    
                    # Reset player action tracker
                    player_action_tracker['last_action'] = 'idle'
                    player_action_tracker['last_position'] = 0
                    player_action_tracker['action_start_time'] = pygame.time.get_ticks()

        #updates screen
        pygame.display.update()

# Run the main game loop
main_game_loop()

#exit pygame
pygame.quit()
sys.exit()