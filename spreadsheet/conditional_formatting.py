class ConditionalFormattingRule:

    def __init__(
        self,
        min_value,
        max_value,
        color,
        mode="within"
    ):

        self.min_value = min_value
        self.max_value = max_value

        self.color = color

        # within / outside

        self.mode = mode

    # =====================================
    # MATCH
    # =====================================

    def matches(self, value):

        try:

            number = float(value)

        except Exception:

            return False

        within = (
            self.min_value
            <= number
            <= self.max_value
        )

        if self.mode == "within":

            return within

        elif self.mode == "outside":

            return not within

        return False