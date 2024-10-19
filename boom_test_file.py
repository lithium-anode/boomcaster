import pygame
import math
import timeit

wall_texture_path = 'wall.png'
floor_texture_path = 'floor.png'
sky_texture_path = 'sky.png'

world = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

walls = {}

for l, row in enumerate(world):
    for n, value in enumerate(row):
        if value:
            walls[(n, l)] = value


doomguy_pos = 1.5, 5
doomguy_vector = 0
doomguy_speed = 2
doomguy_sens = 2
fov = math.pi / 3
scale = 1600 // 600

code_without_cache = """
def lighting(screen, doomguy_pos, doomguy_vector):
    ox, oy = doomguy_pos
    x_map, y_map = int(ox), int(oy)

    main_vector = doomguy_vector - (math.pi / 3) / 2 + 0.1
    for ray in range(800):
        sin_a = math.sin(main_vector)
        cos_a = math.cos(main_vector)

        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(20):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor in walls:
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(20):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert in walls:
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        if depth_vert < depth_hor:
            depth = depth_vert
        else:
            depth = depth_hor

        depth *= math.cos(doomguy_vector - main_vector)

        proj_height = 800 / math.tan((math.pi / 3) / 2) / (depth + 0.0001)

        color = [255 / (1 + depth ** 5 * 0.00002)] * 3
        pygame.draw.rect(screen, color, (ray * scale, 540 - proj_height // 2, scale, proj_height))

        main_vector += (math.pi / 3) / 800
"""

code_with_cache = """
def cached_sin(angle):
    if angle not in sin_cache_dict:
        sin_cache_dict[angle] = math.sin(angle)
    return sin_cache_dict[angle]

def cached_cos(angle):
    if angle not in cos_cache_dict:
        cos_cache_dict[angle] = math.cos(angle)
    return cos_cache_dict[angle]

def cached_tan(angle):
    if angle not in tan_cache_dict:
        tan_cache_dict[angle] = math.tan(angle)
    return tan_cache_dict[angle]

def lighting(screen, doomguy_pos, doomguy_vector):
    ox, oy = doomguy_pos
    x_map, y_map = int(ox), int(oy)

    main_vector = doomguy_vector - (math.pi / 3) / 2 + 0.1
    for ray in range(800):
        sin_a = cached_sin(main_vector)
        cos_a = cached_cos(main_vector)

        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(20):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor in walls:
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(20):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert in walls:
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        if depth_vert < depth_hor:
            depth = depth_vert
        else:
            depth = depth_hor

        depth *= cached_cos(doomguy_vector - main_vector)

        proj_height = 800 / cached_tan((math.pi / 3) / 2) / (depth + 0.0001)

        color = [255 / (1 + depth ** 5 * 0.00002)] * 3
        pygame.draw.rect(screen, color, (ray * scale, 540 - proj_height // 2, scale, proj_height))

        main_vector += (math.pi / 3) / 800
"""


# performance before cache implementation
print("performance before cache implementation:\n")
print(timeit.timeit(stmt=code_without_cache, number=1))
# performance after cache implementation
print("\nperformance after cache implementation:\n")
print(timeit.timeit(stmt=code_with_cache, number=1))