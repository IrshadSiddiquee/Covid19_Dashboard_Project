import pandas as pd
import numpy as np
from datetime import date, timedelta

state_wise_cases = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
dfMonthWise = pd.read_csv("https://api.covid19india.org/csv/latest/states.csv")
state_wise_per_day_case = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv")


def get_case(state):
    if state == "India":
        state = "Total"
    cases = state_wise_cases[state_wise_cases['State'] == state].iloc[:, 0:5].to_dict('records')

    return cases[0]


def get_daily_cases(last_day):
    state_codes = []
    confirmed_cases = []
    recovered_cases = []
    deceased_cases = []
    state_with_code = pd.DataFrame(state_wise_cases,
                                   columns=['State', 'State_code']).to_dict('record')
    for i in range(len(state_with_code)):
        state_code = state_with_code[i]['State_code']
        if state_code != 'TT':
            case = pd.DataFrame(state_wise_per_day_case.loc[(state_wise_per_day_case["Date_YMD"] == str(last_day))],
                                columns=[str(state_code)])
            state_codes.append(state_code)
            confirmed_cases.append(case.iloc[0][str(state_code)])
            recovered_cases.append(case.iloc[1][str(state_code)])
            deceased_cases.append(case.iloc[2][str(state_code)])

    cases = {'State_Code': state_codes,
             'Confirmed': confirmed_cases,
             'Recovered': recovered_cases,
             'Deceased': deceased_cases}

    return cases


def get_state_code(state):
    state_code = ""
    state_with_code = pd.DataFrame(state_wise_cases,
                                   columns=['State', 'State_code']).to_dict('record')
    for i in range(len(state_with_code)):
        if state_with_code[i]['State'] == state:
            state_code = state_with_code[i]['State_code']
            break

    return state_code


def get_state():
    all_state = []
    state_with_code = pd.DataFrame(state_wise_cases,
                                   columns=['State', 'State_code']).to_dict('record')
    for i in range(len(state_with_code)):
        if state_with_code[i]['State'] != 'Total':
            all_state.append(state_with_code[i]['State'])

    return all_state


def get_full_state_name(state):
    all_state = ""
    state_with_code = pd.DataFrame(state_wise_cases,
                                   columns=['State', 'State_code']).to_dict('record')

    for i in range(len(state_with_code)):
        if state_with_code[i]['State'].split(" ", 1)[0] == state:
            all_state = state_with_code[i]['State']
            break

    return all_state


def get_state_wise_daily_case(state_code, current_date):
    cases = ""
    try:
        case = pd.DataFrame(state_wise_per_day_case.loc[(state_wise_per_day_case["Date_YMD"] == str(current_date))],
                            columns=[str(state_code)])
        cases = {'Confirmed': case.iloc[0][str(state_code)],
                 'Recovered': case.iloc[1][str(state_code)],
                 'Deceased': case.iloc[2][str(state_code)],
                 'Active': round(case.iloc[0][str(state_code)] * 0.30)}

        return cases

    except:
        return 0


def get_ten_days_cases(state_code, last_ten_days):
    confirmed_cases = []
    recovered_cases = []
    deceased_cases = []
    case = pd.DataFrame(state_wise_per_day_case.loc[(state_wise_per_day_case["Date_YMD"] >= str(last_ten_days))],
                        columns=[str(state_code)])
    for i in range(0, len(case), 3):
        confirmed_cases.append(case.iloc[i][str(state_code)])
        recovered_cases.append(case.iloc[i + 1][str(state_code)])
        deceased_cases.append(case.iloc[i + 2][str(state_code)])

    cases = {'Confirmed': confirmed_cases,
             'Recovered': recovered_cases,
             'Deceased': deceased_cases}

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

    if state == "India":
        state = 'India'
    else:
        state = get_full_state_name(state)

    iDay = 1
    this_year = int(date.today().year)
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

    last_ten_days = 10
    iDay = 1
    last_day = date.today() - timedelta(iDay)
    daily_cases = 0
    daily_cases = get_state_wise_daily_case(state_code, last_day)
    while daily_cases == 0:
        iDay += 1
        last_ten_days += 1
        last_day = date.today() - timedelta(iDay)
        daily_cases = get_state_wise_daily_case(state_code, last_day)

    last_day = date.today() - timedelta(last_ten_days)
    ten_days_case = get_ten_days_cases(state_code, last_day)

    get_daily_case = get_daily_cases(last_day)
    get_states = get_state()
    return {'Month': month,
            'current_year_confirmed_case': current_year_confirmed_case,
            'current_year_deceased_case': current_year_deceased_case,
            'current_year_recovered_case': current_year_recovered_case,
            'last_year_confirmed_case': last_year_confirmed_case,
            'last_year_recovered_case': last_year_recovered_case,
            'last_year_deceased_case': last_year_deceased_case,
            'Cases': case_data,
            'daily_cases': daily_cases,
            'ten_days_case': ten_days_case,
            'get_daily_case': get_daily_case,
            'get_states': get_states
            }


# last_ten_days = 10
# iDay = 1
# last_day = date.today() - timedelta(iDay)
# daily_cases = 0
# daily_cases = get_state_wise_daily_case("TT", last_day)
# while daily_cases == 0:
#     iDay += 1
#     last_ten_days += 1
#     last_day = date.today() - timedelta(iDay)
#     daily_cases = get_state_wise_daily_case("TT", last_day)
#
# last_day = date.today() - timedelta(last_ten_days)
# ten_days_case = get_ten_days_cases("TT", last_day)
# print(ten_days_case)
