from django.test import TestCase
from .models import Question, Choice
from random import choice


# Create your tests here.
class TestPolls(TestCase):

    index_page = '/'
    id_submit = None

    def setUp(self):
        que_1 = Question.objects.create(
            question_text="What movie to see on Friday 16/1/2019")

        # data test for submit form
        self.id_submit = str(que_1.id)
        dumps = ["GodFather", "Anime", "SAO", "Star War"]
        for data in dumps:
            que_1.answer.create(choice_text=data)

        # test display and show button
        Question.objects.create(
            question_text="What movie to see on Sunday 20/1/2019")
        Question.objects.create(
            question_text="What movie to see on Monday 21/1/2019")
        Question.objects.create(
            question_text="What movie to see on Thursday 24/1/2019")

    def test_was_reponse_home_page(self):
        reponse = self.client.get(self.index_page)
        for que in Question.objects.all():
            self.assertContains(reponse, que.question_text)

    def test_was_show_detail_question(self):
        for ques in Question.objects.all():
            reponse = self.client.get(self.index_page + str(ques.id) + "/")
            if not ques.answer.all():
                self.assertContains(reponse, 'No available option')
                self.assertContains(reponse, 'Go back')
                self.assertNotContains(reponse, 'Submit')
            else:
                self.assertContains(reponse, 'Submit')
                for movie in ques.answer.all():
                    self.assertContains(reponse, movie.choice_text)

    def test_was_reponsed_result(self):
        for ques in Question.objects.all():
            reponse = self.client.get(
                self.index_page + str(ques.id) + "/result/")
            self.assertContains(reponse, 'Go back')

    def test_object_not_found(self):
        for i in range(0, 100):
            reponse = self.client.get(self.index_page + str(i) + "/")
            try:
                Question.objects.get(id=i)
                self.assertEqual(reponse.status_code, 200)
            except Question.DoesNotExist:
                self.assertEqual(reponse.status_code, 404)

    def test_submit_detail_page(self):
        # test validation
        reponse = self.client.post(self.index_page + str(self.id_submit) + "/")
        self.assertContains(reponse, 'Please choice an option')

        # test submit vote with dump date
        for _ in range(0, 100):

            test = choice(Question.objects.get(
                id=self.id_submit).answer.all())
            submit_value = test.votes + 1
            reponse = self.client.post(self.index_page + str(self.id_submit) + "/", {
                'choice': str(test.id)
            })
            self.assertEqual(
                submit_value, Choice.objects.get(id=str(test.id)).votes)
