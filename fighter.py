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

        # Only process input and movement if alive and round not over
        if self.life and not round_over:
            #player1
            if self.player == 1:
                #can only do the following if not attacing
                if self.attacking == False:
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
                if self.attacking == False:
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

        # ALWAYS apply gravity - even when dead
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ALWAYS check ground collision - even when dead  
        if self.rect.bottom + dy > screen_height - 21:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 21 - self.rect.bottom

        # Only apply horizontal movement and screen bounds if alive
        if self.life and not round_over:
            #make sure play stays on screen
            if self.rect.left + dx < 0:
                dx = -self.rect.left

            if self.rect.right + dx > 1000:
                dx = screen_width - self.rect.right

            #make sure players face each other
            self.update_flip(target)

        # ALWAYS apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Apply position updates
        if self.life and not round_over:
            self.rect.x += dx  # Only move horizontally if alive
        
        self.rect.y += dy  # ALWAYS apply vertical movement (gravity/falling)


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

    #attack func
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attacked = False
            self.temp_surface = surface
            self.temp_target = target
            self.attack_cooldown = len(self.animation_list[3]) * 100 // 60

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
        """Update behavior pattern counters"""
        if "attack" in action:
            self.consecutive_attacks += 1
            self.consecutive_jumps = 0
            if self.consecutive_attacks >= 2:
                self.counters['aggressive'] += 1
        elif action == "jump":
            self.consecutive_jumps += 1
            self.consecutive_attacks = 0
            if self.consecutive_jumps >= 1:
                self.counters['jump_happy'] += 1
        else:
            self.consecutive_attacks = 0
            self.consecutive_jumps = 0

    def get_dominant_behavior(self):
        """Identify the player's dominant behavior pattern"""
        if not self.action_history:
            return "neutral"
            
        recent_actions = [entry['action'] for entry in list(self.action_history)[-10:]]
        attack_count = sum(1 for action in recent_actions if "attack" in action)
        jump_count = sum(1 for action in recent_actions if action == "jump")
        move_count = sum(1 for action in recent_actions if action == "move")
        
        if attack_count >= 4:
            return "aggressive"
        elif jump_count >= 3:
            return "jump_heavy"
        elif move_count >= 6:
            return "defensive"
        elif self.counters['counter_heavy'] > 2:
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
        
        # Simplified aggressive AI state management
        self.ai_state = "maintain_distance"
        self.decision_cooldown = 200  # Fast decision making
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
        # Always apply gravity (even when dead)
        GRAVITY = 2
        dy = 0
        
        # Apply gravity to CPU as well
        self.vel_y += GRAVITY
        dy = self.vel_y
        
        # Ground collision (always check, even when dead)
        ground_level = screen_height - 21
        if self.rect.bottom + dy >= ground_level:
            self.rect.bottom = ground_level
            self.vel_y = 0
            self.jump = False
            dy = 0
        
        # Only do AI logic if alive and round not over
        if round_over or not self.life:
            self.running = False
            # Still apply vertical movement (falling)
            if dy != 0:
                self.rect.y += dy
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
        
        # Apply movement with screen bounds checking (only when alive)
        if dx != 0:
            new_x = self.rect.x + dx
            self.rect.x = max(0, min(screen_width - self.rect.width, new_x))
        
        if dy != 0:
            self.rect.y += dy
        
        # Cooldown management
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1