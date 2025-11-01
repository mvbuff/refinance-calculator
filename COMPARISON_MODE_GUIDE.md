# ARM Calculator - Comparison Mode Guide

## Overview

The ARM Refinance Calculator now supports **two comparison modes** to help you analyze different scenarios:

1. **Full 30-Year Comparison** (Default)
2. **ARM Periods Only** (New Feature)

## Why Two Modes?

### Full 30-Year Comparison
Use this when:
- You plan to keep the loan for the full 30-year term
- You want to see the complete financial picture
- You're comparing total lifetime costs

### ARM Periods Only
Use this when:
- You plan to **refinance again** before the adjustable rate period starts
- You plan to **sell the property** within 7-10 years
- You only care about the **initial fixed-rate periods**
- You want to minimize short-term interest costs

## How It Works

### ARM Periods Only Mode

**Original Loan:**
- Compares only the **first 84 months** (7 years) at the initial fixed rate
- Excludes the adjustable rate period (months 85-360)

**Refinance Scenario:**
- Includes interest paid on original loan until refinancing
- Plus interest paid during the **new ARM fixed period** (months 25-108 if you refi at month 24)
- Excludes the new adjustable rate period

## Example Comparison

### Scenario: Refinance at Month 24

| Mode | Original Loan | Refinance | Result |
|------|---------------|-----------|--------|
| **Full 30-Year** | $3,437,013 | $3,033,938 | ✓ Save $403,074 |
| **ARM Only** | $572,560 | $683,628 | ✗ Cost $111,067 more |

### What This Tells You:

**Full 30-Year Mode:**
- Refinancing saves $403k over 30 years
- The savings come from the lower adjustable rate (9% vs 9.875%) in years 8-30

**ARM Only Mode:**
- Refinancing costs $111k more during ARM periods
- You're paying for **more months** at a rate (24 months at 4.875% + 84 months at 4% = 108 months)
- vs. just 84 months at 4.875% on original loan

**Strategic Insight:**
If you plan to refinance again or sell before year 7, the refinance might NOT be worth it despite the lower rate!

## Using the Feature

### Command-Line Version (`arm_refi_cost_calculator.py`)

Edit the variable in the script:

```python
# Comparison mode
compare_arm_only = False     # False: Full 30-year (default)
compare_arm_only = True      # True: ARM periods only
```

### GUI Version (`arm_refi_calculator_gui.py`)

Simply check or uncheck the checkbox:

```
☐ Compare ARM periods only (exclude adjustable rate periods)
ℹ️  Useful if you plan to refinance or sell before the adjustable period starts
```

## Output Examples

### Full 30-Year Mode Output:

```
COMPARISON
================================================================================
MODE: FULL 30-YEAR COMPARISON (Including All Periods)
--------------------------------------------------------------------------------

  SAVINGS from refinancing:    $403,074.83
  Percentage saved:            11.73%

  Original loan total:         $3,437,013.65
  Refinanced loan total:       $3,033,938.82
```

### ARM Periods Only Output:

```
COMPARISON
================================================================================
MODE: ARM PERIODS ONLY (Excluding Adjustable Rate Periods)
--------------------------------------------------------------------------------

  ORIGINAL LOAN (ARM Period Only - Months 1-84):
    Total Paid:                  $572,560.96
    Interest Paid:               $414,392.41
    Principal Paid:              $158,168.56

  REFINANCE SCENARIO (ARM Periods Only - Months 1-108):
    Before Refi (Months 1-24):
      Total Paid:                $163,588.85
      Interest Paid:             $123,750.23
    New ARM Period (Months 25-108):
      Total Paid:                $520,040.08
      Interest Paid:             $324,233.97
    Combined ARM Total:          $683,628.93
    Combined ARM Interest:       $447,984.20

  ARM PERIOD ADDITIONAL COST:  $111,067.97
  Percentage increase:         19.40%

  Original ARM period total:   $572,560.96
  Refinanced ARM period total: $683,628.93

  NOTE: This comparison excludes adjustable rate periods (months 85-360)
        Useful if you plan to refinance or sell before rates adjust.
```

## Use Cases

### Use Case 1: Planning to Sell in 5 Years

**Situation:** You plan to sell the property in 5 years (60 months).

**Action:**
1. Enable "ARM Periods Only" mode
2. Set refinance timing to various months (12, 24, 36, 48, 60)
3. Compare ARM-only costs

**Why:** You'll never experience the adjustable rate period, so total 30-year cost is irrelevant.

### Use Case 2: Serial Refinancer

**Situation:** You refinance every 2-3 years to get the best rates.

**Action:**
1. Use "ARM Periods Only" mode
2. Compare interest paid during just the ARM periods

**Why:** You're constantly resetting to new fixed rates, so long-term adjustable rates don't matter.

### Use Case 3: Traditional Long-Term Owner

**Situation:** You'll keep the loan for the full 30 years.

**Action:**
1. Use "Full 30-Year" mode (default)
2. Focus on total lifetime costs

**Why:** You need to account for the adjustable rate periods in years 8-30.

### Use Case 4: Uncertain Future

**Situation:** You're not sure how long you'll keep the property.

**Action:**
1. Run calculations in **both modes**
2. Compare the results

**Why:** Understand both short-term and long-term implications.

## Key Insights

### 1. Time Horizon Matters
- **Short-term (<7 years):** Use ARM-only mode
- **Long-term (full 30 years):** Use full comparison mode
- **Uncertain:** Check both modes

### 2. Refinancing Extends Your Timeline
- Original loan: 84 months at fixed rate
- After refinancing at month 24: 84 MORE months at new fixed rate
- Total: 108 months instead of 84
- This means **more months of paying interest**, even at a lower rate

### 3. Rate Difference vs. Time Extension
- Lower rate saves money per month
- But more months means more total payments
- ARM-only mode helps you see this tradeoff

### 4. Breakeven Analysis Still Uses 30-Year
- The breakeven rate calculation always uses the full 30-year cost
- This is intentional - it shows the "true" breakeven rate
- ARM-only mode is for evaluating your specific situation

## Tips for Maximum Benefit

### 1. Match Mode to Your Plan
```
Plan to keep loan < 7 years → Use ARM-only mode
Plan to keep loan 7-30 years → Use Full 30-year mode
Unsure → Compare both modes
```

### 2. Test Multiple Timing Scenarios
- Refinance at 12, 24, 36, 48, 60 months
- See how timing affects ARM-only costs
- Earlier refinancing = more total months in ARM periods

### 3. Consider Your Risk Tolerance
- ARM-only mode shows short-term costs
- Full 30-year shows worst-case if rates spike
- Balance both perspectives

### 4. Compare Multiple Offers
- Open multiple GUI windows
- Use same timing but different rates
- Toggle between comparison modes
- Find the best deal for your timeline

## Summary Table

| Factor | Full 30-Year Mode | ARM-Only Mode |
|--------|-------------------|---------------|
| **Time Horizon** | Full loan term (360 months) | Fixed rate periods only (84-108 months) |
| **Best For** | Long-term owners | Short-term owners/refinancers |
| **Includes** | All periods | Only ARM fixed-rate periods |
| **Shows** | Lifetime cost | Short-term cost impact |
| **Use When** | Keeping loan 10+ years | Selling/refinancing in < 7 years |

## Frequently Asked Questions

### Q: Which mode should I use?
**A:** Depends on your plans. If you'll definitely keep the loan long-term, use Full 30-Year. If you'll definitely sell/refi before year 7, use ARM-only. If uncertain, check both.

### Q: Why does ARM-only sometimes show refinancing costs MORE?
**A:** Because you're extending the number of months in fixed-rate periods. Even at a lower rate, more months = more total payments.

### Q: Does the breakeven rate change between modes?
**A:** No, breakeven rate is always calculated using full 30-year costs. It's your target for negotiating, regardless of comparison mode.

### Q: Can I use both modes simultaneously?
**A:** In the GUI, open two windows and check the box in one. In command-line, run twice with different settings.

### Q: Which mode is "correct"?
**A:** Both are correct - they just answer different questions. Use the mode that matches your actual situation.

---

**Remember:** The best comparison mode is the one that matches your real-world plans!

