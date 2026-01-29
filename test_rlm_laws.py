from repl_env import NewtonianREPL
from laws_manager import LawsManager

def test_repl():
    print("Testing NewtonianREPL...")
    repl = NewtonianREPL("Texto de prueba.")
    res = repl.execute_action("<action>examine_context()</action>")
    print(f"Result: {res}")
    assert "caracteres" in res
    print("NewtonianREPL OK\n")

def test_laws_and_rlm_concepts():
    print("Testing Laws + RLM Concepts...")
    lm = LawsManager()
    prompt = lm.get_laws_prompt()
    print(prompt)
    assert "Newton" in prompt or "Ley" in prompt
    print("Concepts OK\n")

if __name__ == "__main__":
    try:
        test_repl()
        test_laws_and_rlm_concepts()
        print("RLM + Laws dry-run PASSED.")
    except Exception as e:
        print(f"Test FAILED: {e}")
