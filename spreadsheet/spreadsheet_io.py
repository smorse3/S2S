import pandas as pd

from openpyxl import Workbook
from openpyxl import load_workbook

from openpyxl.styles import PatternFill

from openpyxl.formatting.rule import (
    CellIsRule
)

from spreadsheet.conditional_formatting import (
    ConditionalFormattingRule
)


class SpreadsheetIO:

    # =====================================
    # SAVE XLSX
    # =====================================

    @staticmethod
    def save_xlsx(model, path):

        wb = Workbook()

        ws = wb.active

        ws.title = "Sheet1"

        # =================================
        # WRITE DATA
        # =================================

        for r_idx, row in enumerate(
            model.df.values,
            start=1
        ):

            for c_idx, value in enumerate(
                row,
                start=1
            ):

                ws.cell(
                    row=r_idx,
                    column=c_idx,
                    value=value
                )

        # =================================
        # EXCEL CONDITIONAL FORMATTING
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

            elif (
                rule.rule_type
                == "not_between"
            ):

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

            elif (
                rule.rule_type
                == "greater_than"
            ):

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

            elif (
                rule.rule_type
                == "less_than"
            ):

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

        # =================================
        # SAVE INTERNAL RULE METADATA
        # =================================

        rules_ws = wb.create_sheet(
            "__S2S_RULES__"
        )

        # HIDE SHEET

        rules_ws.sheet_state = "hidden"

        headers = [

            "rule_type",
            "min_value",
            "max_value",
            "value",
            "color",
            "target_range",
            "stop_if_true"
        ]

        # HEADER ROW

        for col, header in enumerate(
            headers,
            start=1
        ):

            rules_ws.cell(
                row=1,
                column=col,
                value=header
            )

        # RULE ROWS

        for row_idx, rule in enumerate(
            model.conditional_rules,
            start=2
        ):

            rules_ws.cell(
                row=row_idx,
                column=1,
                value=rule.rule_type
            )

            rules_ws.cell(
                row=row_idx,
                column=2,
                value=rule.min_value
            )

            rules_ws.cell(
                row=row_idx,
                column=3,
                value=rule.max_value
            )

            rules_ws.cell(
                row=row_idx,
                column=4,
                value=rule.value
            )

            rules_ws.cell(
                row=row_idx,
                column=5,
                value=rule.color
            )

            rules_ws.cell(
                row=row_idx,
                column=6,
                value=rule.target_range
            )

            rules_ws.cell(
                row=row_idx,
                column=7,
                value=rule.stop_if_true
            )

        wb.save(path)

    # =====================================
    # LOAD XLSX
    # =====================================

    @staticmethod
    def load(path):

        wb = load_workbook(path)

        ws = wb["Sheet1"]

        # =================================
        # LOAD DATAFRAME
        # =================================

        data = []

        for row in ws.iter_rows(
            values_only=True
        ):

            data.append(list(row))

        df = pd.DataFrame(data)

        # =================================
        # LOAD RULES
        # =================================

        rules = []

        if "__S2S_RULES__" in wb.sheetnames:

            rules_ws = wb[
                "__S2S_RULES__"
            ]

            for row in rules_ws.iter_rows(
                min_row=2,
                values_only=True
            ):

                try:

                    rule = (
                        ConditionalFormattingRule(

                            rule_type=row[0],

                            min_value=row[1],

                            max_value=row[2],

                            value=row[3],

                            color=row[4],

                            target_range=row[5],

                            stop_if_true=bool(
                                row[6]
                            )
                        )
                    )

                    rules.append(rule)

                except Exception as e:

                    print(
                        "Rule load failed:",
                        e
                    )

        return df, rules