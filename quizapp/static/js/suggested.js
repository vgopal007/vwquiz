 // Prepare the data to send
            const data = {
                uid: uid,
                answer: event.target.value
                //session_id: session_id,
                question_id: question_id,
                selected_answers: selectedAnswers
            };
            
 
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
        