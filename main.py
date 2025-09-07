import sys
from tetris_game import TetrisGame

def main():
    """Initialize and run the Tetris game"""
    try:
        game = TetrisGame()

        # Show high scores before starting
        print("Welcome to python learing Tetris!")
        game.high_score_manager.display_high_scores()
        print("Use arrow keys to play. Good luck!\n")
        
        game.run()
    except KeyboardInterrupt:
        print("\nGame interiupted by user")
    except Exception as e:
        print(f"Error running game: {e}")
    finally: 
        sys.exit()

if __name__ == "__main__":
    main()