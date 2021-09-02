import covid19dashboard.api_calling as api
import covid19dashboard.constant as const
import pandas as pd
import numpy as np
from datetime import date, timedelta

# Create public variable to store state wise Confirmed', 'Recovered', 'Deaths' and 'Active' cases from dataframe
df_state_wise_cases = api.df_state_wise_cases

# create an interface for state with state code dataframe
df_state_with_code = api.df_state_with_code

# create an interface to import state wise per day cases from API
df_state_wise_per_day_cases = api.df_state_wise_per_day_cases

#  create an interface for month wise Confirmed', 'Recovered', 'Deaths' and 'Active' cases dataframe
df_month_wise_cases = api.df_month_wise_cases


# Pass state name or 'India' into the function to get state wise or pan india cases
# like total number of Confirmed', 'Recovered', 'Deaths' and 'Active'
def get_case(state):
    if state == const.COUNTRY_NAME:
        state = const.STR_TOTAL

    cases = df_state_wise_cases[df_state_wise_cases[const.STR_STATE] == state].iloc[
            :, const.INT_ZERO:const.INT_FIVE].to_dict(const.STR_RECORDS)
    return cases[const.INT_ZERO]


# Get daily state wise Confirmed', 'Recovered' and 'Deceased'.
def get_daily_cases(last_day):
    state_codes = []
    confirmed_cases = []
    recovered_cases = []
    deceased_cases = []

    for i in range(len(df_state_with_code)):
        state_code = df_state_with_code[i][const.STR_STATE_CODE]
        if state_code != const.STR_TT:
            case = pd.DataFrame(df_state_wise_per_day_cases.loc[(df_state_wise_per_day_cases[const.DATE_YMD]
                                                                 == str(last_day))], columns=[str(state_code)])

            state_codes.append(state_code)
            confirmed_cases.append(case.iloc[0][str(state_code)])
            recovered_cases.append(case.iloc[1][str(state_code)])
            deceased_cases.append(case.iloc[2][str(state_code)])

    cases = {const.STR_STATE_CODE: state_codes,
             const.CONFIRMED_CASES: confirmed_cases,
             const.RECOVERED_CASES: recovered_cases,
             const.DECEASED_CASES: deceased_cases}
    return cases


# Get state code based on state name
def get_state_code(state):
    state_code = ""
    for i in range(len(df_state_with_code)):
        if df_state_with_code[i][const.STR_STATE] == state:
            state_code = df_state_with_code[i][const.STR_STATE_CODE]
            break
    return state_code


# Store all state into the list
def get_state():
    all_state = []
    for i in range(len(df_state_with_code)):
        if df_state_with_code[i][const.STR_STATE] != const.STR_TOTAL:
            all_state.append(df_state_with_code[i][const.STR_STATE])
    return all_state


# Store all state into the list
def get_distinct_state_with_code():
    all_state_with_code = {}
    for i in range(len(df_state_with_code)):
        if df_state_with_code[i][const.STR_STATE] != const.STR_TOTAL:
            all_state_with_code[df_state_with_code[i][const.STR_STATE_CODE]] = (df_state_with_code[i][const.STR_STATE])
        else:
            all_state_with_code['IN'] = 'India'
    return all_state_with_code


# Get full state name
def get_full_state_name(state):
    all_state = ""
    for i in range(len(df_state_with_code)):
        if df_state_with_code[i][const.STR_STATE].split(" ", const.INT_ONE)[const.INT_ZERO] == state:
            all_state = df_state_with_code[i][const.STR_STATE]
            break
    return all_state


# Get current day state wise Confirmed', 'Recovered' and 'Deceased'.
def get_state_wise_daily_case(state_code, current_date):
    try:
        case = pd.DataFrame(
            df_state_wise_per_day_cases.loc[(df_state_wise_per_day_cases[const.DATE_YMD] == str(current_date))],
            columns=[str(state_code)])
        cases = {const.CONFIRMED_CASES: case.iloc[0][str(state_code)],
                 const.RECOVERED_CASES: case.iloc[1][str(state_code)],
                 const.DECEASED_CASES: case.iloc[2][str(state_code)],
                 const.ACTIVE_CASES: round(case.iloc[0][str(state_code)] * 0.30)}

        return cases
    except NameError:
        return 0


# get ten days history cases
def get_ten_days_cases(state_code, last_ten_days):
    confirmed_cases = []
    recovered_cases = []
    deceased_cases = []
    case = pd.DataFrame(df_state_wise_per_day_cases.loc[(df_state_wise_per_day_cases[const.DATE_YMD]
                                                         >= str(last_ten_days))], columns=[str(state_code)])
    for i in range(0, len(case), 3):
        confirmed_cases.append(case.iloc[i][str(state_code)])
        recovered_cases.append(case.iloc[i + 1][str(state_code)])
        deceased_cases.append(case.iloc[i + 2][str(state_code)])

    cases = {const.CONFIRMED_CASES: confirmed_cases,
             const.RECOVERED_CASES: recovered_cases,
             const.DECEASED_CASES: deceased_cases}
    return cases


def get_month_wise_case(state, input_year):
    month = []
    confirmed_cases = []
    recovered_cases = []
    deceased_cases = []
    last_confirmed_case = const.INT_ZERO
    last_recovered_case = const.INT_ZERO
    last_deceased_case = const.INT_ZERO

    # if state == const.COUNTRY_NAME:
    #     state = const.COUNTRY_NAME
    # else:
    #     state = get_full_state_name(state)

    clean_date = (pd.to_datetime(df_month_wise_cases[const.STR_DATE].str[:-3]) - pd.Timedelta(days=1)).unique()
    for i in range(len(clean_date)):
        cleaned_date = pd.Timestamp(np.datetime64(clean_date[i]))
        d = pd.to_datetime(cleaned_date).strftime(const.DATE_FORMAT_YMD)
        year = int(pd.to_datetime(cleaned_date).strftime(const.STR_YEAR))
        case = df_month_wise_cases.loc[(str(d) == df_month_wise_cases[const.STR_DATE]) & (
                    state == df_month_wise_cases[const.STR_STATE])].iloc[:, const.INT_ZERO:const.INT_FIVE].to_dict(
            const.STR_RECORDS)
        if year == input_year:
            if len(case) > const.INT_ZERO:
                month.append(pd.to_datetime(case[const.INT_ZERO][const.STR_DATE]).strftime(const.STR_MMMM_YYYY))
                if state != const.COUNTRY_NAME:
                    confirmed_cases.append((case[const.INT_ZERO][const.CONFIRMED_CASES]
                                           - last_confirmed_case) / const.INT_10K)
                    recovered_cases.append((case[const.INT_ZERO][const.RECOVERED_CASES]
                                           - last_recovered_case) / const.INT_10K)
                    deceased_cases.append((case[const.INT_ZERO][const.DECEASED_CASES]
                                          - last_deceased_case) / const.INT_10K)

                else:
                    confirmed_cases.append((case[const.INT_ZERO][const.CONFIRMED_CASES]
                                           - last_confirmed_case) / const.INT_100K)
                    recovered_cases.append((case[const.INT_ZERO][const.RECOVERED_CASES]
                                           - last_recovered_case) / const.INT_100K)
                    deceased_cases.append((case[const.INT_ZERO][const.DECEASED_CASES]
                                          - last_deceased_case) / const.INT_100K)

                last_confirmed_case = case[const.INT_ZERO][const.CONFIRMED_CASES]
                last_recovered_case = case[const.INT_ZERO][const.RECOVERED_CASES]
                last_deceased_case = case[const.INT_ZERO][const.DECEASED_CASES]

            else:
                month.append(pd.to_datetime(d).strftime(const.STR_MMMM_YYYY))
                confirmed_cases.append(const.INT_ZERO)
                recovered_cases.append(const.INT_ZERO)
                deceased_cases.append(const.INT_ZERO)

    return {const.STR_MONTH: month,
            const.CONFIRMED_CASES: confirmed_cases,
            const.RECOVERED_CASES: recovered_cases,
            const.DECEASED_CASES: deceased_cases}


# Combine all function to create dashboard data
def create_dictionary(state):
    if state == const.COUNTRY_NAME:
        state = const.COUNTRY_NAME
    else:
        state = get_full_state_name(state)

    case_data = get_case(state)
    if state == const.COUNTRY_NAME:
        state_code = const.STR_TT
    else:
        state_code = get_state_code(state)

    last_ten_days = const.INT_TEN
    start_day = const.INT_ONE
    last_day = date.today() - timedelta(start_day)
    daily_cases = get_state_wise_daily_case(state_code, last_day)
    while daily_cases == const.INT_ZERO:
        start_day += const.INT_ONE
        last_ten_days += const.INT_ONE
        last_day = date.today() - timedelta(start_day)
        daily_cases = get_state_wise_daily_case(state_code, last_day)

    last_day = date.today() - timedelta(last_ten_days)
    ten_days_case = get_ten_days_cases(state_code, last_day)

    get_daily_case = get_daily_cases(last_day)
    get_states = get_state()

    this_year = int(date.today().year)
    current_year_state_wise_cases = get_month_wise_case(state, this_year)
    last_year_state_wise_cases = get_month_wise_case(state, this_year-1)
    state_with_code = get_distinct_state_with_code()

    return {'case_data': case_data,
            'daily_cases': daily_cases,
            'ten_days_case': ten_days_case,
            'get_daily_case': get_daily_case,
            'get_states': get_states,
            'current_year_state_wise_cases': current_year_state_wise_cases,
            'last_year_state_wise_cases': last_year_state_wise_cases,
            'state_with_code': state_with_code}
