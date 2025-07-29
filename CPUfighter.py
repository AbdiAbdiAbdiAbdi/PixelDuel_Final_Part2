import random
import pygame
from fighter import Fighter

class CPUFighter(Fighter):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, attack_fx, jump_fx):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, attack_fx, jump_fx)
        self.next_action_time = pygame.time.get_ticks()
        self.keep_distance = 250  # distance to maintain from player
        self.attack_range = 100   # when within this range, attack
        self.backoff_distance = 150  # too close = back off
        self.cooldown = 1200  # ms between actions
        self.state = "idle"

    def move(self, screen_width, screen_height, surface, target, round_over):
        if round_over:
            return

        current_time = pygame.time.get_ticks()

        # Face the player
        self.flip = True if self.rect.centerx < target.rect.centerx else False

        # Distance to player
        distance = abs(self.rect.centerx - target.rect.centerx)

        # Decide action based on distance
        if current_time >= self.next_action_time:
            if distance < self.backoff_distance:
                self.state = "backoff"
            elif distance > self.keep_distance:
                self.state = "approach"
            elif distance <= self.attack_range:
                self.state = "attack"
            else:
                self.state = "idle"
            self.next_action_time = current_time + self.cooldown

        # Movement logic
        dx = 0
        if self.state == "approach":
            dx = 5 if self.rect.centerx < target.rect.centerx else -5
        elif self.state == "backoff":
            dx = -5 if self.rect.centerx < target.rect.centerx else 5
        elif self.state == "attack":
            if not self.attacking:
                self.attack(random.randint(0, 1))  # random punch or kick
            self.state = "idle"

        # Apply movement
        self.rect.x += dx

        # Prevent going off screen
        self.rect.x = max(0, min(screen_width - self.rect.width, self.rect.x))

        # Jump occasionally
        if random.random() < 0.01 and self.on_ground:
            self.jump = True