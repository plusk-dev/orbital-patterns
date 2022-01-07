import pygame
import math
import random
from coordinates import Matrix
pi = math.pi

angle = math.radians(45)

planets = {}
count = 0

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
matrix = Matrix(screen)
pygame.display.set_caption("Orbit Visualizer")
done = False
width = screen.get_width()
height = screen.get_height()
fps = pygame.time.Clock()
counter = 0

lines = []

def render():
    global angle,x,y,a, omega, count, planets
    screen.fill((0, 0, 0))
    for planet in planets.values():
        planet["angle"] = planet["angle"] + planet["omega"]
        planet["x"] = planet["a"] * math.cos(planet["angle"] + pi / 2) # New x
        planet["y"] = planet["a"] * math.sin(planet["angle"] + pi / 2) # New y
        pygame.draw.circle(
            screen,
            (5, 255, 230),
            center=matrix.coords(planet["x"],planet["y"]),
            radius=5,
            width=25
        )
        pygame.draw.circle(
            screen,
            (0, 79, 71),
            center=matrix.coords(0,0),
            radius=planet["a"],
            width=1
        )

    if count > 1:
        for i in range(1,count):
            print(list(planets.keys()))
            pygame.draw.line(
                screen,
                (255, 255, 255),
                matrix.coords(planets[f"{i}"]["x"], planets[f"{i}"]["y"]),
                matrix.coords(planets[f"{i+1}"]["x"], planets[f"{i+1}"]["y"])
            )

        for k in range(1,count):
            if counter%6==0:
                lines.append((matrix.coords(planets[f"{k}"]["x"], planets[f"{k}"]["y"]),
                            matrix.coords(planets[f"{int(k)+1}"]["x"], planets[f"{int(k)+1}"]["y"])))
        for j in lines:
            pygame.draw.line(
                screen,
                (255,255,255),
                j[0],j[1]
            )


    pygame.draw.circle(
        screen,
        (253, 184, 19),
        center=matrix.coords(0,0),
        radius=25,
        width=65
    )
    pygame.draw.circle(
        screen,
        (5, 255, 230),
        center=pygame.mouse.get_pos(),
        radius=5,
        width=25
    )
    pygame.draw.circle(
        screen,
        (0, 79, 71),
        center=matrix.coords(0,0),
        radius=math.sqrt((matrix.origin[0]-pygame.mouse.get_pos()[0])**2 + (matrix.origin[1]-pygame.mouse.get_pos()[1])**2),
        width=1
    )
    font = pygame.font.SysFont("monospace", 15)
    radius_display = font.render(f"Radius: {round(math.sqrt((matrix.origin[0]-pygame.mouse.get_pos()[0])**2 + (matrix.origin[1]-pygame.mouse.get_pos()[1])**2))}", 1, (255,255,255))
    # slope = (pygame.mouse.get_pos()[1]-matrix.origin[1]/pygame.mouse.get_pos()[0]-matrix.origin[0])
    screen.blit(radius_display, pygame.mouse.get_pos())
    pygame.display.update()
    fps.tick(60)


while not done:
    counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_e]:
            done = True
        elif pygame.key.get_pressed()[pygame.K_s]:
            print("key press")
            pygame.image.save(screen, f"{counter}.jpeg")
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            count += 1
            rad = math.sqrt((matrix.origin[0]-pygame.mouse.get_pos()[0])**2 + (matrix.origin[1]-pygame.mouse.get_pos()[1])**2)
            ang_vel = math.sqrt(1/rad**3)*60
            planets[str(count)] = {
                "a":rad,
                "angle":45,
                "omega":ang_vel,
                "x":pygame.mouse.get_pos()[0],
                "y":pygame.mouse.get_pos()[1],
            }
    if not done:
        render()
