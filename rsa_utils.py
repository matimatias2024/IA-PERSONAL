import torch
import random
import re
from laws_manager import LawsManager
from repl_env import NewtonianREPL

lm = LawsManager()

def get_aggregation_prompt(question, candidates):
    """
    Prompt de agregación RSA mejorado con:
    1. Leyes persistentes dinámicas.
    2. Ley de Conservación de Razonamiento (pasos explícitos).
    3. Internalización de Verificador (<self_critique>).
    4. Capacidades RLM (Acciones simbólicas).
    """
    laws_text = lm.get_laws_prompt()
    candidates_str = "\n".join([f"Candidato {i+1}: {c}" for i, c in enumerate(candidates)])
    
    prompt = f"""<|im_start|>system
{laws_text}
Eres un razonador de Nivel 5 con capacidades RLM (Recursive Language Modeling).
Tu objetivo es sintetizar la solución definitiva.
REGLAS CRÍTICAS:
- Conservación del razonamiento: Muestra cada paso lógico. No omitas cálculos ni deducciones.
- RLM: Si el problema es extenso o complejo, usa acciones para examinar y descomponer el contexto antes de concluir.
- Acciones soportadas: <action>examine_context()</action>, <action>get_snippet(start:end)</action>.
- Internalización: Antes de dar la respuesta final, realiza una auto-crítica interna buscando violaciones de las leyes.
<|im_end|>
<|im_start|>user
Analiza las siguientes soluciones candidatas. Identifica errores y aciertos.
Sigue este formato estrictamente:
<thought>
[Tu razonamiento paso a paso, aplicando la Ley de Conservación y usando RLM si es necesario]
</thought>
<self_critique>
[Busca contradicciones o errores matemáticos en tu propio <thought> basado en las LEYES PERSISTENTES]
</self_critique>
Solución Final Corregida:
[Tu respuesta final]

Problema: {question}

{candidates_str}
<|im_end|>
<|im_start|>assistant
"""
    return prompt

def sample_population(population, k):
    if len(population) < k:
        return population * (k // len(population)) + random.sample(population, k % len(population))
    return random.sample(population, k)

def aggregate_step(model, tokenizer, question, population, k, n, recursive_audit=False, context=""):
    """
    Realiza un paso de agregación RSA con soporte para RLM.
    Si el asisente emite una <action>, el REPL la ejecuta y se re-inyecta el resultado.
    """
    repl = NewtonianREPL(full_context=context if context else question)
    new_population = []
    
    for _ in range(n):
        subset = sample_population(population, k)
        prompt = get_aggregation_prompt(question, subset)
        
        inputs = tokenizer([prompt], return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=1024, use_cache=True)
        decoded = tokenizer.batch_decode(outputs)[0]
        response = decoded.split("<|im_start|>assistant\n")[-1].split("<|im_end|>")[0].strip()
        
        # Detección y ejecución de acciones RLM
        if "<action>" in response:
            action_match = re.search(r'(<action>.*?</action>)', response, re.DOTALL)
            if action_match:
                action_str = action_match.group(1)
                action_result = repl.execute_action(action_str)
                # Re-alimentación (Inference Scaling)
                follow_up_prompt = f"{prompt}{response}\n<|im_start|>user\nResultado REPL: {action_result}\nContinúa con tu razonamiento hasta llegar a la Solución Final.\n<|im_end|>\n<|im_start|>assistant\n"
                inputs = tokenizer([follow_up_prompt], return_tensors="pt").to("cuda")
                outputs = model.generate(**inputs, max_new_tokens=1024, use_cache=True)
                response = tokenizer.batch_decode(outputs)[0].split("<|im_start|>assistant\n")[-1].split("<|im_end|>")[0].strip()

        if recursive_audit:
            audit_prompt = f"""<|im_start|>system
{lm.get_laws_prompt()}
Revisa la siguiente respuesta. Si el bloque <self_critique> detectó errores, corrígelos.
<|im_end|>
<|im_start|>user
Respuesta: {response}
<|im_end|>
<|im_start|>assistant
"""
            inputs = tokenizer([audit_prompt], return_tensors="pt").to("cuda")
            outputs = model.generate(**inputs, max_new_tokens=1024, use_cache=True)
            response = tokenizer.batch_decode(outputs)[0].split("<|im_start|>assistant\n")[-1].split("<|im_end|>")[0].strip()

        new_population.append(response)
        
    return new_population
