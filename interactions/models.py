from django.conf import settings
from posts.models import Post
from django.db import models



class Interaction(models.Model):
    INTERACTION_TYPES = (
        ("LIKE", "Like"),
        ("SHARE", "Share"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interactions")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="interactions")
    type = models.CharField(max_length=10, choices=INTERACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post", "type")  # prevent duplicate likes/shares

    def __str__(self):
        return f"{self.user.username} {self.type}d Post {self.post.id}"

