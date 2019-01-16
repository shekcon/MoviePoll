from django.test import TestCase
from .models import Question
from random import randrange
# Create your tests here.
class TestPolls(TestCase):

    index_page = '/'

    def test_was_reponse_each_page(self):
        reponse = self.client.get(self.index_page)
        self.assertEqual(200, reponse.status_code)
    
    def test_was_show_noavaiable_question(self):
        for ques in Question.objects.all():
            if not ques.answer:
                reponse = reponse = self.client.get(self.index_page + str(ques.id) + "/")
                self.assertContains(reponse.content, 'No available option')
                self.assertContains(reponse.content, 'Go back')

    def test_was_reponsed_result(self):
        for ques in Question.objects.all():
            reponse = self.client.get(self.index_page + str(ques.id) + "/result")
            self.assertEqual(reponse.status_code, 200)
            self.assertContains(reponse.content, 'Go back')
    
    def test_show_404_page(self):
        for i in range(0, 100):
            reponse = reponse = self.client.get(self.index_page + str(i))
            try:
                Question.objects.get(id=i)
            except Question.DoesNotExist:
                self.assertEqual(reponse.status_code, 404)
            else:
                self.assertEqual(reponse.status_code, 200)