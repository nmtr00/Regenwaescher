import csv
import pandas as pd
import argparse as ap
import os

parser = ap.ArgumentParser(description='Date input')
parser.add_argument('-d', '--date', type=str)
date = ''
args = parser.parse_args()
date = args.date

log_file_path = ".\current\data.log"
# Add error handling for parsing and data manipulation steps as well.
try:
    with open(log_file_path, 'r') as file:
        log_data = file.read()
except FileNotFoundError:
    print(f"Error: File '{log_file_path}' not found.")
    exit(1)
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

output_directory = ".\current"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

df_evaluated = df[df['Date'] == date]
csv_path = os.path.join(output_directory, f'{date}.csv')
df_evaluated.to_csv(csv_path, index=False)

if df_evaluated.empty:
    print(f"No data found for the specified date: {date}")
else:
    print(f"DataFrame filtered successfully and saved to: {csv_path}")
    print(df_evaluated)