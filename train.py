from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
import os

# 1. Configuration
model_name = "unsloth/Mistral-Nemo-Base-2407-bnb-4bit"
max_seq_len = 4096 
dtype = None 
load_in_4bit = True

# 2. Load Model and Tokenizer
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = model_name,
    max_seq_length = max_seq_len,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

# 3. Add LoRA Adapters
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
)

# 4. Data Preparation
def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    inputs       = examples["input"]
    outputs      = examples["output"]
    texts = []
    for instruction, input, output in zip(instructions, inputs, outputs):
        if input:
            # ChatML style with input (e.g. for RSA aggregation)
            text = f"<|im_start|>user\n{instruction}\n\n{input}\n<|im_end|>\n<|im_start|>assistant\n{output}\n<|im_end|>"
        else:
            text = f"<|im_start|>user\n{instruction}\n<|im_end|>\n<|im_start|>assistant\n{output}\n<|im_end|>"
        texts.append(text)
    return { "text" : texts, }

dataset = load_dataset("json", data_files="dataset_ia.json", split="train")
dataset = dataset.map(formatting_prompts_func, batched = True,)

# 5. Trainer
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_len,
    dataset_num_proc = 2,
    packing = False,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 100, # Aumentado para cubrir los nuevos ejemplos
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        save_strategy = "steps",
        save_steps = 30,
        save_total_limit = 1,
    ),
)

# 6. Train
print("\n--- Iniciando entrenamiento de la Fase Matemática y RSA ---")
trainer_stats = trainer.train()

# 7. Save Model
print("\nGuardando modelo en 'outputs'...")
model.save_pretrained("outputs")
tokenizer.save_pretrained("outputs")

print("\n--- Entrenamiento completado y modelo guardado ---")
