import os
from pathlib import Path

REPO_DIR = Path(os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# Text extraction
url1 = 'http://library.crossfit.com/free/pdf/CFJ_English_Level1_TrainingGuide.pdf'
url2 = 'https://library.crossfit.com/free/pdf/CFJ_English_L2_TrainingGuide.pdf'
header_height = 60  # Main text distance from the top of the page: to remove header
footer_height = 540 # Remove footer
left_margin = 120
right_margin = 490
start_page = 4
end_page = 249
extraction_path = REPO_DIR / "llm/data/extracted_text.jsonl"

# Text processing
min_length = 100

# HF repo
hf_repo = "thafiz/llm-crossfit"

# Dataset
context_length = 2048
batch_size = 1000
test_size = 0.1
shuffle = True

# Training
model_name = 'google/gemma-2b' #'bigscience/bloom-3b' #
lora_r = 16 # attention heads
lora_alpha = 32 # alpha scaling
lora_dropout = 0.05
lora_bias = "none"
lora_task_type = "CAUSAL_LM" # set this for CLM or Seq2Seq

## Trainer config
per_device_train_batch_size = 1 
gradient_accumulation_steps = 1
warmup_steps = 100 
num_train_epochs=3
weight_decay=0.1
learning_rate = 2e-4 
fp16 = True
logging_steps = 1
overwrite_output_dir = True
evaluation_strategy = "no"
save_strategy = "no"
push_to_hub = False

## Data collator
mlm =False

## Generate
max_new_tokens = 50
temperature = 0.5
do_sample = False
