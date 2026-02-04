import pandas as pd
import numpy as np
import os
from pathlib import Path
import re
from Scripts import functions as fu
import glob

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

def mergeCweAndLine(list):
    return ",".join(
        str(f'{d['line']}({d['cwe']})')
        for d in list
    )

#REWORK
def getCleanDataframe(path):
    df = pd.read_json(path)
    df['labels'] = df['labels'].apply(mergeCweAndLine)

    return df

#REWORK
def getCleanAiDataframe(path):
    df = pd.read_json(path)
    df['filename'] = df['filename'].apply(os.path.basename)

    df['ai_predictions'] = df['ai_predictions'].apply(clearAiPreds)

    return df

def clearAiPreds(list):

    if not list:
        return np.nan

    return ",".join(
        str(f'{d['line_of_code']}({d['label']})')
        for d in list
    )

def apply_normalizations(df, column):
    df[column] = df[column].astype(str)
    df[column] = df[column].apply(lambda x: re.sub(r'\b0(\d{1})\b|\b0(\d{2})\b', r'\1\2', x))
    df[column] = df[column].apply(lambda x: re.sub(r'(CWE-\d+)-0(\d)', r'\1-\2', x))
    df[column] = df[column].apply(lambda x: ','.join(remove_duplicates(x)))
    return df
  
def remove_duplicates(cwe_list):
    if isinstance(cwe_list, float) and np.isnan(cwe_list):
        return []
    else:
        return sorted(list(set(cwe_list.split(','))))
    

def loadFormattedSastResults(directory:str):
    dataframes = []

    path = os.path.join(directory, "*.json")

    for arquivo in glob.glob(path):
        filename = os.path.basename(arquivo).split('_')[1]

        df = pd.read_json(arquivo).rename(columns={'labels': filename})
        df[filename] = df[filename].apply(mergeCweAndLine)

        df = apply_normalizations(df, filename)

        dataframes.append(df)

    return dataframes


def loadAiAnalysisResults(directory:str):
    dataframes = []

    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".json"):
                path = os.path.join(root, filename)

                cleanFilename = filename.split('ai_analysis_')[1]

                df = pd.read_json(path).rename(columns={'ai_predictions': cleanFilename})
                
                df['filename'] = df['filename'].apply(os.path.basename)
                df[cleanFilename] = df[cleanFilename].apply(clearAiPreds)
                df = apply_normalizations(df, cleanFilename)

                dataframes.append(df)

    return dataframes