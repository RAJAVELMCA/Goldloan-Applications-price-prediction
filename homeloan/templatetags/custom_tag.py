from django import template
from homeloan.models import *
register = template.Library()

@register.filter(name = 'notification')
def notification(obj):
    application = Application.objects.filter(Status__isnull=True)
    return application

@register.simple_tag()
def notificationcount(*args, **kwargs):
    applicationcount  = Application.objects.filter(Status__isnull=True).count()
    return applicationcount