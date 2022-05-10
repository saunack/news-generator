import os
import pandas as pd
import random
import glob

INPUT_DIR = '../raw_scrape/'

def create_dataset(df,title,content):
  start_token = "<|START|>"
  end_token = "<|END|>"
  prompt = "[PROMPT]"
  response = "[RESPONSE]"
  text_series = start_token + prompt + df[title] + response + df[content] + end_token
  return text_series.tolist()

for filename in glob.glob(f"{INPUT_DIR}/*.csv"):
    train = []
    try:
        df = pd.read_csv(filename)
        df = df.dropna(how='any')
        if 'master' in filename:
            master = create_dataset(df,'Title','Content')
            train.extend(master)
        #elif 'japan' in filename:
        #    japan = create_dataset(df[df['Headline'].str.len()<100],'Headline','Content')
        #    train.extend(japan)
    except:
        print(f"{filename} not processed")
        pass

    random.shuffle(train)
    text = "\n".join(train)
    
with open('training.txt','w')as f:
    f.write(text)

