import pandas as pd

from pyexcel_ods3 import get_data

from openpyxl import load_workbook

from openpyxl.styles import PatternFill


class SpreadsheetIO:

    # ==========================================
    # LOAD FILE
    # ==========================================

    @staticmethod
    def load(path):

        if path.endswith(".xlsx"):

            return SpreadsheetIO.load_xlsx(path)

        if path.endswith(".ods"):

            return SpreadsheetIO.load_ods(path)

        raise ValueError(
            "Unsupported file type"
        )

    # ==========================================
    # LOAD XLSX
    # ==========================================

    @staticmethod
    def load_xlsx(path):

        df = pd.read_excel(
            path,
            header=None
        )

        workbook = load_workbook(path)

        sheet = workbook.active

        formatting = {}

        for row in sheet.iter_rows():

            for cell in row:

                if cell.fill:

                    color = (
                        cell.fill.start_color.rgb
                    )

                    formatting[
                        (cell.row - 1,
                         cell.column - 1)
                    ] = color

        return df, formatting

    # ==========================================
    # LOAD ODS
    # ==========================================

    @staticmethod
    def load_ods(path):

        data = get_data(path)

        first_sheet = list(
            data.keys()
        )[0]

        rows = data[first_sheet]

        df = pd.DataFrame(rows)

        formatting = {}

        return df, formatting

    # ==========================================
    # SAVE XLSX
    # ==========================================

    @staticmethod
    def save_xlsx(
        model,
        path
    ):

        model.df.to_excel(
            path,
            index=False,
            header=False
        )

        workbook = load_workbook(path)

        sheet = workbook.active

        # APPLY CONDITIONAL FORMATTING

        for rule in model.conditional_rules:

            for row in range(
                model.df.shape[0]
            ):

                value = model.df.iat[
                    row,
                    rule.column
                ]

                if rule.matches(value):

                    cell = sheet.cell(
                        row=row + 1,
                        column=rule.column + 1
                    )

                    cell.fill = PatternFill(
                        start_color="FFFF00",
                        end_color="FFFF00",
                        fill_type="solid"
                    )

        workbook.save(path)