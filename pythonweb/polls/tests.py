from django.test import TestCase
from .models import Question


# Create your tests here.
class TestPolls(TestCase):

    index_page = '/'

    def setUp(self):
        Question.objects.create(question_text="What movie to see on Friday 16/1/2019")
        Question.objects.create(question_text="What movie to see on Sunday 20/1/2019")
        Question.objects.create(question_text="What movie to see on Monday 21/1/2019")

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
                self.assertNotContains(reponse, 'Sumbit')
            else:
                self.assertContains(reponse, 'Sumbit')
                for movie in ques.answer.all():
                    self.assertContains(reponse, movie.choice_text)

    def test_was_reponsed_result(self):
        for ques in Question.objects.all():
            reponse = self.client.get(self.index_page + str(ques.id) + "/result/")
            self.assertContains(reponse, 'Go back')
    
    def test_object_not_found(self):
        for i in range(0, 100):
            reponse = self.client.get(self.index_page + str(i) + "/")
            try:
                Question.objects.get(id=i)
                self.assertEqual(reponse.status_code, 200)
            except Question.DoesNotExist:
                self.assertEqual(reponse.status_code, 404)      