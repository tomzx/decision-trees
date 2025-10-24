"""
Core abstractions and protocols for the Decision Trees framework.

This module defines the fundamental interfaces and base classes that all
decision modules should implement or extend.
"""

from core.protocols import Decision, DecisionModule
from core.context import DecisionContext, DecisionResult, DecisionOutcome
from core.base import DecisionNode, DecisionSequence

__all__ = [
    "Decision",
    "DecisionModule",
    "DecisionContext",
    "DecisionResult",
    "DecisionOutcome",
    "DecisionNode",
    "DecisionSequence",
]
