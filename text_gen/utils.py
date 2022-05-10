import torch
import run_language_modeling
import random
import numpy as np

import transformers
from transformers import AutoConfig
from transformers import AutoTokenizer
from transformers import AutoModelWithLMHead, AutoModelForCausalLM

import sys
sys.path.insert(1, 'transformers/examples/text-generation')
import run_generation

def load_model(args):
  config = AutoConfig.from_pretrained(args.model_name_or_path, cache_dir=None)

  model = AutoModelForCausalLM.from_pretrained(
      args.model_name_or_path,
      from_tf=bool(".ckpt" in args.model_name_or_path),
      config=config,
      cache_dir=None
  )
  
  model.to(args.device)
  return model

def set_seed(args):
  """Set the random seed."""
  seed = args.seed
  random.seed(seed)
  np.random.seed(seed)
  torch.manual_seed(seed)
  if args.n_gpu > 0:
    torch.cuda.manual_seed_all(args.seed)

def generate_samples(args, model, prompt_text):
  """Generating sampling for the provided prompt using the provided model."""
  set_seed(args)

  tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, cache_dir=None)

  requires_preprocessing = args.model_type in run_generation.PREPROCESSING_FUNCTIONS.keys()
  encoded_prompt = tokenizer.encode(prompt_text, add_special_tokens=False, return_tensors="pt")
  encoded_prompt = encoded_prompt.to(args.device)

  output_sequences = model.generate(
      input_ids=encoded_prompt,
      max_length=args.length + len(encoded_prompt[0]),
      temperature=args.temperature,
      top_k=args.k,
      top_p=args.p,
      repetition_penalty=args.repetition_penalty,
      do_sample=True,
      num_return_sequences=args.num_return_sequences,
  )

  # Remove the batch dimension when returning multiple sequences
  if len(output_sequences.shape) > 2:
    output_sequences.squeeze_()

  generated_sequences = []

  for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
    generated_sequence = generated_sequence.tolist()

    # Decode text
    text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

    # Remove all text after the stop token
    text = text[: text.find(args.stop_token) if args.stop_token else None]

    # Remove the excess text that was used for pre-processing
    text = text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True)) :]

    # Add the prompt at the beginning of the sequence.
    total_sequence = text#prompt_text + text

    generated_sequences.append(total_sequence)

  return generated_sequences
