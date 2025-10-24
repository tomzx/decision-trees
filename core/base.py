"""
Base classes for decision modules.

These base classes provide common functionality and structure for building
decision tree nodes and sequences.
"""

from abc import ABC, abstractmethod
from typing import Optional, Callable
from core.context import DecisionContext, DecisionResult


class DecisionNode(ABC):
    """
    Abstract base class for decision tree nodes.

    This provides the foundation for building structured, well-documented
    decision modules with validation and metadata.
    """

    def __init__(self, name: str, description: str = "", tags: Optional[list[str]] = None):
        """
        Initialize a decision node.

        Args:
            name: Human-readable name for this decision
            description: Detailed description of what this decision does
            tags: Optional tags for categorization (e.g., ["daily", "morning"])
        """
        self.name = name
        self.description = description
        self.tags = tags or []

    def can_execute(self, context: DecisionContext) -> bool:
        """
        Check if this decision can be executed in the current context.

        Override this method to add preconditions. Default implementation
        always returns True.

        Args:
            context: Current decision-making context

        Returns:
            True if preconditions are met, False otherwise
        """
        return True

    @abstractmethod
    def execute(self, context: DecisionContext) -> DecisionResult:
        """
        Execute the decision logic with rich context.

        This is the main method that subclasses must implement.

        Args:
            context: Current decision-making context with person, time, goals, etc.

        Returns:
            DecisionResult with success status, outcomes, and next steps
        """
        pass

    def __call__(self, context: DecisionContext) -> DecisionResult:
        """
        Make the decision node callable.

        This allows using decision nodes like functions: node(context)
        """
        if not self.can_execute(context):
            return DecisionResult(
                success=False, notes=f"Preconditions not met for {self.name}"
            )
        return self.execute(context)


class DecisionSequence(DecisionNode):
    """
    A sequence of decisions to be executed in order.

    This is useful for composing multiple decisions into a routine or workflow.
    """

    def __init__(
        self,
        name: str,
        steps: list[DecisionNode],
        description: str = "",
        tags: Optional[list[str]] = None,
        stop_on_failure: bool = False,
    ):
        """
        Initialize a decision sequence.

        Args:
            name: Name for this sequence
            steps: List of decision nodes to execute in order
            description: Description of the sequence
            tags: Optional tags
            stop_on_failure: If True, stop sequence if any step fails
        """
        super().__init__(name, description, tags)
        self.steps = steps
        self.stop_on_failure = stop_on_failure

    def execute(self, context: DecisionContext) -> DecisionResult:
        """
        Execute all steps in sequence.

        Args:
            context: Decision context

        Returns:
            Combined result from all steps
        """
        results = []
        all_goal_impacts = {}
        all_state_changes = {}

        for step in self.steps:
            if not step.can_execute(context):
                result = DecisionResult(
                    success=False, notes=f"Skipped {step.name}: preconditions not met"
                )
            else:
                result = step.execute(context)

            results.append(result)

            # Accumulate impacts
            for goal_id, delta in result.goal_impacts.items():
                all_goal_impacts[goal_id] = all_goal_impacts.get(goal_id, 0) + delta

            all_state_changes.update(result.state_changes)

            # Stop if step failed and stop_on_failure is True
            if not result.success and self.stop_on_failure:
                return DecisionResult(
                    success=False,
                    notes=f"Sequence stopped at {step.name}: {result.notes}",
                    goal_impacts=all_goal_impacts,
                    state_changes=all_state_changes,
                )

        # All steps completed
        all_succeeded = all(r.success for r in results)
        return DecisionResult(
            success=all_succeeded,
            notes=f"Completed {len(results)} steps",
            goal_impacts=all_goal_impacts,
            state_changes=all_state_changes,
        )


class ConditionalDecision(DecisionNode):
    """
    A decision that executes different branches based on a condition.

    This implements if-then-else logic for decision trees.
    """

    def __init__(
        self,
        name: str,
        condition: Callable[[DecisionContext], bool],
        if_true: DecisionNode,
        if_false: Optional[DecisionNode] = None,
        description: str = "",
        tags: Optional[list[str]] = None,
    ):
        """
        Initialize a conditional decision.

        Args:
            name: Name for this decision
            condition: Function that evaluates the condition
            if_true: Decision to execute if condition is True
            if_false: Decision to execute if condition is False (optional)
            description: Description
            tags: Optional tags
        """
        super().__init__(name, description, tags)
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def execute(self, context: DecisionContext) -> DecisionResult:
        """
        Evaluate condition and execute appropriate branch.

        Args:
            context: Decision context

        Returns:
            Result from the executed branch
        """
        if self.condition(context):
            return self.if_true.execute(context)
        elif self.if_false:
            return self.if_false.execute(context)
        else:
            return DecisionResult(
                success=True, notes=f"Condition false, no else branch for {self.name}"
            )


class LegacyDecisionAdapter(DecisionNode):
    """
    Adapter to wrap legacy call(person) style decision modules.

    This allows using old-style decision modules with the new DecisionNode
    interface.
    """

    def __init__(self, legacy_module, name: str, description: str = ""):
        """
        Initialize the adapter.

        Args:
            legacy_module: Module with a call(person) function
            name: Name for this decision
            description: Description
        """
        super().__init__(name, description)
        self.legacy_module = legacy_module

    def execute(self, context: DecisionContext) -> DecisionResult:
        """
        Execute the legacy module's call function.

        Args:
            context: Decision context (only person is passed to legacy module)

        Returns:
            DecisionResult indicating completion
        """
        try:
            self.legacy_module.call(context.person)
            return DecisionResult(
                success=True, notes=f"Executed legacy module {self.name}"
            )
        except Exception as e:
            return DecisionResult(
                success=False, notes=f"Legacy module failed: {str(e)}"
            )
