import json
from audioop import reverse

from django.test import TestCase
from notification.models import SendMethod , Notification , Template

class ViewTests(TestCase):
    def test_get_all_notifications(self):
        response = self.client.get('/api/notifications/')
        self.assertEqual(response.status_code, 200)

    def test_get_all_templates(self):
        response = self.client.get('/api/templates/')
        self.assertEqual(response.status_code, 200)

    def test_get_all_methods(self):
        response = self.client.get('/api/sendMethod/')
        self.assertEqual(response.status_code, 200)

    def testPostMethods(self):
        my_json = {
             "sendMethod":
                 {
                     "nameMethod": "mail.ru"
                 }
         }
        response = self.client.post('http://127.0.0.1:7000/api/sendMethod/', json.dumps(my_json),
                                    content_type="application/json")
        self.assertTrue(SendMethod.objects.filter(id=response.json()['id']).first())
        self.assertEqual(response.status_code, 200)

    def testPostTemplate(self):
        my_json = {
                "template": {
            "name": "TEST!",
            "text": "Hello #name itis ur new code #code"
        }
        }
        response = self.client.post('http://127.0.0.1:7000/api/templates/', json.dumps(my_json),
                                    content_type="application/json")
        self.assertTrue(Template.objects.filter(id=response.json()['id']).first())
        self.assertEqual(response.status_code, 200)

    def testPostNotification(self):
        s = SendMethod(id=1, nameMethod="qwe")
        s.save()

        t = Template(id=1, name="qwe")
        t.save()

        my_json = {
                 "notification":{
        "params":{
                    "PARAMS1":"abdulla123123123123",
                    "PARAMS2":"dsafsadfsadfsdaf",
                    "PARAMS3":"ghdhdhfdh"
                    },
        "sendMethodID_id": 1,
        "templateID_id": 1
    }
        }
        response = self.client.post('http://127.0.0.1:7000/api/notifications/', json.dumps(my_json),
                                    content_type="application/json")
        self.assertTrue(Notification.objects.filter(id=response.json()['id']).first())
        self.assertEqual(response.status_code, 200)

    def testPutNotification(self):
        s = SendMethod(id=1, nameMethod="qwe")
        s.save()

        t = Template(id=2, name="qwe")
        t.save()
        t2 = Template(id=1, name="qwe")
        t2.save()

        my_json = {
            "notification": {
                "templateID_id": 2
            }
        }

        c = Notification(params = {"params1":"a"}, sendMethodID_id = 1 , templateID_id = 1  )
        c.save()

        response = self.client.put('http://127.0.0.1:7000/api/notifications/' + str(c.id), json.dumps(my_json),
                                   content_type="application/json")
        self.assertTrue(Notification.objects.filter(templateID_id=2).first())
        self.assertEqual(response.status_code, 200)

    def testPutTemplate(self):
        my_json = {
                "template": {
                "text": "Hello"
            }
        }
        c = Template(name="abdulla" , text = "abdulla")
        c.save()
        response = self.client.put('http://127.0.0.1:7000/api/templates/' + str(c.id), json.dumps(my_json),
                                   content_type="application/json")
        self.assertTrue(Template.objects.filter(text="Hello").first())
        self.assertEqual(response.status_code, 200)

    def testPutMethod(self):
        my_json = {
            "sendMethod":
                {
                    "nameMethod": "mail.ru"
                }
        }
        c = SendMethod(nameMethod="abdulla")
        c.save()
        response = self.client.put('http://127.0.0.1:8000/api/sendMethod/' + str(c.id), json.dumps(my_json),
                                   content_type="application/json")
        self.assertTrue(SendMethod.objects.filter(nameMethod="mail.ru").first())
        self.assertEqual(response.status_code, 200)

    def testDeleteNotification(self):
        c = Notification(params={"params1": "a"}, sendMethodID_id=1, templateID_id=1)
        c.save()
        response = self.client.delete('http://127.0.0.1:8000/api/notifications/' + str(c.id))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Notification.objects.filter(id = c.id).first())

    def testDeleteMethod(self):
        c = SendMethod(nameMethod="abdulla")
        c.save()
        response = self.client.delete('http://127.0.0.1:8000/api/sendMethod/' + str(c.id))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(SendMethod.objects.filter(id = c.id).first())

    def testDeleteTemplate(self):
        c = Template(name="abdulla", text="abdulla")
        c.save()
        response = self.client.delete('http://127.0.0.1:8000/api/templates/' + str(c.id))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Template.objects.filter(id = c.id).first())
