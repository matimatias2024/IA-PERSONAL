import json
import os

class LawsManager:
    def __init__(self, laws_file="laws.json"):
        # Use absolute path to ensure persistence across tasks
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.laws_file = os.path.join(base_dir, laws_file)
        self.laws = self.load_laws()

    def load_laws(self):
        if os.path.exists(self.laws_file):
            try:
                with open(self.laws_file, "r") as f:
                    return json.load(f)
            except Exception:
                return self.get_default_laws()
        return self.get_default_laws()

    def get_default_laws(self):
        return [
            "Ley de No Contradicción Semántica: Una contradicción lógica invalida toda la respuesta.",
            "Ley de Integridad Matemática: Cualquier error en una ecuación invalida toda la cadena de razonamiento.",
            "Ley de Conservación del Razonamiento: No se permite saltar pasos. Cada transición debe ser explícita.",
            "Ley de Evidencia: La confianza debe ser proporcional a la prueba lógica presentada."
        ]

    def save_laws(self):
        with open(self.laws_file, "w") as f:
            json.dump(self.laws, f, indent=4, ensure_ascii=False)

    def add_law(self, law):
        if law not in self.laws:
            self.laws.append(law)
            self.save_laws()

    def get_laws_prompt(self):
        prompt = "LEYES PERSISTENTES (Axiomáticas):\n"
        for i, law in enumerate(self.laws):
            prompt += f"{i+1}. {law}\n"
        return prompt

if __name__ == "__main__":
    lm = LawsManager()
    print(lm.get_laws_prompt())
