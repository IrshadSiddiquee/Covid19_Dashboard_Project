import pandas as pd
import numpy as np
from datetime import date

state_wise_cases = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
dfMonthWise = pd.read_csv("https://api.covid19india.org/csv/latest/states.csv")


def get_case(state):
    if state == "India":
        state = "Total"
    sub = state_wise_cases[state_wise_cases['State'] == state].iloc[:, 0:5].to_dict('records')
    return sub[0]


def get_month_wise_case(state):
    month = []
    current_year_confirmed_case = []
    current_year_recovered_case = []
    current_year_deceased_case = []
    last_year_confirmed_case = []
    last_year_recovered_case = []
    last_year_deceased_case = []
    current_confirmed_case = 0
    current_recovered_case = 0
    current_deceased_case = 0
    last_confirmed_case = 0
    last_recovered_case = 0
    last_deceased_case = 0
    this_year = int(date.today().year)
    clean_date = (pd.to_datetime(dfMonthWise['Date'].str[:-3]) - pd.Timedelta(days=1)).unique()
    for i in range(len(clean_date)):
        cleaned_date = pd.Timestamp(np.datetime64(clean_date[i]))
        d = pd.to_datetime(cleaned_date).strftime('%Y-%m-%d')
        year = int(pd.to_datetime(cleaned_date).strftime('%Y'))
        last_year = year - 1
        case = dfMonthWise.loc[(str(d) == dfMonthWise["Date"]) &
                               (state == dfMonthWise["State"])].iloc[:, 0:5].to_dict('records')
        if year >= (this_year - 1):
            if len(case) > 0:
                month.append(pd.to_datetime(case[0]['Date']).strftime('%B-%Y'))
                current_confirmed_case = case[0]['Confirmed'] - last_confirmed_case
                current_recovered_case = case[0]['Recovered'] - last_recovered_case
                current_deceased_case = case[0]['Deceased'] - last_deceased_case
                if state == "INDIA":
                    if year == this_year:
                        current_year_confirmed_case.append(current_confirmed_case)
                        current_year_recovered_case.append(current_recovered_case)
                        current_year_deceased_case.append(current_deceased_case)
                    elif year == (this_year - 1):
                        last_year_confirmed_case.append(current_confirmed_case)
                        last_year_recovered_case.append(current_recovered_case)
                        last_year_deceased_case.append(current_deceased_case)

                else:
                    if year == this_year:
                        current_year_confirmed_case.append(current_confirmed_case / 100000)
                        current_year_recovered_case.append(current_recovered_case / 100000)
                        current_year_deceased_case.append(current_deceased_case / 100000)
                    elif year == (this_year - 1):
                        last_year_confirmed_case.append(current_confirmed_case / 100000)
                        last_year_recovered_case.append(current_recovered_case / 100000)
                        last_year_deceased_case.append(current_deceased_case / 100000)

                last_confirmed_case = case[0]['Confirmed']
                last_recovered_case = case[0]['Recovered']
                last_deceased_case = case[0]['Deceased']

            else:
                month.append(pd.to_datetime(d).strftime('%B-%Y'))
                if year == this_year:
                    current_year_confirmed_case.append(0)
                    current_year_recovered_case.append(0)
                    current_year_deceased_case.append(0)
                elif year == (this_year - 1):
                    last_year_confirmed_case.append(0)
                    last_year_recovered_case.append(0)
                    last_year_deceased_case.append(0)

    case_data = get_case(state)
    return {'Month': month,
            'current_year_confirmed_case': current_year_confirmed_case,
            'current_year_deceased_case': current_year_deceased_case,
            'current_year_recovered_case': current_year_recovered_case,
            'last_year_confirmed_case': last_year_confirmed_case,
            'last_year_recovered_case': last_year_recovered_case,
            'last_year_deceased_case': last_year_deceased_case,
            'Cases': case_data
            }


subs = get_month_wise_case("India")
print(subs['current_year_confirmed_case'][len(subs['current_year_confirmed_case'])-1])

# print(get_case("Bihar"))
