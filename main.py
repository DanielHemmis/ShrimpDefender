import random
import math

import pygame
from pygame import mixer

HEIGHT = 800
WIDTH = 600

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((HEIGHT, WIDTH))

# Background
background = pygame.image.load("underwater800600.png")

# Background Music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Shrimp Defender")
icon = pygame.image.load("lobster small.png")
pygame.display.set_icon(icon)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def projectile(x, y):
    screen.blit(projectileImg, (x, y))


def fire_projectile(x, y):
    global projectile_state
    projectile_state = "fire"
    screen.blit(projectileImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, projectileX, projectileY):
    distance = math.sqrt((math.pow((enemyX - projectileX), 2)) + (math.pow((enemyY - projectileY), 2)))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    gameover = game_over.render("GAME OVER", True, (255, 0, 0))
    screen.blit(gameover, (210, 250))
    mixer.music.stop()


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 48)
textX = 310
textY = 20

# Game Over
game_over = pygame.font.Font('freesansbold.ttf', 64)

# Player
playerImg = pygame.image.load("lobster.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("octopus.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 100))
    enemyX_change.append(0.3)
    enemyY_change.append(20)

# Projectile
# Ready - Projectile invisible
# Fire - Projectile is currently moving
projectileImg = pygame.image.load("bubble.png")
projectileX = 0
projectileY = 480
projectileX_change = 0
projectileY_change = 0.5
projectile_state = "ready"

# Game Loop
running = True
while running:
    # Background + Color
    screen.fill((50, 70, 150))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if projectile_state == "ready":
                    projectileX = playerX
                    fire_projectile(projectileX, projectileY)
                    projectile_sound = mixer.Sound("laser.wav")
                    projectile_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Checking for boundaries of enemy + movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], projectileX, projectileY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            #projectileY = 480
            #projectile_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 100)

        enemy(enemyX[i], enemyY[i], i)

    # Projectile movement
    if projectileY <= 0:
        projectileY = 480
        projectile_state = "ready"

    if projectile_state == "fire":
        fire_projectile(projectileX, projectileY)
        projectileY -= projectileY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
