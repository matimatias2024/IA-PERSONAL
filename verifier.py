import re

class LogicalVerifier:
    def __init__(self):
        # Axiomatic Laws of Level 5 Reasoning
        self.laws = [
            "Law of Semantic Non-Contradiction: A semantic contradiction invalidates the entire response.",
            "Law of Mathematical Integrity: Any incorrect equation invalidates the entire logical chain.",
            "Law of Evidence: Maximum confidence is capped if no evidence/steps are provided."
        ]

    def verify_math(self, text):
        """
        Mathematical Integrity Law: finds equations and checks them.
        """
        # Improved pattern for equations: match numbers, operators, and result
        # Looking for things like 2+2=4, 10 / 2 = 5
        equations = re.findall(r'(\d+[\s\+\-\*\/\^]+\d+)\s*=\s*(\d+)', text)
        violations = []
        for expr, reported_result in equations:
            try:
                # Basic safety check
                if not re.match(r'^[\d\s\+\-\*\/\^]+$', expr):
                    continue
                safe_expr = expr.replace(' ', '').replace('^', '**')
                actual_result = eval(safe_expr)
                if abs(float(actual_result) - float(reported_result)) > 1e-6:
                    violations.append(f"MATH VIOLATION: {expr.strip()} = {reported_result} (Actual: {actual_result})")
            except Exception as e:
                continue
        return violations

    def verify_contradictions(self, text):
        """
        Semantic Non-Contradiction Law: identifies direct logical collisions.
        """
        sentences = re.split(r'[.!?]\s*', text)
        violations = []
        # Pattern: "X is Y" vs "X is not Y"
        for i, s1 in enumerate(sentences):
            for s2 in sentences[i+1:]:
                # Check for "X es Y" vs "X no es Y"
                m1 = re.search(r'(\w+)\s+es\s+(\w+)', s1, re.IGNORECASE)
                m2 = re.search(r'(\w+)\s+no\s+es\s+(\w+)', s2, re.IGNORECASE)
                if m1 and m2 and m1.group(1).lower() == m2.group(1).lower() and m1.group(2).lower() == m2.group(2).lower():
                    violations.append(f"CONTRADICTION VIOLATION: '{s1.strip()}' vs '{s2.strip()}'")
                
                # English check
                m1en = re.search(r'(\w+)\s+is\s+(\w+)', s1, re.IGNORECASE)
                m2en = re.search(r'(\w+)\s+is\s+not\s+(\w+)', s2, re.IGNORECASE)
                if m1en and m2en and m1en.group(1).lower() == m2en.group(1).lower() and m1en.group(2).lower() == m2en.group(2).lower():
                    violations.append(f"CONTRADICTION VIOLATION: '{s1.strip()}' vs '{s2.strip()}'")
        return violations

    def check_evidence(self, text):
        """
        Law of Evidence: Limits confidence if no proof is shown.
        """
        steps = ["porque", "debido a", "pasos", "entonces", "luego", "therefore", "because", "steps", "since", "proof", "prueba"]
        has_steps = any(kw in text.lower() for kw in steps)
        # Any statement that looks like an answer but has no "because/therefore" is flagged
        if not has_steps:
             return ["EVIDENCE VIOLATION: Response provides a result without showing the logical derivation."]
        return []

    def verify_laws(self, text):
        """
        Applies all persistent laws. Returns (is_valid, violations).
        """
        violations = []
        violations.extend(self.verify_math(text))
        violations.extend(self.verify_contradictions(text))
        
        # Immediate invalidation for math or contradiction
        if violations:
            return False, violations
            
        # Evidence check (doesn't invalidate, but caps)
        evidence_violations = self.check_evidence(text)
        return True, evidence_violations

    def get_score(self, text):
        """
        Axiomatic Scoring: 0.0 if laws are broken.
        """
        is_valid, violations = self.verify_laws(text)
        if not is_valid:
            return 0.0
        
        if violations: # Only evidence violations here
            return 0.5 # Capped confidence
            
        return 1.0

if __name__ == "__main__":
    verifier = LogicalVerifier()
    tests = [
        "El cielo es azul. 2 + 2 = 5. El cielo no es azul.", # Invalid (Math + Contradiction)
        "La respuesta es 42.", # Evidence violation
        "Asumiendo X, entonces Y. 2 * 3 = 6. Por lo tanto la respuesta es correcta." # Valid
    ]
    for t in tests:
        score = verifier.get_score(t)
        valid, viols = verifier.verify_laws(t)
        print(f"--- Text: {t} ---")
        print(f"Score: {score}")
        print(f"Violations: {viols}\n")
