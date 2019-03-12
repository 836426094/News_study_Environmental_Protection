#coding=utf-8

from flask import Blueprint

crawlers = Blueprint('crawlers',__name__)

from . import views