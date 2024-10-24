import json
import requests
import time
import random

# Meta AI API endpoint
api_endpoint = "(link unavailable)"

# API parameters
params = {
    "model": "question-generation",
    "topic": "Psychology",
    "num_questions": 20
}

def generate_questions(topic, num_questions, num_repeats):
    questions_and_answers = []
    
    for repeat in range(num_repeats):
        print(f"\nGenerating questions for repeat {repeat+1} of {num_repeats}\n")
        
        params["topic"] = topic
        params["num_questions"] = num_questions
        
        start_time = time.time()
        response = requests.get(api_endpoint, params=params)
        end_time = time.time()
        
        if response.status_code == 200:
            qa_pairs = response.json()["questions"]
            questions_and_answers.extend(qa_pairs)
            print(f"Generated {len(qa_pairs)} questions in {end_time-start_time:.2f} seconds")
        else:
            print(f"Error {response.status_code}: {response.text}")
    
    return questions_and_answers

def save_to_json(questions_and_answers, filename):
    with open(filename, "w") as file:
        json.dump(questions_and_answers, file, indent=4)

def main():
    topic = "Psychology"
    num_questions = 20
    num_repeats = 2  # Change to desired number of repeats
    filename = "psychology_qa.json"
    
    questions_and_answers = generate_questions(topic, num_questions, num_repeats)
    save_to_json(questions_and_answers, filename)
    print(f"Saved {len(questions_and_answers)} questions to {filename}")

if __name__ == "__main__":
    main()