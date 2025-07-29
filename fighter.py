import pygame
import random
from collections import defaultdict, deque

class Fighter():
    #init func
    def __init__(self, player,x,y, flip, data, sprite_sheet, animation_steps, attack_fx, jump_fx):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet,animation_steps)
        self.action = 0 #0=idle, #1=run, #2=jump #3=attack1, #4=attack2, #5=hit, #6=death 
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.jump_sound = jump_fx
        self.num_of_jumps = 0
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attacked = False
        self.attack_sound = attack_fx
        self.hit = False
        self.hit_frame = {3:4, 4:4} if self.player == 1 else {3:4, 4:3}
        self.health = 100
        self.life = True

    def load_images(self, sprite_sheet, animation_steps):
        #extract images from spritesheet
        animation_list = []
        for y, frame in enumerate(animation_steps):
            temp_img_list = []
            for j in range(frame):
                temp_img = sprite_sheet.subsurface(j * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size*self.image_scale, self.size*self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
    

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        # d = delta (change in axis)
        dx = 0
        dy = 0
        self.running = False
        #self.attack_type = 0


        #get keypress
        key = pygame.key.get_pressed()

        #player1
        if self.player == 1:
            #can only do the following if not attacing
            if self.attacking == False and self.life and not round_over:
                #movement keys
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                
                #jump
                #TODO add Double Jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                    self.jump_sound.play()
                
                #attack key
                if key[pygame.K_q] or key[pygame.K_e]:
                    self.attack(surface, target)
                    if key[pygame.K_q]:
                        self.attack_type = 1
                    
                    if key[pygame.K_e]:
                        self.attack_type = 2
        #player2
        if self.player == 2:
            #can only do the following if not attacing
            if self.attacking == False and self.life and not round_over:
                #movement keys
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                
                #jump
                #TODO add Double Jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                    self.jump_sound.play()
                
                #attack key
                if key[pygame.K_n] or key[pygame.K_m]:
                    self.attack(surface, target)
                    if key[pygame.K_n]:
                        self.attack_type = 1
                    
                    if key[pygame.K_m]:
                        self.attack_type = 2

            


        #applyin gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #make sure play stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left

        if self.rect.right + dx > 1000:
            dx = screen_width - self.rect.right
        
        if self.rect.bottom + dy > screen_height - 21:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 21 - self.rect.bottom

        #make sure players face each other
        self.update_flip(target)

        #applys attac cooldown

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        


        #update player postion
        self.rect.x += dx

        self.rect.y += dy


    def update_flip(self, target):
        self.flip = target.rect.centerx < self.rect.centerx


    #updates each frame for animation
    def update(self):
        #check what action player is performing
        if self.health <= 0:
            self.health = 0
            self.life = False
            self.update_action(6)#6:death
        elif self.hit == True:
            self.update_action(5) #5:hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)#3:attack 1
            elif self.attack_type == 2:
                self.update_action(4)#4:attack 2
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        #check if time has passed since last frame shown
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.action in [3, 4]:
            if self.frame_index == self.hit_frame[self.action] and not self.attacked:
                self.check_attack_collision(self.temp_surface, self.temp_target)
                self.attacked = True

        if self.frame_index >= len(self.animation_list[self.action]):
            #if player dead, end animation
            if self.life == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attacked = False
                    self.attack_type = 0
                    self.attack_cooldown = 50
                #Check if damg was taken
                if self.action == 5:
                    self.hit = False
                    
                    #if player was attacking, then attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 50
            """
            #check if an attack was executed
            if self.action == 3 or self.action == 4:
                self.attacking = False
                self.attack_cooldown = 50
            
            """

    #attack func
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attacked = False
            self.temp_surface = surface
            self.temp_target = target
            self.attack_cooldown = len(self.animation_list[3]) * 100 // 60
            #attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)


    def check_attack_collision(self, surface, target):
        self.attack_sound.play()
        sword_range = self.rect.width * 5
        if self.flip:
            #if flipped attack box flips
            attack_x = self.rect.right - sword_range
        else:
            attack_x = self.rect.left

        attacking_rect = pygame.Rect(attack_x, self.rect.y, sword_range, self.rect.height)


        if attacking_rect.colliderect(target.rect):
            target.health -= 50
            target.hit = True

        



        #pygame.draw.rect(surface, (0, 255, 0), attacking_rect)
    
    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #draw func
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))


class BehaviorTracker:
    """Tracks player behavior patterns and contexts"""
    def __init__(self):
        # Context transitions: what happens after certain actions
        self.transitions = defaultdict(lambda: defaultdict(int))
        
        # Time-based patterns
        self.action_history = deque(maxlen=50)  # Last 50 actions
        self.distance_behavior = defaultdict(list)  # Actions at different distances
        
        # State counters
        self.counters = {
            'aggressive': 0,    # Many attacks in sequence
            'defensive': 0,     # Much running/jumping
            'counter_heavy': 0, # Attacks right after being hit
            'jump_happy': 0,    # Frequent jumping
            'pressure': 0       # Constant forward movement
        }
        
        self.last_action = "idle"
        self.last_distance = 0
        self.consecutive_attacks = 0
        self.consecutive_jumps = 0

    def log_action(self, action, distance, time_stamp):
        """Log a player action with context"""
        # Track transitions
        self.transitions[self.last_action][action] += 1
        
        # Track distance-based behavior
        distance_category = self.categorize_distance(distance)
        self.distance_behavior[distance_category].append(action)
        
        # Add to action history
        self.action_history.append({
            'action': action,
            'distance': distance,
            'time': time_stamp
        })
        
        # Update behavioral counters
        self.update_behavior_counters(action)
        
        self.last_action = action
        self.last_distance = distance

    def categorize_distance(self, distance):
        """Categorize distance into close, medium, far"""
        if distance < 150:
            return "close"
        elif distance < 350:
            return "medium"
        else:
            return "far"

    def update_behavior_counters(self, action):
<<<<<<< HEAD
        """Update behavior pattern counters with more sensitive triggers"""
        if "attack" in action:
            self.consecutive_attacks += 1
            self.consecutive_jumps = 0
            # More sensitive: 2 instead of 3 consecutive attacks
=======
        """Update behavior pattern counters"""
        if "attack" in action:
            self.consecutive_attacks += 1
            self.consecutive_jumps = 0
>>>>>>> a44fefe (Final Build)
            if self.consecutive_attacks >= 2:
                self.counters['aggressive'] += 1
        elif action == "jump":
            self.consecutive_jumps += 1
            self.consecutive_attacks = 0
<<<<<<< HEAD
            # More sensitive: 1 instead of 2 consecutive jumps
=======
>>>>>>> a44fefe (Final Build)
            if self.consecutive_jumps >= 1:
                self.counters['jump_happy'] += 1
        else:
            self.consecutive_attacks = 0
            self.consecutive_jumps = 0

    def get_dominant_behavior(self):
<<<<<<< HEAD
        """Identify the player's dominant behavior pattern with more sensitive thresholds"""
=======
        """Identify the player's dominant behavior pattern"""
>>>>>>> a44fefe (Final Build)
        if not self.action_history:
            return "neutral"
            
        recent_actions = [entry['action'] for entry in list(self.action_history)[-10:]]
        attack_count = sum(1 for action in recent_actions if "attack" in action)
        jump_count = sum(1 for action in recent_actions if action == "jump")
        move_count = sum(1 for action in recent_actions if action == "move")
        
<<<<<<< HEAD
        # More sensitive analysis patterns
        if attack_count >= 4:  # Reduced from 6
            return "aggressive"
        elif jump_count >= 3:  # Reduced from 4
            return "jump_heavy"
        elif move_count >= 6:  # Added defensive movement pattern
            return "defensive"
        elif self.counters['counter_heavy'] > 2:  # Reduced from 3
=======
        if attack_count >= 4:
            return "aggressive"
        elif jump_count >= 3:
            return "jump_heavy"
        elif move_count >= 6:
            return "defensive"
        elif self.counters['counter_heavy'] > 2:
>>>>>>> a44fefe (Final Build)
            return "counter_focused"
        else:
            return "neutral"

    def get_likely_next_action(self, current_context):
        """Predict likely next action based on patterns"""
        if current_context in self.transitions:
            transitions = self.transitions[current_context]
            if transitions:
                # Get most common transition
                return max(transitions.items(), key=lambda x: x[1])[0]
        return "idle"


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
<<<<<<< HEAD
            self.attack_cooldown -= 1
            
        # Update bait cooldown
        if self.bait_cooldown > 0:
            self.bait_cooldown -= 16
            
        # Adapt strategy MORE FREQUENTLY
        if current_time - self.adaptation_timer > self.adaptation_interval:
            self.adapt_strategy()
            self.adaptation_timer = current_time
=======
            self.attack_cooldown -= 1
>>>>>>> a44fefe (Final Build)
