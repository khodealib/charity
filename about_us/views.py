from django.contrib.auth import get_user_model
from django.shortcuts import render


def about_us(request):
    if request.method == 'GET':
        users = get_user_model().objects.all()
        content = {'users': users}
        return render(request, 'about_us.html', content)
