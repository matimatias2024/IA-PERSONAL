from unsloth import FastLanguageModel
import torch
import json
import os
from rsa_utils import aggregate_step
from verifier import LogicalVerifier

def generate_unfiltered_dataset(output_file):
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = "outputs", 
        max_seq_length = 32768,
        load_in_4bit = True,
    )
    FastLanguageModel.for_inference(model)
    
    verifier = LogicalVerifier()

    # Temas complejos que requieren RLM (Decomposition + Context Examination)
    topics = [
        "Resume este documento extenso (simulado como texto largo) analizando cada sección con <action>get_snippet</action>.",
        "Compara las teorías económicas de Keynes y Hayek basándote en un análisis detallado por fragmentos.",
        "Resuelve un misterio de lógica deductiva que involucra 10 sospechosos y múltiples pistas dispersas.",
        "Analiza el código fuente de una aplicación compleja buscando vulnerabilidades mediante examen de fragmentos.",
        "Realiza un estudio comparativo de 5 religiones principales analizando sus textos fundamentales por partes."
    ]

    new_examples = []
    
    for topic in topics:
        print(f"Destilando trayectoria RLM + RSA: {topic}")
        N, K = 4, 2
        # Generación inicial
        prompt = f"<|im_start|>user\n{topic}\n<|im_end|>\n<|im_start|>assistant\n"
        inputs = tokenizer([prompt] * N, return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=1024, do_sample=True, temperature=0.8)
        population = [tokenizer.decode(o).split("assistant\n")[-1].split("<|im_end|>")[0].strip() for o in outputs]
        
        # Agregación RSA con soporte REPL (Internal RLM)
        # Pasamos el topic como contexto para que el REPL tenga algo que examinar
        final_responses = aggregate_step(model, tokenizer, topic, population, K, N, recursive_audit=True, context=topic * 50) # Simulamos texto largo
        
        best_response = final_responses[0]
        best_score = -1
        
        for resp in final_responses:
            score = verifier.get_score(resp)
            if score > best_score:
                best_score = score
                best_response = resp
        
        new_examples.append({
            "instruction": topic,
            "input": "",
            "output": best_response,
            "level": "RLM_NEWTONIAN_LEVEL5",
            "quality_score": best_score
        })

    if os.path.exists("dataset_ia.json"):
        with open("dataset_ia.json", "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    
    existing_data.extend(new_examples)
    
    with open(output_file, "w") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
    
    print(f"Dataset RLM Nivel 5 generado en {output_file}")

if __name__ == "__main__":
    generate_unfiltered_dataset("dataset_student.json")
