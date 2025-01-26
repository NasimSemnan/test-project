import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    description = models.CharField(max_length=1_000, null=True, blank=True)
    pub_date = models.DateTimeField("date published")

    # ...
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self) -> str:
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    choice_text = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=1_000, null=True, blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text


class Poll(models.Model):
    title = models.CharField(max_length=200, default="")
    description = models.CharField(max_length=1_000, null=True, blank=True)
    pub_date = models.DateTimeField("date published")
    questions = models.ManyToManyField(Question)

    def __str__(self) -> str:
        return self.title


class PollQuestion(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return f"{self.poll.title} - {self.question.question_text}"


# class Response(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
#     user = models.CharField(max_length=100)
#     def __str__(self):
#         return f"Response to {self.question} by {self.user}"
