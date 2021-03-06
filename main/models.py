# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from validators import validate_comma_separated, validate_command


class API(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    command = models.CharField(max_length=200, validators=[validate_command])
    output_files = models.CharField(max_length=200, blank=True, validators=[validate_comma_separated])
    description = models.TextField()
    num_input_params = models.IntegerField(default=0)
    authorized_groups = models.CharField(default='guest', max_length=200, validators=[validate_comma_separated])

    def __str__(self):
        return self.name


class Request(models.Model):
    REQUEST_STATUS = (
        ('processing', 'Processing'),
        ('finished', 'Finished'),
    )

    api_id = models.ForeignKey(API)
    input_params = models.CharField(max_length=200, blank=True, validators=[validate_comma_separated])
    owner = models.ForeignKey(User, null=True)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + ": " + self.api_id.name