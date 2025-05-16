import sys
import time

import pygame
import pygame.gfxdraw
from filtrations import *


def run_window(filtration=vr_filtration):
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
    DRAW_AREA_WIDTH = 1000
    SIDEBAR_WIDTH = SCREEN_WIDTH - DRAW_AREA_WIDTH

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Vietoris-Rips and Čech complexes")

    BLACK = (0, 0, 0)
    ORANGE = (255, 165, 0, 80)
    WHITE = (255, 255, 255)
    GREY = (220, 220, 220)
    DARK_GREY = (120, 120, 120)
    BLUE = (70, 130, 180)
    LIGHT_BLUE = (100, 180, 220)

    font = pygame.font.SysFont(None, 28)

    r = 50
    points = []
    active_button = None

    slider_x = DRAW_AREA_WIDTH + SIDEBAR_WIDTH // 2 - 5
    slider_width = 10
    slider_height = 300
    slider_top = 100
    slider_bottom = slider_top + slider_height
    slider_knob_height = 12

    dragging_point = None
    dragging_slider = False
    click_start = 0

    button_font = pygame.font.SysFont(None, 17)
    button_labels = [
        "Vietoris-Rips complex",
        "Čech complex",
        "Toogle showing complex",
        "Toogle showing balls",
    ]
    draw_balls = False
    draw_complex = False

    def draw_button(text, x, y, width, height, active=False):
        color = LIGHT_BLUE if active else BLUE
        pygame.draw.rect(screen, color, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 1)  # Thin black border
        label = button_font.render(text, True, WHITE)
        screen.blit(
            label,
            (
                x + (width - label.get_width()) // 2,
                y + (height - label.get_height()) // 2,
            ),
        )

    def button_clicked(mouse_pos, x, y, width, height):
        return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

    def draw_sidebar(r):
        pygame.draw.rect(
            screen, GREY, (DRAW_AREA_WIDTH, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
        )
        label = font.render(f"Radius: {int(r)}", True, BLACK)
        screen.blit(label, (DRAW_AREA_WIDTH + 30, 40))
        pygame.draw.rect(
            screen, DARK_GREY, (slider_x, slider_top, slider_width, slider_height)
        )
        knob_y = slider_bottom - (r / 100) * slider_height
        knob_y = max(slider_top, min(knob_y, slider_bottom - slider_knob_height))
        pygame.draw.rect(
            screen, BLACK, (slider_x - 5, knob_y, slider_width + 10, slider_knob_height)
        )

        button_width, button_height = 180, 40
        button_x = DRAW_AREA_WIDTH + 10
        button_y = slider_bottom + 20

        for i in range(len(button_labels)):
            draw_button(
                button_labels[i],
                button_x,
                button_y + (button_height + 10) * i,
                button_width,
                button_height,
                active_button == button_labels[i],
            )

        return [
            (
                button_labels[i],
                button_x,
                button_y + (button_height + 10) * i,
                button_width,
                button_height,
            )
            for i in range(len(button_labels))
        ]

    def draw_points():
        radius_int = int(r)
        simplices = filtration(points, r)
        if draw_complex:
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
        for x, y in points:
            if r > 0 and draw_balls:
                surface_size = radius_int * 2 + 4
                ball_surface = pygame.Surface(
                    (surface_size, surface_size), pygame.SRCALPHA
                )
                center = radius_int + 2
                pygame.gfxdraw.filled_circle(
                    ball_surface, center, center, radius_int, ORANGE
                )
                screen.blit(ball_surface, (x - center, y - center))
                pygame.gfxdraw.aacircle(screen, x, y, radius_int, BLACK)
            pygame.gfxdraw.filled_circle(screen, x, y, 3, BLACK)
            pygame.gfxdraw.aacircle(screen, x, y, 3, BLACK)


    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(WHITE)
        buttons = draw_sidebar(r)
        draw_points()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button_clicked(mouse_pos, *button[1:]):
                        active_button = button[0]
                        if active_button == button_labels[0]:
                            filtration = vr_filtration
                        elif active_button == button_labels[1]:
                            filtration = cech_filtration
                        elif active_button == button_labels[2]:
                            draw_complex = not (draw_complex)
                        elif active_button == button_labels[3]:
                            draw_balls = not (draw_balls)
                        else:
                            raise ValueError(f"Incorrect button name: {active_button}")
                        active_button = None

                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (
                    slider_x - 5 <= mouse_x <= slider_x + slider_width + 5
                    and slider_top <= mouse_y <= slider_bottom
                ):
                    dragging_slider = True
                else:
                    for point in points[:]:
                        px, py = point
                        if (mouse_x - px) ** 2 + (mouse_y - py) ** 2 <= max(r, 5) ** 2:
                            dragging_point = point
                            click_start = pygame.time.get_ticks()
                            break
                    else:
                        if mouse_x < DRAW_AREA_WIDTH:
                            points.append((mouse_x, mouse_y))
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_point:
                    click_duration = pygame.time.get_ticks() - click_start
                    if click_duration < 200:
                        points.remove(dragging_point)
                    dragging_point = None
                dragging_slider = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging_slider:
                    mouse_y = pygame.mouse.get_pos()[1]
                    mouse_y = max(slider_top, min(mouse_y, slider_bottom))
                    r = 100 * (slider_bottom - mouse_y) / slider_height
                elif dragging_point:
                    idx = points.index(dragging_point)
                    points[idx] = pygame.mouse.get_pos()
                    dragging_point = points[idx]

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
