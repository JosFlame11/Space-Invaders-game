import pygame, os, serial, time, random
pygame.init()
pygame.font.init() #For the font available in your computer

# Arduino
#arduino = serial.Serial("/dev/cu.usbmodem14201", 9600)

# Dimensions
WIDTH = 500
HEIGHT = 375
XWING_W, XWING_H = 50, 40
DEATHSTAR_W, DEATHSTAR_H = 150, 150

#Window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STAR WARS - SPACE INVADERS")

# Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 15)
WINNER_FONT = pygame.font.SysFont('comicsans', 50)

# Colors
WHITE = (255, 255, 255)
GREEN_BULLETS = (42, 250, 0)
RED_BULLETS = (250, 0, 0)
YELLOW = (247, 229, 89)
RED_TEXT = (117, 0, 22)

# Frames per second
FPS = 40
VEL = 4
B_G_VEL = 10
BULLET_VEL = 5
LASER_VEL = 10

# Events
HIT = pygame.USEREVENT + 1
GET_HIT = pygame.USEREVENT + 2
MAX_BULLETS = 5
MAX_LASER = 1
DEATH_STAR_LIVES = 20

#Sprites (images)
XWING_MODEL = pygame.image.load(os.path.join('Space-Invaders-game-master', 'Space-Invaders-game', 'StarWars_Images', 'xwing_model.png'))
XWING = pygame.transform.scale(XWING_MODEL, (XWING_W, XWING_H))
DEATH_STAR_MODEL = pygame.image.load(os.path.join('Space-Invaders-game-master', 'Space-Invaders-game', 'StarWars_Images', 'death_star_fullhealt.png'))
DEATH_STAR_FH = pygame.transform.scale(DEATH_STAR_MODEL, (DEATHSTAR_W, DEATHSTAR_H))
DEATH_STAR_HIT = pygame.transform.scale(pygame.image.load(os.path.join('Space-Invaders-game-master', 'Space-Invaders-game', 'StarWars_Images', 'death_star_hit_2.png')), (DEATHSTAR_W, DEATHSTAR_H))
DEATH_STAR_HIT_2 = pygame.transform.scale(pygame.image.load(os.path.join('Space-Invaders-game-master', 'Space-Invaders-game', 'StarWars_Images', 'death_star_hit.png')), (DEATHSTAR_W, DEATHSTAR_H))
DEATH_STAR_HIT_3 = pygame.transform.scale(pygame.image.load(os.path.join('Space-Invaders-game-master', 'Space-Invaders-game', 'StarWars_Images', 'death_star_hit_3.png')), (DEATHSTAR_W, DEATHSTAR_H))

#Draw things in the window
def Draw(xwing, death_star,  bullets, death_rays, death_laser, player_health, death_star_health):
    WIN.blit(pygame.image.load(os.path.join('Space-Invaders-game-master','Space-Invaders-game','StarWars_Images','background.jpeg')), (0,0))
    WIN.blit(XWING, (xwing.x, xwing.y))

    for laser in death_laser:
        pygame.draw.rect(WIN, GREEN_BULLETS, laser, border_radius = 5)
    
    if death_star_health < 10:
        WIN.blit(DEATH_STAR_HIT_3, (death_star.x, death_star.y))
    else:
        WIN.blit(DEATH_STAR_FH, (death_star.x, death_star.y))

    lives = HEALTH_FONT.render("LIVES: " + str(player_health), 1, YELLOW)
    WIN.blit(lives, (10, HEIGHT - lives.get_width() - 2))
    pygame.draw.rect(WIN, RED_BULLETS, pygame.Rect(10, 10, death_star_health*10, 10), border_radius = 3)

    for bullet in bullets:
        pygame.draw.rect(WIN, RED_BULLETS, bullet, border_radius = 2)
    for ray in death_rays:
        pygame.draw.rect(WIN, GREEN_BULLETS, ray, border_radius = 2)

def malos_movemnt(death_star):
    pos = random.randint(0, WIDTH)
    if pos < death_star.x:
        death_star.x -= B_G_VEL
    if pos > death_star.x:
        death_star.x += B_G_VEL

def bullet_fire(bullets, xwing, death_star, death_rays, death_laser):
    for bullet in bullets:
        bullet.y -= BULLET_VEL
        if death_star.colliderect(bullet):
            bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(HIT))
        elif bullet.y < 0:
            bullets.remove(bullet)
    for ray in death_rays:
        ray.y += BULLET_VEL
        if xwing.colliderect(ray):
            pygame.event.post(pygame.event.Event(GET_HIT))
            death_rays.remove(ray)
        elif ray.y > HEIGHT:
            death_rays.remove(ray)
    for laser in death_laser:
        laser.y += LASER_VEL
        if xwing.colliderect(laser):
            pygame.event.post(pygame.event.Event(GET_HIT))
            death_laser.remove(laser)
        elif laser.y > HEIGHT:
            death_laser.remove(laser)
    
            
def movement(keys_pressed, xwing):
    if keys_pressed[pygame.K_UP] :# == "'1'": #UP
            xwing.y -= VEL
    if keys_pressed[pygame.K_DOWN]: #== "'2'": #DOWN
            xwing.y += VEL
    if keys_pressed[pygame.K_LEFT]: #== "'3'": #LEFT
            xwing.x -= VEL
    if keys_pressed[pygame.K_RIGHT]: #== "'4'": #RIGHT
            xwing.x += VEL

def who_won(winner):
    winner_text = WINNER_FONT.render(winner, 1, RED_TEXT)
    WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2 ))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    xwing = pygame.Rect(WIDTH//2 - XWING_W//2, HEIGHT - XWING_H, XWING_W, XWING_H)
    death_star = pygame.Rect(WIDTH//2 - DEATHSTAR_W//2, 0, DEATHSTAR_H, DEATHSTAR_W)
    bullets = []
    death_rays = []
    death_laser = []
    player_health = 5
    death_star_health = DEATH_STAR_LIVES

    clock = pygame.time.Clock()
    run = True
    while run:
        RAY_CHANCE = random.randint(0, 50) # Odds for the death star to shoot us
        MOVE_CHANCE = random.randint(0, 5)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(xwing.x + xwing.width//2 - 1, xwing.y, 2, 7)
                    bullets.append(bullet)
            if event.type == HIT:
                death_star_health -= 1
            if event.type == GET_HIT:
                player_health -= 1
        winner = ""
        if death_star_health <= 0:
            winner = "FOR THE REPUBLIC!"
        if player_health <= 0:
            winner = "EMPIRE WINS!"
        if winner != "":
            who_won(winner)
            break

        # shows the number of getting a ray
        #print(RAY_CHANCE)
        if RAY_CHANCE == 9:# A bullet from the death star
            ray = pygame.Rect(death_star.x + death_star.width//2 - 2, death_star.bottom, 4, 10)
            death_rays.append(ray)
        elif RAY_CHANCE == 50 and len(death_laser) < MAX_LASER: # A LASER from the death star
            laser = pygame.Rect(death_star.x + death_star.width//2 - 15, death_star.top + DEATHSTAR_H//2, 30, HEIGHT - death_star.bottom)
            death_laser.append(laser)
        keys_pressed = pygame.key.get_pressed()#str(arduino.readline().strip()).strip('b')
        #print(keys_pressed)            #Register which number does the arduino reads

        #print(bullets)
        movement(keys_pressed, xwing)
        # Change malos, make either more spaceships or just a boss
        if MOVE_CHANCE == 1 or MOVE_CHANCE == 3:
            malos_movemnt(death_star)
        bullet_fire(bullets, xwing, death_star, death_rays, death_laser)
        Draw(xwing, death_star,bullets, death_rays, death_laser, player_health, death_star_health)

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()

    