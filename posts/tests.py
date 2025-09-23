from django.test import TestCase, Client
from django.contrib.auth import get_user_model
import json



class PostTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username="amy", email="amy@example.com", password="pw12345")

    def get_token(self, username="amy", password="pw12345"):
        query = '''
        mutation {
          tokenAuth(username: "amy", password: "pw12345") {
            token
          }
        }
        '''
        resp = self.client.post("/graphql/", data=json.dumps({"query": query}), content_type="application/json")
        return resp.json()["data"]["tokenAuth"]["token"]

    def test_create_post(self):
        token = self.get_token()
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        mutation = '''
        mutation {
          createPost(content: "Hello world!") {
            post { id content author { username } }
          }
        }
        '''
        resp = self.client.post("/graphql/", data=json.dumps({"query": mutation}), content_type="application/json", **headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        assert data["data"]["createPost"]["post"]["content"] == "Hello world!"
