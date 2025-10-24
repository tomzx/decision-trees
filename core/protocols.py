"""
Protocol definitions for decision modules.

These protocols define the contracts that decision modules must implement.
Using protocols (PEP 544) allows for structural subtyping without requiring
explicit inheritance.
"""

from typing import Protocol, runtime_checkable
from person import Person


@runtime_checkable
class Decision(Protocol):
    """
    Protocol for decision modules using the legacy call(person) interface.

    All existing decision modules follow this pattern. This protocol makes
    the implicit interface explicit and enables type checking.

    Example:
        >>> def my_decision_call(person: Person) -> None:
        ...     print(f"Making decision for {person}")
        >>> # This function satisfies the Decision protocol
    """

    def call(self, person: Person) -> None:
        """
        Execute the decision logic for the given person.

        Args:
            person: The Person object representing the current user state

        Returns:
            None. Side effects include modifying person state, printing output,
            or calling other decision modules.
        """
        ...


@runtime_checkable
class DecisionModule(Protocol):
    """
    Protocol for enhanced decision modules with metadata and validation.

    This represents the next-generation interface for decision modules,
    supporting richer context, validation, and result tracking.

    Example:
        >>> class MyDecision:
        ...     name = "my_decision"
        ...     description = "Makes an important choice"
        ...
        ...     def can_execute(self, context):
        ...         return context.person.location == Bed
        ...
        ...     def execute(self, context):
        ...         # Decision logic here
        ...         return DecisionResult(success=True)
    """

    name: str
    """Human-readable name for this decision"""

    description: str
    """Detailed description of what this decision does"""

    def can_execute(self, context: "DecisionContext") -> bool:
        """
        Check if this decision can be executed in the current context.

        Args:
            context: Current decision-making context

        Returns:
            True if preconditions are met, False otherwise
        """
        ...

    def execute(self, context: "DecisionContext") -> "DecisionResult":
        """
        Execute the decision logic with rich context.

        Args:
            context: Current decision-making context with person, time, goals, etc.

        Returns:
            DecisionResult with success status, outcomes, and next steps
        """
        ...
