import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

# Create your tests here.

def question_future_or_last(context, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=context, pub_date=time)


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

    
    # def test_questions_with_future_pub_date(self):
    #     """Questions with date greater to timezone.now shouldn't be displayed"""
    #     time = timezone.now() + datetime.timedelta(days=30)
    #     future_question = Question(question_text='manco xd', pub_date=time)
    #     future_question.save()
    #     result = self.client.get(reverse('polls:index'))
    #     self.assertNotIn(future_question, result.context['questions'])

    def test_questions_with_future_pub_date(self):
        """Questions with date greater to timezone.now shouldn't be displayed""" 
        question_future_or_last('future question', 30)
        result = self.client.get(reverse('polls:index'))
        self.assertContains(result, "sorry, Questions not found :(")

    def test_question_with_last_pub_date(self):
        """Questions with date greater to timezone.now shouldn't be displayed (last date)"""
        question = question_future_or_last('future question', -30)
        result = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(result.context['questions'], [question])

    def test_future_question_and_past_question(self):
        past_question = question_future_or_last('past question', -30)
        future_question = question_future_or_last('future question', 30)
        test = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(test.context['questions'], [past_question])

    def test_two_past_questions(self):
        past_question1 = question_future_or_last('past question1', -30)
        past_question2= question_future_or_last('past question2', -40)
        test = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(test.context['questions'], [past_question1, past_question2])

    def test_two_future_questions(self):
        future_question1 = question_future_or_last('future question1', 30)
        future_question2= question_future_or_last('future question2', 40)
        test = self.client.get(reverse('polls:index'))
        self.assertContains(test, 'sorry, Questions not found :(')
        self.assertQuerysetEqual(test.context['questions'], [])



class TestDetailFutureAndPastQuestions(TestCase):
    def test_future_question_detail(self):
        future_question = question_future_or_last('future Question', 30)
        url = reverse('polls:detail' ,args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_detail(self):
        past_question = question_future_or_last('past Question', -30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionResultViewTests(TestCase):
    def test_no_question_result(self):
        """
        The result view of a question that doesn't exist
        return a 404 error not found
        """
        url = reverse("polls:result", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_question_result(self):
        """
        The result view of a question with a pub_date in the future
        return a 404 error not found
        """
        future_question = question_future_or_last("¿Quien es el mejor CD de Platzi?", 5)
        url = reverse("polls:result", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_result(self):
        """
        The result view of a question with a pub_date in the past
        displays the question's text
        """
        past_question = question_future_or_last("Past question", -30)
        url = reverse("polls:result", args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)