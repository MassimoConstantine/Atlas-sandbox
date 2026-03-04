"""Edge-case Python fixture for doc generator stress tests."""

from __future__ import annotations

from typing import Optional, Union


# --- Case 1: Class with no docstring ---
class ClassNoDocstring:
    def process(self, data: str) -> str:
        """Process data and return result."""
        return data


# --- Case 2: Class with no public methods (only __init__) ---
class ClassNoMethods:
    """A class with only __init__ and no public methods."""

    def __init__(self, value: int) -> None:
        """Initialize with a value."""
        self.value = value


# --- Case 3: Class with 20 public methods ---
class BigNode:
    """A node with many methods for stress testing."""

    def method_01(self) -> None:
        """Method 01."""

    def method_02(self) -> None:
        """Method 02."""

    def method_03(self) -> None:
        """Method 03."""

    def method_04(self) -> None:
        """Method 04."""

    def method_05(self) -> None:
        """Method 05."""

    def method_06(self) -> None:
        """Method 06."""

    def method_07(self) -> None:
        """Method 07."""

    def method_08(self) -> None:
        """Method 08."""

    def method_09(self) -> None:
        """Method 09."""

    def method_10(self) -> None:
        """Method 10."""

    def method_11(self) -> None:
        """Method 11."""

    def method_12(self) -> None:
        """Method 12."""

    def method_13(self) -> None:
        """Method 13."""

    def method_14(self) -> None:
        """Method 14."""

    def method_15(self) -> None:
        """Method 15."""

    def method_16(self) -> None:
        """Method 16."""

    def method_17(self) -> None:
        """Method 17."""

    def method_18(self) -> None:
        """Method 18."""

    def method_19(self) -> None:
        """Method 19."""

    def method_20(self) -> None:
        """Method 20."""


# --- Case 4: Function with 10 parameters ---
def many_params_func(
    alpha: str,
    beta: int,
    gamma: float,
    delta: bool,
    epsilon: list[str],
    zeta: dict[str, int],
    eta: tuple[int, ...],
    theta: bytes,
    iota: set[str],
    kappa: Optional[str],
) -> dict[str, str]:
    """A function with 10 typed parameters."""
    return {}


# --- Case 5: Docstring with special markdown characters ---
def markdown_danger_func(data: str) -> str:
    """This docstring has *bold*, **double bold**, and `code` markers.

    It also has # heading-like lines and | pipe | characters |.

    Table-like content:
    | Column A | Column B |
    |----------|----------|
    | value    | other    |
    """
    return data


# --- Case 6: Multiple inheritance ---
class BaseA:
    """Base class A."""


class BaseB:
    """Base class B."""


class BaseC:
    """Base class C."""


class MultiBase(BaseA, BaseB, BaseC):
    """A class that inherits from three base classes."""

    def do_work(self, task: str) -> bool:
        """Perform a task using multi-base capabilities."""
        return True


# --- Case 8: Class with __init__ using complex type hints + public method ---
class ComplexInitNode:
    """Node with complex type hints on __init__."""

    def __init__(
        self,
        config: dict[str, list[int]],
        fallback: Optional[str],
        mode: Union[str, int],
    ) -> None:
        """Initialize with complex types."""
        self.config = config
        self.fallback = fallback
        self.mode = mode

    def run(self, payload: dict[str, Union[str, list[int]]]) -> Optional[dict[str, str]]:
        """Execute the node with a complex payload."""
        return None
