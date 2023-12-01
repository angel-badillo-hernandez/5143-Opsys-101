"""`tickcounter` contains the class `TickCounter`.

`TickCounter` represents a single, "global" instance of a counter.

"""
class TickCounter:
    """A class that provides access to a tick counter.

    The `TickCounter` class provides a singular "tick" counter that can be utilized across
    different scopes.
    """

    __counter: int = 0

    @staticmethod
    def get_ticks() -> int:
        """Returns the current number of ticks.

        Returns the current number of ticks.

        Returns:
            int: The current number of ticks.

        """
        return TickCounter.__counter

    @staticmethod
    def increment_ticks(amount: int = 1) -> None:
        """Increments the tick counter.

        Increments the tick counter by one or more ticks.

        """   
        TickCounter.__counter += amount

    def set_ticks(val: int) -> None:
        """Set the current tick count.

        Sets the current tick count.
        """
        TickCounter.__counter = val

    @staticmethod
    def reset_ticks() -> None:
        """Resets the tick counter.

        Sets the tick counter to 0.

        """
        TickCounter.__counter = 0

if __name__ == "__main__":
    help("tickcounter")
