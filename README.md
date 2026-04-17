-main.py
Entry point.

Loads a dataset and shows a menu:

Data quality report.

Detect column data types.

Suggest code snippets to convert columns.

Clean dataframe and optionally save it.

Generate graphs and correlation heatmap.

-column_type_detective.py
Detects semantic type of each column (numerical, categorical, datetime, text, bool, email, phone, ID, URL) using regexes and heuristics.

Main function: conversion_score(col) → scores for each type + best guess.

-data_profiler.py
run_quality_report(df) prints:

Rows, columns, completion % per column, number of unique values.

Columns with >5% missing data, duplicate rows, invalid emails.

For numeric columns: min, max, number of outliers (>3*std).

-conversion_snippet.py
Uses conversion_score to:

Compare detected type vs pandas dtype.

Print pandas code snippets to convert each column to a suitable dtype (numeric, categorical, datetime, text, bool).

-dataframe_cleaner.py
clean_dataframe(df):

Copies the dataframe, drops rows with any NaN.

Uses conversion_score to decide target type and actually converts columns (numeric/date/category/text/bool).

Returns a cleaned dataframe.

-auto_eda.py
Automatically generates plots:

Numeric: boxplot + histogram per column.

Categorical: bar chart of top 20 categories.

Datetime: line plot over time.

Correlation: heatmap of numeric columns + pairwise Pearson coefficients.

-Main function: graphs(filename, df) asks for output folders and saves PNGs.

