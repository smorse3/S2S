import pandas as pd


class PandasSpreadsheetHandler:

    def __init__(self):
        self.rows = []
        self.columns = []

    def set_columns(self, columns):
        self.columns = columns

    def append_row(self, row):
        self.rows.append(row)

    def dataframe(self):
        return pd.DataFrame(self.rows, columns=self.columns)

    def save_xlsx(self, path):
        df = self.dataframe()

        with pd.ExcelWriter(
            path,
            engine="openpyxl"
        ) as writer:
            df.to_excel(
                writer,
                index=False
            )

    def save_csv(self, path):
        self.dataframe().to_csv(
            path,
            index=False
        )

    def save_ods(self, path):
        self.dataframe().to_excel(
            path,
            engine="odf"
        )