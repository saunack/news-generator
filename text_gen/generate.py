from utils import *
import argparse
import collections

START_TOKEN = "<|START|>"
END_TOKEN = "<END>"

def add_arguments(parser):
    parser.add_argument("--prompt", help="Prompt to run", required=True)
    parser.add_argument("--model_path", default='../model/',help="Default directory for model")
    parser.add_argument(
        "--temperature", "-t", type=float, default=0.6, help="Set temperature"
    )
    parser.add_argument(
        "--length", "-l", type=int, default=500, help="Max length of output"
    )
    parser.add_argument(
        "-k", type=int, default=40, help="Top k smapling"
    )
    parser.add_argument(
        "-p", type=float, default=0.7, help="nucleus sampling (1.0 for disabling)"
    )
    parser.add_argument(
        "-n", type=int, default=3, help="number of samples"
    )
    parser.add_argument(
        "--seed", type=int, default=np.random.randint(1000), help="seed"
    )
    parser.add_argument(
        "--penalty", type=float, default=1.3, help="repetition penalty"
    )

def load(arg_parse):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    n_gpu = torch.cuda.device_count()
    print("Running on device: ", device)

    end_token = END_TOKEN

    args = collections.defaultdict(
        prompt = arg_parse.prompt,
        model_name_or_path=arg_parse.output,
        output_dir=arg_parse.output,
        n_gpu=n_gpu,
        mlm=False,
        device=device,
        model_type='gpt2',
        seed=arg_parse.seed,
        stop_token=end_token, # Set this if your dataset has a special word that indicates the end of a text.
        temperature=arg_parse.temperature,  # temperature sampling. Set this to temperature=1.0 to not use temperature.
        k=arg_parse.k,  # k for top-k sampling. Set this to k=0 to not use top-k.
        p=arg_parse.p,  # p for nucleus sampling. Set this to p=1.0 to not use nucleus sampling.
        repetition_penalty=arg_parse.penalty,
        length=arg_parse.length,  # Number of tokens to generate.
        num_return_sequences=arg_parse.n,  # Number of independently computed samples to generate.
    )

    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)

    args = Struct(**args)
    model = load_model(args)
    return args, model


def generate_from_prompt(args,model):
    prompt = "<|START|>[PROMPT]" + str(args.prompt)

    sequences = generate_samples(args, model, prompt)
    for idx, sequence in enumerate(sequences):
        print('\n====== GENERATION {} ======'.format(idx))
        print(sequence)

if __name__== "__main__" :
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    arg_parse = parser.parse_args()
    args, model = load(arg_parse)
    generate_from_prompt(args,model)
