from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    todo_text = models.CharField(max_length=300)
    is_done = models.BooleanField(default=False)
    todo_author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.todo_text

    def as_dict(self):
        return {
            'todo_text': self.todo_text,
            'is_done': self.is_done,
            'pub_date': self.pub_date
        }
