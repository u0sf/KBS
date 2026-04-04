# Forward-chaining inference engine: applies production rules until fixpoint or diagnosis.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from expert_system.domain.models import Diagnosis, KnowledgeBase, ProductionRule, Question
from expert_system.inference.working_memory import WorkingMemory


@dataclass
class InferenceResult:
    """Structured outcome of an inference cycle (may be empty if no rule concludes)."""

    diagnosis: Optional[Diagnosis] = None
    fired_rule: Optional[ProductionRule] = None
    matched_conditions: Tuple[str, ...] = ()
    confidence: float = 0.0
    trace: Tuple[str, ...] = ()
    derived_facts: Tuple[str, ...] = ()


class ForwardChainingEngine:
    """
    Implements forward chaining (data-driven reasoning):
    repeatedly match rule antecedents against working memory and assert consequents
    until no new information is produced or a terminal diagnosis is reached.
    """

    def __init__(self, knowledge: KnowledgeBase, memory: Optional[WorkingMemory] = None) -> None:
        self._kb = knowledge
        self.memory = memory or WorkingMemory()
        self._rules: Tuple[ProductionRule, ...] = knowledge.all_rules_in_order()

    def reset(self) -> None:
        self.memory.clear()

    def add_observation_fact(self, fact: str) -> None:
        """User- or sensor-asserted fact (e.g. answer to a symptom question)."""
        self.memory.assert_fact(fact)

    def _confidence_for_rule(self, rule: ProductionRule) -> float:
        n = len(rule.antecedents)
        base = 0.55 + 0.09 * max(n, 1)
        return min(0.95, base)

    def _human_conditions(self, rule: ProductionRule) -> Tuple[str, ...]:
        if not rule.antecedent_labels:
            return tuple(sorted(rule.antecedents))
        labels = dict(rule.antecedent_labels)
        return tuple(labels.get(a, a) for a in sorted(rule.antecedents))

    def run_forward_chaining(self) -> InferenceResult:
        trace: List[str] = []
        derived: List[str] = []
        diagnosis: Optional[Diagnosis] = None
        fired: Optional[ProductionRule] = None
        changed = True

        while changed:
            changed = False
            for rule in self._rules:
                if not self.memory.contains_all(rule.antecedents):
                    continue

                cons = rule.consequent
                label = rule.rule_id or "anonymous_rule"

                if cons.startswith("FACT:"):
                    new_fact = cons.split(":", 1)[1]
                    if self.memory.assert_fact(new_fact):
                        changed = True
                        derived.append(new_fact)
                        trace.append(
                            f"[Forward chain] {label}: antecedents satisfied → ASSERT {new_fact}"
                        )
                elif cons.startswith("DX:"):
                    dx_id = cons.split(":", 1)[1]
                    diagnosis = self._kb.diagnoses.get(dx_id)
                    fired = rule
                    trace.append(
                        f"[Forward chain] {label}: antecedents satisfied → CONCLUSION {dx_id}"
                    )
                    changed = False
                    break

        if diagnosis and fired:
            return InferenceResult(
                diagnosis=diagnosis,
                fired_rule=fired,
                matched_conditions=self._human_conditions(fired),
                confidence=self._confidence_for_rule(fired),
                trace=tuple(trace),
                derived_facts=tuple(derived),
            )
        return InferenceResult(trace=tuple(trace), derived_facts=tuple(derived))

    def question_answered(self, q: Question) -> bool:
        return self.memory.contains(q.yes_fact) or self.memory.contains(q.no_fact)

    def next_question(self) -> Optional[Question]:
        for q in self._kb.questions:
            if not self.memory.contains_all(q.prerequisites):
                continue
            if self.question_answered(q):
                continue
            return q
        return None
