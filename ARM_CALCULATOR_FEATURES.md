# ARM Refinance Calculator - Complete Feature Guide

## 🎯 Quick Summary

The ARM Refinance Calculator now includes **3 powerful comparison modes** and a comprehensive help system to analyze your refinancing decision from multiple angles.

## 📊 Available Features

### ✅ Feature 1: Full 30-Year Comparison (Default Mode)

**What it shows:** Total cost over entire loan term

```
Original Loan:  $3,437,013.65
Refinanced:     $3,031,346.85
SAVINGS:        $405,666.80 (11.80%)
```

**Best for:** Long-term homeowners keeping loan 10+ years

**Breakeven Rate:** 5.368% (new rate threshold)
- Your 4.0% rate is BELOW breakeven ✓
- Accounts for escaping high cap rate sooner

---

### ✅ Feature 2: ARM Periods Only Comparison

**What it shows:** Interest costs during ARM periods only + refinance costs

```
Original ARM Interest:  $414,392.41
Refinanced ARM Cost:    $449,465.49 (interest + $2k refi cost)
ADDITIONAL COST:        $35,073.09 (8.46%)
```

**Best for:** Short-term owners selling/refinancing in 5-7 years

**Breakeven Rate:** 3.584% (ARM-only threshold)
- Your 4.0% rate is ABOVE breakeven ✗
- Need very low rate to offset extended ARM period + costs

**Key Insight:** Refinancing extends fixed-rate period from 84 to 108 months!

---

### ✅ Feature 3: Custom Adjustable Rate

**What it shows:** Comparison using same specified rate for years 8-30 in BOTH scenarios

**Example:** Setting custom rate to 4.5%

```
BEFORE (with cap rates):
  Original: 4.875% → 9.875%
  Refinance: 4.0% → 9.0%
  Savings: $405,666.80

AFTER (with custom 4.5%):
  Original: 4.875% → 4.5%
  Refinance: 4.0% → 4.5%
  Savings: $74,240.76
```

**Best for:** 
- Planning to refinance again at year 7
- Testing specific future rate assumptions
- Isolating ARM period advantages

---

## 🔧 How to Use Each Mode

### Scenario 1: "Should I refinance now?" (Long-term owner)

**Your situation:** Keeping the house for 15+ years

**Settings:**
- ☐ ARM periods only: UNCHECKED
- ☐ Custom adjustable rate: UNCHECKED

**Look at:**
- Full 30-year savings
- Breakeven rate (full 30-year): 5.368%
- Your rate: 4.0%

**Decision:** 4.0% < 5.368% → **REFINANCE** ✓

---

### Scenario 2: "Should I refinance?" (Selling in 5 years)

**Your situation:** Selling the property in 60 months

**Settings:**
- ☑ ARM periods only: CHECKED
- ☐ Custom adjustable rate: UNCHECKED

**Look at:**
- ARM period additional cost/savings
- Breakeven rate (ARM-only): 3.584%
- Your rate: 4.0%

**Decision:** 4.0% > 3.584% → **DON'T REFINANCE** ✗
*(Costs $35k more during ARM periods)*

---

### Scenario 3: "Planning to refi again at year 7"

**Your situation:** Will refinance to 4.5% at year 7 regardless

**Settings:**
- ☐ ARM periods only: UNCHECKED
- ☑ Custom adjustable rate: CHECKED (set to 4.5%)

**Look at:**
- Total cost with same 4.5% rate in years 8-30 for both
- Isolates the ARM period rate difference impact

**Decision:** Compare the isolated ARM benefit without cap rate advantage

---

## 📋 Complete Feature Comparison Table

| Feature | Full 30-Year | ARM Only | Custom Rate |
|---------|--------------|----------|-------------|
| **Time Horizon** | 360 months | 84-108 months | 360 months |
| **Includes Adjustable Period** | Yes | No | Yes |
| **Breakeven Rate** | 5.368% | 3.584% | Varies |
| **Focus** | Lifetime cost | Short-term cost | Rate isolation |
| **Best For** | Long-term owners | Short-term owners | Future planning |
| **Your 4.0% Rate** | ✓ GOOD | ✗ BAD | Depends on custom rate |

## 💡 Strategic Insights

### Insight 1: The Extended Timeline Effect

When you refinance:
- Original: 84 months at 4.875%
- After refi at month 24: 24 months at 4.875% + 84 months at 4.0% = **108 total months**

**Result:** You're in fixed-rate periods 24 months LONGER!
- Lower rate helps, but more months means more interest
- Need rate MUCH lower than current to overcome this

### Insight 2: Cap Rate Advantage

Default cap rates:
- Current: 9.875%
- New: 9.0%

**Over 276 months (years 8-30):**
- 0.875% difference = **$332k savings** over 23 years
- This is WHERE most savings come from in 30-year comparison
- ARM-only mode excludes this, showing true short-term picture

### Insight 3: Breakeven Rate Timing

| Refinance Month | Full 30-Yr Breakeven | ARM-Only Breakeven |
|-----------------|---------------------|-------------------|
| 12 | 5.098% | ~3.2% |
| 24 | 5.368% | 3.584% |
| 36 | 5.642% | ~3.9% |
| 60 | 6.300% | ~4.5% |
| 72 | 6.682% | ~5.0% |

**Pattern:** 
- Later refinancing = Higher breakeven rates = More flexibility
- Wait longer → Easier to find beneficial rates

---

## 🎨 GUI Features

### Buttons

| Button | Function |
|--------|----------|
| **Calculate** | Run calculations with current parameters |
| **New Window** | Open comparison window with copied values |
| **Clear Results** | Clear the output display |
| **Help** | Show this comprehensive help guide |

### Checkboxes

| Checkbox | Effect |
|----------|--------|
| **Compare ARM periods only** | Switch between full 30-year and ARM-only comparison |
| **Use custom adjustable rate** | Override cap rates with single custom rate for years 8-30 |

### Input Fields

All values automatically validate on calculation. Invalid inputs show error dialog.

---

## 📖 Reading the Output

### Full 30-Year Mode

```
COMPARISON
==========
MODE: FULL 30-YEAR COMPARISON

  SAVINGS from refinancing:    $405,666.80
  Percentage saved:            11.80%
```
**Interpretation:** Refinancing saves $405k over the entire loan life

### ARM-Only Mode

```
COMPARISON
==========
MODE: ARM PERIODS ONLY - Interest & Refinance Costs

  ARM PERIOD ADDITIONAL COST:  $35,073.09
  Percentage increase:         8.46%
  
  Breakeven ARM rate: 3.584%
  Your 4.0% > Breakeven → costs more during ARM periods
```
**Interpretation:** Refinancing costs $35k more during ARM periods, but saves $405k over 30 years

### Decision Framework

| Your Plan | Check This Mode | Decision Criteria |
|-----------|-----------------|-------------------|
| Keep 10+ years | Full 30-Year | New rate < Full breakeven |
| Sell in 5-7 years | ARM Only | New rate < ARM breakeven |
| Refi at year 7 | Custom Rate | Compare total costs |
| Unsure | Both modes | Consider both perspectives |

---

## 🚀 Getting Started Workflow

### Step 1: Basic Calculation
1. Enter all loan parameters
2. Click "Calculate"
3. Review full 30-year comparison

### Step 2: Check ARM-Only
1. Check "Compare ARM periods only"
2. Click "Calculate"
3. Compare ARM breakeven rate

### Step 3: Test Custom Rate (Optional)
1. Check "Use custom adjustable rate"
2. Enter expected rate at year 7
3. Click "Calculate"
4. See isolated ARM period impact

### Step 4: Compare Multiple Offers
1. Click "New Window" for each offer
2. Adjust only rate and costs
3. Compare side-by-side
4. Choose best option

---

## ⚠️ Important Notes

1. **Refinance costs are OUT-OF-POCKET**
   - Not added to loan principal
   - No interest charged on closing costs
   - One-time expense

2. **Principal is the same**
   - ARM-only mode excludes principal comparison
   - Only interest and refi costs differ
   - Focuses on true cost difference

3. **Breakeven varies by mode**
   - Full 30-year: Usually higher (5.368%)
   - ARM-only: Usually lower (3.584%)
   - Use the one matching your timeline

4. **Cap rates are estimates**
   - Actual rates may vary based on index
   - Calculator uses maximum cap (initial + 5%)
   - Real rates could be lower

---

## 📞 Quick Reference

**Most Important Number:** **Breakeven Rate**
- Below breakeven → Refinance
- Above breakeven → Don't refinance

**Choose Your Mode:**
- **Keeping long-term?** → Full 30-year mode
- **Selling soon?** → ARM-only mode
- **Planning future refi?** → Custom rate mode

**Multiple Offers?** → Use "New Window" for each

**Want to experiment?** → Test different timing scenarios

---

Created by: ARM Refinance Calculator v2.0
Last Updated: November 2025

