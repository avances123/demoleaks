# -*- coding: utf-8 -*-
from django.db import models
from transmeta import TransMeta

class TransModel(models.Model):
    __metaclass__ = TransMeta

