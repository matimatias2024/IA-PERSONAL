from unsloth import FastLanguageModel
import torch
from rsa_utils import aggregate_step
from verifier import LogicalVerifier
import sys

def main():
    model_name = "outputs" # Usaremos el modelo después del fine-tuning
    if len(sys.argv) > 1:
        prompt_text = sys.argv[1]
    else:
        prompt_text = "Calcula la derivada de x^2 + 3x + 5"

    verifier = LogicalVerifier()
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
    T = 2 # Pasos recursivos

    print(f"\n--- Iniciando RSA Nivel 5 para: {prompt_text} ---")
    
    # 1. Población Inicial
    print("Generando población inicial...")
    initial_prompt = f"<|im_start|>user\n{prompt_text}\n<|im_end|>\n<|im_start|>assistant\n"
    inputs = tokenizer([initial_prompt] * N, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=256, use_cache=True, do_sample=True, temperature=0.7)
    population = [tokenizer.decode(o).split("<|im_start|>assistant\n")[-1].split("<|im_end|>")[0].strip() for o in outputs]

    # 2. Bucle RSA con Filtrado de Leyes
    for t in range(T):
        print(f"Paso de Agregación {t+1}/{T}...")
        
        # Filtrado preventivo: solo agregamos los que no violan leyes (o todos si todos fallan, para intentar mejora)
        valid_population = [p for p in population if verifier.get_score(p) > 0]
        if not valid_population:
            print("  ADVERTENCIA: Toda la población viola las leyes. Intentando recuperación...")
            current_pop = population
        else:
            current_pop = valid_population

        population = aggregate_step(model, tokenizer, prompt_text, current_pop, K, N)
        for i, res in enumerate(population):
             score = verifier.get_score(res)
             print(f"  Refinado {i+1}: {res[:50]}... [Score: {score}]")

    # 3. Auditoría Final de Leyes
    print("\n--- Auditoría Final de Leyes (Nivel 5) ---")
    # Seleccionamos el mejor puntuado
    best_candidate = max(population, key=lambda p: verifier.get_score(p))
    is_valid, violations = verifier.verify_laws(best_candidate)
    
    print(f"Resultado Final Validado: {'PASÓ' if is_valid else 'FALLÓ'}")
    if violations:
        for v in violations:
            print(f"  - {v}")
    
    print("\n--- Resultado Final RSA ---")
    print(best_candidate)

if __name__ == "__main__":
    main()
