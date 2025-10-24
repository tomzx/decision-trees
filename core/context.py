"""
Decision context and result types.

This module defines the data structures for passing rich context to decisions
and capturing their outcomes.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
from person import Person


class EnergyLevel(Enum):
    """Energy levels for decision-making capacity"""

    EXHAUSTED = 1
    LOW = 2
    MODERATE = 3
    HIGH = 4
    PEAK = 5


class DecisionPriority(Enum):
    """Priority levels for decisions"""

    OPTIONAL = 1
    RECOMMENDED = 2
    IMPORTANT = 3
    CRITICAL = 4
    REQUIRED = 5


@dataclass
class Goal:
    """
    A goal that guides decision-making.

    Goals provide the "why" behind decisions, enabling the system to
    suggest and optimize choices that align with user objectives.
    """

    id: str
    name: str
    description: str
    target_value: float
    current_value: float = 0.0
    deadline: Optional[datetime] = None
    priority: DecisionPriority = DecisionPriority.IMPORTANT
    tags: list[str] = field(default_factory=list)

    @property
    def progress(self) -> float:
        """Calculate progress toward goal (0.0 to 1.0)"""
        if self.target_value == 0:
            return 1.0
        return min(1.0, self.current_value / self.target_value)

    @property
    def is_complete(self) -> bool:
        """Check if goal has been achieved"""
        return self.current_value >= self.target_value


@dataclass
class Constraint:
    """
    A constraint that limits decision-making options.

    Constraints model real-world limitations like time, energy, or resources.
    """

    name: str
    constraint_type: str  # "time", "energy", "resource", "dependency"
    current_value: float
    max_value: float
    description: str = ""

    @property
    def remaining(self) -> float:
        """Calculate remaining capacity"""
        return max(0.0, self.max_value - self.current_value)

    @property
    def is_exhausted(self) -> bool:
        """Check if constraint is fully consumed"""
        return self.current_value >= self.max_value

    @property
    def utilization(self) -> float:
        """Calculate utilization percentage (0.0 to 1.0)"""
        if self.max_value == 0:
            return 1.0
        return min(1.0, self.current_value / self.max_value)


@dataclass
class DecisionContext:
    """
    Rich context for informed decision-making.

    This context object provides all the information a decision module needs
    to make intelligent choices, including person state, time, goals,
    constraints, and historical patterns.
    """

    person: Person
    """The person making the decision"""

    timestamp: datetime = field(default_factory=datetime.now)
    """When this decision is being made"""

    day_type: Optional[str] = None
    """Type of day (workday, weekend, day_off, etc.)"""

    energy_level: EnergyLevel = EnergyLevel.MODERATE
    """Current energy level (learned from patterns or manually set)"""

    available_time: Optional[timedelta] = None
    """How much time is available for this decision"""

    current_goals: list[Goal] = field(default_factory=list)
    """Active goals that should guide decisions"""

    constraints: list[Constraint] = field(default_factory=list)
    """Active constraints limiting options"""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional context-specific metadata"""

    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Find a goal by ID"""
        return next((g for g in self.current_goals if g.id == goal_id), None)

    def get_constraint(self, name: str) -> Optional[Constraint]:
        """Find a constraint by name"""
        return next((c for c in self.constraints if c.name == name), None)

    def has_time_for(self, duration: timedelta) -> bool:
        """Check if enough time is available"""
        if self.available_time is None:
            return True
        return self.available_time >= duration

    def has_energy_for(self, required_level: EnergyLevel) -> bool:
        """Check if enough energy is available"""
        return self.energy_level.value >= required_level.value


@dataclass
class DecisionResult:
    """
    Result of executing a decision.

    Captures what happened, how long it took, and any impacts on goals
    or state.
    """

    success: bool
    """Whether the decision executed successfully"""

    choice_made: Optional[Any] = None
    """The specific choice that was made (if applicable)"""

    duration: Optional[timedelta] = None
    """How long the decision took to execute"""

    next_decision: Optional[str] = None
    """Suggested next decision module to call"""

    goal_impacts: dict[str, float] = field(default_factory=dict)
    """How this decision affected goals (goal_id -> delta)"""

    state_changes: dict[str, Any] = field(default_factory=dict)
    """Changes made to person state"""

    notes: str = ""
    """Additional notes or explanations"""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional result metadata"""


@dataclass
class DecisionOutcome:
    """
    Tracked outcome of a decision with satisfaction and metrics.

    This extends DecisionResult with subjective feedback and long-term
    tracking information. Used for learning and optimization.
    """

    decision_id: str
    """Unique identifier for the decision module"""

    timestamp: datetime
    """When the decision was made"""

    choice_made: Any
    """The specific choice that was made"""

    duration: timedelta
    """How long it took"""

    satisfaction_rating: Optional[int] = None
    """User satisfaction (1-5 scale), if provided"""

    energy_cost: Optional[EnergyLevel] = None
    """Estimated energy expended"""

    goal_progress: dict[str, float] = field(default_factory=dict)
    """Progress made toward goals (goal_id -> delta)"""

    notes: str = ""
    """User notes about this decision"""

    # Auto-collected metrics
    completion_time: Optional[datetime] = None
    """When the decision was completed"""

    interruptions: int = 0
    """Number of interruptions during execution"""

    context_switches: int = 0
    """Number of context switches during execution"""

    tags: list[str] = field(default_factory=list)
    """Tags for categorization and analysis"""

    @property
    def actual_duration(self) -> Optional[timedelta]:
        """Calculate actual duration from timestamps"""
        if self.completion_time:
            return self.completion_time - self.timestamp
        return self.duration
