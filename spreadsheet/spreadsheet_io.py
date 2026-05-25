import json

import pandas as pd

from openpyxl import Workbook
from openpyxl import load_workbook

from openpyxl.styles import PatternFill

from openpyxl.formatting.rule import (
    CellIsRule,
    FormulaRule
)

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
        
        # =================================
        # CONDITIONAL FORMATTING
        # =================================

        for rule in model.conditional_rules:

            fill = PatternFill(
                start_color=(
                    rule.color.replace("#", "")
                ),
                end_color=(
                    rule.color.replace("#", "")
                ),
                fill_type="solid"
            )

            # -----------------------------
            # BETWEEN
            # -----------------------------

            if rule.rule_type == "between":

                ws.conditional_formatting.add(

                    rule.target_range,

                    CellIsRule(

                        operator="between",

                        formula=[
                            str(rule.min_value),
                            str(rule.max_value)
                        ],

                        fill=fill
                    )
                )

            # -----------------------------
            # NOT BETWEEN
            # -----------------------------

            elif rule.rule_type == "not_between":

                ws.conditional_formatting.add(

                    rule.target_range,

                    CellIsRule(

                        operator="notBetween",

                        formula=[
                            str(rule.min_value),
                            str(rule.max_value)
                        ],

                        fill=fill
                    )
                )

            # -----------------------------
            # GREATER THAN
            # -----------------------------

            elif rule.rule_type == "greater_than":

                ws.conditional_formatting.add(

                    rule.target_range,

                    CellIsRule(

                        operator="greaterThan",

                        formula=[
                            str(rule.min_value)
                        ],

                        fill=fill
                    )
                )

            # -----------------------------
            # LESS THAN
            # -----------------------------

            elif rule.rule_type == "less_than":

                ws.conditional_formatting.add(

                    rule.target_range,

                    CellIsRule(

                        operator="lessThan",

                        formula=[
                            str(rule.min_value)
                        ],

                        fill=fill
                    )
                )

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