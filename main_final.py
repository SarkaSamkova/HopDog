import pygame
import random

pygame.init()

# --------------------- SETTINGS ------------------------
# screen
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hop Dog")

# settings
fps = 60
clock = pygame.time.Clock()

GROUND_VELOCITY = 3
BACKGROUND_VELOCITY = 1
CAT_VELOCITY = 10

# IMAGES

# ground
ground_height = HEIGHT * (3 / 4)
ground_im = pygame.image.load("images/gr.PNG")
ground_im_rect = ground_im.get_rect()
ground_im_rect.x = 0
ground_im_rect.y = ground_height
GROUND_WIDTH = 1200

ground2_im = ground_im.copy()
ground2 = ground_im_rect.copy()
ground2_first_width = GROUND_WIDTH
ground2.x = ground2_first_width

# background
background = pygame.image.load("images/background.PNG")
background_rect = background.get_rect()
background_rect.x, background_rect.y = 0, 0
BG_WIDTH = 1000

bg2 = background.copy()
bg2_rect = background_rect.copy()
bg2_rect.x = BG_WIDTH

# dogs
dog1 = pygame.image.load("images/dog1.PNG")
dog2 = pygame.image.load("images/dog2.png")
dog_jump = pygame.image.load("images/dog3.png")
dead_dog = pygame.image.load("images/dead_dog.PNG")

dog_rect = dog1.get_rect()
DOG_Y = ground_height - 155
dog_rect.x, dog_rect.y = 100, DOG_Y
DOWN_DOG = DOG_Y + 50

# cats
cat = pygame.image.load("images/cat1.png")
cats = pygame.image.load("images/cats.PNG")
supercat = pygame.image.load("images/cat2.PNG")

cat_rect = cat.get_rect()
CAT_Y = ground_height - 70
cat_rect.x, cat_rect.y = WIDTH - 20, CAT_Y

barriers = [cat, cats, supercat]

# ---------------- FUNCTIONS ---------------------

# walking
i = 1


def animation():
    global dog1, dog_rect, dog2, i
    # přidání obrázku
    if i <= 10:
        screen.blit(dog1, dog_rect)

    elif i > 10:
        screen.blit(dog2, dog_rect)
        if i == 20:
            i = 0
    i += 1

# score


points = 0
maximum = 0
font = pygame.font.Font('freesansbold.ttf', 20)


def score():
    global points, maximum, max_points, maxRect
    points += 0.2

    text = font.render(f"Score: {int(points)}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (60, 50)
    screen.blit(text, text_rect)

    if points >= maximum:
        maximum = points
    max_points = font.render(f"Record: {int(maximum)}", True, (0, 0, 0))
    maxRect = max_points.get_rect()
    maxRect.center = (700, 50)
    screen.blit(max_points, maxRect)


# jumping AND down
jumping = False
jump_height = 25
y_velocity = jump_height
y_gravity = 1


def jump():
    global jumping, jump_height, y_velocity, y_gravity

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        jumping = True
    if jumping:
        dog_rect.y -= y_velocity
        y_velocity -= y_gravity
        if y_velocity < -jump_height:
            jumping = False
            y_velocity = jump_height
            dog_rect.y = DOG_Y


downing = False
NUM = 50
num = NUM


def down():
    global downing, num
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        downing = True
        dog_rect.y = DOWN_DOG
    if downing:
        num -= 1
    if num < 0:
        downing = False
        num = NUM
        dog_rect.y = DOG_Y


# barriers motion
bar_mov = True
bar = random.choice(barriers)
acceleration = CAT_VELOCITY


def barriers_motion():
    global bar_mov, cat_rect, bar

    if bar_mov:
        cat_rect.x -= acceleration
        if cat_rect.x < -100:
            cat_rect.x = WIDTH - 20
            bar = random.choice(barriers)

        score()
    # changing pictures - y
    if bar == cats:
        cat_rect.y = CAT_Y - 50
    elif bar == supercat:
        cat_rect.y = CAT_Y - 150
    elif bar == cat:
        cat_rect.y = CAT_Y

    screen.blit(bar, cat_rect)


# collision
def collision():
    global bar_mov
    if dog_rect.colliderect(cat_rect):
        bar_mov = False


# restart
def restart():
    global bar_mov, points, cat_rect
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cat_rect.x = WIDTH - 20
        points = 0
        bar_mov = True


# moving ground
def ground_move():
    ground_im_rect.x -= GROUND_VELOCITY
    screen.blit(ground_im, ground_im_rect)
    ground2.x -= GROUND_VELOCITY
    screen.blit(ground2_im, ground2)
    if ground2.x == 0:
        ground_im_rect.x = ground2_first_width
    if ground_im_rect.x == 0:
        ground2.x = ground2_first_width


# moving background
def background_move():
    background_rect.x -= BACKGROUND_VELOCITY
    screen.blit(background, background_rect)

    bg2_rect.x -= BACKGROUND_VELOCITY
    screen.blit(bg2, bg2_rect)

    if bg2_rect.x == 0:
        background_rect.x = BG_WIDTH
    if background_rect.x == 0:
        bg2_rect.x = BG_WIDTH


# ------------------------ MAIN CYCLE ----------------------------
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if bar_mov:
        jump()
        down()

        collision()
        background_move()
        ground_move()
        barriers_motion()

        # drawings objects
        if jumping or downing:
            screen.blit(dog_jump, dog_rect)
        if downing:
            jumping = False
            jump_height = 25
            y_velocity = jump_height
            jump()
        if jumping:
            downing = False
            num = NUM

        if not jumping:
            if not downing:
                animation()

    elif not bar_mov:
        screen.blit(background, background_rect)
        screen.blit(bg2, bg2_rect)
        screen.blit(ground_im, ground_im_rect)
        screen.blit(ground2_im, ground2)
        screen.blit(bar, cat_rect)

        text_score = font.render(f"Score: {int(points)}", True, (0, 0, 0))
        textRect = text_score.get_rect()
        textRect.center = (60, 50)
        screen.blit(text_score, textRect)

        max_points = font.render(f"Record: {int(maximum)}", True, (0, 0, 0))
        maxRect = max_points.get_rect()
        maxRect.center = (700, 50)
        screen.blit(max_points, maxRect)

        dog_rect.y = DOG_Y
        screen.blit(dead_dog, dog_rect)
        jumping = False
        jump_height = 25
        y_velocity = jump_height
        downing = False
        num = NUM
        acceleration = CAT_VELOCITY
        restart()

    acceleration += 0.01
    # GROUND_VELOCITY += 0.01
    # BACKGROUND_VELOCITY += 0.01

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
