# ARM Refinance Calculator - Streamlit Web App

A modern, interactive web application for comparing ARM refinance scenarios. This Streamlit version provides all the features of the desktop GUI in an easy-to-use web interface.

## Features

- 🏠 **Interactive Web Interface**: Clean, modern UI accessible from any browser
- 📊 **Real-time Calculations**: Instant results as you adjust parameters
- 💰 **Comprehensive Analysis**: Compare full 30-year costs or ARM periods only
- 📈 **Breakeven Analysis**: Find the optimal refinance rate for your situation
- 🔧 **Customizable Parameters**: Adjust all loan parameters and comparison modes
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## Quick Start

### Installation

1. **Install Python** (if not already installed)
   - This app requires Python 3.11 or higher

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

**Option 1: Using Streamlit directly**
```bash
streamlit run streamlit_app.py
```

**Option 2: Using the custom Python interpreter**
```bash
/home/utils/Python/builds/3.11.9-20250401/bin/python3.11 -m streamlit run streamlit_app.py
```

The app will automatically open in your default web browser at `http://localhost:8501`

## Usage

### Input Parameters

All input parameters are located in the **sidebar** on the left:

1. **Loan Amount ($)**: Your original mortgage principal
   - Example: 1,288,000

2. **Current ARM Rate (%)**: Your current loan's initial fixed rate
   - Example: 4.875

3. **New ARM Rate (%)**: The new rate being offered if you refinance
   - Example: 4.0

4. **Refinance After (months)**: When you plan to refinance
   - Example: 24 (2 years)
   - Range: 1-84 months

5. **Refinance Cost ($)**: One-time closing costs paid out of pocket
   - Example: 2,000

### Comparison Options

**Compare ARM periods only**
- ☐ Unchecked (Default): Compare full 30-year costs
- ☑ Checked: Compare only ARM fixed-rate periods (months 1-84)
- Use when planning to sell or refinance again before rates adjust

**Use custom rate for Years 8-30**
- ☐ Unchecked (Default): Use cap rates (initial + 5%)
- ☑ Checked: Use a specific custom rate for adjustable period in both scenarios
- Useful for modeling specific future refinance plans

### Results Tabs

The results are organized into four tabs:

1. **📊 Comparison**: Side-by-side comparison with savings/costs
2. **📋 Original Loan**: Detailed breakdown of keeping your current loan
3. **🔄 Refinance Scenario**: Detailed breakdown of refinancing
4. **📈 Breakeven Analysis**: Rate thresholds and timing scenarios

## Comparison Modes Explained

### Mode 1: Full 30-Year Comparison (Default)

**What it does:**
- Compares total cost over entire 360-month loan term
- Includes both ARM period (years 1-7) and adjustable rate period (years 8-30)
- Shows total payments, interest, and principal for full 30 years

**When to use:**
- You plan to keep the loan for the full term
- You want to see lifetime costs
- You care about the long-term financial impact

**Example Output:**
```
Original loan total:  $3,437,013.65
Refinanced total:     $3,031,346.85
SAVINGS:              $405,666.80 (11.80%)
```

### Mode 2: ARM Periods Only

**What it does:**
- Compares ONLY the ARM fixed-rate periods
- For original: months 1-84
- For refinance: months 1-24 on original + months 25-108 on new loan
- Excludes all adjustable rate periods (years 8-30)
- Focuses on interest paid + refinance costs only

**When to use:**
- You plan to sell the property in 5-7 years
- You'll refinance again before year 7-9
- You want to minimize short-term costs
- You only care about ARM period expenses

**Example Output:**
```
Original ARM interest:  $414,392.41
Refinanced ARM cost:    $449,465.49
ADDITIONAL COST:        $35,073.09 (8.46%)
```

### Mode 3: Custom Adjustable Rate

**What it does:**
- Use a single custom rate for years 8-30 in BOTH scenarios
- Removes the cap rate advantage from comparison
- Useful for modeling specific future refinance plans

**When to use:**
- You plan to refinance again at year 7 to a specific rate
- You want to test "what if" scenarios
- You want to isolate ARM period differences

**Example:**
```
Custom rate = 4.5%

Original scenario:  4.875% for years 1-7, then 4.5% for years 8-30
Refinance scenario: 4.0% for years 1-7, then 4.5% for years 8-30

This focuses comparison on the 0.875% difference during ARM periods.
```

## Key Metrics Explained

### Breakeven Rate

The **breakeven rate** is the new ARM rate at which refinancing becomes neutral (neither saves nor costs more money).

**Full 30-Year Breakeven:**
- Takes into account the entire loan term
- Typically HIGHER than current rate due to cap rate benefits
- Example: If breakeven is 5.368% and current is 4.875%, even rates higher than current can save money

**ARM-Only Breakeven:**
- Focuses only on ARM fixed-rate periods
- Typically LOWER than current rate
- Example: If breakeven is 3.584% and current is 4.875%, you need a very low rate to save during ARM periods

### Savings

- **Positive savings**: Refinancing saves money
- **Negative savings (additional cost)**: Refinancing costs more money
- Percentage shows savings/cost relative to original loan total

### Monthly Payment Changes

- Shows the difference in monthly payments during the new fixed period
- Helps calculate months to break even on refinance costs

## Example Scenarios

### Scenario 1: Long-Term Homeowner

**Goal:** Minimize total 30-year cost

**Settings:**
- Compare ARM periods only: ☐ Unchecked
- Custom adjustable rate: ☐ Unchecked

**Action:**
1. Enter your loan parameters
2. Click "Calculate"
3. Review "Comparison" tab for total savings
4. Check "Breakeven Analysis" tab for rate threshold

**Decision:**
- If new rate < breakeven rate → Refinance ✓
- If new rate > breakeven rate → Don't refinance ✗

### Scenario 2: Planning to Sell in 5 Years

**Goal:** Minimize costs until sale

**Settings:**
- Compare ARM periods only: ☑ Checked
- Custom adjustable rate: ☐ Unchecked

**Action:**
1. Enter your loan parameters
2. Set "Refinance After" to your planned timeline
3. Check "Compare ARM periods only"
4. Click "Calculate"
5. Review ARM-only comparison

**Decision:**
- If new rate < ARM breakeven → Refinance ✓
- Otherwise, keep current loan ✗

### Scenario 3: Comparing Multiple Lender Offers

**Goal:** Find the best offer among 3 lenders

**Action:**
1. Enter first offer details (rate and costs)
2. Click "Calculate"
3. Note the results
4. Change the "New ARM Rate" and "Refinance Cost" for second offer
5. Click "Calculate" again
6. Repeat for third offer
7. Compare all results

## Tips for Best Results

✅ Get actual closing costs from lenders (not estimates)  
✅ Verify your current ARM rate from loan documents  
✅ Consider both comparison modes for complete picture  
✅ Test different timing scenarios (12, 24, 36 months)  
✅ Remember: Breakeven rates change based on timing  
✅ Lower refinance costs → lower breakeven rate needed  

## Technical Details

### Loan Structure: 7/6 ARM

- **Years 1-7** (84 months): Fixed rate period
- **Years 8-30** (276 months): Adjustable rate period
- **Default assumption**: Adjustable rate = Initial rate + 5% (cap)

### Calculation Method

**Original Loan:**
1. Calculate monthly payment at initial rate for 360 months
2. Apply payment for months 1-84 (ARM period)
3. Calculate remaining balance after month 84
4. Recalculate payment at cap rate for remaining 276 months
5. Sum all payments

**Refinance Scenario:**
1. Pay original loan for specified months
2. Pay refinance cost out of pocket
3. New loan = remaining balance (NOT balance + refi cost)
4. Calculate new payment at new rate
5. Apply to new ARM period (84 months or less if fewer months remaining)
6. Recalculate at new cap rate for any remaining time
7. Sum all payments + refi cost

### Key Assumptions

✓ Rates remain fixed during each period  
✗ Does NOT model actual ARM adjustments based on index + margin  
✗ Cap rates are maximum possible, not guaranteed actual rates  
✗ Does NOT account for prepayments or extra payments  
✗ Does NOT consider tax benefits or opportunity costs  
✗ Does NOT discount future payments to present value  

## Troubleshooting

### Port Already in Use

If you see an error like "Address already in use":

```bash
streamlit run streamlit_app.py --server.port 8502
```

### Dependencies Not Found

Make sure you've installed the requirements:

```bash
pip install -r requirements.txt
```

### Browser Doesn't Open Automatically

Manually navigate to: `http://localhost:8501`

## Deployment Options

### Local Network Access

To access from other devices on your network:

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

Then access using your computer's IP address: `http://YOUR_IP:8501`

### Cloud Deployment

The app can be deployed to:
- **Streamlit Community Cloud** (free): https://streamlit.io/cloud
- **Heroku**: Follow Streamlit's Heroku deployment guide
- **AWS/GCP/Azure**: Deploy as a containerized application

## Comparison: Streamlit vs Desktop GUI

| Feature | Streamlit Web App | Desktop GUI (tkinter) |
|---------|------------------|----------------------|
| Installation | Simple (pip install) | Simple (built-in) |
| Access | Any browser | Requires Python/GUI |
| Multiple Windows | Browser tabs | New windows |
| Mobile Support | ✓ Yes | ✗ No |
| Sharing | Share URL | Share script |
| Deployment | Cloud-ready | Local only |
| Updates | Auto-refresh | Manual restart |

## Support

For issues or questions:
1. Check the Help guide in the app (click "Show Help")
2. Review this README
3. Check the original documentation files

## License

This project maintains the same license as the original ARM calculator.

---

**Version:** 1.0.0  
**Last Updated:** November 1, 2025  
**Compatibility:** Python 3.11+, Streamlit 1.28+

