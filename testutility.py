import logging
import os
import subprocess
import yaml
import pandas as pd
import datetime 
import gc
import re


################
# File Reading #
################

def read_config_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)


def replacer(string, char):
    pattern = char + '{2,}'
    string = re.sub(pattern, char, string) 
    return string

def col_header_val(ddf, table_config):
    '''
    replace whitespaces in the column
    and standardized column names
    '''
    ddf.columns = ddf.columns.str.lower()
    ddf.columns = ddf.columns.str.replace('[^\w]', '_', regex=True)
    ddf.columns = list(map(lambda x: x.strip('_'), list(ddf.columns)))
    ddf.columns = list(map(lambda x: replacer(x, '_'), list(ddf.columns)))
    expected_col = list(map(lambda x: x.lower(), table_config['columns']))
    expected_col.sort()
    ddf.columns = list(map(lambda x: x.lower(), list(ddf.columns)))
    ddf = ddf[expected_col]
    if len(ddf.columns) == len(expected_col) and list(expected_col) == list(ddf.columns):
        print("column name and column length validation passed")
        return 1
    else:
        print("column name and column length validation failed")
        mismatched_columns_file = list(set(ddf.columns).difference(expected_col))
        print("Following File columns are not in the YAML file", mismatched_columns_file)
        missing_YAML_file = list(set(expected_col).difference(ddf.columns))
        print("Following YAML columns are not in the file uploaded", missing_YAML_file)
        logging.info(f'ddf columns: {ddf.columns}')
        logging.info(f'expected columns: {expected_col}')
        return 0
