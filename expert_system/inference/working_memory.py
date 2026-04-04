# Working memory (fact base σ): asserted facts available to the inference engine.

from __future__ import annotations

from typing import AbstractSet, Iterator, Set


class WorkingMemory:
    """
    Blackboard-style fact store. In forward chaining, rules are tested against
    the current contents of working memory (closed-world assumption for this project).
    """

    __slots__ = ("_facts",)

    def __init__(self) -> None:
        self._facts: Set[str] = set()

    def clear(self) -> None:
        self._facts.clear()

    def assert_fact(self, fact: str) -> bool:
        """Insert a fact; returns True if it was newly added."""
        if fact in self._facts:
            return False
        self._facts.add(fact)
        return True

    def contains(self, fact: str) -> bool:
        return fact in self._facts

    def contains_all(self, facts: AbstractSet[str]) -> bool:
        return facts <= self._facts

    def snapshot(self) -> frozenset[str]:
        return frozenset(self._facts)

    def __iter__(self) -> Iterator[str]:
        return iter(sorted(self._facts))

    def __len__(self) -> int:
        return len(self._facts)
