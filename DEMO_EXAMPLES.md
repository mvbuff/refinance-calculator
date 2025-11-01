# ARM Refinance Calculator - Demo Examples

This guide provides real-world examples with actual numbers to help you understand how to use the calculator.

---

## 📋 Example 1: Standard Refinance Analysis

### Scenario
- **Current Situation:** $1,288,000 loan at 4.875% ARM
- **Refinance Offer:** 4.0% with $2,000 closing costs
- **Timeline:** Refinance after 2 years (24 months)
- **Goal:** See if refinancing saves money over 30 years

### Using Streamlit Web App

**Step 1: Launch**
```bash
streamlit run streamlit_app.py
```

**Step 2: Inputs** (Sidebar)
- Loan Amount: `1288000`
- Current ARM Rate: `4.875`
- New ARM Rate: `4.0`
- Refinance After: `24` months
- Refinance Cost: `2000`
- Compare ARM periods only: ☐ Unchecked
- Use custom rate: ☐ Unchecked

**Step 3: Calculate**
- Click "Calculate" button

**Step 4: Results**

**Summary Metrics (Top of page):**
```
Original Loan Total:     $3,437,013.65
Refinanced Loan Total:   $3,031,346.85
Total Savings:           $405,666.80 (11.80%)
```

**Breakeven Analysis Tab:**
```
Current ARM Rate:         4.875%
Breakeven NEW ARM Rate:   5.368%
Your New ARM Rate:        4.000%

✓ Your rate (4.000%) is 1.368% BELOW breakeven
  → Refinancing is BENEFICIAL
```

**Monthly Payment Details:**
```
Original Monthly Payment (Years 1-7):   $6,804.98
New Monthly Payment (Years 1-7):        $6,154.84
Monthly Savings:                        $650.14

Months to break even on $2,000 cost:    3.1 months (0.3 years)
```

### Decision
**REFINANCE ✓**
- Save $405,666 over 30 years
- Save $650/month immediately
- Break even on costs in just 3 months
- New rate is 1.37% below breakeven

---

## 📋 Example 2: Planning to Sell in 5 Years

### Scenario
- **Same loan:** $1,288,000 at 4.875%
- **Same offer:** 4.0% with $2,000 costs
- **Timeline:** Refinance after 2 years
- **Goal:** See if refinancing makes sense for SHORT-TERM (selling in 5 years)

### Using Streamlit Web App

**Step 1-2: Same as Example 1**

**Step 3: Enable ARM-Only Mode**
- ✅ **Check "Compare ARM periods only"**
- This focuses on just the fixed-rate years (1-7), ignoring years 8-30

**Step 4: Calculate**

**Step 5: Results (ARM-Only Mode)**

**Comparison Tab:**
```
MODE: ARM Periods Only - Interest & Refinance Costs Comparison

ORIGINAL LOAN (ARM Period - Months 1-84):
  Interest Paid:               $414,392.41
  Refinance Cost:              $0.00
  Total Cost (Interest only):  $414,392.41

REFINANCE SCENARIO (ARM Periods - Months 1-108):
  Before Refi (Months 1-24):
    Interest Paid:             $96,734.28
  New ARM Period (Months 25-108):
    Interest Paid:             $350,731.21
  Combined ARM Interest:       $447,465.49
  Refinance Cost:              $2,000.00
  Total Cost (Interest + Refi): $449,465.49

✗ ARM PERIOD ADDITIONAL COST: $35,073.09 (8.46%)
```

**ARM-Only Breakeven Rate:**
```
Current ARM rate:            4.875%
Your new ARM rate:           4.000%
Breakeven ARM rate:          3.584%

✗ Your rate (4.000%) > Breakeven (3.584%)
  → Costs $35,073.09 more during ARM periods
```

### Decision
**DON'T REFINANCE ✗** (if selling in 5-7 years)
- Costs $35,073 MORE during ARM periods
- Need a rate below 3.584% to save in short term
- BUT: If you end up keeping the house, you'd save $405K (see Example 1)

### Interpretation
This demonstrates an important insight:
- **Short-term (ARM only):** Refinancing costs more
- **Long-term (30 years):** Refinancing saves a lot
- **Decision depends on your timeline!**

---

## 📋 Example 3: Comparing Multiple Lender Offers

### Scenario
You have 3 competing offers:
- **Lender A:** 4.000% with $2,000 costs
- **Lender B:** 3.875% with $4,500 costs
- **Lender C:** 4.125% with $1,000 costs

Which is best?

### Using Streamlit Web App

**Test Lender A:**
- New ARM Rate: `4.0`
- Refinance Cost: `2000`
- Click "Calculate"
- **Result:** Save $405,666 over 30 years

**Test Lender B:**
- New ARM Rate: `3.875`
- Refinance Cost: `4500`
- Click "Calculate"
- **Result:** Save $467,523 over 30 years

**Test Lender C:**
- New ARM Rate: `4.125`
- Refinance Cost: `1000`
- Click "Calculate"
- **Result:** Save $343,809 over 30 years

### Results Summary

| Lender | Rate | Costs | 30-Year Savings | Monthly Savings |
|--------|------|-------|----------------|----------------|
| A | 4.000% | $2,000 | $405,666 | $650 |
| B | 3.875% | $4,500 | $467,523 | $752 |
| C | 4.125% | $1,000 | $343,809 | $548 |

### Decision
**CHOOSE LENDER B ✓**
- Highest total savings: $467,523
- Best monthly savings: $752
- Worth paying extra $2,500 in costs for $62,000 more savings

### Break-Even Analysis
How long until Lender B's extra costs are recouped?

```
Extra cost vs Lender A: $4,500 - $2,000 = $2,500
Extra monthly savings:  $752 - $650 = $102

Break-even: $2,500 / $102 = 24.5 months (2 years)
```

If you're keeping the house for 2+ years, Lender B is the best choice.

---

## 📋 Example 4: Custom Future Refinance Planning

### Scenario
- **Current loan:** $1,288,000 at 4.875%
- **Refinance offer:** 4.0% with $2,000 costs after 2 years
- **Future plan:** You're planning to refinance AGAIN at year 7 to 4.5% (before rates adjust)
- **Goal:** See if the first refinance is still worth it

### Using Streamlit Web App

**Step 1: Enable Custom Rate**
- ✅ Check "Use custom rate for Years 8-30"
- Custom Adjustable Rate: `4.5`

**Step 2: Other Inputs**
- Same as Example 1
- Compare ARM periods only: ☐ Unchecked

**Step 3: Calculate**

**Step 4: Results**

**Comparison:**
```
MODE: FULL 30-YEAR COMPARISON (Including All Periods)

Original loan total:         $2,814,394.79
  (4.875% for years 1-7, then 4.5% for years 8-30)

Refinanced loan total:       $2,759,647.99
  (4.0% for years 1-7, then 4.5% for years 8-30)

SAVINGS from refinancing:    $54,746.80 (1.94%)
```

**Interpretation:**
```
Without custom rate (using cap rates):
  Savings: $405,666 (11.80%)

With custom rate (both at 4.5% for years 8-30):
  Savings: $54,746 (1.94%)

Difference: $350,920

Why? The original analysis assumed you'd stay at 9.875% cap 
in years 8-30, but with custom rate, you're modeling a refi 
to 4.5% in both scenarios. The savings are now just from 
the lower rate in years 1-7 (4.0% vs 4.875%).
```

### Decision
**STILL REFINANCE ✓**
- Even with future refi planned, still save $54,746
- No downside to getting the lower rate now
- If you DON'T refi at year 7, you save even more ($405K)

---

## 📋 Example 5: Marginal Deal Analysis

### Scenario
- **Current loan:** $1,288,000 at 4.875%
- **Refinance offer:** 5.25% with $2,000 costs (HIGHER rate!)
- **Question:** Why would anyone refinance to a higher rate?

### Using Streamlit Web App

**Inputs:**
- Loan Amount: `1288000`
- Current ARM Rate: `4.875`
- New ARM Rate: `5.25` ← Higher than current!
- Refinance After: `24`
- Refinance Cost: `2000`

**Calculate**

**Results:**
```
Original loan total:         $3,437,013.65
Refinanced loan total:       $3,573,159.45

ADDITIONAL COST from refi:   $136,145.80 (3.96%)

✗ DON'T REFINANCE
```

**Breakeven Analysis:**
```
Current ARM rate:            4.875%
Breakeven NEW ARM rate:      5.368%
Your new ARM rate:           5.250%

✗ Your new rate (5.250%) is 0.118% ABOVE breakeven
  → Refinancing is NOT beneficial
```

### Decision
**DON'T REFINANCE ✗**
- Higher rate costs $136,145 more
- Rate is above breakeven (5.368%)

**BUT WAIT...** What if you're planning to refi again before the cap rate kicks in?

**Test with Custom Rate:**
- ✅ Use custom rate for Years 8-30: `5.0`
- This models refinancing to 5.0% at year 7 in BOTH scenarios

**New Results:**
```
Original loan total:         $2,702,538.99
  (4.875% years 1-7, 5.0% years 8-30)

Refinanced loan total:       $2,838,685.79
  (5.25% years 1-7, 5.0% years 8-30)

ADDITIONAL COST:             $136,145.80

✗ STILL DON'T REFINANCE
```

### Lesson
Even with custom modeling, a higher rate is still a bad deal. Only refinance to a **lower** rate!

---

## 📋 Example 6: Break-Even Timing Analysis

### Scenario
- **Current loan:** $1,288,000 at 4.875%
- **Refinance offer:** 4.0% with $2,000 costs
- **Question:** WHEN is the best time to refinance?

### Using Streamlit Web App

**Test Different Timings:**

Navigate to "Breakeven Analysis" tab → See timing table:

```
BREAKEVEN RATES FOR DIFFERENT REFINANCE TIMINGS:
(With refi cost of $2,000)

Month  Years   Breakeven Rate    Your Rate    Decision
   12    1.0       5.407%        4.000%      ✓ GOOD
   24    2.0       5.368%        4.000%      ✓ GOOD
   36    3.0       5.332%        4.000%      ✓ GOOD
   48    4.0       5.299%        4.000%      ✓ GOOD
   60    5.0       5.269%        4.000%      ✓ GOOD
   72    6.0       5.242%        4.000%      ✓ GOOD
```

**Interpretation:**
- Your 4.0% rate is below breakeven for ALL timings
- Breakeven rate decreases slightly as you wait longer
- Earlier refinance = better (more time at lower rate)
- ALL timings are good, but SOONER is better

**Manual Test - Refinance After 12 Months:**
- Refinance After: `12` months
- Click "Calculate"
- **Result:** Save $417,902 (vs $405,666 at 24 months)

**Manual Test - Refinance After 60 Months:**
- Refinance After: `60` months
- Click "Calculate"
- **Result:** Save $344,058 (vs $405,666 at 24 months)

### Decision
**REFINANCE AS SOON AS POSSIBLE ✓**
- Sooner = more savings
- 12 months: $417,902 savings
- 24 months: $405,666 savings
- 60 months: $344,058 savings

---

## 📋 Example 7: High Closing Costs

### Scenario
- **Current loan:** $1,288,000 at 4.875%
- **Refinance offer:** 4.0% with **$15,000** costs (broker fees, points, etc.)
- **Question:** Are high closing costs worth it?

### Using Streamlit Web App

**Inputs:**
- Same as Example 1, but:
- Refinance Cost: `15000`

**Results:**
```
Original loan total:         $3,437,013.65
Refinanced loan total:       $3,044,346.85

SAVINGS from refinancing:    $392,666.80 (11.42%)
```

**Break-Even Analysis:**
```
Monthly payment savings:     $650.14
Months to break even:        23.1 months (1.9 years)
```

**Breakeven Rate:**
```
Breakeven NEW ARM rate:      5.323%
Your new ARM rate:           4.000%

✓ Your rate (4.000%) is 1.323% BELOW breakeven
  → Refinancing is BENEFICIAL
```

### Decision
**STILL REFINANCE ✓** (even with high costs)
- Save $392,666 over 30 years (vs $405,666 with $2K costs)
- Break even in 23 months (vs 3 months with $2K costs)
- If keeping house for 2+ years, worth it

### Comparison

| Closing Costs | 30-Year Savings | Break-Even Time |
|--------------|-----------------|-----------------|
| $2,000 | $405,666 | 3.1 months |
| $5,000 | $402,666 | 7.7 months |
| $10,000 | $397,666 | 15.4 months |
| $15,000 | $392,666 | 23.1 months |

**Lesson:** Lower costs are better, but even $15K costs can be worth it for long-term homeowners.

---

## 🎯 Key Takeaways

1. **Long-term vs Short-term:**
   - 30-year comparison → Long-term homeowners
   - ARM-only comparison → Planning to sell/refi early

2. **Lower rate is better:**
   - Below breakeven = good
   - Above breakeven = bad

3. **Timing matters:**
   - Sooner = more savings
   - Check breakeven timing table

4. **Costs matter, but less than rate:**
   - Lower costs are better
   - But even high costs can be worth it with low enough rate

5. **Multiple offers:**
   - Always compare at least 2-3 lenders
   - Lowest rate doesn't always mean most savings (check total costs)

6. **Plan for the future:**
   - Use custom rate if planning to refi again
   - Test different scenarios

---

## 💪 Practice Exercise

Try this yourself:

**Your Scenario:**
- Loan: $800,000
- Current Rate: 5.25%
- Offer 1: 4.75% with $3,000 costs
- Offer 2: 4.5% with $6,000 costs
- Timeline: Refinance after 18 months
- Plan: Sell house in 6 years

**Tasks:**
1. Calculate 30-year savings for both offers
2. Calculate ARM-only costs for both offers
3. Determine which offer is better
4. Find the breakeven rate

**Expected Results:**
- Offer 1 saves more in ARM-only mode (lower costs)
- Offer 2 saves more in 30-year mode (lower rate)
- Decision depends on your timeline!

---

**Happy Calculating! 🏠💰**

