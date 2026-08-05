from django.test import TestCase
from django.urls import reverse
from lakes.models import Lake
from quiz.models import QuizAnswer, QuizResult
from django.contrib.auth import get_user_model
from quiz.views import QUESTIONS_NUM, OPTIONS_NUM

User = get_user_model()


class TestQuizView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
        )

        cls.lakes = []
        for i in range(QUESTIONS_NUM * OPTIONS_NUM * 2):
            cls.lakes.append(
                Lake.objects.create(
                    name=f'Lake {i:02d}',
                    country=f'Country {i:02d}',
                )
            )

    def setup_quiz_session(self):
        '''Populate the test client's session with quiz answers for POST requests.'''

        session = self.client.session
        session['correct_answers'] = {
            str(lake.id): lake.country
            for lake in self.lakes[:QUESTIONS_NUM]
        }
        session.save()

        return session['correct_answers']

    def test_quiz_page_status_code(self):
        '''Verify that the quiz page loads successfully with a 200 OK status.'''

        response = self.client.get(reverse('quiz:quiz_lakes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/quiz_lakes.html')

    def test_quiz_stores_correct_answers_in_the_session(self):
        '''Verify that correct_answers are stored in the session with expected data.'''

        self.client.get(reverse('quiz:quiz_lakes'))
        session = self.client.session

        self.assertIn('correct_answers', session)
        self.assertEqual(len(session['correct_answers']), QUESTIONS_NUM)

    def test_quiz_submission_redirects_to_results_page(self):
        '''Verify that submitting the quiz redirects to the results page.'''

        post_data = self.setup_quiz_session()

        response = self.client.post(reverse('quiz:quiz_lakes'), post_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('quiz:quiz_results'))

    def test_anonymous_users_do_not_create_quiz_results_in_database(self):
        '''Verify that anonymous users do not create QuizResult records.'''

        post_data = self.setup_quiz_session()

        self.client.post(reverse('quiz:quiz_lakes'), post_data)

        self.assertEqual(QuizResult.objects.count(), 0)

    def test_authenticated_users_create_quiz_result_with_correct_data(self):
        '''Verify that authenticated users create QuizResult object with correct data.'''

        self.client.force_login(self.user)

        post_data = self.setup_quiz_session()

        self.client.post(reverse('quiz:quiz_lakes'), post_data)

        self.assertEqual(QuizResult.objects.count(), 1)

        quiz_result = QuizResult.objects.last()

        self.assertEqual(quiz_result.user, self.user)
        self.assertEqual(quiz_result.score, QUESTIONS_NUM)
        self.assertEqual(quiz_result.total, QUESTIONS_NUM)

    def test_authenticated_users_create_quiz_answers(self):
        '''Verify that authenticated users create QuizAnswer records.'''

        self.client.force_login(self.user)

        post_data = self.setup_quiz_session()

        self.client.post(reverse('quiz:quiz_lakes'), post_data)

        answers = QuizAnswer.objects.all()
        self.assertEqual(answers.count(), QUESTIONS_NUM)

        # Verify that created QuizAnswers relate to QuizResult
        quiz_result = QuizResult.objects.get()
        self.assertEqual(quiz_result.answers.count(), QUESTIONS_NUM)
    
    def test_submission_with_wrong_answers_saves_correct_score(self):
        '''Verify that submitting a quiz with wrong answers saves the correct score.'''

        self.client.force_login(self.user)

        post_data = self.setup_quiz_session()

        first_question = next(iter(post_data))
        post_data[first_question] = 'Wrong Country'

        self.client.post(reverse('quiz:quiz_lakes'), post_data)

        quiz_result = QuizResult.objects.get()
        self.assertEqual(quiz_result.score, QUESTIONS_NUM - 1)

    def test_correct_answers_are_removed_from_the_session_after_post_request(self):
        '''Verify that correct_answers are removed from the session after evaluation in post request.'''

        post_data = self.setup_quiz_session()

        self.client.post(reverse('quiz:quiz_lakes'), post_data)

        updated_session = self.client.session

        self.assertNotIn('correct_answers', updated_session)

    def test_quiz_results_are_stored_in_the_session(self):
        '''Verify that quiz results are stored in the session after submission.'''

        post_data = self.setup_quiz_session()

        self.client.post(reverse('quiz:quiz_lakes'), post_data)

        results = self.client.session['quiz_results']

        self.assertEqual(results['score'], QUESTIONS_NUM)
        self.assertEqual(results['total'], QUESTIONS_NUM)
        self.assertEqual(len(results['results']), QUESTIONS_NUM)

    def test_anonymous_users_are_redirected_from_saved_results(self):
        '''Verify that anonymous users cannot access saved quiz results.'''

        response = self.client.get(reverse('quiz:saved_results'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'{reverse('users:login')}?next={reverse('quiz:saved_results')}'
    )

    def test_authenticated_users_can_access_saved_results(self):
        '''Verify that authenticated users can access saved quiz results.'''

        self.client.force_login(self.user)

        response = self.client.get(reverse('quiz:saved_results'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/saved_results.html')