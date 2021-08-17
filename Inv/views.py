from django.shortcuts import render
from Inv.importdata import get_month_wise_case


# Create your views here.


def dashboard(request):
    context = get_month_wise_case("India")
    return render(request, 'inv/Dashboard.html', context)


def state_wise(request):
    text = request.POST.get("state_name", None)
    context = get_month_wise_case(text)
    return render(request, 'inv/Dashboard.html', context)


# def update_state_wise(request):
#     text = request.POST.get("state_name", None)
#     context = get_month_wise_case(text)
#     return render(request, 'inv/Dashboard.html', context)

# def dashboard(request, **state):
#     context = get_case(s  tate)
#     return render(request, 'inv/Dashboard.html', context)
#
