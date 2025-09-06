import json
import os
from datetime import datetime
from constants import HIGH_SCORES_FILE, MAX_HIGH_SCORES

class HighScoreManager:
    """Manages loading, saving, and updating high scores"""

    def __init__(self):
        self.high_scores = []
        self.load_high_scores()

    def load_high_scores(self):
        """Load high scores from file, create empty list if file doesnt exist"""
        try:
            if os.path.exists(HIGH_SCORES_FILE):
                with open(HIGH_SCORES_FILE, 'r') as file:
                    self.high_scores = json.load(file)
                print(f"Loaded {len(self.high_scores)} high scores")
            else:
                print("No high scores file found, starting fresh...")
                self.high_scores = []
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading high scores: {e}")
            self.high_scores = []
    
    def save_high_score(self): 
        """Save high scores to file"""
        try:
            with open(HIGH_SCORES_FILE, 'w') as file:
                json.dump(self.high_scores, file, indent=2)
            print("High scores saved successfully")
        except IOError as e:
            print(f"Error saving high score: {e}")

    def add_score(self, score, lines_cleared):
        """Add new score if it qualifies for high score list"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_entry = {
            "score": score,
            "lines": lines_cleared,
            "date": timestamp
        }

        # Add to list and sort by score (highest first)
        self.high_scores.append(new_entry)
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)

        # Keep only top scores
        self.high_scores = self.high_scores[:MAX_HIGH_SCORES]

        # Save immediately
        self.save_high_score()

        # Return True if this score made it to the list
        return new_entry in self.high_scores
    
    def is_high_score(self, score):
        """Check if score qualifies as a high score"""
        if len(self.high_scores) < MAX_HIGH_SCORES:
            return True
        return score > self.high_scores[-1]["score"]
    
    def get_high_scores(self):
        """Returns list of high scores"""
        return self.high_scores.copy()
    
    def display_high_scores(self):
        """Prints high scores to console"""
        if not self.high_scores:
            print("No high scores yet")
            return
        
        print("\n" + "="*50)
        print("HIGH SCORES".center(50))
        print("="*50)

        for i, entry in enumerate(self.high_scores, 1):
            print(f"{i:<6}{entry['score']:<10}{entry['lines']:<8}{entry['date']}")
        print("="*50 + "\n")