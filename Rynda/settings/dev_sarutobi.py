# -*- coding: utf-8 -*-

from .local import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'rynda',
        'USER': 'rynda',
        'PASSWORD': 'rynda',
        'HOST': 'localhost',
        'PORT': '',
    }
}

