# ARM Types Quick Reference Guide

A quick guide to configuring different ARM loan types in the calculator.

---

## 📋 Common ARM Types

### 3/1 ARM (3-Year Fixed)

**Description:** Fixed rate for 3 years, then adjusts annually

**Settings:**
- Loan Term: `30` years
- ARM Fixed Period: `3` years
- Refinance After: 1-36 months

**Best For:**
- Short-term homeowners (selling in 3-5 years)
- Expecting significant income increase
- Willing to accept earlier rate risk for lower initial rate

**Example:**
```
Loan Amount:         $1,288,000
Loan Term:          30 years
ARM Fixed Period:   3 years
Current ARM Rate:   4.25%
```

---

### 5/1 ARM (5-Year Fixed)

**Description:** Fixed rate for 5 years, then adjusts annually

**Settings:**
- Loan Term: `30` years
- ARM Fixed Period: `5` years
- Refinance After: 1-60 months

**Best For:**
- Medium-term homeowners (selling in 5-7 years)
- Balance between low rate and stability
- Most popular ARM option

**Example:**
```
Loan Amount:         $1,288,000
Loan Term:          30 years
ARM Fixed Period:   5 years
Current ARM Rate:   4.5%
```

---

### 7/1 ARM (7-Year Fixed) - Default

**Description:** Fixed rate for 7 years, then adjusts annually

**Settings:**
- Loan Term: `30` years
- ARM Fixed Period: `7` years
- Refinance After: 1-84 months

**Best For:**
- Longer-term stability
- Planning to refinance or sell within 7-10 years
- Lower risk tolerance

**Example:**
```
Loan Amount:         $1,288,000
Loan Term:          30 years
ARM Fixed Period:   7 years
Current ARM Rate:   4.875%
```

---

### 10/1 ARM (10-Year Fixed)

**Description:** Fixed rate for 10 years, then adjusts annually

**Settings:**
- Loan Term: `30` years
- ARM Fixed Period: `10` years
- Refinance After: 1-120 months

**Best For:**
- Maximum stability with ARM pricing
- Long-term homeowners wanting protection
- Rate between ARM and fixed-rate mortgages

**Example:**
```
Loan Amount:         $1,288,000
Loan Term:          30 years
ARM Fixed Period:   10 years
Current ARM Rate:   5.0%
```

---

## 🏡 Different Loan Terms

### 15-Year Loan with 7/1 ARM

**Description:** Pay off in 15 years, 7 years fixed

**Settings:**
- Loan Term: `15` years
- ARM Fixed Period: `7` years
- Adjustable Period: Only 8 years (vs 23 for 30-year)

**Benefits:**
- Much less adjustable period exposure
- Significantly less total interest
- Higher monthly payment

**Example:**
```
Loan Amount:         $1,288,000
Loan Term:          15 years
ARM Fixed Period:   7 years
Current ARM Rate:   4.25%
```

**Comparison:**
- 30-year 7/1: 7 years fixed, 23 years adjustable
- 15-year 7/1: 7 years fixed, 8 years adjustable
- **Difference:** 15 fewer years of rate risk!

---

### 20-Year Loan with 5/1 ARM

**Description:** Middle ground - pay off in 20 years

**Settings:**
- Loan Term: `20` years
- ARM Fixed Period: `5` years
- Adjustable Period: 15 years

**Benefits:**
- Lower monthly payment than 15-year
- Less interest than 30-year
- Moderate adjustable period exposure

**Example:**
```
Loan Amount:         $1,288,000
Loan Term:          20 years
ARM Fixed Period:   5 years
Current ARM Rate:   4.5%
```

---

## 🔄 Refinance Scenarios

### Scenario 1: 3/1 ARM → 7/1 ARM Refinance

**Original:**
```
Loan Term:          30 years
ARM Fixed Period:   3 years
Current ARM Rate:   4.75%
```

**Refinance After:** 18 months (halfway through fixed period)

**New Loan:**
```
New ARM Rate:       4.25%
Refi Cost:          $2,500
```

**Analysis:**
- Give up 1.5 years at 4.75%
- Get 7 years at 4.25%
- Plus lower rate (0.5% less)
- Calculator shows if this is worth $2,500 cost

---

### Scenario 2: 7/1 ARM → 10/1 ARM Refinance

**Original:**
```
Loan Term:          30 years
ARM Fixed Period:   7 years
Current ARM Rate:   4.875%
```

**Refinance After:** 48 months (4 years in)

**New Loan:**
```
ARM Fixed Period:   10 years ← Longer stability
New ARM Rate:       5.0% ← Slightly higher
Refi Cost:          $3,000
```

**Analysis:**
- Trade: 0.125% higher rate for 3 more fixed years
- Original: 3 years fixed remaining
- New: 10 years fixed
- Net gain: 7 more years of stability
- Calculator shows total cost of this tradeoff

---

### Scenario 3: 30-Year → 15-Year Refinance

**Original:**
```
Loan Amount:        $1,288,000
Loan Term:          30 years
ARM Fixed Period:   7 years
Current ARM Rate:   4.875%
```

**Refinance After:** 24 months

**New Loan:**
```
Loan Term:          15 years ← Shorter!
ARM Fixed Period:   7 years
New ARM Rate:       4.25%
Refi Cost:          $3,500
```

**Analysis:**
- Dramatically different monthly payment
- Much less total interest
- Only 8 years adjustable vs 23
- Calculator shows total savings

---

## 💡 Decision Framework

### Choose 3/1 ARM if:
- ✅ Selling/refinancing in 3-5 years
- ✅ Want lowest possible rate
- ✅ High risk tolerance
- ✅ Expecting income growth

### Choose 5/1 ARM if:
- ✅ Selling/refinancing in 5-7 years
- ✅ Want balance of rate and stability
- ✅ Moderate risk tolerance
- ✅ Most common choice

### Choose 7/1 ARM if:
- ✅ Selling/refinancing in 7-10 years
- ✅ Want more stability
- ✅ Lower risk tolerance
- ✅ Uncertain about timeline

### Choose 10/1 ARM if:
- ✅ Long-term homeowner
- ✅ Want maximum stability with ARM pricing
- ✅ Lowest risk tolerance among ARMs
- ✅ Planning to keep loan 10+ years

---

## 📊 Rate vs Stability Tradeoff

Typical rate relationship (example):

```
ARM Type    Typical Rate    Fixed Period    Risk Level
--------    ------------    ------------    ----------
3/1         4.25%          3 years         High
5/1         4.50%          5 years         Medium-High
7/1         4.75%          7 years         Medium
10/1        5.00%          10 years        Low
30-yr Fixed 5.25%          30 years        None
```

**Pattern:**
- Shorter fixed period = Lower rate = Higher risk
- Longer fixed period = Higher rate = Lower risk

**The Calculator Helps You:**
- Quantify the cost of extra stability
- Determine if lower rate justifies earlier risk
- Compare total costs over your actual timeline

---

## 🎯 Using the Calculator for ARM Comparisons

### Step 1: Calculate Original Loan
```
Loan Amount:         $1,288,000
Loan Term:          30 years
ARM Fixed Period:   5 years (your current loan)
Current ARM Rate:   4.5%
```
Note the total cost.

### Step 2: Calculate Refinance Option 1 (Lower Rate, Same Period)
```
New ARM Rate:       4.0%
ARM Fixed Period:   5 years (same as original)
Refinance After:    24 months
Refi Cost:          $2,000
```
Compare total cost with original.

### Step 3: Calculate Refinance Option 2 (Higher Rate, Longer Period)
```
New ARM Rate:       4.75%
ARM Fixed Period:   10 years (longer stability!)
Refinance After:    24 months
Refi Cost:          $3,000
```
Compare total cost with original and Option 1.

### Step 4: Analyze Results

**Option 1 (4.0%, 5-year):**
- Pros: Lowest rate, lowest monthly payment
- Cons: Same 5-year period, adjusts at year 5

**Option 2 (4.75%, 10-year):**
- Pros: 10 years of stability, no adjustment until year 10
- Cons: Higher rate, higher monthly payment

**Decision:**
- If selling in <7 years → Choose Option 1 (lower rate)
- If keeping 7-10 years → Choose Option 2 (stability)
- If keeping 10+ years → Consider fixed-rate instead

---

## 🧮 Quick Calculation Examples

### Example 1: 5/1 ARM Analysis

**Inputs:**
```
Loan Amount:         $1,000,000
Loan Term:          30 years
ARM Fixed Period:   5 years
Current ARM Rate:   4.5%
Cap Rate:           9.5% (4.5% + 5%)
```

**Results:**
- Monthly Payment (Years 1-5): ~$5,067
- Monthly Payment (Years 6-30): ~$8,785 (at cap)
- Total Paid: ~$2,687,000
- Total Interest: ~$1,687,000

### Example 2: 7/1 ARM Analysis (Same Rate)

**Inputs:**
```
Loan Amount:         $1,000,000
Loan Term:          30 years
ARM Fixed Period:   7 years ← Only change
Current ARM Rate:   4.5%
Cap Rate:           9.5%
```

**Results:**
- Monthly Payment (Years 1-7): ~$5,067
- Monthly Payment (Years 8-30): ~$9,078 (at cap)
- Total Paid: ~$2,740,000
- Total Interest: ~$1,740,000

**Comparison:**
- Extra 2 years at low rate is worth it
- But costs ~$53,000 more total (23 years adjustable vs 25)
- **Unless you refinance/sell before year 7!**

---

## 📈 Market Insights

### When to Choose ARMs

**ARMs Make Sense When:**
- You'll sell before adjustment period
- You'll refinance before adjustment period
- You expect rates to drop in future
- You can handle payment increases
- You want lowest initial payment

**Fixed-Rate Makes Sense When:**
- Keeping home 10+ years
- Rates are historically low
- You want payment certainty
- You can't handle increases
- You're risk-averse

### Using the Calculator to Decide

1. **Set your ARM type** (3, 5, 7, or 10 years)
2. **Enter current rates**
3. **Model refinance scenarios** at different times
4. **Check ARM-only mode** if selling early
5. **Compare with fixed-rate** (set ARM period = loan term)

---

## 🎓 Advanced Strategies

### Strategy 1: ARM Ladder

**Concept:** Refinance every few years to stay in fixed period

**Example:**
- Start: 5/1 ARM at 4.5%
- Year 3: Refinance to new 5/1 at 4.25%
- Year 6: Refinance to new 5/1 at 4.0%
- **Never experience adjustable period!**

**Calculator Use:**
- Model each refinance
- Account for costs
- Verify it's cheaper than fixed-rate

### Strategy 2: ARM to Fixed Conversion

**Concept:** Start with ARM, convert to fixed before adjustment

**Example:**
- Start: 7/1 ARM at 4.75%
- Year 6: Refinance to 30-year fixed at 5.0%
- **Lock in before adjustment, benefit from 6 years lower payment**

**Calculator Use:**
- Compare 7 years ARM + fixed vs 7 years fixed only
- Calculate savings from lower initial payment
- Verify refinance cost is justified

---

## 📞 Quick Reference Table

| Loan Type | Fixed Period | Typical Rate* | Best Timeline | Risk Level |
|-----------|-------------|--------------|---------------|------------|
| 3/1 ARM   | 3 years     | 4.25%        | 3-5 years     | High       |
| 5/1 ARM   | 5 years     | 4.50%        | 5-7 years     | Medium     |
| 7/1 ARM   | 7 years     | 4.75%        | 7-10 years    | Low-Med    |
| 10/1 ARM  | 10 years    | 5.00%        | 10-15 years   | Low        |
| 15-yr Fix | 15 years    | 5.00%        | 15+ years     | None       |
| 30-yr Fix | 30 years    | 5.25%        | 30 years      | None       |

*Rates are examples, actual rates vary by market

---

**Use this guide to configure the calculator for your specific ARM type and make informed decisions! 🏠💰**

*Last Updated: November 1, 2025*

