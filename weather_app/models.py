from django.db import models

class Comment(models.Model):
    name = models.CharField(default="Anonymous", max_length=200)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
