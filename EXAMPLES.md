# Decision Trees - Usage Examples

This document provides practical examples of using the Decision Trees system.

## Example 1: Basic Goal Tracking

Track your exercise goal and monitor progress:

```python
from core.goals import GoalTracker
from core.context import Goal, DecisionPriority
from datetime import datetime, timedelta

# Initialize tracker
tracker = GoalTracker()

# Create exercise goal
exercise_goal = Goal(
    id="weekly_exercise",
    name="Exercise 4 times per week",
    description="Maintain regular physical activity",
    target_value=4.0,
    current_value=0.0,
    deadline=datetime.now() + timedelta(days=7),
    priority=DecisionPriority.IMPORTANT,
    tags=["health", "weekly", "exercise"]
)

# Save the goal
tracker.create_goal(exercise_goal)

# Record exercise sessions
tracker.update_progress("weekly_exercise", delta=1.0, source="health.exercise", notes="Morning run")
tracker.update_progress("weekly_exercise", delta=1.0, source="health.exercise", notes="Gym session")
tracker.update_progress("weekly_exercise", delta=1.0, source="health.exercise", notes="Cycling")

# Check progress
goal = tracker.get_goal("weekly_exercise")
print(f"Progress: {goal.progress * 100:.0f}%")
print(f"Remaining: {goal.target_value - goal.current_value:.0f} sessions")

# Get detailed statistics
stats = tracker.get_statistics("weekly_exercise")
print(f"Total updates: {stats['total_updates']}")
print(f"Net progress: {stats['net_progress']}")
```

## Example 2: Decision History Analysis

Track breakfast choices and find patterns:

```python
from core.history import DecisionHistory
from core.context import DecisionOutcome, EnergyLevel
from datetime import datetime, timedelta

# Initialize history tracker
history = DecisionHistory()

# Record several breakfast decisions
breakfast_choices = [
    ("oatmeal", 4, datetime(2025, 10, 1, 7, 30)),
    ("eggs", 5, datetime(2025, 10, 2, 7, 15)),
    ("oatmeal", 4, datetime(2025, 10, 3, 7, 45)),
    ("skipped", 2, datetime(2025, 10, 4, 8, 30)),
    ("oatmeal", 4, datetime(2025, 10, 5, 7, 20)),
]

for choice, satisfaction, timestamp in breakfast_choices:
    outcome = DecisionOutcome(
        decision_id="eat.breakfast",
        timestamp=timestamp,
        choice_made=choice,
        duration=timedelta(minutes=15),
        satisfaction_rating=satisfaction,
        energy_cost=EnergyLevel.LOW,
        tags=["morning", "food"]
    )
    history.record(outcome)

# Get statistics
stats = history.get_statistics("eat.breakfast", days=30)
print(f"Breakfast count: {stats['count']}")
print(f"Average satisfaction: {stats['avg_satisfaction']:.1f}/5")
print(f"Average duration: {stats['avg_duration_seconds']/60:.0f} minutes")

# Find patterns
patterns = history.find_patterns("eat.breakfast", days=30)
print(f"Most common day: {patterns['most_common_day']}")
print(f"Most common hour: {patterns['most_common_hour']}")

# Learn default choice
default_choice = history.get_learning_defaults("eat.breakfast", days=30)
print(f"Your usual breakfast: {default_choice}")

# Get most frequent decisions
frequent = history.get_most_frequent(days=30, limit=5)
for item in frequent:
    print(f"{item['decision_id']}: {item['frequency']} times")
```

## Example 3: Creating a Custom Decision Node

Build a meditation decision with goal tracking:

```python
from core.base import DecisionNode
from core.context import DecisionContext, DecisionResult, EnergyLevel
from datetime import timedelta

class MeditationDecision(DecisionNode):
    """
    A decision for daily meditation practice.
    Supports different durations and tracks wellness goals.
    """

    def __init__(self):
        super().__init__(
            name="Daily Meditation",
            description="Mindfulness meditation practice",
            tags=["wellness", "mindfulness", "daily"]
        )
        self.duration_options = {
            "5 minutes": timedelta(minutes=5),
            "10 minutes": timedelta(minutes=10),
            "15 minutes": timedelta(minutes=15),
            "20 minutes": timedelta(minutes=20),
        }

    def can_execute(self, context: DecisionContext) -> bool:
        """Check if we have time and energy to meditate"""
        min_duration = timedelta(minutes=5)
        return (
            context.has_time_for(min_duration) and
            context.has_energy_for(EnergyLevel.LOW)
        )

    def execute(self, context: DecisionContext) -> DecisionResult:
        """Execute meditation decision"""
        # In real usage, this would use generic.choose
        # For now, we'll use a default
        duration_choice = "10 minutes"
        duration = self.duration_options[duration_choice]

        print(f"🧘 Starting {duration_choice} meditation session...")
        print("Focus on your breath and be present.")

        # Track impact on wellness goal
        goal_impacts = {}
        wellness_goal = context.get_goal("wellness")
        if wellness_goal:
            # Each meditation contributes to wellness goal
            goal_impacts["wellness"] = 1.0

        # Update person memory
        context.person.remember("meditated_today", True)
        context.person.remember("last_meditation_duration", duration_choice)

        return DecisionResult(
            success=True,
            choice_made=duration_choice,
            duration=duration,
            goal_impacts=goal_impacts,
            state_changes={
                "meditated_today": True,
                "last_meditation_duration": duration_choice
            },
            notes=f"Completed {duration_choice} meditation session"
        )

# Usage
meditation = MeditationDecision()

# Test with context
from person import Person
from location import Bed

person = Person()
context = DecisionContext(person=person, energy_level=EnergyLevel.MODERATE)

if meditation.can_execute(context):
    result = meditation.execute(context)
    print(f"Success: {result.success}")
    print(f"Choice: {result.choice_made}")
    print(f"Duration: {result.duration}")
```

## Example 4: Building a Routine from Configuration

Create and load a routine from YAML:

```python
from core.config import ConfigLoader, RoutineBuilder
from core.context import DecisionContext
from person import Person

# Create a routine configuration
routine_config = {
    "name": "Evening Routine",
    "description": "Wind down routine before bed",
    "tags": ["evening", "daily"],
    "sequence": [
        {
            "decision": "computer.sleep",
            "name": "Turn off computer",
        },
        {
            "name": "Evening Hygiene",
            "sequence": [
                {"decision": "hygiene.teeth", "name": "Brush teeth"},
                {"decision": "hygiene.floss", "name": "Floss"},
            ]
        },
        {
            "decision": "dress.change_pajamas",
            "name": "Change into pajamas",
        },
        {
            "decision": "daily.sleep",
            "name": "Go to sleep",
        }
    ]
}

# Save configuration
loader = ConfigLoader()
loader.save_routine("evening_routine", routine_config)

# Load and build routine
loaded_config = loader.load_routine("evening_routine")
print(f"Loaded routine: {loaded_config['name']}")

# To execute (requires module registry):
# builder = RoutineBuilder(module_registry)
# routine = builder.build_from_config(loaded_config)
# person = Person()
# context = DecisionContext(person=person)
# result = routine.execute(context)
```

## Example 5: User Profile Management

Create and manage a personalized user profile:

```python
from core.config import UserProfile

# Create profile
profile = UserProfile("my_profile.yaml")

# Set preferences
profile.set("preferences.default_wake_time", "06:30")
profile.set("preferences.exercise_frequency", 5)
profile.set("preferences.work_days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

# Set customizations
profile.set("customizations.clothing.cold_weather_threshold", 15)
profile.set("customizations.food.favorite_breakfast", "smoothie")

# Get preferences
wake_time = profile.get("preferences.default_wake_time")
print(f"Wake time: {wake_time}")

exercise_freq = profile.get("preferences.exercise_frequency")
print(f"Exercise {exercise_freq}x per week")

# Save profile
profile.save()
print("Profile saved!")

# Later, load profile
loaded_profile = UserProfile("my_profile.yaml")
print(f"User: {loaded_profile.get('name')}")
```

## Example 6: Conditional Decisions

Create a decision that branches based on conditions:

```python
from core.base import DecisionNode, ConditionalDecision
from core.context import DecisionContext, DecisionResult

class QuickBreakfast(DecisionNode):
    def __init__(self):
        super().__init__("Quick Breakfast", "Fast breakfast option")

    def execute(self, context: DecisionContext) -> DecisionResult:
        print("Having quick breakfast: granola bar and coffee")
        return DecisionResult(success=True, choice_made="quick")

class FullBreakfast(DecisionNode):
    def __init__(self):
        super().__init__("Full Breakfast", "Complete breakfast")

    def execute(self, context: DecisionContext) -> DecisionResult:
        print("Having full breakfast: eggs, toast, and fruit")
        return DecisionResult(success=True, choice_made="full")

# Create conditional decision based on time
def has_time_for_breakfast(context: DecisionContext) -> bool:
    """Check if we have time for full breakfast"""
    from datetime import timedelta
    return context.has_time_for(timedelta(minutes=30))

breakfast_decision = ConditionalDecision(
    name="Breakfast Choice",
    condition=has_time_for_breakfast,
    if_true=FullBreakfast(),
    if_false=QuickBreakfast(),
    description="Choose breakfast based on available time"
)

# Execute
from person import Person
from datetime import timedelta

person = Person()

# Scenario 1: Plenty of time
context1 = DecisionContext(person=person, available_time=timedelta(minutes=60))
result1 = breakfast_decision.execute(context1)
print(f"With time: {result1.choice_made}")

# Scenario 2: Running late
context2 = DecisionContext(person=person, available_time=timedelta(minutes=10))
result2 = breakfast_decision.execute(context2)
print(f"Running late: {result2.choice_made}")
```

## Example 7: Decision Sequence

Chain multiple decisions into a sequence:

```python
from core.base import DecisionNode, DecisionSequence
from core.context import DecisionContext, DecisionResult
from person import Person

class WakeUpDecision(DecisionNode):
    def __init__(self):
        super().__init__("Wake Up", "Get out of bed")

    def execute(self, context: DecisionContext) -> DecisionResult:
        print("☀️ Waking up...")
        context.person.state = "awake"
        return DecisionResult(success=True)

class StretchDecision(DecisionNode):
    def __init__(self):
        super().__init__("Morning Stretch", "Light stretching")

    def execute(self, context: DecisionContext) -> DecisionResult:
        print("🤸 Doing morning stretches...")
        return DecisionResult(
            success=True,
            goal_impacts={"wellness": 0.5}
        )

class HydrateDecision(DecisionNode):
    def __init__(self):
        super().__init__("Hydrate", "Drink water")

    def execute(self, context: DecisionContext) -> DecisionResult:
        print("💧 Drinking water...")
        return DecisionResult(
            success=True,
            goal_impacts={"health": 0.5}
        )

# Create sequence
morning_start = DecisionSequence(
    name="Morning Start Routine",
    steps=[
        WakeUpDecision(),
        StretchDecision(),
        HydrateDecision(),
    ],
    description="First steps after waking up",
    tags=["morning", "essential"]
)

# Execute sequence
person = Person()
context = DecisionContext(person=person)
result = morning_start.execute(context)

print(f"\nSequence completed: {result.success}")
print(f"Notes: {result.notes}")
print(f"Goal impacts: {result.goal_impacts}")
```

## Example 8: Complete Morning Routine with Goals

Put it all together - goals, history, and decisions:

```python
from core.goals import GoalTracker
from core.history import DecisionHistory
from core.context import DecisionContext, DecisionOutcome, Goal, DecisionPriority, EnergyLevel
from person import Person
from datetime import datetime, timedelta

# Initialize systems
goals = GoalTracker()
history = DecisionHistory()
person = Person()

# Create morning routine goal
morning_goal = Goal(
    id="consistent_morning",
    name="Consistent Morning Routine",
    description="Complete morning routine 7 days in a row",
    target_value=7.0,
    priority=DecisionPriority.IMPORTANT,
    tags=["habits", "morning"]
)
goals.create_goal(morning_goal)

# Simulate completing morning routine
def complete_morning_routine(day: int):
    """Simulate one day's morning routine"""
    timestamp = datetime.now() - timedelta(days=7-day)

    # Decision 1: Wake up
    outcome1 = DecisionOutcome(
        decision_id="daily.wake_up",
        timestamp=timestamp,
        choice_made="wake_at_7am",
        duration=timedelta(minutes=5),
        satisfaction_rating=4,
        energy_cost=EnergyLevel.LOW
    )
    history.record(outcome1)

    # Decision 2: Exercise
    outcome2 = DecisionOutcome(
        decision_id="health.exercise",
        timestamp=timestamp + timedelta(minutes=30),
        choice_made="morning_run",
        duration=timedelta(minutes=30),
        satisfaction_rating=5,
        energy_cost=EnergyLevel.MODERATE,
        goal_progress={"consistent_morning": 1.0}
    )
    history.record(outcome2)

    # Update goal progress
    goals.update_progress("consistent_morning", delta=1.0, source="morning_routine")

    print(f"Day {day}: Morning routine completed")

# Complete routine for 7 days
for day in range(1, 8):
    complete_morning_routine(day)

# Check goal progress
goal = goals.get_goal("consistent_morning")
print(f"\n✅ Goal Progress: {goal.progress * 100:.0f}%")
print(f"Goal achieved: {goal.is_complete}")

# Analyze patterns
stats = history.get_statistics("daily.wake_up", days=30)
print(f"\nWake-up stats:")
print(f"- Count: {stats['count']}")
print(f"- Avg satisfaction: {stats['avg_satisfaction']:.1f}/5")

patterns = history.find_patterns("health.exercise", days=30)
print(f"\nExercise patterns:")
print(f"- Total occurrences: {patterns['total_occurrences']}")
print(f"- Most common day: {patterns['most_common_day']}")
```

## Tips for Real Usage

1. **Start Simple**: Begin with basic goal tracking before adding complex routines

2. **Use Actual Modules**: The examples above use simple classes, but in real usage you'd integrate with the existing decision modules in `day/`, `hygiene/`, `eat/`, etc.

3. **Build Module Registry**: Create a registry mapping decision paths to modules:
   ```python
   import daily.wake_up
   import hygiene.teeth
   import eat.breakfast

   registry = {
       "daily.wake_up": daily.wake_up,
       "hygiene.teeth": hygiene.teeth,
       "eat.breakfast": eat.breakfast,
   }
   ```

4. **Track Consistently**: Record decisions daily for meaningful patterns

5. **Review Weekly**: Check statistics and patterns weekly to understand your habits

6. **Adjust Goals**: Start with achievable targets and increase gradually

7. **Customize Profiles**: Tailor your user profile to your actual preferences

8. **Use Configuration**: Define routines in YAML for easy modification

These examples demonstrate the core capabilities of the enhanced Decision Trees system. Combine these patterns to create your personalized decision intelligence system!
