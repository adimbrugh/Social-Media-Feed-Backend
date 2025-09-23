from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post
import json



class InteractionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username="john", email="john@example.com", password="pass123")
        self.post = Post.objects.create(author=self.user, content="Test Post")

    def get_token(self):
        query = '''
        mutation {
          tokenAuth(username: "john", password: "pass123") { token }
        }
        '''
        resp = self.client.post("/graphql/", data=json.dumps({"query": query}), content_type="application/json")
        return resp.json()["data"]["tokenAuth"]["token"]

    def test_add_like(self):
        token = self.get_token()
        headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}
        mutation = f'''
        mutation {{
          addInteraction(postId: {self.post.id}, type: "LIKE") {{
            interaction {{ id type user {{ username }} post {{ id }} }}
          }}
        }}
        '''
        resp = self.client.post("/graphql/", data=json.dumps({"query": mutation}), content_type="application/json", **headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        assert data["data"]["addInteraction"]["interaction"]["type"] == "LIKE"

