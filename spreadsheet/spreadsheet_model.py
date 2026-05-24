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

        # ---------------------------------
        # MOVE RIGHT
        # ---------------------------------

        if self.direction == "right":

            next_col = (
                self.current_col + 1
            )

            # WRAP TO NEXT ROW

            if (
                self.wrap_enabled
                and
                self._no_data_to_left(
                    self.current_row,
                    next_col
                )
            ):

                self.current_row += 1
                self.current_col = 0

            else:

                self.current_col = next_col

        # ---------------------------------
        # MOVE DOWN
        # ---------------------------------

        elif self.direction == "down":

            next_row = (
                self.current_row + 1
            )

            # WRAP TO NEXT COLUMN

            if (
                self.wrap_enabled
                and
                self._no_data_above(
                    next_row,
                    self.current_col
                )
            ):

                self.current_col += 1
                self.current_row = 0

            else:

                self.current_row = next_row

    # =====================================
    # CHECKS
    # =====================================

    def _no_data_to_left(
        self,
        row,
        col
    ):

        for c in range(col):

            value = self.df.iat[row, c]

            if str(value).strip():

                return False

        return True

    def _no_data_above(
        self,
        row,
        col
    ):

        for r in range(row):

            value = self.df.iat[r, col]

            if str(value).strip():

                return False

        return True