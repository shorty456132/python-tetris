import json
import os

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 780
GRID_SIZE = 30

COLORS = {
    'GRAY':  (100, 100, 100),
    'WHITE':  (255,255,255),
    'RED':    (255, 0, 0),
    'GREEN':  (0, 255, 0),
    'BLUE':   (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'PURPLE': (128, 0, 128),
    'ORANGE': (255, 165, 0), 
    'BLACK':  (0, 0, 0)
}

# Game Settings
FALL_SPEED = 500 # Milliseconds
FPS = 60

# Scoring
LINE_SCORES = {0: 0, 1: 100, 2: 300, 3: 500, 4: 800}

HIGH_SCORES_FILE = "tetris_highscores.json"
MAX_HIGH_SCORES = 10