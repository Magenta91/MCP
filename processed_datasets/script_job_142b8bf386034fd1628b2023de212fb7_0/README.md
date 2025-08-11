# Dataset Processing Report

## Dataset Information
- **Filename**: script_job_142b8bf386034fd1628b2023de212fb7_0.csv
- **Rows**: 1
- **Columns**: 6
- **Processing Date**: 2025-07-26 15:11:41

## Column Details
| Column Name | Data Type | Null Count | Null % | Unique Count | Min Value | Max Value | Mean |
|-------------|-----------|------------|--------|--------------|-----------|-----------|------|
| mean_absolute_error | float64 | 0 | 0.0% | 1 | 0.4941 | 0.4941 | 0.4941 |
| mean_squared_error | float64 | 0 | 0.0% | 1 | 17.7826 | 17.7826 | 17.7826 |
| mean_squared_log_error | float64 | 0 | 0.0% | 1 | 0.0859 | 0.0859 | 0.0859 |
| median_absolute_error | float64 | 0 | 0.0% | 1 | 0.1742 | 0.1742 | 0.1742 |
| r2_score | float64 | 0 | 0.0% | 1 | 0.0092 | 0.0092 | 0.0092 |
| explained_variance | float64 | 0 | 0.0% | 1 | 0.0181 | 0.0181 | 0.0181 |

## Data Quality Summary
- **Total Rules**: 18
- **Error Rules**: 6
- **Warning Rules**: 12

## Data Quality Rules
- 🔴 **NOT_NULL**: Column 'mean_absolute_error' should not contain null values
- 🟡 **UNIQUE**: Column 'mean_absolute_error' should contain unique values
- 🟡 **RANGE**: Column 'mean_absolute_error' values should be between 0.4940700979929911 and 0.4940700979929911
- 🔴 **NOT_NULL**: Column 'mean_squared_error' should not contain null values
- 🟡 **UNIQUE**: Column 'mean_squared_error' should contain unique values
- 🟡 **RANGE**: Column 'mean_squared_error' values should be between 17.782610464656457 and 17.782610464656457
- 🔴 **NOT_NULL**: Column 'mean_squared_log_error' should not contain null values
- 🟡 **UNIQUE**: Column 'mean_squared_log_error' should contain unique values
- 🟡 **RANGE**: Column 'mean_squared_log_error' values should be between 0.0859107107687808 and 0.0859107107687808
- 🔴 **NOT_NULL**: Column 'median_absolute_error' should not contain null values
- 🟡 **UNIQUE**: Column 'median_absolute_error' should contain unique values
- 🟡 **RANGE**: Column 'median_absolute_error' values should be between 0.1742337942123413 and 0.1742337942123413
- 🔴 **NOT_NULL**: Column 'r2_score' should not contain null values
- 🟡 **UNIQUE**: Column 'r2_score' should contain unique values
- 🟡 **RANGE**: Column 'r2_score' values should be between 0.0091867740833386 and 0.0091867740833386
- 🔴 **NOT_NULL**: Column 'explained_variance' should not contain null values
- 🟡 **UNIQUE**: Column 'explained_variance' should contain unique values
- 🟡 **RANGE**: Column 'explained_variance' values should be between 0.0181301156989388 and 0.0181301156989388

## Column Quality Metrics
- **mean_absolute_error**: 100.0% complete, 100.0% unique
- **mean_squared_error**: 100.0% complete, 100.0% unique
- **mean_squared_log_error**: 100.0% complete, 100.0% unique
- **median_absolute_error**: 100.0% complete, 100.0% unique
- **r2_score**: 100.0% complete, 100.0% unique
- **explained_variance**: 100.0% complete, 100.0% unique

## Files Generated
- `script_job_142b8bf386034fd1628b2023de212fb7_0.csv` - Original dataset
- `script_job_142b8bf386034fd1628b2023de212fb7_0_metadata.json` - Detailed metadata
- `script_job_142b8bf386034fd1628b2023de212fb7_0_contract.xlsx` - Data contract with schema and DQ rules
- `script_job_142b8bf386034fd1628b2023de212fb7_0_dq_report.json` - Comprehensive data quality report
- `README.md` - This summary document

## Usage
This dataset has been processed through the MCP Dataset Onboarding pipeline. All artifacts are ready for catalog publication or further analysis.
