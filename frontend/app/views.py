from django.shortcuts import render
from django.http import*
from django.template import Template,Context
from django.template.loader import get_template
# Create your views here.

def test(request):


    return render(request,"index.html")