from repl_env import NewtonianREPL
from rsa_utils import get_aggregation_prompt

def test_repl():
    print("Testing NewtonianREPL...")
    repl = NewtonianREPL("Texto largo de prueba con varias lineas para ver si el REPL funciona correctamente.")
    res = repl.execute_action("<action>examine_context()</action>")
    print(f"Result 1: {res}")
    assert "caracteres" in res
    
    res = repl.execute_action("<action>get_snippet(0:10)</action>")
    print(f"Result 2: {res}")
    assert "Snippet s0" in res
    assert len(repl.snippets) == 1
    print("NewtonianREPL OK\n")

def test_rlm_prompt():
    print("Testing RLM Prompt Format...")
    prompt = get_aggregation_prompt("Pregunta", ["Respuesta A"])
    assert "<action>examine_context()</action>" in prompt
    assert "<action>get_snippet(start:end)</action>" in prompt
    print("RLM Prompt Format OK\n")

if __name__ == "__main__":
    try:
        test_repl()
        test_rlm_prompt()
        print("RLM Integration dry-run PASSED.")
    except Exception as e:
        print(f"Test FAILED: {e}")
