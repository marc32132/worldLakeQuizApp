from django.test import TestCase
from quiz.models import QuizAnswer, QuizResult
from lakes.models import Lake
from django.contrib.auth import get_user_model
from quiz.views import QUESTIONS_NUM

User = get_user_model()


class TestQuizModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
        )

        cls.lakes = []
        for i in range(QUESTIONS_NUM * 2):
            cls.lakes.append(
                Lake.objects.create(
                    name=f'Lake {i:02d}',
                    country=f'Country {i:02d}',
            )
        )

        cls.quiz_result = QuizResult.objects.create(
            user=cls.user,
            score=5,
            total=5,
        )

        cls.deleted_answer = QuizAnswer.objects.create(
            result=cls.quiz_result,
            question=cls.lakes[0],
            user_answer=cls.lakes[0].country,
            correct_answer=cls.lakes[0].country,
            is_correct=True, 
        )
        cls.other_answers = []
        for i in range(1, QUESTIONS_NUM):
            cls.other_answers.append(QuizAnswer.objects.create(
                result=cls.quiz_result,
                question=cls.lakes[i],
                user_answer=cls.lakes[i].country,
                correct_answer=cls.lakes[i].country,
                is_correct=True,
            ))

    def test_quiz_result_string_representation(self):
        '''Verify correct string data representation.'''

        self.assertEqual(str(self.quiz_result), f'testuser - 5/5')

    def test_deleting_lake_preserves_quiz_answer_with_null(self):
        '''Verify that deleting lake does not delete associated answer.'''

        self.lakes[0].delete()

        self.deleted_answer.refresh_from_db()
        for answer in self.other_answers:
            answer.refresh_from_db()

        self.quiz_result.refresh_from_db()

        # Verify that all the answers were kept
        self.assertEqual(self.quiz_result.answers.count(), QUESTIONS_NUM)

        # Verify that the data is still present after deletion of lake
        self.assertIsNone(self.deleted_answer.question)
        self.assertEqual(self.deleted_answer.correct_answer, self.lakes[0].country)
        self.assertEqual(self.deleted_answer.user_answer, self.lakes[0].country)
        self.assertTrue(self.deleted_answer.is_correct)
        self.assertEqual(self.deleted_answer.result, self.quiz_result)

        # Verify that deleting lake did not affect other answers
        for answer in self.other_answers:
            self.assertIsNotNone(answer.question)

    def test_deleting_quiz_result_cascades_to_quiz_answers(self):
        '''Verify that deleting quiz result deletes all related answers'''

        self.quiz_result.delete()

        self.assertEqual(QuizResult.objects.count(), 0)
        self.assertEqual(QuizAnswer.objects.count(), 0)

        # Verify that other related records are not affected
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Lake.objects.count(), QUESTIONS_NUM * 2)
