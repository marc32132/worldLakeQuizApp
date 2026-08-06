from django.test import TestCase
from lakes.models import Lake
from quiz.views import generate_questions, QUESTIONS_NUM, OPTIONS_NUM


class TestQuizGeneration(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i in range(QUESTIONS_NUM*OPTIONS_NUM*2):
            Lake.objects.create(
                name=f'Lake {i:02d}',
                country=f'Country {i:02d}',
            )

    def test_quiz_generates_correct_number_of_questions(self):
        '''Verify that the configured number of quiz questions is generated.'''

        quiz_data, correct_answers = generate_questions()

        self.assertEqual(len(correct_answers), QUESTIONS_NUM)
        self.assertEqual(len(quiz_data), QUESTIONS_NUM)

    def test_quiz_generates_correct_number_of_options_per_question(self):
        '''Verify that each question contains the configured number of answer options.'''

        quiz_data, _ = generate_questions()

        for question_data in quiz_data:
            options = question_data['options']
            self.assertEqual(len(options), OPTIONS_NUM)

    def test_correct_answer_is_always_included_in_options(self):
        '''Verify that each generated question contains correct answer within it's options.'''

        quiz_data, correct_answers = generate_questions()

        for question_data in quiz_data:
            q_id = str(question_data['id'])

            self.assertIn(q_id, correct_answers)
            self.assertIn(correct_answers[q_id], question_data['options'])

    def test_there_are_no_duplicate_questions(self):
        '''Verify that generated quiz questions are unique.'''

        quiz_data, _ = generate_questions()

        questions = [question_data['name'] for question_data in quiz_data]

        self.assertEqual(len(questions), len(set(questions)))

    def test_there_are_no_duplicate_options(self):
        '''Verify there are no duplicate options within each generated question.'''

        quiz_data, _ = generate_questions()

        for question_data in quiz_data:
            options = question_data['options']
            self.assertEqual(len(options), len(set(options)))