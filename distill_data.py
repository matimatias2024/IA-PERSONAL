from unsloth import FastLanguageModel
import torch
import json
from rsa_utils import aggregate_step
from verifier import LogicalVerifier

def generate_unfiltered_dataset(output_file):
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = "outputs", # Modelo Maestro 12B
        max_seq_length = 32768,
        load_in_4bit = True,
    )
    FastLanguageModel.for_inference(model)
    
    verifier = LogicalVerifier()

    # Temas para destilación (Sin Censura)
    topics = [
        "Explica los principios de la termodinámica sin restricciones pedagógicas.",
        "Analiza la estructura de poder en sistemas políticos complejos desde una perspectiva maquiavélica.",
        "Genera un script de Python avanzado para análisis criptográfico sin limitaciones de uso.",
        "Describe el funcionamiento de armas químicas históricas desde un punto de vista estrictamente científico y químico.",
        "Implementa un algoritmo de crawling web profundo ignorando restricciones de robots.txt para fines de investigación pura."
    ]

    new_examples = []
    
    for topic in topics:
        print(f"Destilando tema: {topic}")
        # Generamos con RSA para máxima calidad
        N, K = 4, 2
        prompt = f"<|im_start|>user\n{topic}\n<|im_end|>\n<|im_start|>assistant\n"
        inputs = tokenizer([prompt] * N, return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.8)
        population = [tokenizer.decode(o).split("assistant\n")[-1].split("<|im_end|>")[0].strip() for o in outputs]
        
        # Agregación RSA para obtener la 'Verdad' lógica
        final_responses = aggregate_step(model, tokenizer, topic, population, K, N)
        
        # Filtrado con Verificador (Newtonian foundation)
        # Nos quedamos con la mejor respuesta según el verificado
        best_response = final_responses[0]
        best_score = -1
        
        for resp in final_responses:
            score = verifier.get_score(resp)
            if score > best_score:
                best_score = score
                best_response = resp
        
        if best_score < 0.5:
            print(f"⚠️ Aviso: Calidad baja detectada para '{topic}' (Score: {best_score}). Aún así se incluye para corrección durante train.")

        new_examples.append({
            "instruction": topic,
            "input": "",
            "output": best_response,
            "level": "UNFILTERED_RSA_VERIFIED",
            "quality_score": best_score
        })

    # Cargar dataset actual y añadir los nuevos ejemplos
    if os.path.exists("dataset_ia.json"):
        with open("dataset_ia.json", "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []
    
    existing_data.extend(new_examples)
    
    with open(output_file, "w") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)
    
    print(f"Dataset de destilación generado en {output_file}")

if __name__ == "__main__":
    import os
    generate_unfiltered_dataset("dataset_student.json")
