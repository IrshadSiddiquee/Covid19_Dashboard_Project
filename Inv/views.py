from django.shortcuts import render
from Inv.importdata import get_case

# Create your views here.


def dashboard(request):
    context = get_case('Total')
    return render(request, 'inv/Dashboard.html', context)


def state_wise(request):
    text = request.POST.get("state_name", None)
    context = get_case(text)
    return render(request, 'inv/Dashboard.html', context)

# def dashboard(request, **state):
#     context = get_case(s  tate)
#     return render(request, 'inv/Dashboard.html', context)
#
