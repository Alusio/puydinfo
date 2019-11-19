import tempfile
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from webpush import send_user_notification

from blog.models import User, Programme, Article

tmp = tempfile.NamedTemporaryFile()


@login_required
@transaction.atomic
def dashboard(request):
    users = User.objects.all()
    programme = Programme.objects.order_by('-date')
    articles = Article.objects.all()
    payload = {"head": "Welcome!", "body": "Hello World"}
    send_user_notification(user=request.user, payload=payload, ttl=1000)
    return render(request, 'dashboard.html', {'users': users, 'programme': programme, 'articles': articles})
