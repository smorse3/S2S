import pandas as pd


class SpreadsheetModel:

    def __init__(self):

        # =====================================
        # START WITH DEFAULT GRID
        # =====================================

        self.default_rows = 100
        self.default_cols = 26

        self.df = pd.DataFrame(
            "",
            index=range(self.default_rows),
            columns=range(self.default_cols)
        )

        self.current_row = 0
        self.current_col = 0

        self.conditional_rules = []

    # =====================================
    # ENSURE SIZE
    # =====================================

    def ensure_size(self, row, col):

        # ADD ROWS

        while row >= len(self.df.index):

            self.df.loc[len(self.df)] = [
                ""
                for _ in range(
                    len(self.df.columns)
                )
            ]

        # ADD COLUMNS

        while col >= len(self.df.columns):

            self.df[
                len(self.df.columns)
            ] = ""

    # =====================================
    # SET CELL
    # =====================================

    def set_cell(
        self,
        row,
        col,
        value
    ):

        self.ensure_size(row, col)

        self.df.iat[row, col] = value

    # =====================================
    # GET CELL
    # =====================================

    def get_cell(
        self,
        row,
        col
    ):

        self.ensure_size(row, col)

        return self.df.iat[row, col]

    # =====================================
    # CONDITIONAL FORMATTING
    # =====================================

    def add_rule(self, rule):

        self.conditional_rules.append(rule)