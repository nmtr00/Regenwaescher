import pandas as pd
import re
import os

class ENase:
    def __init__(self, data_file):
        self.data = data_file
        self.df = None

    def csv(self):
        file_name = os.path.splitext(os.path.basename(self.data))[0]
        list = []
        read_file = open(self.data)
        line = read_file.readline()
        while line:
            try:
                list.append(line)
            except ValueError:
                print('Error in line :' + line )
            line = read_file.readline()
        # Regular expression pattern for extracting values
        pattern = r'\[(.*?)\s(.*?)\] MQ2 =([\d.]+) PPM.*?MQ2.SV =([\d.]+).*?MQ3 =([\d.]+) mg/L.*?MQ3.SV =([\d.]+).*?MQ9B =([\d.]+) PPM.*?MQ9B.SV =([\d.]+).*?MQ135 =([\d.]+) PPM.*?MQ135.SV =([\d.]+).*?MP503.SV =([\d.]+).*?HCOH =([\d.]+) PPM.*?HCOH.SV =([\d.]+)'

        # Extracting data into a list of dictionaries
        data_dict = []
        for item in list:
            entries = re.findall(pattern, item)
            for entry in entries:
                date = entry[0]
                time = entry[1]
                mq2_ppm = float(entry[2])
                mq2_sv = float(entry[3])
                mq3_mg_l = float(entry[4])
                mq3_sv = float(entry[5])
                mq9b_ppm = float(entry[6])
                mq9b_sv = float(entry[7])
                mq135_ppm = float(entry[8])
                mq135_sv = float(entry[9])
                mp503_sv = float(entry[10])
                hcoh_ppm = float(entry[11])
                hcoh_sv = float(entry[12])
                data_dict.append({
                    'Date': date.replace('-',''),
                    'Time': time,
                    f'MQ2.SV {file_name}': mq2_sv,
                    f'MQ3.SV {file_name}': mq3_sv,
                    f'MQ9B.SV {file_name}': mq9b_sv,
                    f'MQ135.SV {file_name}': mq135_sv,
                    f'MP503.SV {file_name}': mp503_sv,
                    f'HCOH.SV {file_name}': hcoh_sv
                })

        # Converting list of dictionaries to DataFrame
        self.df = pd.DataFrame(data_dict)
        csv_file_path = f'.\csv\{file_name}.csv'
        self.df.to_csv(csv_file_path, index=False)

vorne_sensor = ENase('.\Vorne.txt')
vorne_sensor.csv()
hinten_sensor = ENase('.\Hinten.txt')
hinten_sensor.csv()

