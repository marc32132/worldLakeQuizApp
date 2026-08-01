from django.test import TestCase
from lakes.models import Lake
from quiz.views import generate_questions

class TestQuizGeneration(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i in range(40):
            Lake.objects.create(
                name=f"Lake {i:02d}",
                country=f"Country {i:02d}",
            )

    def test_quiz_generates_exactly_5_questions(self):
        '''Verify that there are exactly 5 questions generated'''

        quiz_data, correct_answers = generate_questions()

        self.assertEqual(len(correct_answers), 5)
        self.assertEqual(len(quiz_data), 5)

    def test_quiz_generates_4_options_per_question(self):
        '''Verify that each question contains exactly 4 answer options.'''

        quiz_data, correct_answers = generate_questions()

        for question_data in quiz_data:
            options = question_data["options"]
            self.assertEqual(len(options), 4)

    def test_correct_answer_is_always_included_in_options(self):
        '''Verify that each generated question contains correct answer'''

        quiz_data, correct_answers = generate_questions()

        for question_data in quiz_data:
            q_id = str(question_data["id"])

            self.assertIn(q_id, correct_answers)
            self.assertIn(correct_answers[q_id], question_data["options"])

    def test_there_are_no_duplicate_questions(self):
        '''Verify that generated quiz questions are unique.'''

        quiz_data, correct_answers = generate_questions()

        questions = [question_data["name"] for question_data in quiz_data]

        self.assertEqual(len(questions), len(set(questions)))

    def test_there_are_no_duplicate_options(self):
        '''Verify there are no duplicate options within each generated question'''

        quiz_data, correct_answers = generate_questions()

        for question_data in quiz_data:
            options = question_data["options"]
            self.assertEqual(len(options), len(set(options)))

            



    

