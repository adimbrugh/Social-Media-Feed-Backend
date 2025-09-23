from django.test import Client, TestCase
from django.contrib.auth import get_user_model
import json



User = get_user_model

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()

    def test_create_user_and_token(self):
        # create user via ORM
        u = self.User.objects.create_user(username="bob", email="bob@example.com", password="pass1234")
        self.assertTrue(self.User.objects.filter(username="bob").exists())

        # Obtain token via GraphQL
        query = '''
        mutation {
          tokenAuth(username: "bob", password: "pass1234") {
            token
          }
        }
        '''
        resp = self.client.post("/graphql/", data=json.dumps({"query": query}), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        assert "data" in data and "tokenAuth" in data["data"]
        assert data["data"]["tokenAuth"]["token"] is not None
