import pandas as pd


class SpreadsheetModel:

    def __init__(self):

        self.default_rows = 100
        self.default_cols = 26

        self.df = pd.DataFrame(
            "",
            index=range(self.default_rows),
            columns=range(self.default_cols)
        )

        # =====================================
        # CURRENT ACTIVE CELL
        # =====================================

        self.current_row = 0
        self.current_col = 0

        # =====================================
        # MOVEMENT SETTINGS
        # =====================================

        self.direction = "right"

        self.wrap_enabled = True
        
        # =====================================
        # CONDITIONAL FORMATTING
        # =====================================

        self.conditional_rules = []

    # =====================================
    # ENSURE SIZE
    # =====================================

    def ensure_size(self, row, col):

        while row >= len(self.df.index):

            self.df.loc[len(self.df)] = [
                ""
                for _ in range(
                    len(self.df.columns)
                )
            ]

        while col >= len(self.df.columns):

            self.df[
                len(self.df.columns)
            ] = ""

    # =====================================
    # CELL ACCESS
    # =====================================

    def set_cell(
        self,
        row,
        col,
        value
    ):

        self.ensure_size(row, col)

        self.df.iat[row, col] = value

    def get_cell(
        self,
        row,
        col
    ):

        self.ensure_size(row, col)

        return self.df.iat[row, col]

       # =====================================
    # NAVIGATION
    # =====================================

    def move_next(self):

        # =================================
        # MOVE RIGHT
        # =================================

        if self.direction == "right":

            next_row = self.current_row
            next_col = self.current_col + 1

            self.ensure_size(
                next_row,
                next_col
            )

            # ---------------------------------
            # AUTO RETURN
            # ---------------------------------

            if self.wrap_enabled:

                # CHECK:
                # DOES NEXT COLUMN
                # CONTAIN DATA ABOVE CURRENT ROW?

                column_has_data = False

                for r in range(0, self.current_row):

                    value = self.get_cell(
                        r,
                        next_col
                    )

                    # DEBUG
                    print(
                        "CHECK COLUMN:",
                        r,
                        next_col,
                        value
                    )

                    if (
                        value is not None
                        and
                        str(value).strip() != ""
                    ):

                        column_has_data = True
                        break

                # ---------------------------------
                # CONTINUE RIGHT
                # ---------------------------------

                if column_has_data:

                    self.current_col = next_col

                # ---------------------------------
                # WRAP TO NEXT ROW
                # ---------------------------------

                else:

                    self.current_row += 1

                    # FIRST EMPTY COLUMN

                    target_col = 0

                    while True:

                        value = self.get_cell(
                            self.current_row,
                            target_col
                        )

                        if (
                            value is None
                            or
                            str(value).strip() == ""
                        ):

                            break

                        target_col += 1

                    self.current_col = target_col

            else:

                self.current_col = next_col

        # =================================
        # MOVE DOWN
        # =================================

        elif self.direction == "down":

            next_row = self.current_row + 1
            next_col = self.current_col

            self.ensure_size(
                next_row,
                next_col
            )

            # ---------------------------------
            # AUTO RETURN
            # ---------------------------------

            if self.wrap_enabled:

                # CHECK:
                # DOES NEXT ROW
                # CONTAIN DATA TO LEFT?

                row_has_data = False

                for c in range(0, self.current_col):

                    value = self.get_cell(
                        next_row,
                        c
                    )

                    print(
                        "CHECK ROW:",
                        next_row,
                        c,
                        value
                    )

                    if (
                        value is not None
                        and
                        str(value).strip() != ""
                    ):

                        row_has_data = True
                        break

                # ---------------------------------
                # CONTINUE DOWN
                # ---------------------------------

                if row_has_data:

                    self.current_row = next_row

                # ---------------------------------
                # WRAP TO NEXT COLUMN
                # ---------------------------------

                else:

                    self.current_col += 1

                    # FIRST EMPTY ROW

                    target_row = 0

                    while True:

                        value = self.get_cell(
                            target_row,
                            self.current_col
                        )

                        if (
                            value is None
                            or
                            str(value).strip() == ""
                        ):

                            break

                        target_row += 1

                    self.current_row = target_row

            else:

                self.current_row = next_row
    # =====================================
    # CONDITIONAL FORMATTING
    # =====================================

    def add_rule(self, rule):

        self.conditional_rules.append(rule)