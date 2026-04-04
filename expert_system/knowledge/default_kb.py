# Assembles the default PC troubleshooting knowledge base (declarative module).

from __future__ import annotations

from expert_system.domain.models import KnowledgeBase
from expert_system.knowledge.diagnoses import DIAGNOSES
from expert_system.knowledge.production_rules import ordered_production_rules
from expert_system.knowledge.questions import QUESTIONS


def default_knowledge_base() -> KnowledgeBase:
    return KnowledgeBase(
        title="PC Hardware & Performance Troubleshooting",
        description=(
            "Rule-based expert module covering power delivery, video path, performance, "
            "and thermal behaviour using forward chaining over a production-rule base."
        ),
        questions=QUESTIONS,
        diagnoses=DIAGNOSES,
        production_rules=ordered_production_rules(),
    )
