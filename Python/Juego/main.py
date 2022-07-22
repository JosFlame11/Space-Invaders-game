import pygame, os, serial, time
pygame.init()

# Arduino
arduino = serial.Serial("/dev/cu.usbmodem14201", 9600)

# Dimensions
WIDTH = 400
HEIGHT = 400
#Window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
GREEN_BULLETS = (42, 250, 0)
RED_BULLETS = (250, 0, 0)

# Frames per second
FPS = 60
VEL = 2

#Sprites (images)

#Draw things in the window
def Draw(xwing, malos):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, RED_BULLETS, xwing)
    pygame.draw.rect(WIN, GREEN_BULLETS, malos)

def malos_movemnt(malos):
    malos.x += 5
    if malos.x >= WIDTH:
        malos.y += 5
        malos.x = 0

def movement(keys_pressed, xwing):
    if keys_pressed == "'1'":
            xwing.y -= VEL
    if keys_pressed == "'2'":
            xwing.y += VEL
    if keys_pressed == "'3'":
            xwing.x -= VEL
    if keys_pressed == "'4'":
            xwing.x += VEL
def main():
    xwing = pygame.Rect(WIDTH//2 -10, HEIGHT - 10, 10, 10)
    malos = pygame.Rect(0, 0, 20, 5)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = str(arduino.readline().strip()).strip('b')
        print(keys_pressed)
        movement(keys_pressed, xwing)
        malos_movemnt(malos)
        Draw(xwing, malos)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()