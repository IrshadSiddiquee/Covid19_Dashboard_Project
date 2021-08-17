import pandas as pd
import numpy as np
from datetime import date, timedelta

state_wise_cases = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
dfMonthWise = pd.read_csv("https://api.covid19india.org/csv/latest/states.csv")
state_wise_per_day_case = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv")


def get_case(state):
    if state == "India":
        state = "Total"
    sub = state_wise_cases[state_wise_cases['State'] == state].iloc[:, 0:5].to_dict('records')
    return sub[0]


def get_state_code(state):
    state_code = ""
    state_with_code = pd.DataFrame(state_wise_cases,
                                   columns=['State', 'State_code']).to_dict('record')
    for i in range(len(state_with_code)):
        if state_with_code[i]['State'] == state:
            state_code = state_with_code[i]['State_code']
            break

    return state_code


def get_state_wise_daily_case(state_code, current_date):
    cases = ""
    case = pd.DataFrame(state_wise_per_day_case.loc[(state_wise_per_day_case["Date_YMD"] == str(current_date))],
                        columns=[str(state_code)])
    cases = {'Confirmed': case.iloc[0][str(state_code)],
             'Recovered': case.iloc[1][str(state_code)],
             'Deceased': case.iloc[2][str(state_code)]}
    # cases.append({'Recovered': case.iloc[1][str(state_code)]})
    # cases.append({'Deceased': case.iloc[2][str(state_code)]})
    return cases


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
    state_code = ""
    daily_case = ""
    this_year = int(date.today().year)
    last_day = date.today() - timedelta(1)
    clean_date = (pd.to_datetime(dfMonthWise['Date'].str[:-3]) - pd.Timedelta(days=1)).unique()
    for i in range(len(clean_date)):
        cleaned_date = pd.Timestamp(np.datetime64(clean_date[i]))
        d = pd.to_datetime(cleaned_date).strftime('%Y-%m-%d')
        year = int(pd.to_datetime(cleaned_date).strftime('%Y'))
        case = dfMonthWise.loc[(str(d) == dfMonthWise["Date"]) &
                               (state == dfMonthWise["State"])].iloc[:, 0:5].to_dict('records')
        if year >= (this_year - 1):
            if len(case) > 0:
                month.append(pd.to_datetime(case[0]['Date']).strftime('%B-%Y'))
                current_confirmed_case = case[0]['Confirmed'] - last_confirmed_case
                current_recovered_case = case[0]['Recovered'] - last_recovered_case
                current_deceased_case = case[0]['Deceased'] - last_deceased_case
                if state != "India":
                    if year == this_year:
                        current_year_confirmed_case.append(current_confirmed_case / 1000)
                        current_year_recovered_case.append(current_recovered_case / 1000)
                        current_year_deceased_case.append(current_deceased_case / 1000)
                    elif year == (this_year - 1):
                        last_year_confirmed_case.append(current_confirmed_case / 1000)
                        last_year_recovered_case.append(current_recovered_case / 1000)
                        last_year_deceased_case.append(current_deceased_case / 1000)

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
    if state == "India":
        state_code = 'TT'
    else:
        state_code = get_state_code(state)

    daily_cases = get_state_wise_daily_case(state_code, last_day)
    return {'Month': month,
            'current_year_confirmed_case': current_year_confirmed_case,
            'current_year_deceased_case': current_year_deceased_case,
            'current_year_recovered_case': current_year_recovered_case,
            'last_year_confirmed_case': last_year_confirmed_case,
            'last_year_recovered_case': last_year_recovered_case,
            'last_year_deceased_case': last_year_deceased_case,
            'Cases': case_data,
            'daily_cases': daily_cases
            }


# subs = get_month_wise_case("Nagaland")
# print(subs['daily_cases'])

# state = (get_state_code('Nagaland'))
# today_date = dt = date.today() - timedelta(1)
# daily_case = get_state_wise_daily_case(state, today_date)
# print(daily_case)
# # print(get_case("Bihar"))
