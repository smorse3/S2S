import pandas as pd

from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import CellIsRule

from spreadsheet.conditional_formatting import ConditionalFormattingRule


class SpreadsheetIO:

    # =========================================================
    # SAVE XLSX (DATA + CONDITIONAL FORMATTING + RULE METADATA)
    # =========================================================
    @staticmethod
    def save_xlsx(model, path):

        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"

        # -----------------------------
        # WRITE GRID DATA
        # -----------------------------
        df = model.df

        for r_idx, row in enumerate(df.values, start=1):
            for c_idx, value in enumerate(row, start=1):
                ws.cell(
                    row=r_idx,
                    column=c_idx,
                    value=value
                )

        # -----------------------------
        # APPLY EXCEL CONDITIONAL FORMATTING
        # -----------------------------
        for rule in model.conditional_rules:

            fill = PatternFill(
                start_color=rule.color.replace("#", ""),
                end_color=rule.color.replace("#", ""),
                fill_type="solid"
            )

            try:

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

                elif rule.rule_type == "greater_than":

                    ws.conditional_formatting.add(
                        rule.target_range,
                        CellIsRule(
                            operator="greaterThan",
                            formula=[str(rule.min_value)],
                            fill=fill
                        )
                    )

                elif rule.rule_type == "less_than":

                    ws.conditional_formatting.add(
                        rule.target_range,
                        CellIsRule(
                            operator="lessThan",
                            formula=[str(rule.min_value)],
                            fill=fill
                        )
                    )

            except Exception as e:
                print("Conditional formatting export error:", e)

        # -----------------------------
        # WRITE RULE METADATA SHEET
        # -----------------------------
        rules_ws = wb.create_sheet("__S2S_RULES__")
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

        for col, h in enumerate(headers, start=1):
            rules_ws.cell(row=1, column=col, value=h)

        for i, rule in enumerate(model.conditional_rules, start=2):

            rules_ws.cell(row=i, column=1, value=rule.rule_type)
            rules_ws.cell(row=i, column=2, value=rule.min_value)
            rules_ws.cell(row=i, column=3, value=rule.max_value)
            rules_ws.cell(row=i, column=4, value=rule.value)
            rules_ws.cell(row=i, column=5, value=rule.color)
            rules_ws.cell(row=i, column=6, value=rule.target_range)
            rules_ws.cell(row=i, column=7, value=rule.stop_if_true)

        wb.save(path)

    # =========================================================
    # LOAD XLSX (DATA + RULES)
    # =========================================================
    @staticmethod
    def load(path):

        wb = load_workbook(path)

        # -----------------------------
        # LOAD MAIN SHEET
        # -----------------------------
        ws = wb["Sheet1"]

        data = []

        for row in ws.iter_rows(values_only=True):
            data.append(list(row))

        df = pd.DataFrame(data)

        # -----------------------------
        # LOAD CONDITIONAL RULES
        # -----------------------------
        rules = []

        if "__S2S_RULES__" in wb.sheetnames:

            rules_ws = wb["__S2S_RULES__"]

            for row in rules_ws.iter_rows(min_row=2, values_only=True):

                try:
                    if not row:
                        continue

                    rule = ConditionalFormattingRule(

                        rule_type=row[0] if len(row) > 0 else None,
                        min_value=row[1] if len(row) > 1 else None,
                        max_value=row[2] if len(row) > 2 else None,
                        value=row[3] if len(row) > 3 else None,
                        color=row[4] if len(row) > 4 else "#FFFF00",
                        target_range=row[5] if len(row) > 5 else "A1:Z100",
                        stop_if_true=bool(row[6]) if len(row) > 6 else False
                    )

                    rules.append(rule)

                except Exception as e:
                    print("Rule load failed:", e)

        return df, rules