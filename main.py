import pygame, sys
import math
import random
pi = math.pi

planets = {}
count = 0

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Orbit Visualizer")
done = False
width = screen.get_width()
height = screen.get_height()
fps = pygame.time.Clock()
counter = 0
centre = (width//2,height//2)
show_axes = False

lines = []

def from_centre(x,y):
    return (centre[0]+x,centre[1]-y)

def render():
    global angle,x,y,a, omega, count, planets, show_axes
    screen.fill((0, 0, 0))
    for planet in planets.values():
        planet["angle"] = planet["angle"] + planet["omega"]
        planet["x"] = planet["a"] * math.cos(planet["angle"]) # New x
        planet["y"] = planet["a"] * math.sin(planet["angle"]) # New y
        pygame.draw.circle(
            screen,
            (5, 255, 230),
            center=from_centre(planet["x"],planet["y"]),
            radius=5,
            width=25
        )
        pygame.draw.circle(
            screen,
            (0, 79, 71),
            center=centre,
            radius=planet["a"],
            width=1
        )

    if count > 1:
        for i in range(1,count):
            pygame.draw.line(
                screen,
                (255, 255, 255),
                from_centre(planets[f"{i}"]["x"], planets[f"{i}"]["y"]),
                from_centre(planets[f"{i+1}"]["x"], planets[f"{i+1}"]["y"])
            )

        for k in range(1,count):
            if counter%6==0:
                lines.append((from_centre(planets[f"{k}"]["x"], planets[f"{k}"]["y"]),
                            from_centre(planets[f"{int(k)+1}"]["x"], planets[f"{int(k)+1}"]["y"])))
        for j in lines:
            pygame.draw.line(
                screen,
                (255,255,255),
                j[0],j[1]
            )

    if show_axes == True:
        pygame.draw.line(
            screen,
            (0,255,0),
            (0, height//2),
            (width, height//2)
        )
        pygame.draw.line(
            screen,
            (0,255,0),
            (width//2, 0),
            (width//2, height)
        )
    pygame.draw.circle(
        screen,
        (253, 184, 19),
        center=centre,
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
        center=centre,
        radius=math.sqrt((centre[0]-pygame.mouse.get_pos()[0])**2 + (centre[1]-pygame.mouse.get_pos()[1])**2),
        width=1
    )
    font = pygame.font.SysFont("monospace", 15)
    radius_display = font.render(f"Radius: {round(math.sqrt((centre[0]-pygame.mouse.get_pos()[0])**2 + (centre[1]-pygame.mouse.get_pos()[1])**2))}", 1, (255,255,255))
    mouse_pos = pygame.mouse.get_pos()
    ang = math.atan2(
        centre[1]-mouse_pos[1], mouse_pos[0]-centre[0]
    )
    angledisplay = font.render(f"Angle: {math.degrees(ang)}", 1, (255,255,255))
    screen.blit(radius_display, pygame.mouse.get_pos())
    screen.blit(angledisplay, (mouse_pos[0], mouse_pos[1]+20))
    pygame.display.update()
    fps.tick(60)


while not done:
    counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_e]:
            done = True
        elif pygame.key.get_pressed()[pygame.K_s]:
            pygame.image.save(screen, f"{counter}.jpeg")
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            count += 1
            rad = math.sqrt((centre[0]-mouse_pos[0])**2 + (centre[1]-mouse_pos[1])**2)
            ang_vel = math.sqrt(1/rad**3)*60
            ang = math.atan2(
                centre[1]-mouse_pos[1], mouse_pos[0]-centre[0]
            )
            planets[str(count)] = {
                "a":rad,
                "angle":ang,
                "omega":ang_vel,
                "x":pygame.mouse.get_pos()[0],
                "y":pygame.mouse.get_pos()[1],
            }
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            show_axes = True
        else:
            show_axes = False
    if not done:
        render()

pygame.quit()
sys.exit()
