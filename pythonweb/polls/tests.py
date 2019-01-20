from django.test import TestCase
from .models import Question, Choice
from random import choice
from json import load
from pythonweb.settings import BASE_DIR
from django.urls import reverse


class TestPolls(TestCase):

    index_page = '/'
    data = '%s/dump.json' % BASE_DIR
    valid_ques = []
    invalid_ques = []

    def setUp(self):
        # Loading dump data
        with open(self.data, 'r') as f:
            dump_data = load(f)

        for obj in dump_data:
            temp = Question.objects.create(question_text=obj['question'])
            for movie in obj['choices']:
                temp.answer.create(choice_text=movie)
            if obj['choices']:
                self.valid_ques.append(str(temp.id))
            else:
                self.invalid_ques.append(str(temp.id))

    def test_was_reponsed_all_page(self):
        # test home page
        self.check_was_reponsed_url('')

        # test detail, result pages
        for que in Question.objects.all():
            self.check_was_reponsed_url(str(que.id) + "/")
            self.check_was_reponsed_url(str(que.id) + "/result/")
    
    def check_was_reponsed_url(self, url, status_code=200):
        reponse = self.client.get(self.index_page + url)
        self.assertEqual(reponse.status_code, status_code)

    def test_was_no_available_choices(self):
        for ques_id in self.invalid_ques:
            reponse = self.client.get(self.index_page + str(ques_id) + "/")
            self.assertContains(reponse, 'No available option')
            self.assertContains(reponse, 'Return to Poll')
            self.assertNotContains(reponse, 'Vote')

    def test_was_show_detail_question(self):
        for ques_id in self.valid_ques:
            reponse = self.client.get(self.index_page + ques_id + "/")
            ques = Question.objects.get(id=ques_id)
            self.assertContains(reponse, 'Vote')
            for movie in ques.answer.all():
                self.assertContains(reponse, movie.choice_text)

    def test_was_content_reponsed_result(self):
        for ques in Question.objects.all():
            reponse = self.client.get(
                self.index_page + str(ques.id) + "/result/")
            self.assertContains(reponse, 'Return to Poll')

    def test_object_not_found(self):
        for i in range(0, 1000):
            if str(i) not in self.valid_ques + self.invalid_ques:
                self.check_was_reponsed_url("%s/" % (i), 404)

    def test_invalid_submit_page(self):
        for id_ques in self.valid_ques:
            ques = Question.objects.get(id=id_ques)
            reponse = self.client.post(self.index_page + str(ques.id) + "/")
            self.assertContains(reponse, 'Please choice an option')

    def test_valid_submit_page(self):
        for _ in range(0, 1000):
            id_submit = choice(self.valid_ques)
            test = choice(Question.objects.get(id=id_submit).answer.all())
            submit_value = test.votes + 1
            reponse = self.client.post(self.index_page + str(id_submit) + "/", {
                'choice': str(test.id)
            })
            self.assertRedirects(reponse, '/%s/result/' % (id_submit))
            self.assertEqual(submit_value, Choice.objects.get(id=test.id).votes)

    def test_reverse_url_from_namspace_and_name(self):
        for i in range(0, 1000):
            self.check_reverse_match_url_execpted(url_reverse='polls:detail', args=[i], expect_url='%s%s/' % (self.index_page, i))
            self.check_reverse_match_url_execpted(url_reverse='polls:result', args=[i], expect_url='%s%s/result/' % (self.index_page, i))

    def check_reverse_match_url_execpted(self, url_reverse, args, expect_url):
        url = reverse(url_reverse, args=args)
        self.assertEqual(url, expect_url)