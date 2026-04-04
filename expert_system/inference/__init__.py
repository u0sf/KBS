"""Inference: working memory + forward-chaining engine."""

from expert_system.inference.engine import ForwardChainingEngine, InferenceResult
from expert_system.inference.session import ConsultationSession
from expert_system.inference.working_memory import WorkingMemory

__all__ = [
    "ConsultationSession",
    "ForwardChainingEngine",
    "InferenceResult",
    "WorkingMemory",
]
