import pandas as pd # pip install pandas
import os

# path to store data metrics output
METRICS_OUTPUT_PATH = 'tools/dataset_metrics/metrics.xlsx'

if os.path.exists(METRICS_OUTPUT_PATH): # check if excel sheet exist
    os.remove(METRICS_OUTPUT_PATH) # remove the excel sheet

# read the datopian csv into a dataframe
datopian_out_df = pd.read_csv('tools/data/datopian.csv', header=0)
# read the AIR csv into a dataframe
air_out_df = pd.read_csv('tools/data/AIR.csv', header=0)