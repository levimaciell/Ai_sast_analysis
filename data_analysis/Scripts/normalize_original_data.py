import pandas as pd
import numpy as np
from pathlib import Path
import re
from Scripts import functions as fu

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_DIR = BASE_DIR / 'vulnerable_files' / 'labels'

PYT1_FILEPATH = BASE_DIR / 'labels.xlsx'
PYT2_FILEPATH = BASE_DIR / 'PyTy2_final_labels.xlsx'
SIDDIQ_FILEPATH = BASE_DIR / 'siddiq_final_labels.xlsx'


def loadAndNormalizePyt1():
    pyt1 = pd.read_excel(PYT1_FILEPATH, engine='openpyxl', sheet_name='true_label')
    pyt1 = pyt1.rename(columns={'Vulline':'true_label'})
    return pyt1

def loadAndNormalizePyt2():
    pyt2 = pd.read_excel(PYT2_FILEPATH, engine='openpyxl')

    df_pyt2 = pd.DataFrame()
    df_pyt2['Filename'] = pyt2['Filename']
    df_pyt2['true_label'] = pyt2['Mr. Chekideh']
    
    return df_pyt2

def loadAndNormalizeSiddiq():
    siddiq = pd.read_excel(SIDDIQ_FILEPATH, engine='openpyxl')

    df_siddiq = pd.DataFrame()
    df_siddiq['Filename'] = siddiq['Filename']
    df_siddiq['true_label'] = siddiq['Mr. Chekideh']
    
    return df_siddiq


def getTrueLabelsDataframe():

    pyt1 = loadAndNormalizePyt1()
    pyt2 = loadAndNormalizePyt2()
    siddiq = loadAndNormalizeSiddiq()

    unified_df = pd.concat(objs=[pyt1, pyt2, siddiq])

    unified_df['true_label'] = unified_df['true_label'].astype('str')
    unified_df['true_label'] = unified_df['true_label'].apply(fu.remove_spaces)
    unified_df['true_label'] = unified_df['true_label'].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))
    unified_df['true_label'] = unified_df['true_label'].str.replace(', ', ',')
    unified_df['true_label'] = unified_df['true_label'].apply(lambda x: ','.join(fu.remove_duplicates(x)))

    unified_df = unified_df.rename(columns={'Filename': 'filename'})

    return unified_df
