from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from quizapp.models import Types, Question, QuizSession, UserResponse
import json

class QuizAppViewsTestCase(TestCase):
    
    def setUp(self):
        # Set up a test user
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create some sample data
        self.category = Types.objects.create(subject_name='Math')
        self.question = Question.objects.create(
            question='What is 2 + 2?',
            subject=self.category,
            topic='Arithmetic',
            question_type='Multiple Choice',
            answer_explanation='Simple addition',
            reference='Math Book',
            difficulty_level='Easy',
            marks=1,
            source='Test Source'
        )

    def test_quizapp_view(self):
        response = self.client.get(reverse('quizapp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quizapp.html')
        self.assertContains(response, self.category.subject_name)

    def test_quiz_view(self):
        response = self.client.get(reverse('quiz'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz.html')

    def test_get_quiz_valid_subject(self):
        response = self.client.get(reverse('get_quiz'), {'subject': self.category.subject_name})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': True, 'data': [{
            'uid': str(self.question.uid),
            'subject': self.category.subject_name,
            'question_type': self.question.question_type,
            'question': self.question.question,
            'marks': self.question.marks,
            'answer': self.question.get_answers(),
            'answer_explanation': self.question.answer_explanation,
            'reference': self.question.reference,
            'difficulty_level': self.question.difficulty_level,
            'source': self.question.source,
        }]})

    def test_get_quiz_invalid_subject(self):
        response = self.client.get(reverse('get_quiz'), {'subject': 'Invalid Subject'})
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'error': "Key 'subject' not found in request.GET"})

    def test_next_question(self):
        # Create another question to test navigation
        question2 = Question.objects.create(
            question='What is 3 + 3?',
            subject=self.category,
            topic='Arithmetic',
            question_type='Multiple Choice',
            answer_explanation='Simple addition',
            reference='Math Book',
            difficulty_level='Easy',
            marks=1,
            source='Test Source'
        )
        response = self.client.get(reverse('next_question'), {'current_question_id': self.question.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'question_text': question2.question})

    def test_prev_question(self):
        # Create another question
        question2 = Question.objects.create(
            question='What is 1 + 1?',
            subject=self.category,
            topic='Arithmetic',
            question_type='Multiple Choice',
            answer_explanation='Simple addition',
            reference='Math Book',
            difficulty_level='Easy',
            marks=1,
            source='Test Source'
        )
        response = self.client.get(reverse('prev_question'), {'current_question_id': question2.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'question_text': self.question.question})

    def test_review_view(self):
        response = self.client.get(reverse('review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review.html')
        self.assertContains(response, self.question.question)

    def test_save_user_response(self):
        session = QuizSession.objects.create(user=self.user, quiz=self.category)
        response_data = {
            'session_id': str(session.uid),
            'question_id': str(self.question.uid),
            'selected_answers': ['Option A']
        }
        response = self.client.post(reverse('save_user_response'), json.dumps(response_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'User responses saved successfully!'})
        self.assertTrue(UserResponse.objects.filter(session=session, question=self.question).exists())

    def test_get_user_response(self):
        session = QuizSession.objects.create(user=self.user, quiz=self.category)
        UserResponse.objects.create(session=session, question=self.question, selected_answers=['Option A'])
        
        response = self.client.get(reverse('get_user_response'), {'session_id': str(session.uid), 'question_id': str(self.question.uid)})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'selected_answers': ['Option A']})
