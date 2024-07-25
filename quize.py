import random

# Define the questions and answers
questions = [
    {
        "question": "What is the capital of France?",
        "choices": ["A. London", "B. Paris", "C. Rome", "D. Berlin"],
        "answer": "B"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "choices": ["A. Earth", "B. Mars", "C. Jupiter", "D. Saturn"],
        "answer": "B"
    },
    {
        "question": "Who wrote 'To Kill a Mockingbird'?",
        "choices": ["A. Harper Lee", "B. Mark Twain", "C. J.K. Rowling", "D. Ernest Hemingway"],
        "answer": "A"
    },
    {
        "question": "What is the largest ocean on Earth?",
        "choices": ["A. Atlantic Ocean", "B. Indian Ocean", "C. Arctic Ocean", "D. Pacific Ocean"],
        "answer": "D"
    },
    {
        "question": "What is the hardest natural substance on Earth?",
        "choices": ["A. Gold", "B. Iron", "C. Diamond", "D. Silver"],
        "answer": "C"
    },
    {
        "question": "What is the capital of Japan?",
        "choices": ["A. Beijing", "B. Seoul", "C. Tokyo", "D. Bangkok"],
        "answer": "C"
    },
    {
        "question": "Who developed the theory of relativity?",
        "choices": ["A. Isaac Newton", "B. Nikola Tesla", "C. Albert Einstein", "D. Galileo Galilei"],
        "answer": "C"
    },
    {
        "question": "What is the smallest prime number?",
        "choices": ["A. 1", "B. 2", "C. 3", "D. 5"],
        "answer": "B"
    },
    {
        "question": "What is the chemical symbol for water?",
        "choices": ["A. O2", "B. H2O", "C. CO2", "D. H2"],
        "answer": "B"
    },
    {
        "question": "What is the tallest mountain in the world?",
        "choices": ["A. K2", "B. Kangchenjunga", "C. Mount Everest", "D. Lhotse"],
        "answer": "C"
    }
]

# Function to ask questions
def ask_question(question):
    print("\n" + question["question"])
    for choice in question["choices"]:
        print(choice)
    while True:
        answer = input("Enter your answer (A, B, C, or D): ").upper()
        if answer in ["A", "B", "C", "D"]:
            return answer == question["answer"]
        else:
            print("Invalid input. Please enter A, B, C, or D.")

# Function to display the score
def display_score(score, total):
    print(f"\nYour final score is {score} out of {total}")
    percentage = (score / total) * 100
    print(f"That's {percentage:.2f}% correct!")

# Main function to run the quiz game
def quiz_game():
    print("Welcome to the Quiz Game!")
    random.shuffle(questions)  # Shuffle the questions for each game
    score = 0

    for question in questions:
        if ask_question(question):
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was {question['answer']}.")

    display_score(score, len(questions))

if _name_ == "_main_":
    quiz_game()
