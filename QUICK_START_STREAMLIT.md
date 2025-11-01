# Quick Start Guide - ARM Refinance Calculator (Streamlit)

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install streamlit
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Run the App

```bash
streamlit run streamlit_app.py
```

Or use the provided script:

```bash
./run_streamlit_app.sh
```

### Step 3: Use the Calculator

The app will open in your browser at `http://localhost:8501`

1. **Enter your loan details** in the sidebar (left panel)
2. **Click "Calculate"** to see results
3. **Review results** in the tabs

## 📋 Default Example

The app comes pre-loaded with an example:

- **Loan Amount:** $1,288,000
- **Current ARM Rate:** 4.875%
- **New ARM Rate:** 4.0%
- **Refinance After:** 24 months
- **Refinance Cost:** $2,000

Just click "Calculate" to see the results!

## 💡 Common Use Cases

### Use Case 1: Should I Refinance?

**Question:** "I have a 4.875% ARM. Should I refinance to 4.0%?"

**Steps:**
1. Enter your loan amount
2. Enter current rate: 4.875
3. Enter new rate: 4.0
4. Set when you plan to refinance (e.g., 24 months)
5. Enter refinance costs
6. Click "Calculate"
7. Look at "Comparison" tab → See if you save money
8. Check "Breakeven Analysis" → Is your new rate below breakeven?

**Decision:** If new rate < breakeven rate → Refinance ✓

---

### Use Case 2: Planning to Sell in 5 Years

**Question:** "I'm selling in 5 years. Is refinancing worth it for the short term?"

**Steps:**
1. Enter your loan details
2. ✅ **Check "Compare ARM periods only"** (Important!)
3. Click "Calculate"
4. Review "Comparison" tab → Focus on ARM period costs
5. Check ARM-only breakeven rate

**Decision:** If new rate < ARM breakeven → Refinance ✓

---

### Use Case 3: Compare 3 Different Lender Offers

**Question:** "I have offers from 3 lenders. Which is best?"

**Offer 1:** 4.0% with $2,000 costs  
**Offer 2:** 3.875% with $4,500 costs  
**Offer 3:** 4.125% with $1,000 costs  

**Steps:**
1. Enter Offer 1 details, click "Calculate", note savings
2. Change to Offer 2 details, click "Calculate", note savings
3. Change to Offer 3 details, click "Calculate", note savings
4. Choose the offer with the highest savings

**Tip:** Open multiple browser tabs to compare side-by-side!

---

## 🎯 Key Metrics to Watch

### 1. Total Savings (or Additional Cost)

- **Green** (Savings) → Refinancing saves money ✓
- **Red** (Additional Cost) → Refinancing costs more ✗

**Location:** Top of results page, middle metric

### 2. Breakeven Rate

- **Your rate BELOW breakeven** → Good deal ✓
- **Your rate ABOVE breakeven** → Bad deal ✗

**Location:** "Breakeven Analysis" tab

### 3. Monthly Payment Savings

- Shows how much you save per month
- Helps calculate when you break even on closing costs

**Location:** "Comparison" tab (if applicable)

---

## 🔧 Advanced Options

### Compare ARM Periods Only

**What it does:** Ignores years 8-30, focuses only on years 1-7

**When to use:**
- Planning to sell before year 7
- Planning to refinance again before rates adjust

**How to enable:**
- Sidebar → ✅ Check "Compare ARM periods only"

---

### Custom Adjustable Rate

**What it does:** Use a specific rate for years 8-30 in both scenarios

**When to use:**
- Planning to refinance again at year 7
- Want to test "what if I get 4.5% at year 7" scenarios

**How to enable:**
- Sidebar → ✅ Check "Use custom rate for Years 8-30"
- Enter your custom rate (e.g., 4.5%)

---

## 📊 Understanding the Results

### Comparison Tab

Shows side-by-side comparison:
- **Original Loan Total** vs **Refinanced Loan Total**
- **Savings** or **Additional Cost**
- **Monthly payment changes**

### Original Loan Tab

Details if you keep your current loan:
- Monthly payments for years 1-7 and 8-30
- Total interest and principal breakdown

### Refinance Scenario Tab

Details if you refinance:
- What you pay before refinancing
- What you pay after refinancing
- Total costs including refinance fee

### Breakeven Analysis Tab

The magic numbers:
- **Breakeven rate:** Any rate below this saves money
- **Timing table:** Shows breakeven rates if you refinance at different times

---

## ⚡ Quick Tips

1. **Start with default values** → Click "Calculate" to see how it works
2. **Use realistic costs** → Get actual quotes from lenders
3. **Test multiple timings** → Try refinancing at 12, 24, 36 months
4. **Check both modes** → Full 30-year AND ARM-only
5. **Lower costs = better deal** → Even $1,000 vs $2,000 makes a difference

---

## ❓ Common Questions

**Q: Why is my breakeven rate higher than my current rate?**  
A: Because refinancing lets you avoid the high cap rate (current + 5%) sooner. Even a higher rate can save money long-term!

**Q: ARM-only mode shows I lose money, but full mode shows I save. Which is right?**  
A: Both are right for different timeframes. If keeping the house 30 years, use full mode. If selling in 5-7 years, use ARM-only mode.

**Q: What if I don't know my refinance costs yet?**  
A: Use $2,000 as an estimate, then update once you get actual quotes. Check the "Breakeven Analysis" tab to see how timing affects the decision.

**Q: Can I save these results?**  
A: Take a screenshot or use your browser's print function to save as PDF.

---

## 🚨 Troubleshooting

### App Won't Start

**Error:** "streamlit: command not found"

**Solution:**
```bash
pip install streamlit
```

---

### Browser Doesn't Open

**Solution:** Manually go to: `http://localhost:8501`

---

### Port Already in Use

**Error:** "Address already in use"

**Solution:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

Then go to: `http://localhost:8502`

---

## 📱 Mobile Access

Want to access from your phone?

1. Run the app with:
   ```bash
   streamlit run streamlit_app.py --server.address 0.0.0.0
   ```

2. Find your computer's IP address:
   - Mac: System Preferences → Network
   - Windows: `ipconfig`
   - Linux: `ifconfig`

3. On your phone, go to: `http://YOUR_IP:8501`

---

## 🎓 Example Walkthrough

Let's walk through a complete example:

**Scenario:** You have a $1,288,000 loan at 4.875%. A lender offers 4.0% with $2,000 closing costs. You're considering refinancing after 2 years.

**Step 1:** Open the app
```bash
streamlit run streamlit_app.py
```

**Step 2:** Verify default values (they match our scenario!)
- ✓ Loan Amount: $1,288,000
- ✓ Current ARM Rate: 4.875%
- ✓ New ARM Rate: 4.0%
- ✓ Refinance After: 24 months
- ✓ Refinance Cost: $2,000

**Step 3:** Click "Calculate"

**Step 4:** Review results

**Comparison Tab shows:**
- Original Loan Total: $3,437,013.65
- Refinanced Total: $3,031,346.85
- **Savings: $405,666.80 (11.80%)**
- ✓ This is a GOOD deal!

**Breakeven Analysis shows:**
- Current ARM Rate: 4.875%
- Breakeven Rate: 5.368%
- Your New Rate: 4.000%
- ✓ Your rate is 1.368% BELOW breakeven → BENEFICIAL

**Decision:** Refinance! You'll save over $400,000 over 30 years.

**Step 5:** Test ARM-only mode (in case you sell early)

- ✅ Check "Compare ARM periods only"
- Click "Calculate" again

**ARM-only results:**
- Original ARM cost: $414,392.41
- Refinanced ARM cost: $449,465.49
- ✗ Additional Cost: $35,073.09

**Interpretation:** If you sell before year 7-9, refinancing costs MORE in the short term. But if keeping the house long-term, you save $400K+.

---

## 🎉 You're Ready!

That's it! You now know how to use the ARM Refinance Calculator.

**Next Steps:**
1. Enter your actual loan details
2. Get quotes from lenders
3. Compare different offers
4. Make an informed decision

**Need More Help?**
- Click "Show Help" in the sidebar
- Read the full README_STREAMLIT.md
- Review the original documentation files

---

**Happy Calculating! 🏠💰**

