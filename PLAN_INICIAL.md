# Plan de Trabajo para Fine-Tuning y Compresión en RTX 3090

Este documento detalla la estrategia para entrenar y reducir modelos de IA en tu RTX 3090 (24GB VRAM).

## 1. Modelo Recomendado: Mistral NeMo 12B (Abliterated)
Para tu objetivo de tener algo "GPT-level" y des-censurado, este es el mejor punto de partida.

### Por qué Mistral NeMo 12B?
- **Inteligencia:** Supera a los modelos de 7B/8B en razonamiento complejo.
- **Abliterated:** Ya viene con los filtros de "seguridad" (negativas a responder) desactivados mediante vectores ortogonales.
- **Ventana de Contexto:** 128k tokens, ideal para procesar grandes cantidades de datos.
- **Eficiencia en VRAM:** En tu 3090 (24GB), carga en 4-bit ocupando solo ~8GB, dándote mucho margen para entrenar.

## 2. Estrategia de Reducción (4-5B)
1. **Fine-tuning con Unsloth:** Reforzamos el conocimiento específico y la personalidad "uncensored".
2. **Destilación de Conocimiento:** Usaremos este modelo de 12B como "Maestro" para entrenar un modelo más pequeño (como Qwen 2.5 3B o Llama 3.2 3B). Esta es la forma más eficiente de bajar a 4-5B sin perder la "chispa" de inteligencia.

## 3. Herramientas Necesarias
He preparado un script (`setup_env.ps1`) para instalar:
- **PyTorch + CUDA:** El núcleo para el entrenamiento.
- **Unsloth:** Optimización extrema para GPUs NVIDIA serie 3000/4000.
- **Llama-Factory:** Suite completa de entrenamiento.
- **Transformers / PEFT / BitsAndBytes:** Librerías estándar de Hugging Face.

## 4. Próximos Pasos
1. Ejecuta el script de configuración.
2. Elige un dataset para el fine-tuning.
3. Inicia el entrenamiento en QLoRA.
