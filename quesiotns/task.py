import random

# ---------------- DATA ----------------
quiz = [
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "answer": 3
    },
    {
        "question": "How many legs does an octopus have?",
        "options": ["6", "8", "10", "12"],
        "answer": 2
    },
    {
        "question": "What is the main ingredient in hummus?",
        "options": ["Chickpeas", "Lentils", "Black beans", "Peanuts"],
        "answer": 1
    },
    {
        "question": "Which country is known as the Land of the Rising Sun?",
        "options": ["China", "South Korea", "Japan", "Thailand"],
        "answer": 3
    },
    {
        "question": "What is the hardest natural substance on Earth?",
        "options": ["Gold", "Iron", "Diamond", "Granite"],
        "answer": 3
    },
    {
        "question": "Which fruit has seeds on the outside?",
        "options": ["Apple", "Strawberry", "Banana", "Grape"],
        "answer": 2
    },
    {
        "question": "Who painted the Sistine Chapel roof?",
        "options": ["Leonardo da Vinci", "Picasso", "Michelangelo", "Van Gogh"],
        "answer": 3
    },
    {
        "question": "What is the only even prime number?",
        "options": ["0", "2", "4", "6"],
        "answer": 2
    },
    {
        "question": "What is the capital of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
        "answer": 3
    },
    {
        "question": "Which animal has a very long neck?",
        "options": ["Elephant", "Giraffe", "Kangaroo", "Camel"],
        "answer": 2
    }
]


# ---------------- ENGINE ----------------
def run_quiz():
    user_answers = []

    for q in quiz:
        print("\n" + q["question"])

        for i, option in enumerate(q["options"], start=1):
            print(f"{i}) {option}")

        while True:
            try:
                answer = int(input("Your answer (1-4): "))
                if 1 <= answer <= 4:
                    break
                else:
                    print("Enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Enter a number.")

        user_answers.append(answer)

    return user_answers


# ---------------- EVALUATION ----------------
def calculate_score (user_answers):
    score = 0

    for i in range(len(quiz)):
        if user_answers[i] == quiz[i]["answer"]:
            score += 1

    return score


# ---------------- MAIN ----------------
def main():
    answers = run_quiz()
    score = calculate_score(answers)

    print("\n===================")
    print(f"Your score: {score}/{len(quiz)}")
    print("===================")

main()

