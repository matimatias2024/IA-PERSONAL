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
        },
        # Fase 3: Programación (Nivel D)
        {
            "instruction": "Escribe una función en Python para calcular el n-ésimo número de Fibonacci.",
            "input": "",
            "output": "def fibonacci(n):\n    if n <= 0: return 0\n    elif n == 1: return 1\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b",
            "level": "D"
        },
        {
            "instruction": "Implementa una búsqueda binaria en Python.",
            "input": "",
            "output": "def binary_search(arr, target):\n    low, high = 0, len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == target: return mid\n        elif arr[mid] < target: low = mid + 1\n        else: high = mid - 1\n    return -1",
            "level": "D"
        },
        # Fase RSA: Agregación de Código (Nivel C - Extendido)
        {
            "instruction": "Analiza los siguientes fragmentos de código y genera una versión final corregida y optimizada.",
            "input": "Problema: Función para invertir una cadena.\nCandidato 1: s[::-1]\nCandidato 2: ''.join(reversed(s))\nCandidato 3: For loop manual.",
            "output": "La forma más eficiente y 'pythonic' es usar el slicing (Candidato 1).\nSolución Final:\ndef reverse_string(s):\n    return s[::-1]",
            "level": "C"
        },
        {
            "instruction": "Refina esta implementación de recursión basándote en los candidatos.",
            "input": "Problema: Factorial de n.\nCandidato A: def f(n): return n * f(n-1) si n > 1 else 1\nCandidato B: def fact(n): if n == 0: return 1; return n * fact(n-1)\nCandidato C: Implementación sin caso base.",
            "output": "El Candidato B es el más claro y seguro al incluir explícitamente el caso base n == 0.\nSolución Final:\ndef factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)",
            "level": "C"
        },
        # Fase 4: Optimización y Complejidad (Nivel E)
        {
            "instruction": "¿Cuál es la complejidad temporal (Big-O) de un algoritmo de ordenamiento de burbuja (Bubble Sort)?",
            "input": "",
            "output": "La complejidad temporal de Bubble Sort es O(n^2) en el peor de los casos y en el caso promedio, debido a sus dos bucles anidados que recorren la lista.",
            "level": "E"
        },
        {
            "instruction": "Explica la diferencia entre O(n) y O(log n).",
            "input": "",
            "output": "O(n) representa una complejidad lineal donde el tiempo escala directamente con el tamaño de la entrada. O(log n) es una complejidad logarítmica, típica de algoritmos de divide y vencerás (como búsqueda binaria), donde el tiempo crece muy lentamente a medida que aumenta n.",
            "level": "E"
        },
        # Fase RSA: Optimización Basada en Complejidad (Nivel C - Extendido)
        {
            "instruction": "Analiza las siguientes implementaciones para encontrar un elemento en una lista ordenada y selecciona la más eficiente.",
            "input": "Problema: Buscar un número en lista ordenada de 1 millón de elementos.\nCandidato 1: Búsqueda lineal (for i in lista: if i == x: return True)\nCandidato 2: Búsqueda binaria (O(log n))",
            "output": "El Candidato 2 es significativamente más eficiente. Mientras que la búsqueda lineal (Candidato 1) es O(n) y tomaría en promedio 500k operaciones, la búsqueda binaria (Candidato 2) es O(log n) y resolvería el problema en aproximadamente 20 pasos.\nSolución Final: Utilizar búsqueda binaria.",
            "level": "C"
        },
        {
            "instruction": "Optimiza el siguiente código para reducir su complejidad temporal.",
            "input": "Problema: Encontrar duplicados en una lista.\nCódigo: for i in l: for j in l: if i == j and l.index(i) != l.index(j): return True",
            "output": "El código original es O(n^2) debido a los bucles anidados. Podemos optimizarlo a O(n) usando un conjunto (set) para rastrear elementos ya vistos.\nSolución Final:\ndef tiene_duplicados(l):\n    vistos = set()\n    for x in l:\n        if x in vistos: return True\n        vistos.add(x)\n    return False",
            "level": "C"
        }
    ]
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    create_newtonian_dataset('dataset_ia.json')
    print("Dataset 'dataset_ia.json' actualizado con éxito con todas las fases.")
