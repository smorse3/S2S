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

            next_row = self.current_row
            next_col = self.current_col + 1

            # ENSURE GRID SIZE

            self.ensure_size(
                next_row,
                next_col
            )

            # ---------------------------------
            # AUTO RETURN LOGIC
            # ---------------------------------

            if self.wrap_enabled:

                # CHECK:
                # Are ALL cells ABOVE empty?

                all_above_empty = True

                for r in range(next_row):

                    value = self.get_cell(
                        r,
                        next_col
                    )

                    if str(value).strip():

                        all_above_empty = False
                        break

                # ---------------------------------
                # WRAP TO NEXT ROW
                # ---------------------------------

                if all_above_empty:

                    self.current_row += 1

                    # FIND FIRST EMPTY COLUMN

                    target_col = 0

                    while True:

                        value = self.get_cell(
                            self.current_row,
                            target_col
                        )

                        if not str(value).strip():

                            break

                        target_col += 1

                    self.current_col = target_col

                    return

            # NORMAL RIGHT MOVEMENT

            self.current_col = next_col

        # ---------------------------------
        # MOVE DOWN
        # ---------------------------------

        elif self.direction == "down":

            next_row = self.current_row + 1
            next_col = self.current_col

            # ENSURE GRID SIZE

            self.ensure_size(
                next_row,
                next_col
            )

            # ---------------------------------
            # AUTO RETURN LOGIC
            # ---------------------------------

            if self.wrap_enabled:

                # CHECK:
                # Are ALL cells TO LEFT empty?

                all_left_empty = True

                for c in range(next_col):

                    value = self.get_cell(
                        next_row,
                        c
                    )

                    if str(value).strip():

                        all_left_empty = False
                        break

                # ---------------------------------
                # WRAP TO NEXT COLUMN
                # ---------------------------------

                if all_left_empty:

                    self.current_col += 1

                    # FIND FIRST EMPTY ROW

                    target_row = 0

                    while True:

                        value = self.get_cell(
                            target_row,
                            self.current_col
                        )

                        if not str(value).strip():

                            break

                        target_row += 1

                    self.current_row = target_row

                    return

            # NORMAL DOWN MOVEMENT

            self.current_row = next_row