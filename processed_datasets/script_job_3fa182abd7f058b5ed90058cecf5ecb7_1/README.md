# Dataset Processing Report

## Dataset Information
- **Filename**: script_job_3fa182abd7f058b5ed90058cecf5ecb7_1.csv
- **Rows**: 1
- **Columns**: 6
- **Processing Date**: 2025-07-26 14:51:44

## Column Details
| Column Name | Data Type | Null Count | Null % | Unique Count | Min Value | Max Value | Mean |
|-------------|-----------|------------|--------|--------------|-----------|-----------|------|
| precision | float64 | 0 | 0.0% | 1 | 0.6707 | 0.6707 | 0.6707 |
| recall | float64 | 0 | 0.0% | 1 | 0.5883 | 0.5883 | 0.5883 |
| accuracy | float64 | 0 | 0.0% | 1 | 0.7980 | 0.7980 | 0.7980 |
| f1_score | float64 | 0 | 0.0% | 1 | 0.5977 | 0.5977 | 0.5977 |
| log_loss | float64 | 0 | 0.0% | 1 | 1.0183 | 1.0183 | 1.0183 |
| roc_auc | float64 | 0 | 0.0% | 1 | 0.9389 | 0.9389 | 0.9389 |

## Data Quality Summary
- **Total Rules**: 18
- **Error Rules**: 6
- **Warning Rules**: 12

## Data Quality Rules
- 🔴 **NOT_NULL**: Column 'precision' should not contain null values
- 🟡 **UNIQUE**: Column 'precision' should contain unique values
- 🟡 **RANGE**: Column 'precision' values should be between 0.6706848862094611 and 0.6706848862094611
- 🔴 **NOT_NULL**: Column 'recall' should not contain null values
- 🟡 **UNIQUE**: Column 'recall' should contain unique values
- 🟡 **RANGE**: Column 'recall' values should be between 0.5883348859492953 and 0.5883348859492953
- 🔴 **NOT_NULL**: Column 'accuracy' should not contain null values
- 🟡 **UNIQUE**: Column 'accuracy' should contain unique values
- 🟡 **RANGE**: Column 'accuracy' values should be between 0.7979704526634372 and 0.7979704526634372
- 🔴 **NOT_NULL**: Column 'f1_score' should not contain null values
- 🟡 **UNIQUE**: Column 'f1_score' should contain unique values
- 🟡 **RANGE**: Column 'f1_score' values should be between 0.5977163580794566 and 0.5977163580794566
- 🔴 **NOT_NULL**: Column 'log_loss' should not contain null values
- 🟡 **UNIQUE**: Column 'log_loss' should contain unique values
- 🟡 **RANGE**: Column 'log_loss' values should be between 1.018343291384798 and 1.018343291384798
- 🔴 **NOT_NULL**: Column 'roc_auc' should not contain null values
- 🟡 **UNIQUE**: Column 'roc_auc' should contain unique values
- 🟡 **RANGE**: Column 'roc_auc' values should be between 0.9388905094905096 and 0.9388905094905096

## Column Quality Metrics
- **precision**: 100.0% complete, 100.0% unique
- **recall**: 100.0% complete, 100.0% unique
- **accuracy**: 100.0% complete, 100.0% unique
- **f1_score**: 100.0% complete, 100.0% unique
- **log_loss**: 100.0% complete, 100.0% unique
- **roc_auc**: 100.0% complete, 100.0% unique

## Files Generated
- `script_job_3fa182abd7f058b5ed90058cecf5ecb7_1.csv` - Original dataset
- `script_job_3fa182abd7f058b5ed90058cecf5ecb7_1_metadata.json` - Detailed metadata
- `script_job_3fa182abd7f058b5ed90058cecf5ecb7_1_contract.xlsx` - Data contract with schema and DQ rules
- `script_job_3fa182abd7f058b5ed90058cecf5ecb7_1_dq_report.json` - Comprehensive data quality report
- `README.md` - This summary document

## Usage
This dataset has been processed through the MCP Dataset Onboarding pipeline. All artifacts are ready for catalog publication or further analysis.
