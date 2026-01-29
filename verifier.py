import re

class LogicalVerifier:
    def __init__(self):
        pass

    def verify_math(self, text):
        """
        Simple math verification: finds equations like 'X + Y = Z' and checks them.
        """
        # Match pattern like 2 + 2 = 4 or 10 * 5 = 50
        equations = re.findall(r'(\d+[\s\+\-\*\/]+\d+)\s*=\s*(\d+)', text)
        errors = []
        for expr, reported_result in equations:
            try:
                # Basic safety: only allow digits and operators
                if not re.match(r'^[\d\s\+\-\*\/]+$', expr):
                    continue
                actual_result = eval(expr)
                if abs(actual_result - float(reported_result)) > 1e-9:
                    errors.append(f"Math Error: {expr} = {reported_result} (Actual: {actual_result})")
            except Exception:
                continue
        return errors

    def verify_contradictions(self, text):
        """
        Naive contradiction detection using simple patterns.
        """
        sentences = re.split(r'[.!?]\s*', text)
        errors = []
        # Example pattern: "A es B" vs "A no es B"
        # We'll use a very basic check for now
        for i, s1 in enumerate(sentences):
            for s2 in sentences[i+1:]:
                # Check for "X es Y" vs "X no es Y" (very rough)
                match1 = re.search(r'(\w+)\s+es\s+(\w+)', s1, re.IGNORECASE)
                match2 = re.search(r'(\w+)\s+no\s+es\s+(\w+)', s2, re.IGNORECASE)
                if match1 and match2:
                    if match1.group(1).lower() == match2.group(1).lower() and match1.group(2).lower() == match2.group(2).lower():
                        errors.append(f"Contradiction detected: '{s1}' vs '{s2}'")
        return errors

    def get_score(self, text):
        """
        Returns a score from 0 to 1 based on verification.
        0 = many errors, 1 = no errors found.
        """
        math_errors = self.verify_math(text)
        contradiction_errors = self.verify_contradictions(text)
        
        total_errors = len(math_errors) + len(contradiction_errors)
        if total_errors == 0:
            return 1.0
        return max(0.0, 1.0 - (total_errors * 0.2))

if __name__ == "__main__":
    verifier = LogicalVerifier()
    test_text = "El cielo es azul. 2 + 2 = 5. El cielo no es azul."
    print(f"Scoring: '{test_text}'")
    print(f"Score: {verifier.get_score(test_text)}")
    print(f"Math errors: {verifier.verify_math(test_text)}")
    print(f"Contradictions: {verifier.verify_contradictions(test_text)}")
