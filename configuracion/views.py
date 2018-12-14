# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.utils.functional import wraps
from django.template.context import RequestContext
import django.http as http
from django.views.decorators.http import require_POST

