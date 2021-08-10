from django.shortcuts import render
from Inv.importdata import get_case


# state_wise_cases = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
#
# sub = state_wise_cases[state_wise_cases['State'] == 'Total'].iloc[:, 1:5].to_dict('records')
# print(sub[0])


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
