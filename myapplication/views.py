from django.shortcuts import render
from django.http import HttpResponse
from myapplication.forms import UserForm

# Create your views here.

def index(request):
	return HttpResponse("Hello World.")

def login(request):
	if request.method == 'POST':
		form = UserForm(request.POST)

		if form.is_valid():
			form.save(commit=True)

			return index(request)
		else:
			print(form.errors)
	else:
		form = UserForm()

	return render(request, 'login.html', {'form': form})