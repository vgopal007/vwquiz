
      const app = Vue.createApp({
        delimiters: ['[[', ']]'],
        data() {
          return {
            <!-- subject: '{{subject}}', // Placeholder for quiz identifier -->
            subject: subject, // Use the subject value passed from the template
            questions: [], // Array to hold fetched questions
            session_id : "", // session gets value from get_questions view
            currentQuestionIndex: 0, // Index to track the current question
            markedQuestions: [], // Array to track marked questions
            selectedAnswers: {}, // Object to track selected answers
            correctAnswers: 0, // Counter for correct answers
            incorrectAnswers: 0, // Counter for incorrect answers
            quizEnded: false, // Flag to indicate if the quiz has ended
            timer: null, // Timer reference
            timeLeft: 1800,  // 30 minutes in seconds
            results: { // To store results after the quiz ends
                correctAnswers: 0,
                incorrectAnswers: 0,
                totalQuestions: 0   
            }         
          };
        },
        computed: {
          minutes() {
            return Math.floor(this.timeLeft / 60);
          },
          seconds() {
            return this.timeLeft % 60;
          }
        },
        methods: {
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
         
 
        //function selectAnswer(event, session_id, question_id) {
        //const selectedAnswers = [event.target.value]; // Assuming selected_answers is a list 
        
        selectAnswer(event, uid) {
            this.selectedAnswers[uid] = event.target.value;
          
        },
 
          
          
          // Check the selected answer and update counters
        checkAnswer(uid) {
            let iscorrect=false;
            const question = this.questions.find(q => q.uid === uid);
            console.log("Question is : ", question); // Debugging line
            console.log("Question_ID is : ", uid); // Debugging line

            const answer = question.answer.find(a => a.answer === this.selectedAnswers[uid]);
            console.log("Selected Answer is : ", this.selectedAnswers[uid]); // Debugging line
            
            const session_id = this.session_id;
            console.log("Session is : ", session_id); // Debugging line
  
            if (answer && answer.is_correct) {
              iscorrect=true
              this.correctAnswers++;
            } else {
              iscorrect=false
              this.incorrectAnswers++;
            }
            console.log("iscorrect : ", iscorrect); // Debugging line  

            const data = {
                //uid: uid,
                //answer: event.target.value
                session_id: session_id,
                question_id: uid, 
                selected_answers: this.selectedAnswers[uid],
                is_correct : iscorrect,
            };


            // Function to get CSRF token from cookies
            function getCookie(name) {
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
            }            
 
            // Send the data to the Django view using fetch
            fetch('/storeuserresponse/', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for security
            },
                body: JSON.stringify(data)
                })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                })
            .catch((error) => {
                console.error('Error:', error);
                });
                



            
   
          },


   
        // Navigate to the next question
         
        nextQuestion() {
            this.checkAnswer(this.questions[this.currentQuestionIndex].uid);
            if (this.currentQuestionIndex < this.questions.length - 1) {
              this.currentQuestionIndex++;
            }
          },
          // Navigate to the previous question
        prevQuestion() {
            this.checkAnswer(this.questions[this.currentQuestionIndex].uid);
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
            const questionNumber = prompt("Enter question number:");
            const index = parseInt(questionNumber) - 1;
            if (index >= 0 && index < this.questions.length) {
              this.currentQuestionIndex = index;
            } else {
              alert("Invalid question number");
            }
          },
          // Confirm exit
        confirmExit() {
          if (confirm("Are you sure you want to exit?")) {
             this.callGetQuizResults()
             this.endQuiz();
             }
          },
          
          // End the quiz and display results
        endQuiz() {
              
            //this.questions.forEach(question => {
            //  this.checkAnswer(question.uid);
            //});
            this.results.correctAnswers = this.correctAnswers;
            this.results.incorrectAnswers = this.incorrectAnswers;
            this.results.totalQuestions = this.questions.length;

            this.quizEnded = true;
            clearInterval(this.timer);
          },
          
        callGetQuizResults() {
            fetch('/get_quiz_results/', {
            method: 'POST',
            headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({
                // You can send the necessary quiz-related data to the server here
                subject: this.subject, // Example: sending the subject or other needed information
                selectedAnswers: this.selectedAnswers // Example: sending selected answers for further processing
            })
            })
        .then(response => response.json())
        .then(data => {
            // Assuming 'data' contains the quiz results (like correct answers, score, etc.)
            this.results.correctAnswers = data.correctAnswers;
            this.results.incorrectAnswers = data.incorrectAnswers;
            this.results.totalQuestions = data.totalQuestions;

            // Set quizEnded to true to display the results
            this.quizEnded = true;
        })
            .catch(error => {
                console.error('Error fetching quiz results:', error);
                alert('There was an error retrieving your quiz results.');
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
        
        // Fetch questions and start the timer when the component is created
        created() {
          this.getQuestions();
          this.startTimer();
          
        }
      });

      app.mount('#app');
   
    