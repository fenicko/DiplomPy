from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'dish/html/index.html', {'title': 'Home'})

def dishs(request):
    return render(request, 'dish/html/dishs.html')