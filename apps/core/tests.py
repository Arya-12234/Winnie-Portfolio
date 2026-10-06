from unittest.mock import patch

from django.core import mail
from django.test import Client, SimpleTestCase, override_settings

CONTACT_SETTINGS = {
    "EMAIL_BACKEND": "django.core.mail.backends.locmem.EmailBackend",
    "DEFAULT_FROM_EMAIL": "owner@example.com",
    "PERSONAL_EMAIL": "owner@example.com",
}


@override_settings(**CONTACT_SETTINGS)
class ContactFormTests(SimpleTestCase):
    def setUp(self):
        mail.outbox = []
        self.client = Client(enforce_csrf_checks=True)
        self.valid_payload = {
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "subject": "Hello",
            "message": "I would like to talk about a project.",
        }

    def _token(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("csrftoken", self.client.cookies)
        return self.client.cookies["csrftoken"].value

    def _post(self, payload, token=None):
        data = dict(payload)
        headers = {}
        if token is not None:
            data["csrfmiddlewaretoken"] = token
            headers["HTTP_X_CSRFTOKEN"] = token
        return self.client.post("/contact", data, **headers)

    def test_get_contact_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="contact"')
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertContains(response, 'for="contact-email"')

    def test_valid_post_sends_email(self):
        token = self._token()
        payload = dict(self.valid_payload)
        payload["name"] = '<script>alert("x")</script>'
        payload["subject"] = "Hello\r\nBcc: evil@example.com"
        response = self._post(payload, token)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(len(mail.outbox), 1)
        sent = mail.outbox[0]
        self.assertEqual(sent.from_email, "owner@example.com")
        self.assertEqual(sent.to, ["owner@example.com"])
        self.assertEqual(sent.reply_to, ["ada@example.com"])
        self.assertNotIn("\n", sent.subject)
        self.assertNotIn("\r", sent.subject)
        html = sent.alternatives[0][0]
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_invalid_email(self):
        token = self._token()
        payload = dict(self.valid_payload)
        payload["email"] = "not-an-email"
        response = self._post(payload, token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Please enter a valid email address.")
        self.assertEqual(len(mail.outbox), 0)

    def test_missing_required_fields(self):
        token = self._token()
        payload = dict(self.valid_payload)
        payload["message"] = "   "
        response = self._post(payload, token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Please complete all required fields.")
        self.assertEqual(len(mail.outbox), 0)

    def test_post_without_csrf_is_rejected(self):
        response = self._post(self.valid_payload)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(mail.outbox), 0)

    @patch("apps.core.views.send_contact_email", side_effect=RuntimeError("smtp password leaked"))
    def test_email_failure_returns_generic_error(self, _send):
        token = self._token()
        response = self._post(self.valid_payload, token)
        self.assertEqual(response.status_code, 500)
        body = response.content.decode()
        self.assertIn("could not be sent", body)
        self.assertNotIn("password", body)
        self.assertNotIn("smtp", body.lower())
