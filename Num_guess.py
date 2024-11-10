import random
import time
import json
from datetime import datetime

def get_difficulty():
    """Allow user to select a difficulty level, which adjusts the range and max attempts."""
    print("Select difficulty level:")
    print("1. Easy (Range: 1-10, Unlimited guesses)")
    print("2. Medium (Range: 1-50, 10 guesses)")
    print("3. Hard (Range: 1-100, 7 guesses)")
    print("4. Expert (Range: 1-500, 5 guesses)")

    while True:
        choice = input("Enter difficulty level (1-4): ")
        if choice in ['1', '2', '3', '4']:
            choice = int(choice)
            if choice == 1:
                return 10, None
            elif choice == 2:
                return 50, 10
            elif choice == 3:
                return 100, 7
            elif choice == 4:
                return 500, 5
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def provide_feedback(guess, number):
    """Provide feedback based on proximity to the correct answer."""
    difference = abs(guess - number)
    if difference == 0:
        return "Correct!"
    elif difference <= 3:
        return "Very close!"
    elif difference <= 10:
        return "Close!"
    elif difference <= 20:
        return "Far!"
    else:
        return "Very far!"

def play_game():
    """Main game function where the user guesses the number."""
    print("Welcome to the Enhanced Number Guessing Game!")
    time.sleep(1)

    range_limit, max_attempts = get_difficulty()
    random_number = random.randint(1, range_limit)
    guesses = 0
    score = 100

    print(f"\nI've selected a number between 1 and {range_limit}. Try to guess it!")

    while True:
        guesses += 1
        if max_attempts and guesses > max_attempts:
            print("Out of guesses! Better luck next time!")
            return 0

        user_guess = input(f"Attempt {guesses}/{max_attempts if max_attempts else '∞'} - Enter your guess: ")

        if user_guess.isdigit():
            user_guess = int(user_guess)
        else:
            print("Please enter a valid number.")
            continue

        feedback = provide_feedback(user_guess, random_number)
        print(feedback)

        if user_guess == random_number:
            print(f"\nCongratulations! You guessed the number {random_number} correctly in {guesses} attempts.")
            return max(1, score - (guesses * (100 // range_limit)))

        # Adjust score for each incorrect guess
        score -= 5
        if user_guess > random_number:
            print("Your guess is too high!")
        else:
            print("Your guess is too low!")

def save_game_history(score, difficulty_level):
    """Save game history with date, difficulty, and score to a file."""
    game_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "difficulty": difficulty_level,
        "score": score
    }

    try:
        with open("game_history.json", "r") as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []

    history.append(game_data)

    with open("game_history.json", "w") as file:
        json.dump(history, file, indent=4)

def main():
    """Main function to run the game and manage rounds."""
    while True:
        score = play_game()
        
        if score > 0:
            print(f"\nYour final score: {score}")
            difficulty = ["Easy", "Medium", "Hard", "Expert"]
            difficulty_level = difficulty[get_difficulty()[1] - 1]
            save_game_history(score, difficulty_level)

        play_again = input("\nDo you want to play again? (yes/no): ")
        if play_again.lower() != 'yes':
            break
    print("\nThanks for playing the Enhanced Number Guessing Game! Check 'game_history.json' for your scores.")

if __name__ == "__main__":
    main()
