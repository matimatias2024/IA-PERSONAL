import re

class NewtonianREPL:
    """
    Entorno de ejecución simbólico para RLM (Recursive Language Modeling).
    Soporta acciones de examen y descomposición de contexto.
    """
    def __init__(self, full_context=""):
        self.full_context = full_context
        self.snippets = {}
        self.logs = []

    def execute_action(self, action_string):
        """
        Parsea y ejecuta una acción del tipo <action>command(args)</action>
        """
        match = re.search(r'<action>(.*?)\((.*?)\)</action>', action_string)
        if not match:
            return "ERROR: Formato de acción inválido."

        command = match.group(1).strip()
        args = match.group(2).strip()

        if command == "examine_context":
            return self.examine_context()
        elif command == "get_snippet":
            return self.get_snippet(args)
        elif command == "summarize_snippets":
            return self.summarize_snippets()
        else:
            return f"ERROR: Comando desconocido '{command}'"

    def examine_context(self):
        length = len(self.full_context)
        paragraphs = self.full_context.count('\n\n') + 1
        summary = f"Contexto total: {length} caracteres, aproximadamente {paragraphs} párrafos."
        self.logs.append(f"Examine: {summary}")
        return summary

    def get_snippet(self, range_str):
        """
        range_str format: "start:end"
        """
        try:
            start, end = map(int, range_str.split(':'))
            snippet = self.full_context[start:end]
            snippet_id = f"s{len(self.snippets)}"
            self.snippets[snippet_id] = snippet
            result = f"Snippet {snippet_id} extraído (chars {start}-{end})."
            self.logs.append(f"GetSnippet: {result}")
            return result
        except Exception as e:
            return f"ERROR: Rango inválido '{range_str}': {e}"

    def summarize_snippets(self):
        if not self.snippets:
            return "No hay snippets cargados."
        summary = "Snippets actuales:\n"
        for sid, content in self.snippets.items():
            summary += f"- {sid}: {content[:50]}...\n"
        return summary

    def get_state(self):
        return {
            "num_snippets": len(self.snippets),
            "logs": self.logs
        }
