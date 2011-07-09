from django.contrib.auth import forms
from django.contrib.auth import views
from django import shortcuts
from django import http

def create_new_user(request):
    form = forms.UserCreationForm()
    # if form was submitted, bind form instance.
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user must be active for login to work
            user.is_active = True
            user.put()
            return http.HttpResponseRedirect('/accounts/login/')
    return shortcuts.render_to_response(
        'accounts/user_create_form.html', {'form': form})

def login(request):
  return views.login(
      request, template_name='login.html')


def logout(request):
  return views.logout(request, next_page='/')
