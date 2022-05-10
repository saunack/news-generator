# News Generator using GPT 2
News generator using OpenAI's GPT2 via the [transformers library](https://huggingface.co/transformers/v2.0.0/index.html) provided by [HuggingFace](https://huggingface.co/)

The project is split into 3 parts:
1. Extracting news from the web
2. Fine tuning the model (reference to relevant scripts are provided)
3. Generating news

### Setup
All requirements are listed in requirements.txt (both web scraping and text generation). This project uses pytorch, however, any other framework can be used as well with appropriate changes.

## Steps
### 1. News extraction
Running the script `extract_articles` from the `scraping` folder will be sufficient to generate the file. The script will generate individual files for data scraped for each year and collate all text extracted into a single csv file in the folder `raw_scrape` in the parent directory. The files contain the article title, date and the url of the article.

Articles are currently extracted from a single website (The Hindu, a leading news company in India) as of 2022 January.

### 2. Fine tuning the model
A newer guide has been published [here](https://towardsdatascience.com/natural-language-generation-part-2-gpt-2-and-huggingface-f3acb35bc86a) which uses a similar method of dataset creation and finetuning. For training, the titles of the articles are treated as prompts for the article text. To create a training file from the output of the previous step, a script `create_data.py` in `text_gen` is present.

For a more up to date reference, please see the [original guide](https://github.com/huggingface/transformers/blob/eca77f4719531ecaabe9ec6b2dee6075a391d98a/examples/pytorch/language-modeling/README.md) published by huggingface.


### 3. Generating text
Once the model has been trained, the model can be used to generate text when given a prompt. Usage of the python script for generation is as follows:

```
python3 generate.py --prompt <prompt> \
    -t <temperature> \
    -k <top k samples>\
    --penalty <repetition penalty>\
    -p <nucleus sampling (1.0 for disabling)>\
    -n <number of samples>\
    --seed <seed for random generator>\
    --length <max length of output> 
```

To check outputs for different hyperparameters for the same prompt, use `text_gen/generate.sh` to create a file named `hyperparam.csv` with different values of hyperparameters for the same prompt in `sample_output` folder. Generally, best results are obtained for `k = 50`, `penalty=1.3`, `nucleus sampling=0.7`, `temperature=.6`.
