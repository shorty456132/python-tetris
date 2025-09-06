import pygame
import sys
import random
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, COLORS, FALL_SPEED, LINE_SCORES
from tetromino import Tetromino 



class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python learning tetris")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fall_time = 0
        self.fall_speed = 500 # Milliseconds

        # Grid dimensions
        self.grid_width = WINDOW_WIDTH // GRID_SIZE #round down to the lowest int
        self.grid_height = WINDOW_HEIGHT // GRID_SIZE

        # Create empty grid - lists because we'll modify it
        self.grid = [[0 for _ in range(self.grid_width)]
                     for _ in range(self.grid_height)]

        self.current_piece = Tetromino("L", COLORS['BLUE'])

        self.score = 0
        self.lines_cleared_total = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    self.current_piece.move(-1, 0, self.grid)
                elif event.key == pygame.K_RIGHT:
                    self.current_piece.move(1, 0, self.grid)
                elif event.key == pygame.K_DOWN:
                    self.current_piece.move(0, 1, self.grid)
                elif event.key == pygame.K_UP:
                    self.current_piece.rotate(self.grid)

    def update(self):
        # Auto fall timing
        current_time = pygame.time.get_ticks()
        if current_time - self.fall_time > self.fall_speed:
            if not self.current_piece.move(0, 1, self.grid): # Move piece down
                print("Piece Landed")
                self.lock_piece()
                
                # Clear any full lines and update score
                lines_cleared = self.clear_lines()
                if lines_cleared > 0:
                    self.update_score(lines_cleared)
                    print(f"Cleared {lines_cleared} lines! Score: {self.score}")
                
                # Create new piece
                self.current_piece = self.create_new_piece()

                if not self.current_piece.is_valid_position(self.grid, 0, 0):
                    # print("GAME OVER!")
                    self.running = False
            self.fall_time = current_time
        
    def draw(self):
        self.screen.fill(COLORS['BLACK'])

        # Draw locked pieces from grid
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] != 0:
                    x = col * GRID_SIZE
                    y = row * GRID_SIZE
                    pygame.draw.rect(self.screen, self.grid[row][col],
                                     (x, y, GRID_SIZE, GRID_SIZE))
        # Draw grid lines
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, COLORS['WHITE'],
                            (x, 0), (x, WINDOW_HEIGHT))
        
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, COLORS['WHITE'],
                            (0, y), (WINDOW_WIDTH, y))
            
        # Draw current falling piece
        self.draw_piece(self.current_piece)

        pygame.display.flip()

    def update_score(self, lines_cleared):
        """Update score based on lines cleared simultaneously"""
        # Classic tetris scoring - more lines at once = higher score
        line_scores = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}
        self.score += line_scores.get(lines_cleared, 0)
        self.lines_cleared_total += lines_cleared

    def create_new_piece(self):
        """Create a new random piece"""
        shapes = list(self.current_piece.SHAPES.keys()) # ['I', 'O', 'L']
        random_shape = random.choice(shapes)

        # ** replaced by line below
        # colors = [COLORS['RED'], COLORS['GREEN'], COLORS['BLUE'],
        #           COLORS['YELLOW'], COLORS['PURPLE'], COLORS['ORANGE']]
        valid_colors = [color for color in COLORS.values() if color != COLORS['BLACK']]
        random_color = random.choice(valid_colors)

        return Tetromino(random_shape, random_color)

    def draw_piece(self, piece):
        shape = piece.SHAPES[piece.shape][piece.rotation]
        for row, line in enumerate(shape):
            for col, cell in enumerate(line):
                if cell == '#':
                    x = (piece.x + col) * GRID_SIZE
                    y = (piece.y + row) * GRID_SIZE
                    pygame.draw.rect(self.screen, piece.color, 
                                     (x, y, GRID_SIZE, GRID_SIZE))

    def is_line_full(self, row):
        """Check if a grid row is completely filled"""
        filled_cells = 0
        for cell in self.grid[row]:
            if cell != 0:  # Non-zero means filled
                filled_cells += 1

        is_full = filled_cells == len(self.grid[row])
        print(f"Row {row}: {filled_cells}/{len(self.grid[row])} filled, Full: {is_full}")  # Debug
        return is_full

    def clear_lines(self):
        """Remove full lines and drop remaining lines down"""
        lines_cleared = 0

        print("Checking for full lines...") # Debug

        full_lines_found = True
        while full_lines_found:
            full_lines_found = False

            # Critical: Iterate backwards to avoid index problems when deleting
            for row in range(len(self.grid) - 1, -1, -1): # Bottom to top
                if self.is_line_full(row):
                    # Remove the full line
                    del self.grid[row]

                    # Add new empty line at top
                    empty_line = [0 for _ in range(len(self.grid[0]))]
                    self.grid.insert(0, empty_line)

                    lines_cleared += 1
                    full_lines_found = True # use this a flag to check again
                    break #start over from the bottom
        
        print(f"Total lines cleared this time: {lines_cleared}") # Debug
        return lines_cleared 

    def lock_piece(self):
        """Lock current piece into the grid"""
        shape = self.current_piece.SHAPES[self.current_piece.shape][self.current_piece.rotation]
        
        for row, line in enumerate(shape):
            for col, cell in enumerate(line):
                if cell == '#':
                    grid_x = self.current_piece.x + col
                    grid_y = self.current_piece.y + row

                    # Store color value in grid (non-zero means occupied)
                    self.grid[grid_y][grid_x] = self.current_piece.color
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60) # 60 FPS

        pygame.quit()
        sys.exit()

# if __name__ == "__main__":
#     game = TetrisGame() # Instanciate the TetrisGame class
#     game.run() # Run the game loop