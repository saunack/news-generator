import pandas as pd
import os

ROOT_DIR = '../sample_output/'
f = open(os.path.join(ROOT_DIR,'hyperparam_output_log.txt'),'r').read()
text = f.split('#END#')

df = []
for t in text:
    param = t.strip().split('\n')[0]
    if len(param) == 0:
        continue
    param = [int(float(x)*10) if i in [1,3] else int(x) for i,x in enumerate(param.split(', '))]
    df.append(param+['\n'.join(t.strip().split('\n')[1:])])

df = pd.DataFrame(df,columns=['k','t','p','n','text'])
df.to_csv(os.path.join(ROOT_DIR,'hyperparam.csv'),index=False)
