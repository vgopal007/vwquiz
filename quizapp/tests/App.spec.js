// tests/App.spec.js

import { mount } from '@vue/test-utils';
import App from '../path/to/your/component'; // Adjust the path as needed

describe('Quiz App', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(App, {
      propsData: {
        subject: 'Artificial Intelligence' // or any subject you need
      }
    });
  });

  test('renders correctly', () => {
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.vm.subject).toBe('Math');
  });

  test('fetches questions on created', async () => {
    // Mock fetch
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ data: [{ uid: 1, answer: [{ answer: 'Option A', is_correct: true }] }] } }),
      })
    );

    await wrapper.vm.getQuestions();

    expect(global.fetch).toHaveBeenCalledWith('/api/get-quiz/?subject=Math');
    expect(wrapper.vm.questions).toEqual([{ uid: 1, answer: [{ answer: 'Option A', is_correct: true }] }]);
  });

  test('selects an answer', () => {
    const questionUid = 1;
    const event = { target: { value: 'Option A' } };
    wrapper.vm.selectAnswer(event, questionUid);
    expect(wrapper.vm.selectedAnswers[questionUid]).toBe('Option A');
  });

  test('checks correct answer', () => {
    // Setup the question
    wrapper.setData({
      questions: [{ uid: 1, answer: [{ answer: 'Option A', is_correct: true }] }]
    });
    wrapper.vm.selectedAnswers[1] = 'Option A';
    wrapper.vm.checkAnswer(1);
    
    expect(wrapper.vm.correctAnswers).toBe(1);
    expect(wrapper.vm.incorrectAnswers).toBe(0);
  });

  test('navigates to next question', () => {
    wrapper.setData({ questions: [{ uid: 1 }, { uid: 2 }] });
    wrapper.vm.currentQuestionIndex = 0;
    wrapper.vm.nextQuestion();
    
    expect(wrapper.vm.currentQuestionIndex).toBe(1);
  });

  test('marks a question for review', () => {
    wrapper.vm.markForReview();
    
    expect(wrapper.vm.markedQuestions).toContain(0);
  });

  test('ends the quiz and calculates results', () => {
    wrapper.setData({ questions: [{ uid: 1 }, { uid: 2 }] });
    wrapper.vm.correctAnswers = 1; // Simulate answering questions
    wrapper.vm.incorrectAnswers = 0;
    wrapper.vm.endQuiz();

    expect(wrapper.vm.results.correctAnswers).toBe(1);
    expect(wrapper.vm.results.incorrectAnswers).toBe(0);
    expect(wrapper.vm.results.totalQuestions).toBe(2);
    expect(wrapper.vm.quizEnded).toBe(true);
  });
});

