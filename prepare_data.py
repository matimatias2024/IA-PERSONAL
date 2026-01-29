import json
import os

def create_newtonian_dataset(output_file):
    # Dataset estructurado basado en principios de lógica y matemáticas
    dataset = [
        # Fase 1: Lógica (Nivel A)
        {
            "instruction": "Si todos los hombres son mortales y Sócrates es un hombre, ¿qué se puede concluir?",
            "input": "",
            "output": "Sócrates es mortal. (Silogismo Barbara)",
            "level": "A"
        },
        {
            "instruction": "Resuelve la siguiente ecuación para x: 2x + 5 = 15",
            "input": "",
            "output": "2x = 10 -> x = 5",
            "level": "A"
        },
        # Fase Matemática (Nivel A - Extendido)
        {
            "instruction": "Deriva la función f(x) = x^2 + 3x + 5 respecto a x.",
            "input": "",
            "output": "f'(x) = 2x + 3. (Regla de la potencia y suma de derivadas)",
            "level": "A"
        },
        {
            "instruction": "Calcula la integral indefinida de cos(x).",
            "input": "",
            "output": "sin(x) + C",
            "level": "A"
        },
        # Fase RSA: Agregación (Nivel C)
        {
            "instruction": "Analiza las siguientes soluciones candidatas a un problema y genera una respuesta final corregida y unificada.",
            "input": "Problema: Resuelve 3x - 7 = 11\nCandidato 1: 3x = 4 -> x = 4/3\nCandidato 2: 3x = 18 -> x = 6\nCandidato 3: 3x = 18 -> x = 6",
            "output": "Al analizar los candidatos, el Candidato 1 cometió un error de signo al pasar el 7 al otro lado. Los candidatos 2 y 3 son correctos.\nSolución Final:\n3x = 11 + 7\n3x = 18\nx = 6",
            "level": "C"
        },
        {
            "instruction": "Refina la siguiente solución matemática agregando información de los candidatos.",
            "input": "Problema: Simplifica (x^2 - 1)/(x - 1)\nCandidato A: Es x+1 porque (x-1)(x+1) = x^2 - 1.\nCandidato B: x+2.\nCandidato C: x+1.",
            "output": "La simplificación correcta es x+1. El Candidato A proporciona el razonamiento correcto mediante la factorización de la diferencia de cuadrados (x^2 - 1) = (x-1)(x+1). Al dividir por (x-1), queda x+1.",
            "level": "C"
        },
        # Fase 2: Explicación (Nivel B)
        {
            "instruction": "Explica el principio de conservación de la energía.",
            "input": "",
            "output": "La energía no se crea ni se destruye, solo se transforma. En un sistema cerrado, la energía total permanece constante.",
            "level": "B"
        }
    ]
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    create_newtonian_dataset("dataset_ia.json")
    print("Dataset 'dataset_ia.json' actualizado con éxito con Fase Matemática y RSA.")
