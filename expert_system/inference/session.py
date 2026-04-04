# Consultation session: orchestrates user answers, inference cycles, and audit trail.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

from expert_system.domain.models import KnowledgeBase, Question
from expert_system.inference.engine import ForwardChainingEngine, InferenceResult
from expert_system.inference.working_memory import WorkingMemory


@dataclass
class ConsultationSession:
    """
    Controller for one diagnostic consultation: wraps the engine and keeps a
    human-readable log suitable for explanation / demonstration.
    """

    knowledge: KnowledgeBase
    engine: ForwardChainingEngine = field(init=False)
    consultation_log: List[str] = field(default_factory=list)
    step_index: int = 0

    def __post_init__(self) -> None:
        self.engine = ForwardChainingEngine(self.knowledge, WorkingMemory())

    def reset(self) -> None:
        self.engine.reset()
        self.consultation_log.clear()
        self.step_index = 0
        self._log("-- New consultation: working memory (sigma) cleared --")

    def current_question(self) -> Question | None:
        return self.engine.next_question()

    def submit_boolean_answer(self, yes: bool) -> InferenceResult:
        q = self.engine.next_question()
        if q is None:
            return InferenceResult()

        self.step_index += 1
        fact = q.yes_fact if yes else q.no_fact
        label = "YES" if yes else "NO"
        self._log(f"Q{self.step_index} [{q.id}] User: {label} → fact `{fact}` added to working memory.")

        self.engine.add_observation_fact(fact)
        result = self.engine.run_forward_chaining()

        for line in result.trace:
            self._log(line)
        return result

    def _log(self, line: str) -> None:
        self.consultation_log.append(line)

    def log_text(self) -> str:
        return "\n".join(self.consultation_log) if self.consultation_log else "(No events yet.)"

    def working_memory_lines(self) -> Tuple[str, ...]:
        return tuple(self.engine.memory)
