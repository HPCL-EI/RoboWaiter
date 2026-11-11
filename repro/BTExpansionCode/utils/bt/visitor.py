
from py_trees.visitors import VisitorBase


class StatusVisitor(VisitorBase):
    """
    Logging is done with the behaviour's logger.
    """

    def __init__(self) -> None:
        super(StatusVisitor, self).__init__(full=False)
        self.output_str = ""

    def initialise(self) -> None:
        """Override if any resetting of variables needs to be performed between ticks (i.e. visitations)."""
        self.output_str = ""


    def run(self, behavior) -> None:
        """
        Log behaviour information on the debug channel.

        Args:
            behavior: behaviour being visited.
        """
        if behavior.type in ("Sequence","Selector"):
            return
        else:
            self.output_str += f"{behavior.print_name}: {behavior.status.value}\n"

