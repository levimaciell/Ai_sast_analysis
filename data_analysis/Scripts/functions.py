import re
import numpy as np

def remove_spaces(text):
    return re.sub(r'(\d) +\(', r'\1(', text)

def remove_duplicates(cwe_list):
    if isinstance(cwe_list, float) and np.isnan(cwe_list):
        return []
    else:
        return sorted(list(set(cwe_list.split(','))))