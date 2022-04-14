from datetime import timedelta
from django.db import models
from django.utils import timezone 

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def time_antique(self):
        return timezone.now() >= self.pub_date >= timezone.now() - timedelta(days=1)

class Choise(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) 
    choise_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choise_text