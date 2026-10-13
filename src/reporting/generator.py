from datetime import datetime
from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill


class ReportGenerator:
    def __init__(self, output_folder: str | Path):
        self.output_folder = Path(output_folder)

        self.output_folder.mkdir(parents=True, exist_ok=True)

    def generate_excel(self, dataframe: pd.DataFrame, metrics: dict) -> Path:

        date = datetime.now().strftime("%Y%m%d")

        output_file = self.output_folder / f"library_report_{date}.xlsx"

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            # Books sheet
            dataframe.to_excel(writer, sheet_name="Books", index=False)

            # Metrics sheet
            metrics_dataframe = pd.DataFrame(
                list(metrics.items()), columns=["Metric", "Value"]
            )

            metrics_dataframe.to_excel(writer, sheet_name="Metrics", index=False)

            # Get worksheets
            books_sheet = writer.sheets["Books"]
            metrics_sheet = writer.sheets["Metrics"]

            # Header style
            header_fill = PatternFill(fill_type="solid", fgColor="1F4E78")

            header_font = Font(color="FFFFFF", bold=True)

            # Format Books header
            for cell in books_sheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")

            # Format Metrics header
            for cell in metrics_sheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")

            # Column widths - Books
            books_sheet.column_dimensions["A"].width = 22
            books_sheet.column_dimensions["B"].width = 35
            books_sheet.column_dimensions["C"].width = 30
            books_sheet.column_dimensions["D"].width = 20
            books_sheet.column_dimensions["E"].width = 18

            # Column widths - Metrics
            metrics_sheet.column_dimensions["A"].width = 25
            metrics_sheet.column_dimensions["B"].width = 15

            # Freeze headers
            books_sheet.freeze_panes = "A2"
            metrics_sheet.freeze_panes = "A2"

            # Filters
            books_sheet.auto_filter.ref = books_sheet.dimensions

        return output_file

    def generate_csv_summary(
        self, top_years: pd.DataFrame, top_languages: pd.DataFrame
    ) -> Path:

        output_file = self.output_folder / "library_summary.csv"

        # Add a column to identify each metric type
        years = top_years.copy()
        years.insert(0, "category", "publication_year")

        languages = top_languages.copy()
        languages.insert(0, "category", "language")

        # Give both DataFrames the same column names
        years.columns = ["category", "value", "count"]
        languages.columns = ["category", "value", "count"]

        # Combine both summaries
        summary = pd.concat([years, languages], ignore_index=True)

        summary.to_csv(output_file, index=False, encoding="utf-8")

        return output_file

    def generate_json(self, dataframe: pd.DataFrame) -> Path:

        output_file = self.output_folder / "library_data.json"

        dataframe.to_json(output_file, orient="records", force_ascii=False, indent=None)

        return output_file
