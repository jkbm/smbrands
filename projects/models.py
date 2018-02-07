# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models
from django.urls import reverse 
from django_countries.fields import CountryField
from django.utils import timezone
# Create your models here.

class Project(models.Model):

    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Dataset(models.Model):

    project = models.ForeignKey(Project, on_delete="models.CASCADE")

    filename = models.CharField(max_length=50, null=True, blank=True)
    number_of_messages = models.IntegerField(null=True, blank=True)
    saved = models.BooleanField(default=True)

    def __str__(self):

        return self.filename


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    following = models.IntegerField()
    followers = models.IntegerField()
    messages = models.IntegerField()
    likes = models.IntegerField()

    def __str__(self):
        return self.name + "|" + self.user_id

class Twitter_data(models.Model):

    message = models.CharField(max_length=500)
    likes = models.IntegerField()
    retweets = models.IntegerField()
    replies = models.IntegerField()
    user = models.BigIntegerField()
    date = models.DateField(null=True, blank=True)
    dataset = models.ForeignKey(Dataset, null=True, blank=True, on_delete=models.CASCADE)
    