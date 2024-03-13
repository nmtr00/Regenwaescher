import pandas as pd
import re


class ENase:
    def __init__(self, data_file):
        self.data = data_file
        self.df = None

    def csv(self):
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
                    'MQ2.SV': mq2_sv,
                    'MQ3.SV': mq3_sv,
                    'MQ9B.SV': mq9b_sv,
                    'MQ135.SV': mq135_sv,
                    'MP503.SV': mp503_sv,
                    'HCOH.SV': hcoh_sv
                })

        # Converting list of dictionaries to DataFrame
        self.df = pd.DataFrame(data_dict)

vorne_sensor = ENase('.\Vorne.txt')
vorne_sensor.csv()
hinten_sensor = ENase('.\Hinten.txt')
hinten_sensor.csv()
