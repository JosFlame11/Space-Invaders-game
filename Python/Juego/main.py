import pygame, os, serial, time
pygame.init()

# Arduino
#arduino = serial.Serial("/dev/cu.usbmodem14201", 9600)

# Dimensions
WIDTH = 400
HEIGHT = 400
MALOS_W, MALOS_H = 20, 5
#Window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STAR WARS - SPACE INVADERS")

# Colors
WHITE = (255, 255, 255)
GREEN_BULLETS = (42, 250, 0)
RED_BULLETS = (250, 0, 0)

# Frames per second
FPS = 60
VEL = 2
BULLET_VEL = 5
# Events
HIT = pygame.USEREVENT + 1
#Sprites (images)

#Draw things in the window
def Draw(xwing, malos, bullets):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, RED_BULLETS, xwing)
    pygame.draw.rect(WIN, GREEN_BULLETS, malos[1])
    for bullet in bullets:
        pygame.draw.rect(WIN, RED_BULLETS, bullet)

def malos_movemnt(malos):
    for malo in malos: 
        malo.x += 5
        if malo.x >= WIDTH:
            malo.y += 5
            malo.x = 0

def bullet_fire(bullets, xwing):
    for bullet in bullets:
        bullet.y -= BULLET_VEL
        if bullet.y < 0:
            bullets.remove(bullet)

def movement(keys_pressed, xwing):
    if keys_pressed[pygame.K_UP] :# == "'1'": #UP
            xwing.y -= VEL
    if keys_pressed[pygame.K_DOWN]: #== "'2'": #DOWN
            xwing.y += VEL
    if keys_pressed[pygame.K_LEFT]: #== "'3'": #LEFT
            xwing.x -= VEL
    if keys_pressed[pygame.K_RIGHT]: #== "'4'": #RIGHT
            xwing.x += VEL
def main():
    xwing = pygame.Rect(WIDTH//2 -10, HEIGHT - 10, 10, 10)
    malos = []
    bullets = []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(xwing.x + xwing.width//2 - 1, xwing.y, 2, 7)
                    bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()#str(arduino.readline().strip()).strip('b')
        #print(keys_pressed)            #Register which number does the arduino reads

        print(bullets)
        movement(keys_pressed, xwing)
        for i in range(5):
            malo = pygame.Rect(0, 0, MALOS_W, MALOS_H)
            malos.append(malo)
        malos_movemnt(malos)
        bullet_fire(bullets, xwing)
        Draw(xwing, malos, bullets)

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()