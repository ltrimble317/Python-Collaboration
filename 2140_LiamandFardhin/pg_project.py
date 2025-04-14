import pygame
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load images for both settings
backgrounds = {
    "Vietnam": pygame.image.load('Vietnambg.png'),
    "Afghanistan": pygame.image.load('Afghanistan.png'),
    "Germany": pygame.image.load('ww2germany.png'),
    "USSR":pygame.image.load('ussrfight.png')
}

enemies = {
    "Vietnam": pygame.image.load('vietcongexp.png'),
    "Afghanistan": pygame.image.load('af_exp.png'),
    "Germany": pygame.image.load('experimental_1.png'),
    "USSR": pygame.image.load('exp_3ussr.png')
}
playerImage = pygame.image.load('new_player.png')
playerImage = pygame.transform.scale(playerImage, (100, 100))

# Game variables
pX, pY = WIDTH // 2, HEIGHT - 100
pXspeed = 0
bullet_speed = 24
enemy_bullet_speed = 6
bullets = []
enemy_bullets = []
enemy_list = []
enemy_speed = 3
score = 0
lives = 3
paused = False
high_score = 0

# Background scrolling
bgY1 = 0
bgY2 = -HEIGHT
bg_speed = 4
difficulty_multiplier = 1.0  # Will increase over time

# Font setup
font = pygame.font.Font(None, 36)

# Game functions

def draw_text(text, x, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def spawn_enemy():
    x = random.randint(50, WIDTH - 150)
    y = random.randint(-200, -100)

    # Adjust enemy hitbox size if necessary
    enemy_rect = pygame.Rect(x, y, 85, 128)  #Slightly reduced width (changed from 128 to 90)
    enemy_list.append(enemy_rect)

def reset_game():
    global pX, bullets, enemy_bullets, enemy_list, score, lives, enemy_speed, difficulty_multiplier, bg_speed, enemy_bullet_speed
    pX = WIDTH // 2
    bullets.clear()
    enemy_bullets.clear()
    enemy_list.clear()
    score = 0
    lives = 3
    enemy_speed = 3
    difficulty_multiplier = 1.0
    bg_speed = 4
    enemy_bullet_speed = 6

def pause_game():
    global paused
    while paused:
        screen.fill("black")
        draw_text("PAUSED", WIDTH // 2 - 60, HEIGHT // 2 - 50, (255, 255, 0))
        draw_text("Press 'P' to Resume", WIDTH // 2 - 120, HEIGHT // 2, (200, 200, 200))
        draw_text("Press 'Q' to Quit", WIDTH // 2 - 120, HEIGHT // 2 + 50, (200, 200, 200))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()                     
            
            
def menu_screen():
    options = ["Vietnam", "Afghanistan", "Germany", "USSR"]  #list syntax
    index = 0  # Keeps track of selected option

    while True:
        screen.fill("black")
        draw_text("Choose a setting:", WIDTH // 2 - 100, HEIGHT // 2 - 100)

        for i, option in enumerate(options):
            color = (255, 0, 0) if i == index else (255, 255, 255)  # Highlight selected option in red with rgb
            draw_text(f"> {option}" if i == index else option, WIDTH // 2 - 80, HEIGHT // 2 - 50 + (i * 30), color)

        draw_text("PRESS ENTER TO START", WIDTH // 2 - 100, HEIGHT // 2 + 100, (150, 0, 220))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    index = (index - 1) % len(options)  # Move up in menu 
                elif event.key == pygame.K_DOWN:
                    index = (index + 1) % len(options)  # Move down in menu
                elif event.key == pygame.K_RETURN:
                    return options[index]  # Return selected option

def game_over_screen():
    global score, selected_setting, high_score
    if score > high_score:
        high_score = score #updating new high score
        
    while True:
        screen.fill("black")
        draw_text("GAME OVER", WIDTH // 2 - 80, HEIGHT // 2 - 100, (255, 0, 0))
        draw_text(f"High Score: {high_score}", WIDTH // 2 - 80, HEIGHT // 2 - 50, (255, 255, 255))
        draw_text("1. Choose new level", WIDTH // 2 - 120, HEIGHT // 2, (200, 200, 200))
        draw_text("2. Quit game", WIDTH // 2 - 80, HEIGHT // 2 + 50, (200, 200, 200))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_setting = menu_screen()  # Select new level
                    reset_game()  # Reset variables                  
                    return  # Restart game loop
                if event.key == pygame.K_2:
                    pygame.quit()
                    exit()

# Run the menu
selected_setting = menu_screen()
bgImage = pygame.transform.scale(backgrounds[selected_setting], (WIDTH, HEIGHT))
enemyImage = pygame.transform.scale(enemies[selected_setting], (116, 116))

# Game loop
running = True
while running:
    screen.fill("black")

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = True
            if event.key == pygame.K_SPACE:
                if len(bullets) < 3:
                    bullets.append(pygame.Rect(pX + 26, pY, 12, 48))

    if paused:
        pause_game()

    #Increase difficulty over time
    difficulty_multiplier += 0.001
    enemy_speed = int(3 * difficulty_multiplier)
    bg_speed = int(4 * difficulty_multiplier)  # Background moves faster
    enemy_bullet_speed = int(6 * difficulty_multiplier)  # Enemy bullets go faster

    # Move background
    bgY1 += bg_speed
    bgY2 += bg_speed
    if bgY1 >= HEIGHT:
        bgY1 = -HEIGHT
    if bgY2 >= HEIGHT:
        bgY2 = -HEIGHT

    # Draw background
    screen.blit(bgImage, (0, bgY1))
    screen.blit(bgImage, (0, bgY2))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pXspeed = -6
    elif keys[pygame.K_RIGHT]:
        pXspeed = 6
    else:
        pXspeed = 0

    pX += pXspeed
    pX = max(0, min(WIDTH - 64, pX))

    # Move bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Spawn enemies
    if random.randint(1, 60) == 1:
        spawn_enemy()

    # Enemy shooting
    for enemy in enemy_list:
        if random.randint(1, 120) == 1:
            enemy_bullets.append(pygame.Rect(enemy.x + 48, enemy.y + 128, 12, 48))

    # Move enemy bullets (faster over time)
    for bullet in enemy_bullets[:]:
        bullet.y += enemy_bullet_speed
        if bullet.y > HEIGHT:
            enemy_bullets.remove(bullet)

    # Move enemies (faster over time)
    for enemy in enemy_list[:]:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemy_list.remove(enemy)

    # Collision detection (bullet vs enemy)
    for bullet in bullets[:]:
        for enemy in enemy_list[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemy_list.remove(enemy)
                score += 10
                break

    # Collision detection (enemy bullet vs player)
    player_rect = pygame.Rect(pX, pY, 64, 64)
    for bullet in enemy_bullets[:]:
        if bullet.colliderect(player_rect):
            enemy_bullets.remove(bullet)
            lives -= 1

     # Player vs enemy collision detection 
    for enemy in enemy_list[:]:
         adjusted_enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width - 10, enemy.height - 10)
         if player_rect.colliderect(adjusted_enemy_rect):
             lives -= 1
             enemy_list.remove(enemy)



    if lives <= 0:
        game_over_screen()  #Calls the earlier game over function
        bgImage = pygame.transform.scale(backgrounds[selected_setting], (WIDTH, HEIGHT))
        enemyImage = pygame.transform.scale(enemies[selected_setting], (116, 116)) 
        reset_game()  # Reset game state and start fresh

#Players hitbox (initial testing)
    screen.blit(playerImage, (pX, pY))
    player_rect = pygame.Rect(pX - 5, pY, 90, 95)  #Slightly smaller, shifted left
    for enemy in enemy_list:
        screen.blit(enemyImage, (enemy.x, enemy.y))  #Draw enemy sprite

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, "gold", bullet)

    # Draw enemy bullets
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, "red", bullet)

    # Draw UI
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Lives: {lives}", 10, 40)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()