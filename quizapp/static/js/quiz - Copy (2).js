
      const app = Vue.createApp({
        delimiters: ['[[', ']]'],
        data() {
          return {
            <!-- subject: '{{subject}}', // Placeholder for quiz identifier -->
            subject: subject, // Use the subject value passed from the template
			test_mode: test_mode,
			// subject: "{{ subject }}",
            // test_mode: "{{ test_mode }}",
			feedback: '',
            questions: [], // Array to hold fetched questions
            session_id : "", // session gets value from get_questions view
            currentQuestionIndex: 0, // Index to track the current question
            markedQuestions: [], // Array to track marked questions
			userResponses: {}, // Object to store user responses

            selectedAnswers: {}, // Object to track selected answers
            selectedAnswer: {}, // Object to track selected answer
            quizEnded: false, // Flag to indicate if the quiz has ended
            timer: null, // Timer reference
            timeLeft: 1800,  // 30 minutes in seconds
            results: { // To store results after the quiz ends
                totalQuestions: 0,   
                correctAnswers: 0,
                incorrectAnswers: 0,
				overallScore: 0, 
				reportData: [],
            }         
          };
        },
		
		mounted() {
			console.log("subject :", this.subject, ", test_mode : ", this.test_mode);
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

            fetch(`/api/get-quiz/?subject=${this.subject}`)
              .then(response => response.json())
              .then(result => {
                console.log(result); // Debugging line
                this.questions = result.data;
                this.session_id = result.session_id
               
              });
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
          
          // Check the selected answer and update counters
        checksaveAnswer(uid) {
			const session_id = this.session_id;
            console.log("Session is : ", session_id); // Debugging line
 
            let iscorrect=false;
            const question = this.questions.find(q => q.uid === uid);
            console.log("Question is : ", question); // Debugging line
            console.log("Question_ID is : ", uid); // Debugging line
			const questionType=question.question_type;
            console.log("Question type is : ", questionType); // Debugging line
 			const selectedAnswer = questionType === 'IN' || questionType === 'RB'
				? this.selectedAnswer[uid]
				: this.selectedAnswers[uid];
            console.log("Selected Answer is : ", selectedAnswer); // Debugging line


            const data = {
                //uid: uid,
                //answer: event.target.value
                session_id: session_id,
                question_id: uid, 
                selected_answers: this.selectedAnswers[uid],
                selected_answer: this.selectedAnswer[uid],
                is_correct: iscorrect,
            };
			

    
			
            // Send the data to the Django view using fetch
            fetch('/storeuserresponse/', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken') // Include CSRF token for security
            },
                body: JSON.stringify(data)
                })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
				let isAnswer = data.is_answer; 
				let correctResponse = data.correct_response;
				let explanation = data.explanation
				console.log('test_mode : ', this.test_mode, 'correctResponse : ', correctResponse, 'isAnswer : ', isAnswer)
				if (this.test_mode=="P") {
					if (isAnswer==true) {
						// document.getElementById('feedback').innerText= 'Correct!';
						this.feedback = 'Correct!';
					}
				else {
						let message = `Incorrect!\nThe correct answer is: ${correctResponse}\n${explanation || ''}`;
						// document.getElementById('feedback').innerText= message;
						this.feedback = message;					
					}
					console.log('Feedback:', this.feedback);

				}

                })
            .catch((error) => {
                console.error('Error:', error);
                });  
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
			this.clearFeedback();
			
            const questionNumber = prompt("Enter question number:");
            const index = parseInt(questionNumber) - 1;
            if (index >= 0 && index < this.questions.length) {
              this.currentQuestionIndex = index;

            } else {
              alert("Invalid question number");
            }
          },
		  
		  checkResponse() {
			 this.checksaveAnswer(this.questions[this.currentQuestionIndex].uid);
 
		  },
		  
		  // Confirm exit
		confirmExit() {
			this.checksaveAnswer(this.questions[this.currentQuestionIndex].uid);
			if (confirm("Are you sure you want to exit?")) {
				this.endQuiz();
			
				const url = `/update_quiz_session/${this.session_id}/`;
				fetch(url, {
					method: 'POST',
					headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': this.getCookie('csrftoken'), 
				},
			
				})
				.then(response => response.json())
				.then(data => console.log(data))
				.catch(error => console.error(error));

				this.callGetQuizResults(); 

			}
		},

		// End the quiz and display results
		endQuiz() {
			this.quizEnded = true;
			clearInterval(this.timer);
		},
		  
	
    callGetQuizResults() {
		console.log('Starting callGetQuizResults');
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

		console.log('Quiz results data:', JSON.stringify(data, null, 2));

		this.results.totalQuestions = data.total_questions;
		this.results.correctAnswers = data.correct_answers;
		this.results.incorrectAnswers = data.incorrect_answers;
		this.results.overallScore = data.score;
		this.results.reportData = data.question_report;
		console.log('Quiz results :', this.results);
		this.quizEnded = true;
	
		Vue.nextTick(() => {
			this.$forceUpdate();
			});
	    console.log('Ending callGetQuizResults');
		})
		.catch(error => {
			console.error('Error fetching quiz results:', error);
			alert('Error retrieving quiz results. Please try again.');
			this.quizEnded = false;
		});
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
			await this.getQuestions();
			this.startTimer();
			console.log('Created:', this.results);
		},
		
      });

      app.mount('#app');
   
    