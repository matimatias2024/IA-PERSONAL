import torch
import random

def get_aggregation_prompt(question, candidates):
    """
    Basado en el prompt de agregación sugerido por RSA para LLMs,
    incorporando las Leyes Persistentes de Newton.
    """
    candidates_str = "\n".join([f"Candidato {i+1}: {c}" for i, c in enumerate(candidates)])
    prompt = f"""<|im_start|>system
LEYES PERSISTENTES (Nivel 5):
1. Ley de No Contradicción: Una contradicción semántica invalida toda la respuesta.
2. Ley de Integridad Matemática: Una ecuación incorrecta invalida toda la cadena lógica.
3. Ley de Evidencia: Si no hay pasos lógicos/evidencia, la confianza es mínima.
Estas leyes son axiomáticas y nunca deben violarse.
<|im_end|>
<|im_start|>user
Analiza las siguientes soluciones candidatas al problema planteado. Tu objetivo es identificar aciertos y errores en los razonamientos para producir una solución final corregida, unificada y precisa que cumpla estrictamente con las LEYES PERSISTENTES.

Problema: {question}

{candidates_str}

Solución Final Corregida y Unificada:
<|im_end|>
<|im_start|>assistant
"""
    return prompt

def sample_population(population, k):
    """
    Muestrea K elementos de la población sin reemplazo.
    """
    if len(population) < k:
        return population * (k // len(population)) + random.sample(population, k % len(population))
    return random.sample(population, k)

def aggregate_step(model, tokenizer, question, population, k, n):
    """
    Realiza un paso de agregación RSA:
    1. Forma N conjuntos de agregación de tamaño K.
    2. Genera una solución mejorada para cada conjunto.
    """
    new_population = []
    for _ in range(n):
        subset = sample_population(population, k)
        prompt = get_aggregation_prompt(question, subset)
        
        inputs = tokenizer([prompt], return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=512, use_cache=True)
        # Extraer solo la respuesta del asistente
        decoded = tokenizer.batch_decode(outputs)[0]
        response = decoded.split("<|im_start|>assistant\n")[-1].split("<|im_end|>")[0].strip()
        new_population.append(response)
        
    return new_population
