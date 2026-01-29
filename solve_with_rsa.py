from unsloth import FastLanguageModel
import torch
from rsa_utils import aggregate_step
import sys

def main():
    model_name = "outputs" # Usaremos el modelo después del fine-tuning
    if len(sys.argv) > 1:
        prompt_text = sys.argv[1]
    else:
        prompt_text = "Calcula la derivada de x^2 + 3x + 5"

    max_seq_len = 131072
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = model_name,
        max_seq_length = max_seq_len,
        load_in_4bit = True,
    )
    FastLanguageModel.for_inference(model)

    # Parámetros RSA
    N = 4 # Tamaño de la población
    K = 2 # Tamaño de agregación
    T = 2 # Pasos recursivos (reducido para demo rápida)

    print(f"\n--- Iniciando RSA para: {prompt_text} ---")
    
    # 1. Población Inicial
    print("Generando población inicial...")
    initial_prompt = f"<|im_start|>user\n{prompt_text}\n<|im_end|>\n<|im_start|>assistant\n"
    inputs = tokenizer([initial_prompt] * N, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=256, use_cache=True, do_sample=True, temperature=0.7)
    population = [tokenizer.decode(o).split("<|im_start|>assistant\n")[-1].split("<|im_end|>")[0].strip() for o in outputs]

    # 2. Bucle RSA
    for t in range(T):
        print(f"Paso de Agregación {t+1}/{T}...")
        population = aggregate_step(model, tokenizer, prompt_text, population, K, N)
        for i, res in enumerate(population):
             print(f"  Candidato Refinado {i+1}: {res[:100]}...")

    # 3. Resultado Final (por voto o el primero)
    print("\n--- Resultado Final RSA ---")
    print(population[0])

if __name__ == "__main__":
    main()
