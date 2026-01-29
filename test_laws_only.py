from laws_manager import LawsManager

def test_laws():
    print("Testing LawsManager...")
    lm = LawsManager()
    prompt = lm.get_laws_prompt()
    print(prompt)
    assert "Ley de No Contradicción" in prompt
    assert "Ley de Conservación" in prompt
    print("LawsManager OK\n")

if __name__ == "__main__":
    try:
        test_laws()
        print("LawsManager dry-run PASSED.")
    except Exception as e:
        print(f"Test FAILED: {e}")
