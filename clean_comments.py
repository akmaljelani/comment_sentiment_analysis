import pandas as pd
import csv

# df = pd.read_csv('marvel_secret_wars_YT_comments.csv')
# df = df.iloc[:, 7]
# #print(df.head)

def clean_csv(input_file, output_file, column_index):
    df = pd.read_csv(input_file).iloc[:, column_index]
    df.to_csv(output_file, index=False)

# Select column 7 and all the rows
clean_csv('banjir_kelantan_raw.csv', 'banjir_kelantan_clean.csv', 7)