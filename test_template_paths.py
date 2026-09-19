import unittest

from app import app


class TemplatePathTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_auth_pages_render(self):
        self.assertEqual(self.client.get('/auth/login').status_code, 200)
        self.assertEqual(self.client.get('/auth/register').status_code, 200)

    def test_error_page_renders(self):
        response = self.client.get('/definitely-missing-page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'File Not Found', response.data)


if __name__ == '__main__':
    unittest.main()
