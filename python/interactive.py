import pygame
import pygame.gfxdraw
import sys

from filtrations import *

def run_window(filtration):
    # Initialize pygame
    pygame.init()

    # Screen dimensions — higher resolution
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
    DRAW_AREA_WIDTH = 1000  # Leave sidebar
    SIDEBAR_WIDTH = SCREEN_WIDTH - DRAW_AREA_WIDTH

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Interactive Points with Smooth Radius Control")

    # Colors
    BLACK = (0, 0, 0)
    ORANGE = (255, 165, 0, 80)  # Transparent orange
    WHITE = (255, 255, 255)
    GREY = (220, 220, 220)
    DARK_GREY = (120, 120, 120)

    # Font
    font = pygame.font.SysFont(None, 28)

    # Parameters
    r = 50  # radius
    points = []

    # Slider config
    slider_x = DRAW_AREA_WIDTH + SIDEBAR_WIDTH // 2 - 5
    slider_width = 10
    slider_height = 300
    slider_top = 100
    slider_bottom = slider_top + slider_height
    slider_knob_height = 12

    # State
    dragging_point = None
    dragging_slider = False
    click_start = 0

    # Draw sidebar UI
    def draw_sidebar(r):
        pygame.draw.rect(screen, GREY, (DRAW_AREA_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))
        label = font.render(f"Radius: {int(r)}", True, BLACK)
        screen.blit(label, (DRAW_AREA_WIDTH + 30, 40))
        pygame.draw.rect(screen, DARK_GREY, (slider_x, slider_top, slider_width, slider_height))
        knob_y = slider_bottom - (r / 100) * slider_height
        knob_y = max(slider_top, min(knob_y, slider_bottom - slider_knob_height))
        pygame.draw.rect(screen, BLACK, (slider_x - 5, knob_y, slider_width + 10, slider_knob_height))

    # Draw points
    def draw_points():
        radius_int = int(r)
        

        simplices = filtration(points, r)
        print(f"SIMPLICES: {simplices}")
        print(f"POINTS: {points}")

        for dim, simpl in reversed(list(enumerate(simplices))):
            match dim:
                case 0:
                    pass
                case 1:
                    for s in simpl:
                        pygame.draw.aaline(screen, BLACK, s[0], s[1])

                case _:
                    for s in simpl:
                        pygame.draw.polygon(screen, (64, 224, 208, 1), s)




        # # Draw triangles between every set of three points
        # if len(points) >= 3:
        #     for i in range(len(points) - 2):
        #         p1, p2, p3 = points[i], points[i + 1], points[i + 2]
        #         pygame.draw.polygon(screen, (64, 224, 208, 1), [p1, p2, p3])
        #
        # # Draw lines between points
        # if len(points) >= 2:
        #     for i in range(len(points) - 1):
        #         pygame.draw.aaline(screen, BLACK, points[i], points[i + 1])

        # Draw circles
        for x, y in points:
            if r > 0:
                surface_size = radius_int * 2 + 4
                ball_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
                center = radius_int + 2
                pygame.gfxdraw.filled_circle(ball_surface, center, center, radius_int, ORANGE)
                screen.blit(ball_surface, (x - center, y - center))
                pygame.gfxdraw.aacircle(screen, x, y, radius_int, BLACK)
            pygame.gfxdraw.filled_circle(screen, x, y, 3, BLACK)
            pygame.gfxdraw.aacircle(screen, x, y, 3, BLACK)

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(WHITE)
        draw_sidebar(r)
        draw_points()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if clicking slider knob area
                if slider_x - 5 <= mouse_x <= slider_x + slider_width + 5 and slider_top <= mouse_y <= slider_bottom:
                    dragging_slider = True
                else:
                    for point in points[:]:
                        px, py = point
                        if (mouse_x - px)**2 + (mouse_y - py)**2 <= max(r, 5)**2:
                            dragging_point = point
                            click_start = pygame.time.get_ticks()
                            break
                    else:
                        if mouse_x < DRAW_AREA_WIDTH:
                            points.append((mouse_x, mouse_y))

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_point:
                    click_duration = pygame.time.get_ticks() - click_start
                    if click_duration < 200:  # Click (not drag)
                        points.remove(dragging_point)
                    dragging_point = None
                dragging_slider = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging_slider:
                    mouse_y = pygame.mouse.get_pos()[1]
                    # Clamp mouse_y within slider bounds
                    mouse_y = max(slider_top, min(mouse_y, slider_bottom))
                    # Update radius based on slider position
                    r = 100 * (slider_bottom - mouse_y) / slider_height
                elif dragging_point:
                    idx = points.index(dragging_point)
                    points[idx] = pygame.mouse.get_pos()
                    dragging_point = points[idx]

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

run_window(vr_filtration)
