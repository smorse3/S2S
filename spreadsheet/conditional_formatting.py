class ConditionalFormattingRule:

    def __init__(
        self,
        column,
        operator,
        value,
        bg="yellow"
    ):

        self.column = column

        self.operator = operator

        self.value = value

        self.bg = bg

    # ==========================================
    # EVALUATION
    # ==========================================

    def matches(self, cell_value):

        try:

            if self.operator == ">":

                return (
                    float(cell_value)
                    >
                    float(self.value)
                )

            if self.operator == "<":

                return (
                    float(cell_value)
                    <
                    float(self.value)
                )

            if self.operator == "=":

                return (
                    str(cell_value)
                    ==
                    str(self.value)
                )

        except Exception:

            return False

        return False