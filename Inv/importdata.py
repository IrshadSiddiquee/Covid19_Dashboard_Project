import pandas as pd

state_wise_cases = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')


def get_case(state):
    sub = state_wise_cases[state_wise_cases['State'] == state].iloc[:, 1:5].to_dict('records')
    return sub[0]


# print(get_case('Delhi'))

# print('Confirmed Case - ' + str(state_wise_cases['confirmed'].sum()))
# print('Death Case - ' + str(state_wise_cases['deaths'].sum()))
# print('Recover Case - ' + str(state_wise_cases['recovered'].sum()))
# print('Active Case - ' + str(state_wise_cases['active'].sum()))
#
# print(state_wise_cases.groupby('state')['confirmed', 'deaths', 'recovered', 'active'].sum())
