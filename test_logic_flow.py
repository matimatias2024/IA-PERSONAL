from laws_manager import LawsManager
from rsa_utils import get_aggregation_prompt

def test_laws():
    print("Testing LawsManager...")
    lm = LawsManager()
    prompt = lm.get_laws_prompt()
    print(prompt)
    assert "Ley de No Contradicción" in prompt
    assert "Ley de Conservación" in prompt
    print("LawsManager OK\n")

def test_prompt_format():
    print("Testing RSA Prompt Format...")
    question = "2+2=?"
    candidates = ["4", "5"]
    prompt = get_aggregation_prompt(question, candidates)
    print(prompt)
    assert "<thought>" in prompt
    assert "<self_critique>" in prompt
    assert "Solución Final Corregida:" in prompt
    print("Prompt Format OK\n")

if __name__ == "__main__":
    try:
        test_laws()
        test_prompt_format()
        print("All dry-run tests PASSED.")
    except Exception as e:
        print(f"Test FAILED: {e}")
