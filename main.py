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
<<<<<<< HEAD
=======
menu_fx = pygame.mixer.Sound("assets/sounds/SFX_UI_MenuSelections.mp3")
confirm_fx = pygame.mixer.Sound("assets/sounds/SFX_UI_Confirm.mp3")
menu_fx.set_volume(0.5)
confirm_fx.set_volume(0.5)
>>>>>>> a44fefe (Final Build)

#define font
count_font = pygame.font.Font("assets/background/turok.ttf", 150)
score_font = pygame.font.Font("assets/background/turok.ttf", 30)
menu_font = pygame.font.Font("assets/background/turok.ttf", 80)
start_font = pygame.font.Font("assets/background/turok.ttf", 40)
ai_font = pygame.font.Font("assets/background/turok.ttf", 20)
victory_menu_font = pygame.font.Font("assets/background/turok.ttf", 60)
<<<<<<< HEAD
=======
controls_font = pygame.font.Font("assets/background/turok.ttf", 30)
controls_text_font = pygame.font.Font("assets/background/turok.ttf", 25)
>>>>>>> a44fefe (Final Build)
start_bg_img = pygame.image.load("assets/background/backdrop.jpg").convert_alpha()
start_bg_scaled = pygame.transform.scale(start_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

#define game count
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#[P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
WINS_TO_WIN = 3  # Number of wins needed to win the match

<<<<<<< HEAD
# Player action tracking for AI learning - more sensitive
=======
# Player action tracking for AI learning
>>>>>>> a44fefe (Final Build)
player_action_tracker = {
    'last_action': 'idle',
    'last_position': 0,
    'last_keys': set(),
    'action_start_time': 0,
<<<<<<< HEAD
    'action_duration_threshold': 100,  # Reduced from implicit 1000ms
    'movement_threshold': 5            # More sensitive movement detection
=======
    'action_duration_threshold': 100,
    'movement_threshold': 5
>>>>>>> a44fefe (Final Build)
}

class CPUFighter(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, attack_fx, jump_fx):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, attack_fx, jump_fx)
        
<<<<<<< HEAD
        # Enhanced AI state management with MORE AGGRESSIVE neutral spacing
        self.ai_state = "neutral"
        self.state_timer = 0
        self.decision_cooldown = 300  # Faster decision making (was 400)
=======
        # Simplified aggressive AI state management
        self.ai_state = "maintain_distance"
        self.decision_cooldown = 200  # Fast decision making
>>>>>>> a44fefe (Final Build)
        self.last_decision_time = 0
        
        # Behavior tracking
        self.behavior_tracker = BehaviorTracker()
        
<<<<<<< HEAD
        # INCREASED neutral distances but more aggressive approach patterns
        self.preferred_distance = 320  # INCREASED from 280 for better neutral spacing
        self.attack_commitment_distance = 180  # INCREASED from 160 for more aggressive attacks
        self.retreat_distance = 140  # Increased from 130
        self.bait_distance = 250  # Increased from 220
        self.spacing_tolerance = 50  # INCREASED tolerance for more natural movement
        
        # More aggressive baiting and movement patterns
        self.bait_timer = 0
        self.bait_cooldown = 0
        self.movement_pattern = "neutral"
        self.last_bait_success = False
        self.whiff_punish_timer = 0
        
        # Health-based difficulty scaling - MORE AGGRESSIVE
        self.initial_health = 100
        self.difficulty_multiplier = 1.2  # Start more aggressive (was 1.0)
        self.desperation_mode = False
        self.health_thresholds = {
            80: 1.4,   # INCREASED aggression at each threshold
            60: 1.7,   
            40: 2.0,   
            20: 2.5    # Maximum aggression in desperation
        }
        
        # Enhanced strategy profiles with AGGRESSIVE neutral spacing
        self.strategies = {
            "spacing_control": {
                "preferred_range": 320,  # INCREASED neutral distance
                "attack_range": 180,     # INCREASED attack commitment range
                "retreat_threshold": 130,
                "aggression": 0.7,       # INCREASED from 0.5
                "bait_frequency": 0.4,   # INCREASED from 0.3
                "reaction_time": 200,    # Faster reactions (was 250)
                "patience": 0.7          # LESS patient (was 0.9)
            },
            "counter_punish": {
                "preferred_range": 300,  # INCREASED 
                "attack_range": 180,     # INCREASED
                "retreat_threshold": 120,
                "aggression": 0.8,       # INCREASED from 0.6
                "counter_chance": 0.8,   # INCREASED from 0.7
                "reaction_time": 150,    # Faster (was 200)
                "whiff_punish": 0.9      # INCREASED from 0.8
            },
            "bait_heavy": {
                "preferred_range": 330,  # INCREASED neutral distance
                "attack_range": 170,     # INCREASED
                "retreat_threshold": 140,
                "aggression": 0.6,       # INCREASED from 0.4
                "bait_frequency": 0.8,   # INCREASED from 0.6
                "reaction_time": 180,    # Faster (was 220)
                "fake_approach": 0.8     # INCREASED from 0.6
            },
            "pressure_waves": {
                "preferred_range": 280,  # Increased from 220
                "attack_range": 190,     # INCREASED from 170
                "retreat_threshold": 110,
                "aggression": 0.9,       # INCREASED from 0.7
                "wave_intensity": 0.7,   # INCREASED from 0.5
                "reaction_time": 120,    # Faster (was 150)
                "commitment": 0.8        # INCREASED from 0.6
            },
            "desperation": {
                "preferred_range": 220,  # Increased from 180
                "attack_range": 200,     # INCREASED from 180
                "retreat_threshold": 100,
                "aggression": 1.0,       # Maximum aggression
                "reaction_time": 80,     # Fastest reactions (was 100)
                "all_or_nothing": 0.9    # INCREASED from 0.8
            }
        }
        
        self.current_strategy = "spacing_control"
        self.adaptation_timer = 0
        self.adaptation_interval = 4000  # Faster adaptation (was 5000)
        
        # Advanced timing and reads
        self.pattern_recognition = defaultdict(int)
        self.player_habits = {
            'approaches_after_jump': 0,
            'attacks_after_movement': 0,
            'retreats_when_pressured': 0,
            'button_mashes': 0
        }
        
        # More aggressive movement state
        self.current_movement_goal = "maintain_distance"
        self.movement_commitment = 0
        self.fake_approach_timer = 0

    def update_difficulty_from_health(self):
        """Dynamically adjust difficulty based on health loss"""
        health_lost_percentage = ((self.initial_health - self.health) / self.initial_health) * 100
        
        # Update difficulty multiplier based on health thresholds
        new_multiplier = 1.2  # Start at 1.2 instead of 1.0
        for threshold, multiplier in sorted(self.health_thresholds.items(), reverse=True):
            if self.health <= threshold:
                new_multiplier = multiplier
                break
        
        # Smooth transition between difficulty levels
        if new_multiplier > self.difficulty_multiplier:
            self.difficulty_multiplier = min(new_multiplier, self.difficulty_multiplier + 0.02)
        
        # Enter desperation mode at very low health
        if self.health <= 20 and not self.desperation_mode:
            self.desperation_mode = True
            self.current_strategy = "desperation"
            self.decision_cooldown = max(150, int(self.decision_cooldown * 0.8))
            
        # Adjust strategy selection based on health
        elif self.health <= 40:
            self.current_strategy = "pressure_waves"
        elif self.health <= 60:
            self.current_strategy = "counter_punish"

    def calculate_ideal_distance(self, target):
        """Calculate the ideal distance with IMPROVED neutral spacing"""
        strategy = self.strategies[self.current_strategy]
        base_distance = strategy.get("preferred_range", 320)  # Higher default
        
        # Adjust based on target's state - MORE AGGRESSIVE positioning
        if target.attacking:
            return max(base_distance + 40, 300)  # Less retreat when they attack (was +60, 280)
        elif target.jump:
            return base_distance - 50  # Get MUCH closer for anti-air (was -30)
        elif target.running:
            return base_distance + 20  # Less space when they're mobile (was +40)
        else:
            return base_distance

    def should_commit_to_attack(self, target, distance):
        """Determine if it's safe to commit to an attack - MORE AGGRESSIVE"""
        strategy = self.strategies[self.current_strategy]
        
        # MORE AGGRESSIVE distance check
        if distance > strategy.get("attack_range", 180):  # Increased range
            return False
            
        # More willing to attack even if target is attacking
        if target.attacking and random.random() > strategy.get("counter_chance", 0.5):  # Increased from 0.3
            return False
            
        # Consider target's state - MORE AGGRESSIVE
        if target.jump and distance > 150:  # Increased threshold from 120
            return True
            
        # Consider our own state and cooldowns
        if self.attack_cooldown > 0:
            return False
            
        # Apply difficulty multiplier with HIGHER base aggression
        aggression = strategy.get("aggression", 0.7) * self.difficulty_multiplier  # Higher base
        return random.random() < aggression  # Removed 0.8 conservation factor

    def plan_baiting_action(self, target, distance):
        """Plan a baiting action to make the opponent whiff - MORE AGGRESSIVE"""
        if self.bait_cooldown > 0:
            return None
            
        strategy = self.strategies[self.current_strategy]
        bait_chance = strategy.get("bait_frequency", 0.4) * self.difficulty_multiplier  # Removed 0.7 multiplier
        
        if random.random() < bait_chance:
            # Choose bait type based on distance and target state - MORE AGGRESSIVE ranges
            if distance < 220:  # INCREASED from 190
                return "dash_back_bait"
            elif distance < 280:  # INCREASED from 250
                return "fake_approach"
            else:
                return "jump_bait"
        return None

    def make_decision(self, target, distance):
        """Enhanced decision making with MORE AGGRESSIVE spacing priority"""
        strategy = self.strategies[self.current_strategy]
        current_time = pygame.time.get_ticks()
        
        # Update difficulty based on health
        self.update_difficulty_from_health()
        
        # Calculate ideal positioning
        ideal_distance = self.calculate_ideal_distance(target)
        distance_error = distance - ideal_distance
        
        # Priority 1: Punish whiffed attacks - MORE AGGRESSIVE
        if self.whiff_punish_timer > 0:
            self.whiff_punish_timer -= 16
            if target.attacking and distance < 200:  # INCREASED threshold from 170
                return "whiff_punish"
        
        # Priority 2: Counter attack opportunities - MORE AGGRESSIVE
        if target.attacking and distance < strategy.get("retreat_threshold", 140):  # Increased threshold
            counter_chance = strategy.get("counter_chance", 0.6) * self.difficulty_multiplier  # Higher base, removed 0.8 multiplier
            if random.random() < counter_chance:
                return "counter_attack"
            else:
                return "defensive_retreat"
        
        # Priority 3: Maintain ideal spacing - MORE TOLERANT of distance
        if abs(distance_error) > self.spacing_tolerance:
            if distance_error > 100:  # INCREASED threshold from 80 - too far
                return "aggressive_approach"  # NEW more aggressive approach
            elif distance_error < -80:  # INCREASED threshold from -60 - too close
                return "create_space"
        
        # Priority 4: Baiting actions - MORE FREQUENT
        bait_action = self.plan_baiting_action(target, distance)
        if bait_action:
            self.bait_cooldown = random.randint(1000, 2000)  # SHORTER cooldown (was 1500-3000)
            return bait_action
        
        # Priority 5: Attack commitment - MORE AGGRESSIVE
        if self.should_commit_to_attack(target, distance) and distance < 200:  # INCREASED from 160
            return "committed_attack"
        
        # Priority 6: Proactive neutral positioning - MORE AGGRESSIVE
        if distance < ideal_distance - 60:  # INCREASED threshold from -50
            return "maintain_space"
        elif distance > ideal_distance + 100:  # INCREASED threshold from +80
            return "proactive_approach"  # NEW more aggressive approach
        
        return "aggressive_neutral"  # NEW more aggressive neutral

    def execute_action(self, decision, target, surface, screen_width):
        """Execute actions with MORE AGGRESSIVE movement and BETTER neutral spacing"""
        dx = 0
        strategy = self.strategies[self.current_strategy]
        current_distance = abs(self.rect.centerx - target.rect.centerx)
        
        # Apply difficulty multiplier to movement speed - FASTER base speed
        base_speed = 5  # INCREASED from 4
        speed_multiplier = min(1.5, 1.0 + (self.difficulty_multiplier - 1.0) * 0.3)  # Higher multiplier
        adjusted_speed = int(base_speed * speed_multiplier)
        
        if decision == "close_distance" or decision == "aggressive_approach":
            # MORE AGGRESSIVE controlled approach
            approach_speed = 5 if current_distance > 350 else 4  # INCREASED speeds
            dx = approach_speed if self.rect.centerx < target.rect.centerx else -approach_speed
            self.running = True
            self.movement_pattern = "approach"
            
        elif decision == "proactive_approach":
            # NEW: More proactive approaching
            approach_speed = 4
            dx = approach_speed if self.rect.centerx < target.rect.centerx else -approach_speed
            self.running = True
            self.movement_pattern = "approach"
            
        elif decision == "create_space":
            # Quick but measured retreat
            retreat_speed = adjusted_speed
            dx = -retreat_speed if self.rect.centerx < target.rect.centerx else retreat_speed
            self.running = True
            self.movement_pattern = "retreat"
            
        elif decision == "controlled_approach":
            # FASTER measured approach (was 2 speed)
            dx = 3 if self.rect.centerx < target.rect.centerx else -3
            self.running = True
            self.movement_pattern = "approach"
            
        elif decision == "maintain_space":
            # Small adjustments to maintain ideal distance
            adjust_speed = 2  # INCREASED from 1
            dx = -adjust_speed if self.rect.centerx < target.rect.centerx else adjust_speed
            self.running = True
            self.movement_pattern = "maintain"
            
        elif decision == "dash_back_bait":
            # Quick retreat to bait whiff
            dx = -7 if self.rect.centerx < target.rect.centerx else 7  # INCREASED from -6
            self.running = True
            self.movement_pattern = "bait"
            self.whiff_punish_timer = 600  # INCREASED timer from 500
            
        elif decision == "fake_approach":
            # Step forward MORE AGGRESSIVELY then retreat
            if self.fake_approach_timer <= 0:
                self.fake_approach_timer = 350  # Shorter fake approach (was 400)
                dx = 4 if self.rect.centerx < target.rect.centerx else -4  # INCREASED from 3
            elif self.fake_approach_timer > 175:
                dx = 2 if self.rect.centerx < target.rect.centerx else -2  # INCREASED from 1
            else:
                dx = -4 if self.rect.centerx < target.rect.centerx else 4  # INCREASED from -3
                
            self.fake_approach_timer -= 16
            self.running = True
            self.movement_pattern = "bait"
            
        elif decision == "jump_bait":
            # Jump to bait anti-air
            if not self.jump:
                self.vel_y = -25  # Shorter jump for baiting
                self.jump = True
                self.jump_sound.play()
            self.movement_pattern = "bait"
            
        elif decision == "whiff_punish":
            # Quick punish after successful bait - MORE AGGRESSIVE
            if not self.attacking and self.attack_cooldown == 0:
                # MORE AGGRESSIVE range for punishing
                if current_distance < 170:  # INCREASED from 140
                    self.attack_type = 2  # Heavy attack for whiff punish
                else:
                    self.attack_type = 1  # Light attack to close distance
                self.attack(surface, target)
                self.movement_pattern = "punish"
                
        elif decision == "counter_attack":
            # Counter attack with FASTER timing
            if not self.attacking and self.attack_cooldown == 0:
                # Faster counter timing
                reaction_delay = max(60, int(150 / self.difficulty_multiplier))  # FASTER
                if random.random() < 0.8:  # INCREASED success rate from 0.7
                    self.attack_type = 1 if current_distance > 140 else 2  # INCREASED threshold from 120
                    self.attack(surface, target)
                    
        elif decision == "committed_attack":
            # MORE AGGRESSIVE attack positioning
            if not self.attacking and self.attack_cooldown == 0:
                # Step forward for better range
                if current_distance > 150:  # INCREASED threshold from 130
                    dx = 2 if self.rect.centerx < target.rect.centerx else -2  # INCREASED from 1
                    
                # Choose attack type based on situation
                if target.jump:
                    self.attack_type = 2  # Anti-air
                elif current_distance < 140:  # INCREASED from 120
                    self.attack_type = 2  # Close range heavy
                else:
                    self.attack_type = 1  # Mid range light
                    
                self.attack(surface, target)
                self.movement_pattern = "attack"
                
        elif decision == "defensive_retreat":
            # Safe retreat from pressure
            retreat_speed = adjusted_speed + 2  # INCREASED urgency from +1
            dx = -retreat_speed if self.rect.centerx < target.rect.centerx else retreat_speed
            self.running = True
            self.movement_pattern = "retreat"
            
        elif decision == "aggressive_neutral":
            # NEW: More active neutral positioning
            if random.random() < 0.4:  # INCREASED movement frequency from 0.2
                adjust = random.choice([-2, -1, 0, 1, 2])  # Wider range of movement
                dx = adjust
                self.running = adjust != 0
            self.movement_pattern = "neutral"
            
        elif decision == "neutral_positioning":
            # More active positioning adjustments
            if random.random() < 0.3:  # INCREASED movement frequency from 0.2
                adjust = random.choice([-1, 0, 1])
                dx = adjust
                self.running = adjust != 0
            self.movement_pattern = "neutral"
            
        else:  # Default neutral behavior
            # More frequent small movements to stay active
            if random.random() < 0.1:  # INCREASED from 0.05
                dx = random.choice([-1, 0, 1])  # Removed extra zeros for more movement
                self.running = dx != 0
            self.movement_pattern = "neutral"
=======
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
>>>>>>> a44fefe (Final Build)
            
        return dx

    def move(self, screen_width, screen_height, surface, target, round_over):
        if round_over or not self.life:
            self.running = False
            return

        current_time = pygame.time.get_ticks()
        distance = abs(self.rect.centerx - target.rect.centerx)
        
        # Face the target
        self.flip = self.rect.centerx > target.rect.centerx
        
<<<<<<< HEAD
        # FASTER decision speed based on difficulty
        base_cooldown = self.decision_cooldown
        adjusted_cooldown = max(150, int(base_cooldown / max(1.0, self.difficulty_multiplier)))  # Removed 0.8 multiplier
        
        if current_time - self.last_decision_time >= adjusted_cooldown:
=======
        # Make decisions quickly
        if current_time - self.last_decision_time >= self.decision_cooldown:
>>>>>>> a44fefe (Final Build)
            self.ai_state = self.make_decision(target, distance)
            self.last_decision_time = current_time
            
        # Execute the current decision
        dx = self.execute_action(self.ai_state, target, surface, screen_width)
        
<<<<<<< HEAD
        # Enhanced movement and physics
        GRAVITY = 2
        dy = 0
        
        # Jump physics and air control
=======
        # Physics
        GRAVITY = 2
        dy = 0
        
        # Jump physics
>>>>>>> a44fefe (Final Build)
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
<<<<<<< HEAD
                
                # FASTER decision after landing
                if distance < 220:  # INCREASED threshold from 180 for better neutral spacing
                    self.last_decision_time = current_time - adjusted_cooldown + 50  # FASTER from +100
=======
>>>>>>> a44fefe (Final Build)
        
        # Apply movement with screen bounds checking
        if dx != 0:
            new_x = self.rect.x + dx
            self.rect.x = max(0, min(screen_width - self.rect.width, new_x))
        
        if dy != 0:
            self.rect.y += dy
        
        # Cooldown management
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
<<<<<<< HEAD
            
        # Update bait cooldown
        if self.bait_cooldown > 0:
            self.bait_cooldown -= 16
            
        # Adapt strategy MORE FREQUENTLY
        if current_time - self.adaptation_timer > self.adaptation_interval:
            self.adapt_strategy()
            self.adaptation_timer = current_time

    def learn_from_player_action(self, action, distance, time_stamp):
        """Enhanced learning with pattern recognition"""
        self.behavior_tracker.log_action(action, distance, time_stamp)
        
        # More sensitive learning - reduced thresholds for habit detection
        if action == "attack" and distance > 120:  # Reduced from implicit 150
            self.player_habits['button_mashes'] += 1
        elif action == "move" and self.movement_pattern == "bait":
            self.player_habits['approaches_after_jump'] += 1
        elif action == "move" and distance < 150:
            self.player_habits['retreats_when_pressured'] += 1
        elif action == "attack" and hasattr(self, 'last_action') and self.last_action == "move":
            self.player_habits['attacks_after_movement'] += 1
            
        # Adjust baiting frequency based on success rate
        if self.movement_pattern == "bait" and action == "attack":
            self.last_bait_success = True
        
        self.last_action = action
            
    def adapt_strategy(self):
        """Adapt strategy with health-based considerations"""
        # Health-based strategy override
        if self.desperation_mode:
            self.current_strategy = "desperation"
            return
        elif self.health <= 40:
            self.current_strategy = "pressure_waves"
            return
        elif self.health <= 70:
            self.current_strategy = "counter_punish"
            return
            
        # More sensitive adaptation based on learned behavior
        dominant_behavior = self.behavior_tracker.get_dominant_behavior()
        
        if dominant_behavior == "aggressive":
            self.current_strategy = "bait_heavy"
        elif dominant_behavior == "jump_heavy":
            self.current_strategy = "counter_punish"
        elif dominant_behavior == "defensive":
            self.current_strategy = "pressure_waves"
        elif self.player_habits['button_mashes'] > 3:  # Reduced from 5
            self.current_strategy = "bait_heavy"
        elif self.player_habits['attacks_after_movement'] > 2:  # New pattern
            self.current_strategy = "counter_punish"
        else:
            self.current_strategy = "spacing_control"
=======
>>>>>>> a44fefe (Final Build)

#draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#starting screen
def show_start_screen():
    selected_option = 0
<<<<<<< HEAD
    options = ["Single Player Mode", "Versus Mode"]
=======
    options = ["Single Player Mode", "Versus Mode", "Controls"]
>>>>>>> a44fefe (Final Build)
    waiting = True

    while waiting:
        screen.blit(start_bg_scaled, (0, 0))
        draw_text("PIXAL FIGHTER", menu_font, RED, SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 4)
        
<<<<<<< HEAD
        # Add subtitle explaining AI learning
        draw_text("Single Player Mode: learns from your playstyle!", ai_font, YELLOW, SCREEN_WIDTH // 2 - 210, SCREEN_HEIGHT // 4 + 100)
=======
        # Add subtitle
        draw_text("Single Player Mode: Fight against aggressive CPU!", ai_font, YELLOW, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 4 + 100)
>>>>>>> a44fefe (Final Build)

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
<<<<<<< HEAD
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selected_option  # 0 for single, 1 for versus
=======
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
>>>>>>> a44fefe (Final Build)

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
<<<<<<< HEAD
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
=======
                    menu_fx.play()  # Play menu sound when navigating
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    menu_fx.play()  # Play menu sound when navigating
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    confirm_fx.play()  # Play confirm sound when selecting
>>>>>>> a44fefe (Final Build)
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

<<<<<<< HEAD
def draw_ai_info(cpu_fighter, x, y):
    """Draw AI learning information with difficulty indicators"""
    if hasattr(cpu_fighter, 'current_strategy'):
        strategy_text = f"AI Strategy: {cpu_fighter.current_strategy.replace('_', ' ').title()}"
        color = RED if cpu_fighter.current_strategy == "desperation" else GREEN
        draw_text(strategy_text, ai_font, color, x, y)
        
        state_text = f"AI State: {cpu_fighter.ai_state.replace('_', ' ').title()}"
        draw_text(state_text, ai_font, BLUE, x, y + 25)
        
        # Show behavior analysis
        if cpu_fighter.behavior_tracker.action_history:
            behavior = cpu_fighter.behavior_tracker.get_dominant_behavior()
            behavior_text = f"Your Style: {behavior.replace('_', ' ').title()}"
            draw_text(behavior_text, ai_font, WHITE, x, y + 50)
            
        # Show difficulty escalation based on health
        difficulty_level = min(int((100 - cpu_fighter.health) / 20), 5)
        difficulty_text = f"AI Difficulty: {'★' * difficulty_level}{'☆' * (5 - difficulty_level)}"
        difficulty_color = YELLOW if difficulty_level < 3 else RED
        draw_text(difficulty_text, ai_font, difficulty_color, x, y + 75)
        
        # Show movement pattern
        pattern_text = f"AI Pattern: {cpu_fighter.movement_pattern.replace('_', ' ').title()}"
        draw_text(pattern_text, ai_font, WHITE, x, y + 100)
        
        # Show health-based multiplier
        multiplier_text = f"Skill Multiplier: {cpu_fighter.difficulty_multiplier:.1f}x"
        multiplier_color = WHITE if cpu_fighter.difficulty_multiplier < 1.5 else RED
        draw_text(multiplier_text, ai_font, multiplier_color, x, y + 125)
        
        # Desperation mode indicator
        if cpu_fighter.desperation_mode:
            draw_text("AI: DESPERATION MODE!", ai_font, RED, x, y + 150)

def detect_player_action(fighter, keys):
    """Detect and categorize player actions with increased sensitivity"""
=======
def detect_player_action(fighter, keys):
    """Detect and categorize player actions"""
>>>>>>> a44fefe (Final Build)
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
    
<<<<<<< HEAD
    # More sensitive detection - check position changes and shorter time thresholds
=======
    # Check for action changes
>>>>>>> a44fefe (Final Build)
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
<<<<<<< HEAD
            fighter_2.difficulty_multiplier = old_cpu_data['difficulty_multiplier']
            fighter_2.player_habits = old_cpu_data['player_habits']
            fighter_2.adapt_strategy()
=======
>>>>>>> a44fefe (Final Build)
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

<<<<<<< HEAD
        # Show AI learning info in single player mode
        if selected_mode == 0 and isinstance(fighter_2, CPUFighter):
            draw_ai_info(fighter_2, 20, 90)

=======
>>>>>>> a44fefe (Final Build)
        #updates countdown
        if intro_count <= 0:
            # Move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
            
<<<<<<< HEAD
            # AI Learning in single player mode with more sensitive detection
=======
            # AI Learning in single player mode
>>>>>>> a44fefe (Final Build)
            if selected_mode == 0 and isinstance(fighter_2, CPUFighter):
                # Track player actions
                keys = pygame.key.get_pressed()
                action, distance, timestamp = detect_player_action(fighter_1, keys)
                
                if action and not round_over:
<<<<<<< HEAD
                    fighter_2.learn_from_player_action(action, distance, timestamp)
=======
                    fighter_2.behavior_tracker.log_action(action, distance, timestamp)
>>>>>>> a44fefe (Final Build)
            
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
<<<<<<< HEAD
                                'behavior_tracker': fighter_2.behavior_tracker,
                                'difficulty_multiplier': fighter_2.difficulty_multiplier,
                                'player_habits': fighter_2.player_habits.copy()
=======
                                'behavior_tracker': fighter_2.behavior_tracker
>>>>>>> a44fefe (Final Build)
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
<<<<<<< HEAD
                            'behavior_tracker': fighter_2.behavior_tracker,
                            'difficulty_multiplier': fighter_2.difficulty_multiplier,
                            'player_habits': fighter_2.player_habits.copy()
=======
                            'behavior_tracker': fighter_2.behavior_tracker
>>>>>>> a44fefe (Final Build)
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