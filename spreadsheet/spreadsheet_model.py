import pandas as pd


class SpreadsheetModel:

    def __init__(self):

        self.df = pd.DataFrame()

        self.current_row = 0
        self.current_col = 0

        self.conditional_rules = []

    # ==========================================
    # ENSURE SIZE
    # ==========================================

    def ensure_size(self, row, col):

        while self.df.shape[0] <= row:

            self.df.loc[len(self.df)] = []

        while self.df.shape[1] <= col:

            self.df[self.df.shape[1]] = ""

    # ==========================================
    # CELL ACCESS
    # ==========================================

    def set_cell(self, row, col, value):

        self.ensure_size(row, col)

        self.df.iat[row, col] = value

    def get_cell(self, row, col):

        self.ensure_size(row, col)

        return self.df.iat[row, col]

    # ==========================================
    # CONDITIONAL FORMATTING
    # ==========================================

    def add_rule(self, rule):

        self.conditional_rules.append(rule)