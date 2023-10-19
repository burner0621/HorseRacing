import os
import pandas as pd
import numpy as np

import sys
sys.path.append ("..")
from horse_racing_backend.utils.logging import algoLogger

CSV_FILE = "prompts/data/20230911-grafton-r04.csv"
CSV_FILE = "prompts/data/2.csv"

def parseCSV (file_path):
    # Load the dataset
    data = pd.read_csv(file_path, sep=',', header=0, dtype={'vote': int})
    columns =  list(data.columns)
    # Remove the columns

    # column rename
    rename_dic = {}
    for i in range(len(columns) - 1):
        rename_dic[columns[i]] = columns[i + 1]
    rename_dic[columns[-1]] = 'removed'
    data.rename(columns = rename_dic, inplace = True)
    del data['removed']

    remove_columns = [
        "BetEasy Odds",
        "Jockey Weight Claim",
        "Form Guide Url",
        "Horse Profile Url",
        "Jockey Profile Url",
        "Finish Result (Updates after race)"
    ]
    for col in remove_columns:
        try:
            del data[col]
        except Exception as e:
            algoLogger.error(f"Remove columns from list.", exc_info = True)
    data.insert (0, "Num", list(data.index))

    # Preprocessing the data according to the instructions
    # Setting NaN values in 'Last Start Margin' column to 0 where 'Last Start Finish Position' is 1
    data.loc[data['Last Start Finish Position'] == 1, 'Last Start Margin'] = 0
    # Filling other NaN values with appropriate replacements
    data = data.fillna(data.median(numeric_only=True))
    return data

def getRankHorse():
    data = parseCSV (os.path.join(os.getcwd(), CSV_FILE))

    # List of metrics where higher values are better
    higher_is_better = [
        'Career Strike Rate',
        'Career Place Strike Rate',
        'Average Prize Money',
        'This Track Strike Rate',
        'This Track Place Strike Rate',
        'This Distance Strike Rate',
        'This Distance Place Strike Rate',
        'This Condition Strike Rate',
        'This Condition Place Strike Rate',
        'Jockey Last 100 Strike Rate',
        'Jockey Last 100 Place Strike Rate',
        'Trainer Last 100 Strike Rate',
        'Trainer Last 100 Place Strike Rate'
    ]
    # Normalizing the metrics where higher values are better
    for col in higher_is_better:
        data[col] = (data[col] - data[col].min()) / (data[col].max() - data[col].min())

    # List of metrics where lower values are better
    lower_is_better = [
        'Weight Carried',
        'Barrier',
        'Last Start Finish Position',
        'Last Start Margin'
    ]

    # Normalizing the metrics where lower values are better
    for col in lower_is_better:
        data[col] = 1 - (data[col] - data[col].min()) / (data[col].max() - data[col].min())

    # Combining the metrics with equal weighting to generate a composite score
    weighted_cols = higher_is_better + lower_is_better
    data['Composite Score'] = data[weighted_cols].mean(axis=1)

    # Rescaling the composite scores to be within the 1-10 range
    min_score = data['Composite Score'].min()
    max_score = data['Composite Score'].max()
    data['Composite Score'] = 1 + 9 * (data['Composite Score'] - min_score) / (max_score - min_score)

    # Sorting the horses based on their composite scores
    ranked_horses = data[['Horse Name', 'Composite Score']].sort_values(by='Composite Score', ascending=False).reset_index(drop=True)

    return ranked_horses