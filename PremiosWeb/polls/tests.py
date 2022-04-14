import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_time_antique_with_date_future(self):
        """test with future date :)"""
        time = timezone.now() + datetime.timedelta(days=30)
        question_future = Question(question_text='¿who is the best developer?', pub_date=time)
        self.assertIs(question_future.time_antique(), False)

    def test_was_time_antique_with_date_last(self):
        """test with last date"""
        time = timezone.now() - datetime.timedelta(days=30)
        question_last = Question(question_text='¿who is the best developer?', pub_date=time)
        self.assertEqual(question_last.time_antique(), False)

    def test_was_time_antique_with_date_present(self):
        """test with present date"""
        time = timezone.now()
        question_last = Question(question_text='¿who is the best developer?', pub_date=time)
        self.assertEqual(question_last.time_antique(), True)

class QuestionIndexViewTest(TestCase):

    def test_not_questions(self):
        """if not question exist, an appropiate message is displayed"""
        result = self.client.get(reverse("polls:index"))
        self.assertEqual(result.status_code, 200)
        self.assertContains(result, "sorry, Questions not found :(")
        self.assertQuerysetEqual(result.context["questions"], [])

    
    def test_questions_with_future_pub_date(self):
        """Questions with date greater to timezone.now shouldn't be displayed"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text='manco xd', pub_date=time)
        future_question.save()
        result = self.client.get(reverse('polls:index'))
        self.assertNotIn(future_question, result.context['questions'])


