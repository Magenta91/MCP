# Dataset Processing Report

## Dataset Information
- **Filename**: bquxjob_5cbc3452_196eba58105.csv
- **Rows**: 100
- **Columns**: 46
- **Processing Date**: 2025-07-26 15:11:46

## Column Details
| Column Name | Data Type | Null Count | Null % | Unique Count | Min Value | Max Value | Mean |
|-------------|-----------|------------|--------|--------------|-----------|-----------|------|
| Instrument_Key | object | 0 | 0.0% | 66 | N/A | N/A | N/A |
| Name | object | 0 | 0.0% | 4 | N/A | N/A | N/A |
| Trading_Symbol | object | 0 | 0.0% | 4 | N/A | N/A | N/A |
| InstrumentType | object | 0 | 0.0% | 1 | N/A | N/A | N/A |
| AssetSymbol | object | 0 | 0.0% | 4 | N/A | N/A | N/A |
| Instrument | object | 0 | 0.0% | 4 | N/A | N/A | N/A |
| TradeDate | object | 0 | 0.0% | 36 | N/A | N/A | N/A |
| TradeHour_IST | int64 | 0 | 0.0% | 1 | 9.0000 | 9.0000 | 9.0000 |
| TradeMinute | int64 | 0 | 0.0% | 40 | 17.0000 | 59.0000 | 35.9100 |
| TradingSession | object | 0 | 0.0% | 1 | N/A | N/A | N/A |
| Day_Spread | float64 | 0 | 0.0% | 56 | 1.0000 | 51.0000 | 10.9665 |
| Hourly_Spread | float64 | 0 | 0.0% | 63 | 0.0000 | 679.0000 | 217.5935 |
| DailyGain | float64 | 0 | 0.0% | 2 | -0.5000 | 0.5000 | -0.2300 |
| HourlyGain | float64 | 0 | 0.0% | 52 | -2.0937 | 2.0179 | 0.1055 |
| Timestamp | object | 0 | 0.0% | 98 | N/A | N/A | N/A |
| ist_ts | object | 0 | 0.0% | 98 | N/A | N/A | N/A |
| HourBucket | object | 0 | 0.0% | 1 | N/A | N/A | N/A |
| Open | float64 | 0 | 0.0% | 95 | 10801.0000 | 51440.0000 | 29062.5365 |
| High | float64 | 0 | 0.0% | 96 | 10803.5000 | 51440.0000 | 29068.2810 |
| Low | float64 | 0 | 0.0% | 95 | 10799.5000 | 51406.0500 | 29057.7365 |
| Close | float64 | 0 | 0.0% | 96 | 10800.0000 | 51416.3500 | 29062.9005 |
| Volume_S | int64 | 0 | 0.0% | 36 | 1000.0000 | 21120.0000 | 2793.8000 |
| Volume_H | int64 | 0 | 0.0% | 66 | 12330.0000 | 214560.0000 | 36271.8500 |
| Volume_L | int64 | 0 | 0.0% | 10 | 30.0000 | 1680.0000 | 108.6000 |
| Volume_D | int64 | 0 | 0.0% | 66 | 134890.0000 | 915480.0000 | 266533.1000 |
| Value | float64 | 0 | 0.0% | 98 | 1344000.0000 | 236060400.0000 | 24728929.8675 |
| Total_Buy_Quantity | float64 | 0 | 0.0% | 100 | 36262000.0000 | 24376177000.0000 | 11661399280.0000 |
| Total_Sell_Quantity | float64 | 0 | 0.0% | 100 | 36262000.0000 | 24376177000.0000 | 11661399280.0000 |
| OpenInterest | float64 | 0 | 0.0% | 100 | 362620000.0000 | 243761770000.0000 | 116613992800.0000 |
| ChangeOI | float64 | 0 | 0.0% | 100 | 11841900.0000 | 221375070000.0000 | 87307981201.0000 |
| DailyGain_Bucket | object | 0 | 0.0% | 2 | N/A | N/A | N/A |
| HourlyGain_Bucket | object | 0 | 0.0% | 4 | N/A | N/A | N/A |
| Day_Spread_Bucket | object | 0 | 0.0% | 5 | N/A | N/A | N/A |
| Hour_Spread_Bucket | object | 0 | 0.0% | 2 | N/A | N/A | N/A |
| Volume_D_Bucket | object | 0 | 0.0% | 2 | N/A | N/A | N/A |
| Volume_S_Bucket | object | 0 | 0.0% | 2 | N/A | N/A | N/A |
| Volume_H_Bucket | object | 0 | 0.0% | 4 | N/A | N/A | N/A |
| Volume_L_Bucket | object | 0 | 0.0% | 2 | N/A | N/A | N/A |
| OI_Bucket | object | 0 | 0.0% | 1 | N/A | N/A | N/A |
| ChangeOI_Bucket | object | 0 | 0.0% | 1 | N/A | N/A | N/A |
| BuyQty_bin | int64 | 0 | 0.0% | 4 | 1.0000 | 4.0000 | 2.4400 |
| SellQty_bin | int64 | 0 | 0.0% | 4 | 1.0000 | 4.0000 | 2.4400 |
| Volume_bin | int64 | 0 | 0.0% | 4 | 1.0000 | 4.0000 | 1.2500 |
| OpenInterest_bin | int64 | 0 | 0.0% | 4 | 1.0000 | 4.0000 | 2.4400 |
| Spread_bin | int64 | 0 | 0.0% | 4 | 1.0000 | 4.0000 | 3.4000 |
| Gain_bin | int64 | 0 | 0.0% | 4 | 1.0000 | 4.0000 | 2.8000 |

## Data Quality Summary
- **Total Rules**: 80
- **Error Rules**: 46
- **Warning Rules**: 34

## Data Quality Rules
- 🔴 **NOT_NULL**: Column 'Instrument_Key' should not contain null values
- 🔴 **NOT_NULL**: Column 'Name' should not contain null values
- 🔴 **NOT_NULL**: Column 'Trading_Symbol' should not contain null values
- 🔴 **NOT_NULL**: Column 'InstrumentType' should not contain null values
- 🔴 **NOT_NULL**: Column 'AssetSymbol' should not contain null values
- 🔴 **NOT_NULL**: Column 'Instrument' should not contain null values
- 🔴 **NOT_NULL**: Column 'TradeDate' should not contain null values
- 🔴 **NOT_NULL**: Column 'TradeHour_IST' should not contain null values
- 🟡 **RANGE**: Column 'TradeHour_IST' values should be between 9.0 and 9.0
- 🔴 **NOT_NULL**: Column 'TradeMinute' should not contain null values
- 🟡 **RANGE**: Column 'TradeMinute' values should be between 17.0 and 59.0
- 🔴 **NOT_NULL**: Column 'TradingSession' should not contain null values
- 🔴 **NOT_NULL**: Column 'Day_Spread' should not contain null values
- 🟡 **RANGE**: Column 'Day_Spread' values should be between 1.0 and 51.0
- 🔴 **NOT_NULL**: Column 'Hourly_Spread' should not contain null values
- 🟡 **RANGE**: Column 'Hourly_Spread' values should be between 0.0 and 679.0
- 🔴 **NOT_NULL**: Column 'DailyGain' should not contain null values
- 🟡 **RANGE**: Column 'DailyGain' values should be between -0.5 and 0.5
- 🔴 **NOT_NULL**: Column 'HourlyGain' should not contain null values
- 🟡 **RANGE**: Column 'HourlyGain' values should be between -2.0937214349767985 and 2.0179372197309418
- 🔴 **NOT_NULL**: Column 'Timestamp' should not contain null values
- 🟡 **UNIQUE**: Column 'Timestamp' should contain unique values
- 🔴 **NOT_NULL**: Column 'ist_ts' should not contain null values
- 🟡 **UNIQUE**: Column 'ist_ts' should contain unique values
- 🔴 **NOT_NULL**: Column 'HourBucket' should not contain null values
- 🔴 **NOT_NULL**: Column 'Open' should not contain null values
- 🟡 **RANGE**: Column 'Open' values should be between 10801.0 and 51440.0
- 🔴 **NOT_NULL**: Column 'High' should not contain null values
- 🟡 **UNIQUE**: Column 'High' should contain unique values
- 🟡 **RANGE**: Column 'High' values should be between 10803.5 and 51440.0
- 🔴 **NOT_NULL**: Column 'Low' should not contain null values
- 🟡 **RANGE**: Column 'Low' values should be between 10799.5 and 51406.05
- 🔴 **NOT_NULL**: Column 'Close' should not contain null values
- 🟡 **UNIQUE**: Column 'Close' should contain unique values
- 🟡 **RANGE**: Column 'Close' values should be between 10800.0 and 51416.35
- 🔴 **NOT_NULL**: Column 'Volume_S' should not contain null values
- 🟡 **RANGE**: Column 'Volume_S' values should be between 1000.0 and 21120.0
- 🔴 **NOT_NULL**: Column 'Volume_H' should not contain null values
- 🟡 **RANGE**: Column 'Volume_H' values should be between 12330.0 and 214560.0
- 🔴 **NOT_NULL**: Column 'Volume_L' should not contain null values
- 🟡 **RANGE**: Column 'Volume_L' values should be between 30.0 and 1680.0
- 🔴 **NOT_NULL**: Column 'Volume_D' should not contain null values
- 🟡 **RANGE**: Column 'Volume_D' values should be between 134890.0 and 915480.0
- 🔴 **NOT_NULL**: Column 'Value' should not contain null values
- 🟡 **UNIQUE**: Column 'Value' should contain unique values
- 🟡 **RANGE**: Column 'Value' values should be between 1344000.0 and 236060400.0
- 🔴 **NOT_NULL**: Column 'Total_Buy_Quantity' should not contain null values
- 🟡 **UNIQUE**: Column 'Total_Buy_Quantity' should contain unique values
- 🟡 **RANGE**: Column 'Total_Buy_Quantity' values should be between 36262000.0 and 24376177000.0
- 🔴 **NOT_NULL**: Column 'Total_Sell_Quantity' should not contain null values
- 🟡 **UNIQUE**: Column 'Total_Sell_Quantity' should contain unique values
- 🟡 **RANGE**: Column 'Total_Sell_Quantity' values should be between 36262000.0 and 24376177000.0
- 🔴 **NOT_NULL**: Column 'OpenInterest' should not contain null values
- 🟡 **UNIQUE**: Column 'OpenInterest' should contain unique values
- 🟡 **RANGE**: Column 'OpenInterest' values should be between 362620000.0 and 243761770000.0
- 🔴 **NOT_NULL**: Column 'ChangeOI' should not contain null values
- 🟡 **UNIQUE**: Column 'ChangeOI' should contain unique values
- 🟡 **RANGE**: Column 'ChangeOI' values should be between 11841900.0 and 221375070000.0
- 🔴 **NOT_NULL**: Column 'DailyGain_Bucket' should not contain null values
- 🔴 **NOT_NULL**: Column 'HourlyGain_Bucket' should not contain null values
- 🔴 **NOT_NULL**: Column 'Day_Spread_Bucket' should not contain null values
- 🔴 **NOT_NULL**: Column 'Hour_Spread_Bucket' should not contain null values
- 🔴 **NOT_NULL**: Column 'Volume_D_Bucket' should not contain null values
- 🔴 **NOT_NULL**: Column 'Volume_S_Bucket' should not contain null values
- 🔴 **NOT_NULL**: Column 'Volume_H_Bucket' should not contain null values
- 🔴 **NOT_NULL**: Column 'Volume_L_Bucket' should not contain null values
- 🔴 **NOT_NULL**: Column 'OI_Bucket' should not contain null values
- 🔴 **NOT_NULL**: Column 'ChangeOI_Bucket' should not contain null values
- 🔴 **NOT_NULL**: Column 'BuyQty_bin' should not contain null values
- 🟡 **RANGE**: Column 'BuyQty_bin' values should be between 1.0 and 4.0
- 🔴 **NOT_NULL**: Column 'SellQty_bin' should not contain null values
- 🟡 **RANGE**: Column 'SellQty_bin' values should be between 1.0 and 4.0
- 🔴 **NOT_NULL**: Column 'Volume_bin' should not contain null values
- 🟡 **RANGE**: Column 'Volume_bin' values should be between 1.0 and 4.0
- 🔴 **NOT_NULL**: Column 'OpenInterest_bin' should not contain null values
- 🟡 **RANGE**: Column 'OpenInterest_bin' values should be between 1.0 and 4.0
- 🔴 **NOT_NULL**: Column 'Spread_bin' should not contain null values
- 🟡 **RANGE**: Column 'Spread_bin' values should be between 1.0 and 4.0
- 🔴 **NOT_NULL**: Column 'Gain_bin' should not contain null values
- 🟡 **RANGE**: Column 'Gain_bin' values should be between 1.0 and 4.0

## Column Quality Metrics
- **Instrument_Key**: 100.0% complete, 66.0% unique
- **Name**: 100.0% complete, 4.0% unique
- **Trading_Symbol**: 100.0% complete, 4.0% unique
- **InstrumentType**: 100.0% complete, 1.0% unique
- **AssetSymbol**: 100.0% complete, 4.0% unique
- **Instrument**: 100.0% complete, 4.0% unique
- **TradeDate**: 100.0% complete, 36.0% unique
- **TradeHour_IST**: 100.0% complete, 1.0% unique
- **TradeMinute**: 100.0% complete, 40.0% unique
- **TradingSession**: 100.0% complete, 1.0% unique
- **Day_Spread**: 100.0% complete, 56.0% unique
- **Hourly_Spread**: 100.0% complete, 63.0% unique
- **DailyGain**: 100.0% complete, 2.0% unique
- **HourlyGain**: 100.0% complete, 52.0% unique
- **Timestamp**: 100.0% complete, 98.0% unique
- **ist_ts**: 100.0% complete, 98.0% unique
- **HourBucket**: 100.0% complete, 1.0% unique
- **Open**: 100.0% complete, 95.0% unique
- **High**: 100.0% complete, 96.0% unique
- **Low**: 100.0% complete, 95.0% unique
- **Close**: 100.0% complete, 96.0% unique
- **Volume_S**: 100.0% complete, 36.0% unique
- **Volume_H**: 100.0% complete, 66.0% unique
- **Volume_L**: 100.0% complete, 10.0% unique
- **Volume_D**: 100.0% complete, 66.0% unique
- **Value**: 100.0% complete, 98.0% unique
- **Total_Buy_Quantity**: 100.0% complete, 100.0% unique
- **Total_Sell_Quantity**: 100.0% complete, 100.0% unique
- **OpenInterest**: 100.0% complete, 100.0% unique
- **ChangeOI**: 100.0% complete, 100.0% unique
- **DailyGain_Bucket**: 100.0% complete, 2.0% unique
- **HourlyGain_Bucket**: 100.0% complete, 4.0% unique
- **Day_Spread_Bucket**: 100.0% complete, 5.0% unique
- **Hour_Spread_Bucket**: 100.0% complete, 2.0% unique
- **Volume_D_Bucket**: 100.0% complete, 2.0% unique
- **Volume_S_Bucket**: 100.0% complete, 2.0% unique
- **Volume_H_Bucket**: 100.0% complete, 4.0% unique
- **Volume_L_Bucket**: 100.0% complete, 2.0% unique
- **OI_Bucket**: 100.0% complete, 1.0% unique
- **ChangeOI_Bucket**: 100.0% complete, 1.0% unique
- **BuyQty_bin**: 100.0% complete, 4.0% unique
- **SellQty_bin**: 100.0% complete, 4.0% unique
- **Volume_bin**: 100.0% complete, 4.0% unique
- **OpenInterest_bin**: 100.0% complete, 4.0% unique
- **Spread_bin**: 100.0% complete, 4.0% unique
- **Gain_bin**: 100.0% complete, 4.0% unique

## Files Generated
- `bquxjob_5cbc3452_196eba58105.csv` - Original dataset
- `bquxjob_5cbc3452_196eba58105_metadata.json` - Detailed metadata
- `bquxjob_5cbc3452_196eba58105_contract.xlsx` - Data contract with schema and DQ rules
- `bquxjob_5cbc3452_196eba58105_dq_report.json` - Comprehensive data quality report
- `README.md` - This summary document

## Usage
This dataset has been processed through the MCP Dataset Onboarding pipeline. All artifacts are ready for catalog publication or further analysis.
