# -*- coding: utf-8 -*-
from django.db import models

class TransModel(models.Model):
    __metaclass__ = TransMeta

