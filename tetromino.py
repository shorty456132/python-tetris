class Tetromino:
    """Tetris piece with shape, position, and rotation logic"""

    SHAPES = {
        'I': [['.....',
               '..#..',
               '..#..',
               '..#..',
               '..#..'],
               ['.....',
                '.....',
                '####.',
                '.....',
                '.....'
                ]
            ],
        'O': [['.....',
               '.....',
               '.##..',
               '.##..',
               '.....']],
        'L': [[
                '.....',
                '.....',
                '..#..',
                '..#..',
                '..##.'],
              [
                '.....',
                '.....',
                '.###.',
                '.#...',
                '.....'
              ],
              [
                '.....',
                '.....',
                '.##..',
                '..#..',
                '..#..'
              ],
              [
                '.....',
                '.....',
                '...#.',
                '.###.',
                '.....'
              ]
            ],
        'V': [
                [
                    '.....',
                    '.....',
                    '...#.',
                    '...#.',
                    '..##.'
                ],
                [
                    '.....',
                    '.....',
                    '.#...',
                    '.###.',
                    '.....'
                ],
                [
                    '.....',
                    '.....',
                    '..##.',
                    '..#..',
                    '..#..'
                ],
                [
                    '.....',
                    '.....',
                    '.###.',
                    '...#.',
                    '.....'
                ],
            ],
        'Z': [
            [
                '.....',
                '.....',
                '.##..',
                '..##.',
                '.....'
            ],
            [
                '.....',
                '...#.',
                '..##.',
                '..#..',
                '.....'
            ]
        ],
        'N': [
            [
                '.....',
                '..#..',
                '..##.',
                '...#.',
                '.....'
            ],
            [
                '.....',
                '.....',
                '..##.',
                '.##..',
                '.....'
            ],
        ],
        'Tee': [
            [
                '.....',
                '.....',
                '..#..',
                '.###.',
                '.....'
            ],
            [
                '.....',
                '..#..',
                '..##.',
                '..#..',
                '.....'
            ],
            [
                '.....',
                '.....',
                '.###.',
                '..#..',
                '.....'
            ],
            [
                '.....',
                '..#..',
                '.##..',
                '..#..',
                '.....'
            ],
        ]
    }

    def __init__(self, shape, color):
        self.shape = shape  #2D list representing the pieces
        self.color = color  # Color from our COLORS dict
        self.x = 3          # Starting X position
        self.y = 0          # Starting Y position
        self.rotation = 0   # Current rotating state
    

    def is_valid_position(self, grid, dx=0, dy=0):
        """Check if piece would be in valid position with given offset"""
        shape = self.SHAPES[self.shape][self.rotation]

        for row, line in enumerate(shape):
            for col, cell in enumerate(line):
                if cell == '#':
                    new_x = self.x + col + dx
                    new_y = self.y + row + dy

                    # Chained comparison
                    if not (0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid)):
                        return False
                    
                    # Check if grid cell is occupied (non-zero)
                    if grid[new_y][new_x] != 0:
                        return False   
                      
        return True

    def move(self, dx, dy, grid):
        """Move piece by dx, dy offset if position is valid"""
        if self.is_valid_position(grid, dx, dy):
            self.x += dx
            self.y += dy
            # print(f"Moved to {self.x}, {self.y}")
            return True 
        
        return False

    def rotate(self, grid):
        """Rotatae piece clockwise"""
        #TODO: for now we'll just sycle through rotations
        old_rotation = self.rotation
        max_rotations = len(self.SHAPES[self.shape])
        self.rotation = (self.rotation + 1) % max_rotations

        #if new rotation is not valid, revert
        if not self.is_valid_position(grid, 0,0):
            self.rotation = old_rotation
            return False
        return True
