from dataclasses import dataclass


@dataclass
class ConditionalFormattingRule:

    rule_type: str

    min_value: float = None
    max_value: float = None

    value: str = None

    color: str = "#FFFF00"

    target_range: str = "A1:Z100"

    stop_if_true: bool = False

    # =====================================
    # MATCH
    # =====================================

    def matches(self, value):

        try:

            numeric = float(value)

        except Exception:

            numeric = None

        # ---------------------------------
        # BETWEEN
        # ---------------------------------

        if self.rule_type == "between":

            if numeric is None:
                return False

            return (
                self.min_value
                <= numeric
                <= self.max_value
            )

        # ---------------------------------
        # NOT BETWEEN
        # ---------------------------------

        elif self.rule_type == "not_between":

            if numeric is None:
                return False

            return not (
                self.min_value
                <= numeric
                <= self.max_value
            )

        # ---------------------------------
        # GREATER THAN
        # ---------------------------------

        elif self.rule_type == "greater_than":

            if numeric is None:
                return False

            return numeric > self.min_value

        # ---------------------------------
        # LESS THAN
        # ---------------------------------

        elif self.rule_type == "less_than":

            if numeric is None:
                return False

            return numeric < self.min_value

        # ---------------------------------
        # EQUAL
        # ---------------------------------

        elif self.rule_type == "equal":

            return str(value) == str(self.value)

        # ---------------------------------
        # TEXT CONTAINS
        # ---------------------------------

        elif self.rule_type == "contains":

            return (
                self.value.lower()
                in
                str(value).lower()
            )

        # ---------------------------------
        # BLANK
        # ---------------------------------

        elif self.rule_type == "blank":

            return str(value).strip() == ""

        # ---------------------------------
        # NOT BLANK
        # ---------------------------------

        elif self.rule_type == "not_blank":

            return str(value).strip() != ""

        return False