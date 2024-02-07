import csv
import pandas as pd
import argparse as ap


parser = ap.ArgumentParser(description='Date input')
parser.add_argument('-d', '--date', type=str)
date = ''
args = parser.parse_args()
date = args.date

log_file_path = "D:\Dev\EONERC\Regenwaescher\data.log"
with open(log_file_path, 'r') as file:
    log_data = file.read()

#create a list to store datarows
data_row = []

#split lines and skip lines starting with '#'
for line in log_data.split('\n'):
    if not line.startswith('#'):
        #replace tabs with command and append to the data_rows list
        data_row.append(line.split('\t'))

#column names
columns = ['Date', 'Time', 'Ch1: [ppm]', 'Concentration Status', 'Temp [°C]', 'Temp. Status']
df = pd.DataFrame(data_row, columns = columns)

df = df.iloc[7:]
df = df.dropna()
#conver numeric columns to numeric types
numeric_columns = ['Ch1: [ppm]', 'Temp [°C]']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

#reformat 'date column to yymmdd
df['Date'] = df['Date'].dt.strftime('%Y%m%d')
df_evaluated = df[df['Date'] == date]
csv_name = f'{date}.csv'
df_evaluated.to_csv(csv_name, index=False)
print("DataFrame filtered successfully, and saved to log_data_dataframe_filtered.csv:")
print(df_evaluated)