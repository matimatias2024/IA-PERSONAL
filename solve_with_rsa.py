from unsloth import FastLanguageModel
import torch
from rsa_utils import aggregate_step
from verifier import LogicalVerifier
import sys

def main():
    model_name = "outputs" 
    if len(sys.argv) > 1:
        prompt_text = sys.argv[1]
    else:
        # Prompt de prueba complejo
        prompt_text = "Si un tren sale de A a 100km/h y otro de B a 120km/h hacia A, con una distancia de 440km, ¿en qué punto exacto y cuándo se cruzan? Muestra todos los pasos lógicos."

    verifier = LogicalVerifier()
    max_seq_len = 32768
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = model_name,
        max_seq_length = max_seq_len,
        load_in_4bit = True,
    )
    FastLanguageModel.for_inference(model)

    # Parámetros RSA Nivel 5
    N = 4 # Población
    K = 2 # Agregación
    T = 2 # Pasos RSA
    RECURSIVE_AUDIT = True # Habilitamos auto-auditoría recursiva limitada

    print(f"\n--- Iniciando RSA Nivel 5 + Audit para: {prompt_text} ---")
    
    # 1. Población Inicial
    print("Generando población inicial...")
    # Usamos el prompt base pero pidiendo el formato de Nivel 5
    initial_prompt = f"""<|im_start|>user
{prompt_text}
Recuerda aplicar la Ley de Conservación del Razonamiento y el formato <thought>, <self_critique>, Solución Final.
<|im_end|>
<|im_start|>assistant
"""
    inputs = tokenizer([initial_prompt] * N, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=512, use_cache=True, do_sample=True, temperature=0.7)
    population = [tokenizer.decode(o).split("<|im_start|>assistant\n")[-1].split("<|im_end|>")[0].strip() for o in outputs]

    # 2. Bucle RSA con Audit
    for t in range(T):
        print(f"Paso de Agregación y Auditoría {t+1}/{T}...")
        
        # RSA realiza la agregación y el audit recursivo si se habilita
        population = aggregate_step(model, tokenizer, prompt_text, population, K, N, recursive_audit=RECURSIVE_AUDIT)
        
        for i, res in enumerate(population):
             score = verifier.get_score(res)
             # Extraemos un pedazo del self_critique si existe
             critique_snippet = "No critique"
             if "<self_critique>" in res:
                 critique_snippet = res.split("<self_critique>")[-1].split("</self_critique>")[0][:50].strip() + "..."
             print(f"  Candidato {i+1} [Score: {score}] | Critique: {critique_snippet}")

    # 3. Verificación Final
    print("\n--- Selección y Validación Final ---")
    best_candidate = max(population, key=lambda p: verifier.get_score(p))
    is_valid, violations = verifier.verify_laws(best_candidate)
    
    print(f"Resultado Final Validado: {'PASÓ' if is_valid else 'FALLÓ'}")
    if violations:
        for v in violations:
            print(f"  - {v}")
    
    print("\n--- Resultado Final RSA (Nivel 5) ---")
    print(best_candidate)

if __name__ == "__main__":
    main()
