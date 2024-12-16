"""The base command."""

from typing import Any, Dict


class Base:
    """A base command template.

    This class is intended to be subclassed. Subclasses must implement the `run()` method.
    """

    def __init__(self, options: Dict[str, Any], *args: Any, **kwargs: Any) -> None:
        """
        Initialize the base command.

        Args:
            options (dict): Command options (e.g., CLI flags).
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        """Execute the command.

        This method must be implemented in subclasses.
        """
        raise NotImplementedError(
            'The run() method must be implemented by the subclass.'
        )
