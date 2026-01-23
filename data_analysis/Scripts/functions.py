import re
import numpy as np

def remove_spaces(text):
    return re.sub(r'(\d) +\(', r'\1(', text)

def remove_duplicates(cwe_list):
    if isinstance(cwe_list, float) and np.isnan(cwe_list):
        return []
    else:
        return sorted(list(set(cwe_list.split(','))))
    
def reder(df, col):
    '''
    Vai pegar uma coluna, e gerar valores no formato X-Y(CWE-ZZZ), onde X é a linha referenciando a linha do filename do dataframe original, Y é a linha onde está a vuln,
    Z é o numero da CWE
    '''
    temp = df[col][df[col].notna()].str.split(',').explode()
    preds = (temp.index.astype(str) + '-' + temp)
    preds = preds[preds.notna()].values

    return preds


## DIST_LABELS SERA LABELS! PREDS É BANDITPREDS, SEMGREPPREDS, ...
def my_pre(labels, preds):
    '''
    De tudo que eu classifiquei como verdade, quantas realmente eram verdades?
    '''
    #De todos os x que estão em preds, quais também estão em labels? Ou seja, de tudo que classifiquei, quais são realmente verdade?
    tp = [x for x in preds if x in labels]
    if(len(preds) == 0): 
        return 0
    #A parte depois da divisão significa tudo que eu entendi como sendo positivo (true positive + false positive)
    return len(tp)/len([x for x in preds if '-nan' not in x])

def my_rec(labels, preds):
    '''
    De tudo que realmente é verdade (ou seja, o que o especialista disse), quantas eu classifiquei como verdade?
    '''
    rec_samples = [x for x in preds if x in labels]
    return len(rec_samples)/len(labels)

def my_f1(precision, recall):
    return 2 * (precision * recall) / (precision + recall)

def bench_it(labels, preds, attack = ''):
    if attack != '':
        attack = '('+attack+')'
    labels = [x for x in labels if attack.lower() in x.lower()]
    attack.lower()
    preds = [x for x in preds if attack.lower() in x.lower()]
    
    pre = my_pre(labels, preds)
    rec = my_rec(labels, preds)
    f1 = my_f1(pre, rec)

    if (pre + rec) == 0:
        return [pre, rec, 0]
    
    return [pre, rec, f1]