import pandas as pd

state_wise_cases = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')


def get_case(state):
    sub = state_wise_cases[state_wise_cases['State'] == state].iloc[:, 1:5].to_dict('records')
    return sub[0]

