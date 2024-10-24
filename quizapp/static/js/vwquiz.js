// Assuming you have an HTML element with id "questionDisplay"
const questionDisplay = document.getElementById('questionDisplay');
const nextQuestionButton = document.getElementById('nextQuestionButton'); // Assuming you have a button for next question

let currentQuestionIndex = 0; // Keep track of the current question

function showNextQuestion(questions) {
    if (currentQuestionIndex < questions.length) {
        questionDisplay.innerText = questions[currentQuestionIndex].question;
        currentQuestionIndex++;
    } else {
        questionDisplay.innerText = "Congratulations! You've completed the quiz.";
        nextQuestionButton.style.display = 'none'; // Hide the button when all questions are done
    }
}

// Assuming you have fetched your questions and stored them in an array called "questions"
fetch(`/api/get-quiz/?gfg=${this.gfg}`)
    .then(response => response.json())
    .then(result => {
        const questions = result.data; // Assuming the data structure contains an array of questions
        showNextQuestion(questions); // Show the first question
    });

// Assuming you have an event listener for the "Next Question" button
nextQuestionButton.addEventListener('click', () => {
    showNextQuestion(questions);
});