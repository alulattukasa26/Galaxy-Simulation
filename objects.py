import random
import math
import pygame
import config

class BlackHole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mass = 12000.0
        self.radius = 28
        self.color = (20, 20, 20)

    def draw(self, surface, zoom, camera_dx, camera_dy, center_x, center_y):
        screen_x = int(center_x + (self.x - config.V_CENTER_X + camera_dx) * zoom)
        screen_y = int(center_y + (self.y - config.V_CENTER_Y + camera_dy) * zoom)
        current_radius = max(1, int(self.radius * zoom))
        
        pygame.draw.circle(surface, self.color, (screen_x, screen_y), current_radius)
        pygame.draw.circle(surface, (138, 43, 226), (screen_x, screen_y), current_radius + max(1, int(8 * zoom)), max(1, int(4 * zoom)))

class Star:
    def __init__(self, mode="spiral", arms=2, max_dist=1600, spin=0.003, direction=1):
        if mode == "spiral":
            num_arms = arms
            arm = random.randint(0, num_arms - 1)
            distance_from_center = 40 + (random.random() ** 2.2) * (max_dist - 40)
            
            base_angle = (arm * 2 * math.pi) / num_arms
            arm_angle = base_angle + distance_from_center * spin
            spread = 25.0 / (distance_from_center ** 0.3)
            total_angle = arm_angle + random.uniform(-spread, spread)
            
            self.x = config.V_CENTER_X + math.cos(total_angle) * distance_from_center
            self.y = config.V_CENTER_Y + math.sin(total_angle) * distance_from_center
            orbital_speed = 5.0 + (distance_from_center * 0.003)
        elif mode == "sombrero":
            if random.random() < 0.6:
                distance_from_center = (random.random() ** 2.0) * 200
                spread = random.uniform(0, 2 * math.pi)
                self.x = config.V_CENTER_X + math.cos(spread) * distance_from_center
                self.y = config.V_CENTER_Y + math.sin(spread) * distance_from_center
                orbital_speed = 8.5
            else:
                distance_from_center = random.uniform(600, 1400)
                angle = random.uniform(0, 2 * math.pi)
                self.x = config.V_CENTER_X + math.cos(angle) * distance_from_center
                self.y = config.V_CENTER_Y + math.sin(angle) * distance_from_center
                orbital_speed = 6.2
        elif mode == "meteor":
            spawn_side = random.randint(0, 3)
            if spawn_side == 0:
                self.x = random.uniform(100, config.SPACE_WIDTH - 100)
                self.y = 100
            elif spawn_side == 1:
                self.x = random.uniform(100, config.SPACE_WIDTH - 100)
                self.y = config.SPACE_HEIGHT - 100
            elif spawn_side == 2:
                self.x = 100
                self.y = random.uniform(100, config.SPACE_HEIGHT - 100)
            else:
                self.x = config.SPACE_WIDTH - 100
                self.y = random.uniform(100, config.SPACE_HEIGHT - 100)
                
            angle_to_center = math.atan2(config.V_CENTER_Y - self.y, config.V_CENTER_X - self.x)
            speed = random.uniform(12.0, 18.0)
            self.vx = math.cos(angle_to_center) * speed
            self.vy = math.sin(angle_to_center) * speed
            
            self.mass = 600.0
            self.radius = 8
            self.color = (255, 255, 255)
            return
        else:
            distance_from_center = (random.random() ** 2.0) * 1200
            angle = random.uniform(0, 2 * math.pi)
            self.x = config.V_CENTER_X + math.cos(angle) * distance_from_center
            self.y = config.V_CENTER_Y + math.sin(angle) * distance_from_center
            orbital_speed = 4.5

        dx = self.x - config.V_CENTER_X
        dy = self.y - config.V_CENTER_Y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist > 0:
            self.vx = (-dy / dist) * orbital_speed * direction
            self.vy = (dx / dist) * orbital_speed * direction
        else:
            self.vx = 0.0
            self.vy = 0.0
        
        self.mass = random.uniform(10.0, 80.0)
        self.radius = max(4, int(self.mass // 10))
        self.color = random.choice(config.STAR_COLORS)

    def attract(self, other, dt):
        if self is other:
            return
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < 15:
            distance = 15
            
        force = config.G * (self.mass * other.mass) / (distance**2)
        acceleration = force / self.mass
        
        self.vx += acceleration * (dx / distance) * dt
        self.vy += acceleration * (dy / distance) * dt

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        margin = 30
        bounce_factor = -0.5

        if self.x < margin:
            self.x = margin
            self.vx *= bounce_factor
        elif self.x > config.SPACE_WIDTH - margin:
            self.x = config.SPACE_WIDTH - margin
            self.vx *= bounce_factor

        if self.y < margin:
            self.y = margin
            self.vy *= bounce_factor
        elif self.y > config.SPACE_HEIGHT - margin:
            self.y = config.SPACE_HEIGHT - margin
            self.vy *= bounce_factor

    def draw(self, surface, zoom, camera_dx, camera_dy, show_velocity, center_x, center_y):
        screen_x = int(center_x + (self.x - config.V_CENTER_X + camera_dx) * zoom)
        screen_y = int(center_y + (self.y - config.V_CENTER_Y + camera_dy) * zoom)
        current_radius = max(1, int(self.radius * zoom))
        
        if show_velocity:
            speed = math.sqrt(self.vx**2 + self.vy**2)
            max_speed = 16.0
            factor = min(1.0, speed / max_speed)
            
            r = int(50 + (255 - 50) * factor)
            g = int(50 + (255 - 50) * factor)
            b = int(255 + (50 - 255) * factor)
            current_color = (r, g, b)
        else:
            current_color = self.color
            
        pygame.draw.circle(surface, current_color, (screen_x, screen_y), current_radius)
