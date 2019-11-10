import pygame
import pygame.freetype
import random
import copy

class Block:
  def __init__(self, shape, color, x, y, rotation):
    self.shape = shape
    self.color = color
    self.x = x
    self.y = y
    self.rotation = rotation

I_shape = [["    ",
            "OOOO",
            "    ",
            "    "],

           ["  O ",
            "  O ",
            "  O ",
            "  O "]]

J_shape = [["   ",
            "OOO",
            "  O"],

           [" O ",
            " O ",
            "OO "],

            ["   ",
             "O  ",
             "OOO"],

            [" OO",
             " O ",
             " O "]]

L_shape = [["   ",
            "OOO",
            "O  "],

           ["OO ",
            " O ",
            " O "],
     
           ["   ",
            "  O",
            "OOO"],
     
           [" O ",
            " O ",
            " OO"]]

O_shape = [["OO",
            "OO"]]

S_shape = [["   ",
            " OO",
            "OO "],

           ["O  ",
            "OO ",
            " O "]]

T_shape = [["   ",
            "OOO",
            " O "],

           [" O ",
            "OO ",
            " O "],
     
           ["   ",
            " O ",
            "OOO"],
     
           [" O ",
            " OO",
            " O "]]

Z_shape = [["   ",
            "OO ",
            " OO"],

           ["  O",
            " OO",
            " O "]]

colors = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)]
blocks = [
  Block(I_shape, colors[0], 3, 0, 0),
  Block(J_shape, colors[1], 3, 0, 0),
  Block(L_shape, colors[2], 3, 0, 0),
  Block(O_shape, colors[3], 4, 0, 0),
  Block(S_shape, colors[4], 3, 0, 0),
  Block(T_shape, colors[5], 3, 0, 0),
  Block(Z_shape, colors[6], 3, 0, 0),
]

def get_next_block():
  return copy.deepcopy(random.choice(blocks))

def is_in_valid_x_location(block, grid):
  for i, shape_row in enumerate(block.shape[block.rotation]):
    for j, spot in enumerate(shape_row):
      if spot == "O":
        abs_pos = block.x + j
        if abs_pos < 0 or abs_pos > len(grid[0]) - 1 or grid[block.y + i][block.x + j] != (0, 0, 0):
          return False
  return True

def is_in_valid_y_location(block, grid):
  for i, shape_row in enumerate(block.shape[block.rotation]):
    for j, spot in enumerate(shape_row):
      if spot == "O":
        abs_pos = block.y + i
        if abs_pos > len(grid) - 1 or grid[block.y + i][block.x + j] != (0, 0, 0):
          return False
  return True

def main():
  pygame.init()
  pygame.display.set_caption("Tetris")

  block_size = 36
  row_length = 10
  col_length = 20
  margin = 300
  fall_interval = 500

  grid_color = (60, 60, 60)

  grid = [[(0, 0, 0) for i in range(0, row_length)] for j in range(0, col_length)]

  screen = pygame.display.set_mode((block_size * row_length + 2 * margin, block_size * col_length + 2))

  block = get_next_block()
  next_block = get_next_block()

  clock = pygame.time.Clock()
  time_since_last_fall = 0

  was_in_invalid_y_location = False
  score = 0

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          block.x -= 1
          if not is_in_valid_x_location(block, grid):
            block.x += 1
        if event.key == pygame.K_RIGHT:
          block.x += 1
          if not is_in_valid_x_location(block, grid):
            block.x -= 1
        if event.key == pygame.K_UP:
          block.rotation = (block.rotation + 1) % len(block.shape)
          while not is_in_valid_x_location(block, grid):
            if block.x < row_length / 2:
              block.x += 1;
            else:
              block.x -= 1;
        if event.key == pygame.K_DOWN:
          if was_in_invalid_y_location:
            for i, shape_row in enumerate(block.shape[block.rotation]):
              for j, spot in enumerate(shape_row):
                if spot == "O":
                  grid[block.y + i][block.x + j] = block.color
            new_grid = []
            for i, grid_row in enumerate(grid):
              empty_spot_count = 0
              for j, spot in enumerate(grid_row):
                if spot == (0, 0, 0):
                  empty_spot_count += 1
              if empty_spot_count != 0:
                new_grid.append(grid_row)
              else:
                score += 1
            while len(new_grid) < col_length:
              new_grid.insert(0, [(0, 0, 0) for _ in range(row_length)])
            grid = new_grid
            block = next_block
            next_block = get_next_block()

          block.y += 1
          if not is_in_valid_y_location(block, grid):
            block.y -= 1
            was_in_invalid_y_location = True
          else:
            was_in_invalid_y_location = False

          time_since_last_fall = 0

    time_since_last_fall += clock.tick()

    if time_since_last_fall >= fall_interval:
      if was_in_invalid_y_location:
        for i, shape_row in enumerate(block.shape[block.rotation]):
          for j, spot in enumerate(shape_row):
            if spot == "O":
              grid[block.y + i][block.x + j] = block.color
        new_grid = []
        for i, grid_row in enumerate(grid):
          empty_spot_count = 0
          for j, spot in enumerate(grid_row):
            if spot == (0, 0, 0):
              empty_spot_count += 1
          if empty_spot_count != 0:
            new_grid.append(grid_row)
          else:
            score += 1
        while len(new_grid) < col_length:
          new_grid.insert(0, [(0, 0, 0) for _ in range(row_length)])
        grid = new_grid
        block = next_block
        next_block = get_next_block()

      block.y += 1
      if not is_in_valid_y_location(block, grid):
        block.y -= 1
        was_in_invalid_y_location = True
      else:
        was_in_invalid_y_location = False

      time_since_last_fall = 0

    # background
    screen.fill((0, 0, 0))

    # score
    font = pygame.freetype.SysFont("SFUI", 36)
    font.render_to(screen, (margin / 2, block_size * col_length / 2), str(score), (255, 255, 255))

    # colors
    for i, _ in enumerate(grid):
      for j, color in enumerate(grid[i]):
        pygame.draw.rect(screen, color, (margin + j * block_size, i * block_size, block_size, block_size))

    # current block
    for i, shape_row in enumerate(block.shape[block.rotation]):
      for j, spot in enumerate(shape_row):
        if spot == "O":
          pygame.draw.rect(screen, block.color, ((block.x + j) * block_size + margin, (block.y + i) * block_size, block_size, block_size))

    # next block
    for i, shape_row in enumerate(next_block.shape[next_block.rotation]):
      for j, spot in enumerate(shape_row):
        if spot == "O":
          pygame.draw.rect(screen, next_block.color, (row_length * block_size + margin * 1.4 + j * block_size, col_length * block_size / 2 + i * block_size, block_size, block_size))

    # grid
    for i in range(col_length):
      pygame.draw.line(screen, grid_color, (margin, i * block_size), (margin + row_length * block_size, i * block_size), 1)
    for i in range(row_length):
      pygame.draw.line(screen, grid_color, (margin + i * block_size, 0), (margin + i * block_size, col_length * block_size), 1)

    # grid border
    pygame.draw.rect(screen, grid_color, (margin, 0, block_size * row_length, block_size * col_length), 2)

    pygame.display.flip()

if __name__ == "__main__":
  main()
