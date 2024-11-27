		
        const app = Vue.createApp({
        delimiters: ['[[', ']]'],
        data() {
          return {	
	        subject: subjectData.subject_name,
            test_mode: test_mode,
	        num_questions: subjectData.test_numberofquestions,
			apply_fuzzylogic: subjectData.apply_fuzzylogic,
			
			save_userresponse: true,
			
			feedback: '',
            session_id : "", // session gets value from get_questions view
            currentQuestionIndex: 0, // Index to track the current question
            markedQuestions: [], // Array to track marked questions

            questions: [], // Array to hold fetched questions
			userResponses: {}, // Object to store user responses
			userisCorrect: {},
            selectedAnswers: {}, // Object to track selected answers
            selectedAnswer: {}, // Object to track selected answer
            quizEnded: false, // Flag to indicate if the quiz has ended
            timer: null, // Timer reference
            timeLeft:0,  
            results: { // To store results after the quiz ends
                totalQuestions: 0,   
                correctAnswers: 0,
                incorrectAnswers: 0,
				unattemptedAnswers: 0,
				overallScore: 0, 
				reportData: [],
            }         
          };
        },

        computed: {
          minutes() {
            return Math.floor(this.timeLeft / 60);
          },
          seconds() {
            return this.timeLeft % 60;
          },
		  
		  formattedAnswers() {
			return this.results.reportData.map(question => {
				return {
					...question,
					joinedAnswers: question.selected_answers ? question.selected_answers.join(', ') : ''
				};
				});
			},
			
			
        },
		
        methods: {
    
			// Function to get CSRF token from cookies
			getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
					for (let i = 0; i < cookies.length; i++) {
						const cookie = cookies[i].trim();
						// Does this cookie string begin with the name we want?
						if (cookie.substring(0, name.length + 1) === (name + '=')) {
							cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
						break;
					}
				}
            }
            return cookieValue;
            },   // end getCookie         
 		         
		// Fetch questions from the API
		getQuestions() {
			fetch(`/api/get-quiz/?subject=${this.subject}&test_mode=${this.test_mode}`)
				.then(response => response.json())
			.then(result => {
			//console.log(result); // Debugging line
			if (result.data && result.data.length > 0) {
				this.questions = result.data;
				this.results.totalQuestions=result.data.length;
				this.session_id = result.session_id;
			} else {
				this.displayErrorMessage("No questions found.");
				this.questions = []; // Ensure questions is an empty array
				// Optional: Redirect or exit
			}
			})
				.catch(error => {
			console.error("Error fetching questions:", error);
		// Optional: Display an error message to the user
			});
		},

		// Display error message function
			displayErrorMessage(message) {
			document.getElementById("error-message").innerHTML = message;
			// Optional: Redirect or exit after delay
			setTimeout(() => {
			// window.location.href = '/error'; // Redirect
			// or
			//  window.close(); // Exit
			}, 3000); // 3-second delay
		},
		
 		
		selectAnswer(event, uid, questionType) {
			// Assuming event.target.value contains the user's selected answer
			// and questionType indicates the type of question (e.g., 'input', 'radio', 'checkbox')
			// Initialize user response if it doesn't exist
			if (questionType === 'RB' || questionType === 'CB') {
				if (!this.userResponses[uid]) {
					this.userResponses[uid] = questionType === 'CB' ? [] : '';
				}
			}

			if (questionType === 'IN' || questionType === 'RB') {
				// For user input (text or numeric), store the value directly
				this.selectedAnswer[uid] = event.target.value;
				this.userResponses[uid] = event.target.value;
				// Clear selectedAnswers for this question since it's single-choice
				this.selectedAnswers[uid] = [];			
			} else if (questionType === 'CB') {
				// For checkbox questions (multiple-choice), store the selected options as an array
				// Assuming this.selectedAnswers is an object (dictionary) with uid as keys
				if (!this.selectedAnswers[uid]) {
					this.selectedAnswers[uid] = []; // Initialize if not already set
				}
				
				const answerIndex = this.userResponses[uid].indexOf(event.target.value);
				if (answerIndex === -1) {
					this.userResponses[uid].push(event.target.value);
					this.selectedAnswers[uid].push(event.target.value);

				} else {
					this.userResponses[uid].splice(answerIndex, 1);
					this.selectedAnswers[uid].splice(answerIndex, 1);
				}

				// this.selectedAnswers[uid].push(event.target.value);
				this.selectedAnswer[uid] = " "
			}
		},
 
 
		// Fetch user response for a question
		getUserResponse(uid) {
			return this.userResponses[uid];
		},
          
		  
checksaveAnswer(uid) {
    const session_id = this.session_id;
  
    let isCorrect = false;
    const question = this.questions.find(q => q.uid === uid);
    const questionType = question.question_type;
    const selectedAnswer = questionType === 'IN' || questionType === 'RB'
        ? this.selectedAnswer[uid]
        : this.selectedAnswers[uid];

    const data = {
        session_id,
        question_id: uid,
        selected_answers: this.selectedAnswers[uid],
        selected_answer: this.selectedAnswer[uid],
        is_correct: isCorrect,
        test_mode: this.test_mode,
        apply_fuzzylogic: this.apply_fuzzylogic,
    };
  
    //console.log('Calling storeuserresponse with data :', data);

    return fetch('/storeuserresponse/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const isAnswer = data.is_answer;
        const correctResponse = data.correct_response;
        const explanation = data.explanation;

        this.userisCorrect[uid] = isAnswer;
		if (isAnswer) {
			this.results.correctAnswers++;
		} else {
			this.results.incorrectAnswers++;
		}
        return {
            isAnswer: isAnswer,
            correctResponse: correctResponse,
            explanation: explanation
        };
    })
    .catch(error => console.error('Error:', error));
},
		  
		  
		  
		  
  checksaveAnswerold(uid) {

  const session_id = this.session_id;
  
  let isCorrect = false;
  const question = this.questions.find(q => q.uid === uid);
  const questionType = question.question_type;
  const selectedAnswer = questionType === 'IN' || questionType === 'RB'
    ? this.selectedAnswer[uid]
    : this.selectedAnswers[uid];

  const data = {
    session_id,
    question_id: uid,
    selected_answers: this.selectedAnswers[uid],
    selected_answer: this.selectedAnswer[uid],
    is_correct: isCorrect,
    test_mode: this.test_mode,
    apply_fuzzylogic: this.apply_fuzzylogic,
  };
  
   //console.log('Calling storeuserresponse with data :', data);

    return fetch('/storeuserresponse/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCookie('csrftoken')
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => ({
      isAnswer: data.is_answer,
      correctResponse: data.correct_response,
      explanation: data.explanation,
    }))
    .catch(error => console.error('Error:', error));
},

		clearFeedback() {
			// document.getElementById('feedback').innerText = '';
			this.feedback = '';
		},
		
        nextQuestion() {
 			this.checksaveAnswer(this.questions[this.currentQuestionIndex].uid);
			this.clearFeedback();


            if (this.currentQuestionIndex < this.questions.length - 1) {
				this.currentQuestionIndex++;
            }
          },
          // Navigate to the previous question
        prevQuestion() {
 			this.checksaveAnswer(this.questions[this.currentQuestionIndex].uid);
			this.clearFeedback();


            if (this.currentQuestionIndex > 0) {
				this.currentQuestionIndex--;
 
            }
          },
          // Mark the current question for review
        markForReview() {
            if (!this.markedQuestions.includes(this.currentQuestionIndex)) {
              this.markedQuestions.push(this.currentQuestionIndex);
            }
          },
          // Check if a question is marked for review
          isMarked(index) {
            return this.markedQuestions.includes(index);
          },
          // Jump to a specific question
        gotoQuestion() {
			this.checksaveAnswer(this.questions[this.currentQuestionIndex].uid);
			
            const questionNumber = prompt("Enter question number:");
            const index = parseInt(questionNumber) - 1;
            if (index >= 0 && index < this.questions.length) {
              this.currentQuestionIndex = index;

            } else {
              alert("Invalid question number");
            }
          },
		  
		checkResponse() {
			this.checksaveAnswer(this.questions[this.currentQuestionIndex].uid)
			.then(response => {
				//console.log(response.isAnswer, response.correctResponse, response.explanation);
			if (this.test_mode == "P") {
				if (response.isAnswer == true) {
					this.feedback = 'Correct!';
				} else {
					let message = `Incorrect!\nThe correct answer is: ${response.correctResponse}\n${response.explanation || ''}`;
					this.feedback = message;
				}
				// console.log('Feedback:', this.feedback);
			}
		});
		},
		  
		  // Confirm exit
		confirmExit() {
			this.checksaveAnswer(this.questions[this.currentQuestionIndex].uid);
			if (confirm("Are you sure you want to exit?")) {
				this.endQuiz();
				if (this.test_mode === "T") {
					const url = `/update_quiz_session/${this.session_id}/`;
					fetch(url, {
					method: 'POST',
					headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': this.getCookie('csrftoken'), 
					},
			
					})
					.then(response => response.json())
					.then(data => {})
					.catch(error => console.error(error));
				}
				this.callGetQuizResults(); 

			}
		},

		// End the quiz and display results
		endQuiz() {
			this.quizEnded = true;
			clearInterval(this.timer);
		},
		  
	callGetQuizResults() {
  if (this.test_mode === "P") {
    //console.log('Quiz results data:', this.results);
	//console.log('Questions : ', this.questions);
	//console.log('UserResponses: ', this.userResponses); 
	//console.log('IsCorrect:', this.userisCorrect);
	fetch('/practice_report/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': this.getCookie('csrftoken')
			},
			body: JSON.stringify({
				results: this.results,
				questions: this.questions,
				userResponses: this.userResponses,
				userisCorrect: this.userisCorrect
				})
			})
	.then(response => response.json())
	.then(data => {
	 if (!data) {
        console.error('Invalid quiz results data:', data);
        alert('Error retrieving quiz results. Please try again.');
        return;
      }

      //console.log('Quiz results data:', JSON.stringify(data, null, 2));

      this.results.totalQuestions = data.total_questions;
      this.results.correctAnswers = data.correct_answers;
      this.results.incorrectAnswers = data.incorrect_answers;
	  this.results.unattemptedAnswers = data.unattempted_answers;
      this.results.overallScore = data.score;
      this.results.reportData = data.question_report;
      // console.log('Quiz results:', this.results);
      this.quizEnded = true;

      Vue.nextTick(() => {
        this.$forceUpdate();
      });
      //console.log('Ending callGetQuizResults');
    })	
	.catch(error => console.error(error));
  } else {
    // Fetch quiz results from the server
    return fetch('/session_report/' + this.session_id + '/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCookie('csrftoken')
      },
    })
    .then(response => response.json())
    .then(data => {
      if (!data) {
        console.error('Invalid quiz results data:', data);
        alert('Error retrieving quiz results. Please try again.');
        return;
      }

      //console.log('Quiz results data:', JSON.stringify(data, null, 2));

      this.results.totalQuestions = data.total_questions;
      this.results.correctAnswers = data.correct_answers;
      this.results.incorrectAnswers = data.incorrect_answers;
	  this.results.unattemptedAnswers = data.unattempted_answers;
      this.results.overallScore = data.score;
      this.results.reportData = data.question_report;
      //console.log('Quiz results:', this.results);
      this.quizEnded = true;

      Vue.nextTick(() => {
        this.$forceUpdate();
      });
      //console.log('Ending callGetQuizResults');
    })
    .catch(error => {
      console.error('Error fetching quiz results:', error);
      alert('Error retrieving quiz results. Please try again.');
      this.quizEnded = false;
    });
  }
},

 
          // Start the timer
        startTimer() {
            this.timer = setInterval(() => {
              if (this.timeLeft > 0) {
                this.timeLeft--;
              } else {
                this.endQuiz();
              }
			  
            }, 1000);
          }
        },
 
 
		async created() {
			this.duration = subjectData?.test_duration_minutes || 30;
			this.timeLeft = this.duration * 60; // Initialize timeLeft here

			await this.getQuestions();
			this.startTimer();
			// console.log('Created:', this.results);
		},
		
	

	
		mounted() {
			//console.log(subjectData);
			//console.log("subject :", this.subject, ", test_mode : ", this.test_mode);
			//console.log("duration :", this.duration, ", Number of Questions : ", this.num_questions,"Apply Fuzzy Logic :", this.apply_fuzzylogic);
			//console.log(typeof subjectData.test_duration_minutes); // Check data type
			//console.log(subjectData.test_duration_minutes); // Verify value
			// Disable browser actions
			window.addEventListener('beforeunload', function(event) {
			event.preventDefault();
		});
		history.pushState(null, null, location.href);
		window.onpopstate = function() {
			history.go(1);
		};
		document.addEventListener('contextmenu', function(event) {
		event.preventDefault();
		});
		document.addEventListener('keydown', function(event) {
		if (event.keyCode === 116) { // F5 key
		event.preventDefault();
		}
	});
},

		
      });

      app.mount('#app');
   
    