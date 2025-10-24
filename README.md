# Decision Trees - Personal Decision Intelligence System

**Transform your daily routines into executable, analyzable, and optimizable code.**

Decision Trees is a personal decision-making framework that helps you model, track, and improve your daily decision processes. It's an introspection tool that turns your habits and routines into inspectable code, enabling you to understand, analyze, and optimize how you make decisions.

## What is Decision Trees?

Decision Trees codifies your daily decision-making processes as executable Python modules organized in a tree structure. Starting from waking up to going to sleep, it guides you through your routines while tracking your choices, learning from patterns, and helping you achieve your goals.

**Core Philosophy**:
- **Decisions as Code**: Make your thinking process explicit and inspectable
- **Introspection First**: A mirror for examining your own decision patterns
- **Continuous Improvement**: Learn from history to optimize future decisions
- **Goal Alignment**: Every decision should serve a purpose
- **Reduced Cognitive Load**: Automate routine decisions to save mental energy

## Key Features

### 🌳 **Hierarchical Decision Modeling**
Model your life as a tree of decisions, from high-level routines down to specific choices.

### 📊 **Decision History & Analytics**
Track every decision with timestamps, outcomes, and satisfaction ratings. Analyze patterns over time.

### 🎯 **Goal-Oriented Decision Making**
Define goals and see how each decision contributes to achieving them.

### 🧠 **Adaptive Learning**
The system learns from your choices and suggests better defaults over time.

### ⚙️ **Configuration-Driven Routines**
Define routines using YAML configuration files instead of pure Python code.

### 📈 **Progress Tracking**
Monitor your adherence to routines and progress toward goals.

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

**Interactive CLI** (legacy mode):
```bash
python main.py
```

**With trace output** (see decision flow):
```bash
python main.py --trace
```

**Debug specific decision**:
```bash
python main.py --debug-decision daily.wake_up
```

### Example Trace Output

```
> C:\decision-trees\day\routine.py:24
 > C:\decision-trees\daily\wake_up.py:6
switch mode to user/conscious
> C:\decision-trees\day\routine.py:24
 > C:\decision-trees\daily\wake_up.py:9
What day is it? (monday,tuesday,wednesday,thursday,friday,saturday,sunday) (default: Thursday)
[...]
```

## Enhanced System (New!)

The project now includes powerful new features for tracking, learning, and optimization:

### Setting Goals

```python
from core.goals import GoalTracker
from core.context import Goal, DecisionPriority

tracker = GoalTracker()

goal = Goal(
    id="exercise_weekly",
    name="Exercise 4x per week",
    target_value=4.0,
    priority=DecisionPriority.IMPORTANT
)

tracker.create_goal(goal)
tracker.update_progress("exercise_weekly", delta=1.0)
```

### Tracking Decisions

```python
from core.history import DecisionHistory
from core.context import DecisionOutcome

history = DecisionHistory()

outcome = DecisionOutcome(
    decision_id="eat.breakfast",
    choice_made="oatmeal",
    satisfaction_rating=4
)

history.record(outcome)
stats = history.get_statistics("eat.breakfast", days=30)
```

### Configuration-Based Routines

Create `routines/morning.yaml`:

```yaml
name: "Morning Routine"
sequence:
  - decision: daily.wake_up
  - decision: hygiene.shower
  - decision: dress.dress
  - decision: eat.breakfast
```

## Project Structure

```
decision-trees/
├── core/              # Enhanced framework (new)
│   ├── protocols.py   # Decision interfaces
│   ├── context.py     # Rich decision context
│   ├── base.py        # Base classes
│   ├── history.py     # Decision tracking
│   ├── goals.py       # Goal management
│   └── config.py      # Configuration system
│
├── routines/          # YAML routine definitions
├── day/               # Daily routines
├── daily/             # Daily setup (wake, sleep)
├── hygiene/           # Hygiene decisions
├── eat/               # Eating decisions
├── dress/             # Clothing decisions
├── computer/          # Computer usage
├── travel/            # Transportation
├── generic/           # Reusable utilities
└── tests/             # Test suite
```

## Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Comprehensive guide for new users
- **[VISION.md](VISION.md)** - Future direction and enhanced vision
- **[user_profile_example.yaml](user_profile_example.yaml)** - Example user configuration
- **[routines/morning_routine_example.yaml](routines/morning_routine_example.yaml)** - Example routine definition

## Use Cases

- **Personal Routine Optimization**: Model and improve your daily habits
- **Decision Fatigue Reduction**: Automate routine decisions with smart defaults
- **Goal Achievement**: Align daily actions with long-term objectives
- **Self-Understanding**: Analyze your decision patterns and behaviors
- **Habit Building**: Track consistency and build better habits
- **Time Management**: Understand where your time actually goes

## Requirements

- Python 3.11+ (recommended) or Python 3.8+
- Poetry (for dependency management)
- SQLite (included with Python)

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_routine.py
```

## References
* https://en.wikipedia.org/wiki/Decision_tree

## License
`Decision trees` is licensed under the [MIT license](http://choosealicense.com/licenses/mit/). See [LICENSE](LICENSE).
