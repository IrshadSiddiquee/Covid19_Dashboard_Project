import pandas as pd
import covid19dashboard.constant as const
import numpy as np
from datetime import date, timedelta

# import state wise cases from API
df_state_wise_cases = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')

# import month wise cases from API
df_month_wise_cases = pd.read_csv("https://api.covid19india.org/csv/latest/states.csv")

# import state wise per day cases from API
df_state_wise_per_day_cases = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv")

# Create a dataframe to store state name with state code
df_state_with_code = pd.DataFrame(df_state_wise_cases,
                                  columns=[const.STR_STATE, const.STR_STATE_CODE]).to_dict(const.STR_RECORDS)
