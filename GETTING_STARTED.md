# Getting Started with Decision Trees

Welcome to Decision Trees - a Personal Decision Intelligence System that helps you model, track, and optimize your daily decision-making processes.

## What is Decision Trees?

Decision Trees transforms your daily routines and decisions into executable, inspectable code. It helps you:

- **Model your routines**: Define your daily habits and decision processes
- **Track your choices**: Record and analyze your decision patterns over time
- **Optimize your life**: Learn from your history and improve your defaults
- **Achieve your goals**: Align your decisions with your long-term objectives
- **Reduce decision fatigue**: Automate routine decisions with smart defaults

## Core Concepts

### 1. Decisions

A **decision** is a single choice point in your routine. Examples:
- What to eat for breakfast
- What to wear
- When to exercise
- How to commute to work

### 2. Decision Trees

A **decision tree** is a sequence of related decisions that form a routine. Examples:
- Morning routine (wake up → hygiene → dress → breakfast)
- Work routine (commute → work → lunch → meetings → commute home)
- Exercise routine (change clothes → warm up → workout → cool down → shower)

### 3. Context

**Context** provides the information needed to make intelligent decisions:
- Current time and day
- Your location
- Your energy level
- Active goals
- Available time
- Weather (future integration)
- Calendar events (future integration)

### 4. Goals

**Goals** give your decisions purpose and direction:
- "Exercise 4x per week"
- "Maintain consistent morning routine"
- "Improve work productivity"
- "Achieve work-life balance"

### 5. History & Learning

The system **learns from your choices** over time:
- Tracks what you decide and when
- Identifies patterns in your behavior
- Suggests better defaults based on history
- Provides insights and analytics

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/tomzx/decision-trees.git
cd decision-trees

# Install dependencies (requires Poetry)
poetry install

# Activate virtual environment
poetry shell
```

### Basic Usage

#### Option 1: Use the Legacy CLI

Run the interactive decision tree:

```bash
python main.py
```

This will guide you through your daily routine, asking questions at each decision point.

**Trace mode** (see decision flow):
```bash
python main.py --trace
```

**Debug mode** (test specific decision):
```bash
python main.py --debug-decision daily.wake_up
```

#### Option 2: Use the Enhanced System (Recommended)

The new system adds goals, history tracking, and configuration-based routines.

```python
from core import DecisionContext
from core.history import DecisionHistory
from core.goals import GoalTracker
from person import Person

# Initialize person
person = Person()

# Create decision context
context = DecisionContext(
    person=person,
    day_type="workday"
)

# Initialize tracking
history = DecisionHistory()
goals = GoalTracker()

# Load and execute routine (coming soon)
# routine = load_routine("morning_routine")
# result = routine.execute(context)
```

## Configuration-Based Routines

The enhanced system allows defining routines in YAML instead of Python.

### Example Routine Configuration

Create `routines/my_morning.yaml`:

```yaml
name: "My Morning Routine"
description: "Simple morning routine"
tags: [daily, morning]

sequence:
  - decision: daily.wake_up
    name: "Wake Up"

  - name: "Hygiene"
    sequence:
      - decision: hygiene.teeth
      - decision: hygiene.shower

  - decision: dress.dress
    name: "Get Dressed"

  - decision: eat.breakfast
    name: "Eat Breakfast"
```

### User Profile

Customize your experience with a user profile (`user_profile.yaml`):

```yaml
name: "Your Name"

preferences:
  default_wake_time: "07:00"
  work_days: [Monday, Tuesday, Wednesday, Thursday, Friday]
  exercise_frequency: 4

goals:
  - id: "health"
    name: "Stay Healthy"
    target_value: 30
    priority: "important"

routines:
  morning: "my_morning"
```

See `user_profile_example.yaml` for a complete example.

## Setting Goals

Goals give your decisions purpose. Here's how to create and track them:

```python
from core.goals import GoalTracker
from core.context import Goal, DecisionPriority

tracker = GoalTracker()

# Create a goal
goal = Goal(
    id="exercise_weekly",
    name="Exercise 4x per week",
    description="Maintain regular exercise habit",
    target_value=4.0,
    priority=DecisionPriority.IMPORTANT,
    tags=["health", "weekly"]
)

tracker.create_goal(goal)

# Update progress
tracker.update_progress("exercise_weekly", delta=1.0, source="health.exercise")

# Check statistics
stats = tracker.get_statistics("exercise_weekly")
print(f"Progress: {stats['progress']*100:.0f}%")
```

## Tracking Decisions

The system automatically tracks your decisions for learning and analytics:

```python
from core.history import DecisionHistory
from core.context import DecisionOutcome, EnergyLevel
from datetime import datetime, timedelta

history = DecisionHistory()

# Record a decision
outcome = DecisionOutcome(
    decision_id="eat.breakfast",
    timestamp=datetime.now(),
    choice_made="oatmeal",
    duration=timedelta(minutes=15),
    satisfaction_rating=4,
    energy_cost=EnergyLevel.LOW
)

history.record(outcome)

# Get statistics
stats = history.get_statistics("eat.breakfast", days=30)
print(f"You've had breakfast {stats['count']} times in the last 30 days")
print(f"Average satisfaction: {stats['avg_satisfaction']:.1f}/5")

# Learn default
default_breakfast = history.get_learning_defaults("eat.breakfast")
print(f"Your usual breakfast: {default_breakfast}")
```

## Creating Custom Decisions

### Method 1: Legacy Style (Python)

Create a new Python module with a `call(person)` function:

```python
# my_decisions/meditation.py
def call(person):
    from generic.choose import choose

    duration = choose(
        "How long do you want to meditate?",
        ["5 minutes", "10 minutes", "15 minutes", "20 minutes"],
        default="10 minutes"
    )

    print(f"Meditating for {duration}...")
    # Update person state
    person.remember("meditated_today", True)
```

### Method 2: Enhanced Style (Recommended)

Create a class extending `DecisionNode`:

```python
# my_decisions/meditation.py
from core.base import DecisionNode
from core.context import DecisionContext, DecisionResult, EnergyLevel
from datetime import timedelta

class MeditationDecision(DecisionNode):
    def __init__(self):
        super().__init__(
            name="Meditation",
            description="Daily meditation practice",
            tags=["wellness", "mindfulness"]
        )

    def can_execute(self, context: DecisionContext) -> bool:
        # Only meditate if we have time and some energy
        return (
            context.has_time_for(timedelta(minutes=5)) and
            context.has_energy_for(EnergyLevel.LOW)
        )

    def execute(self, context: DecisionContext) -> DecisionResult:
        # Ask user for duration
        from generic.choose import choose

        duration = choose(
            "How long do you want to meditate?",
            ["5 minutes", "10 minutes", "15 minutes", "20 minutes"],
            default="10 minutes"
        )

        print(f"Meditating for {duration}...")

        # Update goal progress (if wellness goal exists)
        goal_impacts = {}
        if context.get_goal("wellness"):
            goal_impacts["wellness"] = 1.0

        return DecisionResult(
            success=True,
            choice_made=duration,
            duration=self._parse_duration(duration),
            goal_impacts=goal_impacts,
            notes="Completed meditation session"
        )

    def _parse_duration(self, duration_str: str) -> timedelta:
        minutes = int(duration_str.split()[0])
        return timedelta(minutes=minutes)

# Usage
meditation = MeditationDecision()
```

## Understanding the Project Structure

```
decision-trees/
├── main.py                 # Entry point (legacy CLI)
├── person.py              # Person state model
├── location.py            # Location definitions
├── memory.py              # Memory/fact storage
├── item.py                # Item system
│
├── core/                  # Enhanced framework (new)
│   ├── protocols.py       # Decision interfaces
│   ├── context.py         # Rich decision context
│   ├── base.py            # Base classes for decisions
│   ├── history.py         # Decision tracking
│   ├── goals.py           # Goal management
│   └── config.py          # Configuration system
│
├── routines/              # YAML routine definitions
│   └── *.yaml             # Declarative routines
│
├── day/                   # Daily routine decisions
├── daily/                 # Daily setup (wake, sleep, etc.)
├── hygiene/              # Hygiene routines
├── eat/                  # Eating decisions
├── dress/                # Clothing decisions
├── computer/             # Computer usage
├── travel/               # Transportation
├── work/                 # Work-related decisions
├── health/               # Health & exercise
├── generic/              # Reusable utilities
│   ├── choose.py         # Selection helper
│   ├── askBoolean.py     # Yes/no questions
│   └── ...
│
└── tests/                # Test suite
```

## Next Steps

1. **Review the Vision**: Read [VISION.md](VISION.md) to understand the project's future direction

2. **Customize Your Profile**: Copy `user_profile_example.yaml` to `user_profile.yaml` and customize it

3. **Set Your Goals**: Define what you want to achieve using the goal system

4. **Run the System**: Start making decisions and let the system track them

5. **Create Custom Routines**: Build YAML configurations for your personal routines

6. **Review Analytics**: Check your decision patterns and progress toward goals

7. **Contribute**: Add new decision modules or improve existing ones

## Tips for Success

1. **Start Small**: Begin with one routine (e.g., morning) and expand gradually

2. **Be Consistent**: Use the system daily to build meaningful patterns

3. **Set Realistic Goals**: Start with achievable targets and increase over time

4. **Review Regularly**: Check your statistics weekly to understand your patterns

5. **Customize Defaults**: As you use the system, it learns better defaults

6. **Experiment**: Try different approaches and see what works best for you

## Getting Help

- **Documentation**: See additional docs in the project
- **Examples**: Check `routines/*.yaml` and `user_profile_example.yaml`
- **Vision**: Read `VISION.md` for the bigger picture
- **Code**: Explore the existing decision modules for patterns

## Philosophy

Decision Trees is based on several principles:

1. **Decisions as Code**: Make your thinking process explicit and inspectable
2. **Introspection**: Understanding yourself through your choices
3. **Continuous Improvement**: Learn from history to make better defaults
4. **Goal Alignment**: Every decision should serve a purpose
5. **Reduced Cognitive Load**: Automate routine decisions to save mental energy
6. **Personal Growth**: Use data to identify areas for improvement

Welcome to a more intentional way of living!
