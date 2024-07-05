from django.db import models


class Resume(models.Model):
    name = models.CharField(max_length=250)
    job_title = models.CharField(max_length=250)
    skills = models.TextField()

    def __str__(self):
        return self.name

