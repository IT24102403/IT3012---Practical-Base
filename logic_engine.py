# logic_engine.py

class KnowledgeBase:
    """Stores known facts and Horn clause rules, running forward chaining inference."""

    def __init__(self):
        # Stores unique active string facts (e.g., 'TargetVisible', 'HasDust')
        self.facts = set()
        # Stores rules as tuples: ([premise_1, premise_2, ...], conclusion)
        self.rules = []

    def tell_fact(self, fact_string: str):
        """Adds a raw sensor fact to the Knowledge Base."""
        self.facts.add(fact_string)

    def tell_rule(self, premise_list: list, conclusion_string: str):
        """Adds a Horn Clause rule: IF all premises are true, THEN conclusion is true."""
        self.rules.append((premise_list, conclusion_string))

    def clear_facts(self):
        """Clears temporary percept facts between evaluation steps."""
        self.facts.clear()

    def forward_chain(self):
        """Data-driven inference loop that applies Modus Ponens until no new facts can be derived."""
        new_facts_added = True
        
        while new_facts_added:
            new_facts_added = False
            for premises, conclusion in self.rules:
                # If we haven't already proven this conclusion
                if conclusion not in self.facts:
                    # Modus Ponens Check: Are ALL required premises currently known facts?
                    if all(premise in self.facts for premise in premises):
                        self.facts.add(conclusion)
                        new_facts_added = True