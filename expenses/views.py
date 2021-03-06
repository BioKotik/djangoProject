from django.shortcuts import render, redirect
from expenses.models import Record
from expenses.forms import LoginForm
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


# Create your views here.
@login_required
def all_records(request):
    records = Record.objects.all().order_by('date')
    return render(request, 'workplace.html', {'records': records})


class RecordListView(ListView):
    queryset = Record.objects.all()
    context_object_name = 'records'
    template_name = 'workplace.html'


def create(request):
    if request.method == "POST":
        adding = Record()
        adding.transaction = request.POST.get("transaction")
        adding.category = request.POST.get("category")
        adding.place = request.POST.get("place")
        adding.author = request.user
        adding.save()
    return render(request, 'add.html', {'create': create})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/workplace/')
                    # return HttpResponse('Authentificated successfully')
                else:
                    return HttpResponse('Disabled user')
            else:
                return HttpResponse('Invalid credentials (login or password)')
    else:
        form = LoginForm()
    return render(request, 'log-in.html', {'form': form})
