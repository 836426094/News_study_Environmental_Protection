#coding=utf-8

from flask import Blueprint

data_analysis = Blueprint('data_analysis',__name__)

from . import views