from django.shortcuts import render
from covid19dashboard.filter_function import create_dictionary


def index(request):
    context = create_dictionary("India")
    return render(request, 'dashboard/index.html', context)


def state_wise(request):
    text = request.POST.get("state_name", None)
    context = create_dictionary(text)
    return render(request, 'dashboard/index.html', context)
