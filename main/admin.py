# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import API, Request


admin.site.register(API)
admin.site.register(Request)