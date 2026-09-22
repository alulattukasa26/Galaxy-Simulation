import sys
import math
import pygame
import config
from objects import BlackHole, Star
from commands import execute_command

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Galactic Simulation")

center_x = config.WIDTH // 2
center_y = config.HEIGHT // 2

zoom = 1.0
camera_dx = 0
camera_dy = 0
is_dragging = False

current_galaxy_name = "MilkyWay"
show_links = False
show_velocity_color = False
is_paused = False
dt_modifier = config.DT

input_text = ""
input_active = False

font = pygame.font.SysFont("Consolas", 18)

black_hole = BlackHole(config.V_CENTER_X, config.V_CENTER_Y)
stars = [Star("spiral", arms=2, max_dist=1600, spin=0.003, direction=random_choice) for random_choice in [1] for _ in range(120)]

import random
for s in stars:
    s.vx *= random.choice([1, -1])
    s.vy *= random.choice([1, -1])

clock = pygame.time.Clock()
running = True

while running:
    current_width, current_height = screen.get_size()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            center_x = event.w // 2
            center_y = event.h // 2
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                is_dragging = True
                pygame.mouse.get_rel()
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                is_dragging = False
                
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    res_stars, res_name, success = execute_command(input_text)
                    if success:
                        if res_name == "exit":
                            running = False
                            pygame.quit()
                            sys.exit()
                        elif res_name == "meteor":
                            for _ in range(5):
                                stars.append(Star(mode="meteor"))
                        else:
                            stars = res_stars
                            current_galaxy_name = res_name
                    input_text = ""
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            else:
                if event.key == pygame.K_RETURN:
                    input_active = True
                elif event.key == pygame.K_UP:
                    dt_modifier += 0.1
                elif event.key == pygame.K_DOWN:
                    dt_modifier = max(0.0, dt_modifier - 0.1)
                elif event.key == pygame.K_l:
                    show_links = not show_links
                elif event.key == pygame.K_v:
                    show_velocity_color = not show_velocity_color
                elif event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                elif event.key == pygame.K_c:
                    camera_dx = 0
                    camera_dy = 0
                    zoom = 1.0

    if is_dragging:
        rel_x, rel_y = pygame.mouse.get_rel()
        camera_dx += rel_x / zoom
        camera_dy += rel_y / zoom

    if not input_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            zoom += 0.02
        if keys[pygame.K_s]:
            zoom = max(0.05, zoom - 0.02)

    if not is_paused:
        for star1 in stars:
            for star2 in stars:
                star1.attract(star2, dt_modifier)
            star1.attract(black_hole, dt_modifier)
                
        for star in stars:
            star.update(dt_modifier)

    screen.fill((0, 0, 0))
    
    if show_links:
        for i in range(len(stars)):
            for j in range(i + 1, len(stars)):
                s1 = stars[i]
                s2 = stars[j]
                dx = s2.x - s1.x
                dy = s2.y - s1.y
                dist = math.sqrt(dx**2 + dy**2)
                if dist < 60:
                    x1 = int(center_x + (s1.x - config.V_CENTER_X + camera_dx) * zoom)
                    y1 = int(center_y + (s1.y - config.V_CENTER_Y + camera_dy) * zoom)
                    x2 = int(center_x + (s2.x - config.V_CENTER_X + camera_dx) * zoom)
                    y2 = int(center_y + (s2.y - config.V_CENTER_Y + camera_dy) * zoom)
                    pygame.draw.line(screen, (40, 40, 40), (x1, y1), (x2, y2), 1)

    black_hole.draw(screen, zoom, camera_dx, camera_dy, center_x, center_y)
    for star in stars:
        star.draw(screen, zoom, camera_dx, camera_dy, show_velocity_color, center_x, center_y)
    
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (200, 200, 200))
    state_text = font.render(f"Galaxy: {current_galaxy_name}", True, (0, 255, 255))
    count_text = font.render(f"Stars: {len(stars)}", True, (200, 200, 200))
    dt_text = font.render(f"Time Step (DT): {round(dt_modifier, 1)}", True, (255, 255, 0))
    links_text = font.render(f"Grav-Lines (L): {'ON' if show_links else 'OFF'}", True, (0, 255, 0) if show_links else (255, 0, 0))
    vel_text = font.render(f"Velocity Color (V): {'ON' if show_velocity_color else 'OFF'}", True, (0, 255, 0) if show_velocity_color else (255, 0, 0))
    pause_text = font.render(f"Simulation: {'PAUSED (SPACE)' if is_paused else 'RUNNING'}", True, (255, 100, 100) if is_paused else (100, 255, 100))
    
    screen.blit(fps_text, (20, 20))
    screen.blit(state_text, (20, 45))
    screen.blit(count_text, (20, 70))
    screen.blit(dt_text, (20, 95))
    screen.blit(links_text, (20, 120))
    screen.blit(vel_text, (20, 145))
    screen.blit(pause_text, (20, 170))
    
    input_box_y = current_height - 50
    input_box_width = 300
    input_box_height = 32
    
    box_color = (255, 255, 255) if input_active else (80, 80, 80)
    pygame.draw.rect(screen, box_color, (20, input_box_y, input_box_width, input_box_height), 2)
    
    text_surface = font.render(input_text + ("|" if input_active and pygame.time.get_ticks() % 1000 < 500 else ""), True, (255, 255, 255))
    screen.blit(text_surface, (28, input_box_y + 6))
    
    pygame.display.flip()
