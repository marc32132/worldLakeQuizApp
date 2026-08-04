from django.test import TestCase
from lakes.models import Lake
from quiz.views import calculate_score, QUESTIONS_NUM


class TestScoreHandling(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.lakes = []

        for i in range(QUESTIONS_NUM*2):
            cls.lakes.append(
                Lake.objects.create(
                    name=f"Lake {i:02d}",
                    country=f"Country {i:02d}",
                )
            )
        cls.correct_answers = {
            str(lake.id): lake.country
            for lake in cls.lakes[:QUESTIONS_NUM]
        }

        
    def test_calculating_score_when_all_answers_are_correct(self):
        '''Verify that a perfect quiz submission receives the maximum score.'''
   
        user_answers = {
            str(lake.id): lake.country
            for lake in self.lakes[:QUESTIONS_NUM]
        }

        _, score = calculate_score(self.correct_answers,user_answers)

        self.assertEqual(score, QUESTIONS_NUM)

    def test_calculating_score_when_no_answers_are_correct(self):
        '''Verify that an entirely incorrect submission receives a score of zero.'''

        user_answers = {
            str(lake.id): lake.country
            for lake in self.lakes[QUESTIONS_NUM:]
        }

        _, score = calculate_score(self.correct_answers,user_answers)

        self.assertEqual(score, 0)


    def test_calculating_score_when_some_of_the_answers_are_correct(self):
        '''Verify that partially correct answers produce the expected score.'''

        user_answers = {
            str(lake.id): lake.country
            for lake in self.lakes[3:QUESTIONS_NUM+3]
        }

        _, score = calculate_score(self.correct_answers,user_answers)

        self.assertEqual(score, QUESTIONS_NUM-3)

    def test_calculating_score_when_some_answers_are_missing(self):
        '''Verify that unanswered questions are counted as incorrect.'''

        user_answers = {
            str(lake.id): lake.country if lake.id % 2 else None
            for lake in self.lakes[:QUESTIONS_NUM]
                    }

        _, score = calculate_score(self.correct_answers,user_answers)

        self.assertEqual(score, (QUESTIONS_NUM//2) + (QUESTIONS_NUM % 2))

    def test_returned_results_have_correct_structure(self):
        '''Verify that each result dictionary contains the expected keys.'''

        user_answers = {
            str(lake.id): lake.country if lake.id % 2 else None
            for lake in self.lakes[:QUESTIONS_NUM]
                    }

        results, _ = calculate_score(self.correct_answers,user_answers)

        for result in results:
            self.assertSetEqual(set(result.keys()), {"question", "user_answer", "correct_answer", "is_correct"})

    def test_returned_results_contain_required_data(self):
        '''Verify that generated result entries contain all required data.'''

        user_answers = {
            str(lake.id): lake.country if lake.id % 2 else None
            for lake in self.lakes[:QUESTIONS_NUM]
                    }

        results, _ = calculate_score(self.correct_answers,user_answers)

        for result in results:
            # Verify that required fields are not None
            self.assertIsNotNone(result.get("question"))
            self.assertIsNotNone(result.get("correct_answer"))
            self.assertIsNotNone(result.get("is_correct"))

            self.assertIsInstance(result["is_correct"], bool)

            # Verify that string values are not empty
            self.assertTrue(len(str(result["question"]).strip()) > 0)
            self.assertTrue(len(str(result["correct_answer"]).strip()) > 0)
            if result["user_answer"] is not None:
                self.assertTrue(len(str(result["user_answer"]).strip()) > 0)

        # Verify that length of the data matches the number of questions
        self.assertEqual(len(results), QUESTIONS_NUM)
        self.assertEqual(len(self.correct_answers), QUESTIONS_NUM)
        self.assertEqual(len(user_answers), QUESTIONS_NUM)

    def test_returned_results_correctly_mark_answers(self):
        '''Verify that each result correctly reflects whether the user's answer is correct.'''

        user_answers = {
            str(lake.id): lake.country if lake.id % 2 else None
            for lake in self.lakes[:QUESTIONS_NUM]
                    }

        results, _ = calculate_score(self.correct_answers,user_answers)

        for result in results:
            if result["user_answer"] == result["correct_answer"]:
                self.assertTrue(result["is_correct"])
            else:
                self.assertFalse(result["is_correct"])