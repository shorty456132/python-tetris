import sys
from tetris_game import TetrisGame

def main():
    """Initialize and run the Tetris game"""
    try:
        game = TetrisGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interiupted by user")
    except Exception as e:
        print(f"Error running game: {e}")
    finally: 
        sys.exit()

if __name__ == "__main__":
    main()