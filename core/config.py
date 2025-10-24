"""
Configuration system for declarative routine definition.

This module allows users to define routines and decision trees using
YAML configuration files instead of pure Python code, making the system
more accessible and easier to customize.
"""

import yaml
from pathlib import Path
from typing import Any, Optional, Callable
from datetime import time as time_type
from core.base import DecisionNode, DecisionSequence, ConditionalDecision
from core.context import DecisionContext, DecisionResult, DecisionPriority


class ConfigLoader:
    """
    Loads and parses routine configuration files.

    Supports YAML format for defining decision trees declaratively.
    """

    def __init__(self, config_dir: str = "routines"):
        """
        Initialize the configuration loader.

        Args:
            config_dir: Directory containing routine configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)

    def load_routine(self, name: str) -> Optional[dict[str, Any]]:
        """
        Load a routine configuration by name.

        Args:
            name: Name of the routine (without .yaml extension)

        Returns:
            Parsed configuration dictionary, or None if not found
        """
        config_path = self.config_dir / f"{name}.yaml"

        if not config_path.exists():
            return None

        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def save_routine(self, name: str, config: dict[str, Any]):
        """
        Save a routine configuration.

        Args:
            name: Name of the routine
            config: Configuration dictionary
        """
        config_path = self.config_dir / f"{name}.yaml"

        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    def list_routines(self) -> list[str]:
        """
        List all available routine configurations.

        Returns:
            List of routine names
        """
        return [f.stem for f in self.config_dir.glob("*.yaml")]


class RoutineBuilder:
    """
    Builds executable decision trees from configuration.

    Converts declarative YAML definitions into DecisionNode objects
    that can be executed.
    """

    def __init__(self, module_registry: Optional[dict[str, Any]] = None):
        """
        Initialize the routine builder.

        Args:
            module_registry: Dictionary mapping decision module paths to modules
                            (e.g., {"daily.wake_up": wake_up_module})
        """
        self.module_registry = module_registry or {}

    def register_module(self, path: str, module: Any):
        """
        Register a decision module for use in routines.

        Args:
            path: Dot-separated path (e.g., "daily.wake_up")
            module: The module or DecisionNode instance
        """
        self.module_registry[path] = module

    def build_from_config(self, config: dict[str, Any]) -> DecisionNode:
        """
        Build a decision tree from configuration.

        Args:
            config: Configuration dictionary

        Returns:
            Executable DecisionNode
        """
        name = config.get("name", "Unnamed Routine")
        description = config.get("description", "")
        tags = config.get("tags", [])

        if "sequence" in config:
            # Build a sequence of steps
            steps = []
            for step_config in config["sequence"]:
                step = self._build_step(step_config)
                if step:
                    steps.append(step)

            return DecisionSequence(
                name=name,
                steps=steps,
                description=description,
                tags=tags,
                stop_on_failure=config.get("stop_on_failure", False),
            )
        else:
            # Single decision
            return self._build_step(config)

    def _build_step(self, step_config: dict[str, Any]) -> Optional[DecisionNode]:
        """
        Build a single step from configuration.

        Args:
            step_config: Step configuration

        Returns:
            DecisionNode or None if invalid
        """
        if "decision" in step_config:
            # Reference to a registered decision module
            decision_path = step_config["decision"]
            module = self.module_registry.get(decision_path)

            if not module:
                print(f"Warning: Decision module '{decision_path}' not found")
                return None

            # Wrap in a DecisionNode if it's a legacy module
            from core.base import LegacyDecisionAdapter

            if hasattr(module, "call") and not isinstance(module, DecisionNode):
                return LegacyDecisionAdapter(
                    module,
                    name=step_config.get("name", decision_path),
                    description=step_config.get("description", ""),
                )
            else:
                return module

        elif "sequence" in step_config:
            # Nested sequence
            substeps = []
            for substep_config in step_config["sequence"]:
                substep = self._build_step(substep_config)
                if substep:
                    substeps.append(substep)

            return DecisionSequence(
                name=step_config.get("name", "Substeps"),
                steps=substeps,
                description=step_config.get("description", ""),
            )

        elif "conditional" in step_config:
            # Conditional decision
            condition_config = step_config["conditional"]
            condition_fn = self._build_condition(condition_config)

            if_true = self._build_step(condition_config.get("if_true", {}))
            if_false = self._build_step(condition_config.get("if_false", {}))

            return ConditionalDecision(
                name=step_config.get("name", "Conditional"),
                condition=condition_fn,
                if_true=if_true,
                if_false=if_false,
                description=step_config.get("description", ""),
            )

        return None

    def _build_condition(self, condition_config: dict[str, Any]) -> Callable:
        """
        Build a condition function from configuration.

        Args:
            condition_config: Condition configuration

        Returns:
            Function that evaluates to bool
        """
        condition_type = condition_config.get("type")

        if condition_type == "time_range":
            # Check if current time is within range
            start_time = self._parse_time(condition_config.get("start"))
            end_time = self._parse_time(condition_config.get("end"))

            def time_range_condition(context: DecisionContext) -> bool:
                current_time = context.timestamp.time()
                return start_time <= current_time <= end_time

            return time_range_condition

        elif condition_type == "location":
            # Check if person is at specific location
            required_location = condition_config.get("location")

            def location_condition(context: DecisionContext) -> bool:
                return context.person.location.__class__.__name__ == required_location

            return location_condition

        elif condition_type == "day_type":
            # Check day type
            required_day_type = condition_config.get("day_type")

            def day_type_condition(context: DecisionContext) -> bool:
                return context.day_type == required_day_type

            return day_type_condition

        elif condition_type == "energy_level":
            # Check minimum energy level
            min_energy = condition_config.get("min_level", 1)

            def energy_condition(context: DecisionContext) -> bool:
                return context.energy_level.value >= min_energy

            return energy_condition

        else:
            # Default: always true
            return lambda context: True

    def _parse_time(self, time_str: str) -> time_type:
        """
        Parse time string (HH:MM format).

        Args:
            time_str: Time string like "08:30"

        Returns:
            time object
        """
        from datetime import datetime

        return datetime.strptime(time_str, "%H:%M").time()


class UserProfile:
    """
    User profile for personalized decision-making.

    Stores user preferences, customizations, and settings.
    """

    def __init__(self, profile_path: str = "user_profile.yaml"):
        """
        Initialize user profile.

        Args:
            profile_path: Path to profile configuration file
        """
        self.profile_path = Path(profile_path)
        self.data = self._load_profile()

    def _load_profile(self) -> dict[str, Any]:
        """Load profile from file"""
        if not self.profile_path.exists():
            return self._get_default_profile()

        with open(self.profile_path, "r") as f:
            return yaml.safe_load(f) or self._get_default_profile()

    def _get_default_profile(self) -> dict[str, Any]:
        """Get default profile structure"""
        return {
            "name": "User",
            "preferences": {
                "default_wake_time": "07:00",
                "default_sleep_time": "23:00",
                "exercise_frequency": 3,
                "work_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            },
            "goals": [],
            "routines": {
                "morning": "morning_routine",
                "evening": "evening_routine",
            },
            "customizations": {},
        }

    def save(self):
        """Save profile to file"""
        with open(self.profile_path, "w") as f:
            yaml.dump(self.data, f, default_flow_style=False, sort_keys=False)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a profile value.

        Args:
            key: Dot-separated key path (e.g., "preferences.wake_time")
            default: Default value if key not found

        Returns:
            The value or default
        """
        keys = key.split(".")
        value = self.data

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        Set a profile value.

        Args:
            key: Dot-separated key path
            value: Value to set
        """
        keys = key.split(".")
        data = self.data

        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]

        data[keys[-1]] = value
