from django.shortcuts import render

def home(request):
    context = {
        "name": "Neha",
        "college": "I2IT Pune",
        "year": 3
    }

    return render(request, "tweets/home.html", context)