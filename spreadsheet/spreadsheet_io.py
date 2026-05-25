import json

import pandas as pd

from openpyxl import Workbook
from openpyxl import load_workbook

from openpyxl.styles import PatternFill


class SpreadsheetIO:

    # =====================================
    # SAVE XLSX
    # =====================================

    @staticmethod
    def save_xlsx(model, path):

        wb = Workbook()

        ws = wb.active

        # ---------------------------------
        # DATA
        # ---------------------------------

        for r_idx, row in enumerate(
            model.df.values,
            start=1
        ):

            for c_idx, value in enumerate(
                row,
                start=1
            ):

                cell = ws.cell(
                    row=r_idx,
                    column=c_idx
                )

                cell.value = value

                # CONDITIONAL FORMATTING

                color = (
                    model.get_matching_color(
                        value
                    )
                )

                if color:

                    hex_color = (
                        color.replace("#", "")
                    )

                    fill = PatternFill(
                        start_color=hex_color,
                        end_color=hex_color,
                        fill_type="solid"
                    )

                    cell.fill = fill

        # ---------------------------------
        # SAVE RULES
        # ---------------------------------

        rules = []

        for rule in model.conditional_rules:

            rules.append({

                "min": rule.min_value,
                "max": rule.max_value,
                "color": rule.color,
                "mode": rule.mode
            })

        ws["ZZ1"] = json.dumps(rules)

        wb.save(path)

    # =====================================
    # LOAD XLSX
    # =====================================

    @staticmethod
    def load(path):

        wb = load_workbook(path)

        ws = wb.active

        data = []

        formatting = {}

        max_row = ws.max_row
        max_col = ws.max_column

        for r in range(1, max_row + 1):

            row_data = []

            for c in range(1, max_col + 1):

                cell = ws.cell(
                    row=r,
                    column=c
                )

                value = cell.value

                row_data.append(value)

                fill = cell.fill

                if (
                    fill
                    and
                    fill.fill_type == "solid"
                ):

                    color = (
                        fill.start_color.rgb
                    )

                    formatting[
                        (r - 1, c - 1)
                    ] = color

            data.append(row_data)

        df = pd.DataFrame(data)

        rules = []

        try:

            raw = ws["ZZ1"].value

            if raw:

                rules = json.loads(raw)

        except Exception:

            pass

        return df, formatting, rules