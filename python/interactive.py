import pygame
import pygame.gfxdraw
import sys

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
ORANGE = (255, 165, 0, 80)  # Transparent orange (alpha = 80/255)
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

# Draw sidebar UI
def draw_sidebar(r):
    pygame.draw.rect(screen, GREY, (DRAW_AREA_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT))

    # Radius label
    label = font.render(f"Radius: {int(r)}", True, BLACK)
    screen.blit(label, (DRAW_AREA_WIDTH + 30, 40))

    # Slider track
    pygame.draw.rect(screen, DARK_GREY, (slider_x, slider_top, slider_width, slider_height))

    # Slider knob
    knob_y = slider_bottom - (r / 100) * slider_height
    knob_y = max(slider_top, min(knob_y, slider_bottom - slider_knob_height))
    pygame.draw.rect(screen, BLACK, (slider_x - 5, knob_y, slider_width + 10, slider_knob_height))

def draw_points():
    radius_int = int(r)
    for x, y in points:
        if r > 0:
            # Create translucent orange ball surface
            surface_size = radius_int * 2 + 4
            ball_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
            center = radius_int + 2

            # Filled translucent orange circle on separate surface
            pygame.gfxdraw.filled_circle(ball_surface, center, center, radius_int, ORANGE)

            # Blit to main screen
            screen.blit(ball_surface, (x - center, y - center))

            # Now draw black anti-aliased outline directly on screen
            pygame.gfxdraw.aacircle(screen, x, y, radius_int, BLACK)

        # Black center dot (3 px)
        pygame.gfxdraw.filled_circle(screen, x, y, 3, BLACK)
        pygame.gfxdraw.aacircle(screen, x, y, 3, BLACK)

# Main loop
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

            # Slider interaction
            if mouse_x >= DRAW_AREA_WIDTH:
                knob_y = slider_bottom - (r / 100) * slider_height
                knob_y = max(slider_top, min(knob_y, slider_bottom - slider_knob_height))
                if slider_x - 5 <= mouse_x <= slider_x + slider_width + 5 and knob_y <= mouse_y <= knob_y + slider_knob_height:
                    dragging_slider = True

            # Drawing area
            elif mouse_x < DRAW_AREA_WIDTH:
                for point in points:
                    px, py = point
                    if (mouse_x - px)**2 + (mouse_y - py)**2 <= max(r, 5)**2:
                        dragging_point = point
                        break

                if dragging_point is None:
                    points.append((mouse_x, mouse_y))

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_point = None
            dragging_slider = False

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if dragging_point:
                idx = points.index(dragging_point)
                new_x = min(DRAW_AREA_WIDTH - 1, max(0, mouse_x))
                new_y = min(SCREEN_HEIGHT - 1, max(0, mouse_y))
                points[idx] = (new_x, new_y)
                dragging_point = points[idx]

            elif dragging_slider:
                mouse_y = max(slider_top, min(slider_bottom, mouse_y))
                slider_pos = slider_bottom - mouse_y
                r = (slider_pos / slider_height) * 100
                r = max(0, min(r, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

