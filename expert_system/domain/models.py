# expert_system/domain/models.py — Abstract knowledge representation (academic layer).

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Mapping, Tuple


@dataclass(frozen=True)
class Diagnosis:
    """
    Terminal hypothesis produced by the inference engine (conclusion of a rule chain).
    Maps to the classical expert-system notion of a goal assertion.
    """

    problem: str
    solution: str
    explanation: str
    supporting_fact_hints: Tuple[str, ...] = ()


@dataclass
class Question:
    """
    Acquisition rule for user data: when prerequisites hold in working memory,
    the system may ask this question; the answer asserts a new fact (yes/no branch).
    """

    id: str
    text: str
    prerequisites: FrozenSet[str] = field(default_factory=frozenset)
    yes_fact: str = ""
    no_fact: str = ""


@dataclass(frozen=True)
class ProductionRule:
    """
    IF–THEN production rule for forward chaining.
    Antecedents: conjunction of facts in working memory.
    Consequent: either FACT:name (assert intermediate conclusion) or DX:id (terminal diagnosis key).
    """

    antecedents: FrozenSet[str]
    consequent: str
    antecedent_labels: Tuple[Tuple[str, str], ...] = ()
    # Optional stable id for trace / documentation (not required for matching)
    rule_id: str = ""


@dataclass(frozen=True)
class KnowledgeBase:
    """
    Bundles the declarative parts of the expert system: what can be asked,
    what can be concluded, and how facts propagate.
    """

    title: str
    description: str
    questions: Tuple[Question, ...]
    diagnoses: Mapping[str, Diagnosis]
    production_rules: Tuple[ProductionRule, ...]

    def all_rules_in_order(self) -> Tuple[ProductionRule, ...]:
        """Ordered rule base as evaluated by forward chaining (priority = list order)."""
        return self.production_rules
