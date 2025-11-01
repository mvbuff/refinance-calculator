# ARM Refinance Cost Calculator

A comprehensive calculator for analyzing ARM (Adjustable Rate Mortgage) refinance scenarios. Available in **three versions** to suit different needs:

1. **🌐 Streamlit Web App** (NEW!) - Modern web interface, accessible from any browser
2. **🖥️ Desktop GUI** - Traditional tkinter application for desktop use
3. **⌨️ Command Line** - Script-based calculator for terminal users

---

## 🌟 Features

- **Configurable ARM Analysis**: Support for any ARM type (3/1, 5/1, 7/1, 10/1, etc.) with customizable fixed periods
- **Flexible Loan Terms**: Configure loan term (15, 20, 30 years) and ARM fixed period independently
- **Comprehensive Comparison**: Compare keeping original loan vs. refinancing
- **Breakeven Rate Analysis**: Find the exact rate where refinancing becomes beneficial
- **Multiple Comparison Modes**:
  - Full loan term cost comparison
  - ARM periods only (great for those planning to sell/refi early)
  - Custom adjustable rate scenarios
- **Timing Analysis**: See how refinancing at different times affects savings
- **Detailed Breakdowns**: Interest, principal, and payment schedules for all scenarios

---

## 🚀 Quick Start

### Option 1: Streamlit Web App (Recommended)

**Best for:** Everyone! Modern interface, works on any device, no coding required

```bash
# Install
pip install streamlit

# Run
streamlit run streamlit_app.py
```

**Or use the launcher:**
```bash
./run_streamlit_app.sh
```

The app opens in your browser at `http://localhost:8501`

📖 **[Read the Streamlit Quick Start Guide](QUICK_START_STREAMLIT.md)**

---

### Option 2: Desktop GUI Application

**Best for:** Users who prefer traditional desktop applications

```bash
# Run
python3 arm_refi_calculator_gui.py
```

**Or use the launcher:**
```bash
./run_arm_calculator.sh
```

Opens a desktop window with input forms and results display.

📖 **[Read the GUI Guide](ARM_CALCULATOR_GUI_README.md)**

---

### Option 3: Command Line Script

**Best for:** Quick calculations, scripting, automation

```bash
# Edit parameters in the file first
python3 arm_refi_cost_calculator.py
```

Results print to the terminal.

📖 **[Read the Features Guide](ARM_CALCULATOR_FEATURES.md)**

---

## 📊 Comparison: Which Version Should I Use?

| Feature | Streamlit Web | Desktop GUI | Command Line |
|---------|--------------|-------------|--------------|
| **Interface** | Modern web UI | Traditional desktop | Terminal output |
| **Installation** | `pip install streamlit` | Python built-in | Python built-in |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Mobile Support** | ✓ Yes | ✗ No | ✗ No |
| **Multiple Scenarios** | Browser tabs | New windows | Edit & re-run |
| **Sharing** | Share URL | Share script | Share script |
| **Real-time Updates** | ✓ Instant | ✓ Click button | ✗ Re-run script |
| **Help System** | Built-in expandable | Popup window | In code comments |
| **Export Results** | Screenshot/Print | Copy text | Redirect output |
| **Cloud Deployment** | ✓ Yes | ✗ No | ✗ No |

**Recommendation:**
- **New users**: Start with Streamlit Web App
- **Desktop users**: Use Desktop GUI
- **Power users/Automation**: Use Command Line

---

## 📖 Documentation

- **[Quick Start - Streamlit](QUICK_START_STREAMLIT.md)** - Get started with web app in 3 steps
- **[Streamlit README](README_STREAMLIT.md)** - Complete web app documentation
- **[Desktop GUI Guide](ARM_CALCULATOR_GUI_README.md)** - Desktop application documentation
- **[Features Guide](ARM_CALCULATOR_FEATURES.md)** - Detailed feature explanations
- **[Comparison Mode Guide](COMPARISON_MODE_GUIDE.md)** - Understanding comparison modes

---

## 💡 Example Use Cases

### 1. Should I Refinance?

**Scenario:** You have a 4.875% ARM. A lender offers 4.0% with $2,000 closing costs.

**Using Streamlit:**
1. Open the app: `streamlit run streamlit_app.py`
2. Enter your details (pre-filled with similar example)
3. Click "Calculate"
4. Check "Comparison" tab → See savings
5. Check "Breakeven Analysis" → Verify rate is below breakeven

**Result:** Save $405,666 over 30 years ✓

---

### 2. Planning to Sell in 5 Years

**Scenario:** Same loan, but you're selling soon. Should you still refinance?

**Using Streamlit:**
1. Enter loan details
2. ✅ **Check "Compare ARM periods only"**
3. Click "Calculate"
4. Review ARM-only comparison

**Result:** Costs $35,073 more in ARM periods (but saves $405K if you keep it) ⚠️

---

### 3. Compare Multiple Lender Offers

**Scenario:** You have 3 offers with different rates and costs.

**Using Streamlit:**
1. Open 3 browser tabs
2. Enter each offer in a separate tab
3. Compare results side-by-side

**Result:** Find the best deal! 🎯

---

## 🧮 What It Calculates

### For Original Loan (Keep Current ARM)
- Monthly payments for years 1-7 (fixed rate period)
- Monthly payments for years 8-30 (capped at initial + 5%)
- Total amount paid over 30 years
- Total interest paid
- Principal paid by period

### For Refinance Scenario
- Payments on original loan until refinance
- Balance at refinance point
- New loan payments (Phase 1: fixed rate)
- New loan payments (Phase 2: adjustable rate)
- Total cost including refinance fees
- Total savings (or additional cost)

### Breakeven Analysis
- **Breakeven rate:** The new ARM rate where refinancing is neutral
- **Timing scenarios:** Breakeven rates for different refinance timings
- **ARM-only breakeven:** Rate needed to save money in just the ARM periods

---

## 🔧 Installation

### Streamlit Web App

```bash
# Using pip
pip install streamlit

# Or using requirements.txt
pip install -r requirements.txt
```

### Desktop GUI / Command Line

No additional installation needed! Uses Python's built-in tkinter.

**Requirements:**
- Python 3.11 or higher
- tkinter (usually included with Python)

---

## 📱 Running the Apps

### Streamlit Web App

```bash
# Method 1: Direct
streamlit run streamlit_app.py

# Method 2: Using launcher
./run_streamlit_app.sh

# Method 3: With custom port
streamlit run streamlit_app.py --server.port 8502
```

**Access:** Open browser to `http://localhost:8501`

---

### Desktop GUI

```bash
# Method 1: Direct
python3 arm_refi_calculator_gui.py

# Method 2: Using launcher
./run_arm_calculator.sh

# Method 3: With custom values
python3 arm_refi_calculator_gui.py
```

**Access:** Opens in a new desktop window

---

### Command Line

```bash
# Edit parameters in the script first
python3 arm_refi_cost_calculator.py

# Redirect output to file
python3 arm_refi_cost_calculator.py > results.txt
```

**Access:** Output displays in terminal

---

## 🌐 Network/Cloud Access

### Access from Other Devices (Local Network)

```bash
# Run Streamlit with network access
streamlit run streamlit_app.py --server.address 0.0.0.0

# Find your IP address
# Mac/Linux: ifconfig
# Windows: ipconfig

# Access from phone/tablet
# Go to: http://YOUR_IP:8501
```

### Deploy to Cloud (Streamlit Only)

**Free options:**
- [Streamlit Community Cloud](https://streamlit.io/cloud)
- [Heroku](https://www.heroku.com/)
- [Railway](https://railway.app/)

**Full guide:** See [README_STREAMLIT.md](README_STREAMLIT.md#deployment-options)

---

## 📊 Key Concepts

### ARM Structure (Configurable)
- **Fixed Period** (configurable: 3, 5, 7, 10 years, etc.): Fixed at initial rate (e.g., 4.875%)
- **Adjustable Period** (remaining years): Adjustable, capped at initial + 5% (e.g., 9.875%)
- **Loan Term** (configurable: 15, 20, 30 years, etc.): Total loan duration

**Examples:**
- 3/1 ARM: 3 years fixed, then adjustable
- 5/1 ARM: 5 years fixed, then adjustable
- 7/1 ARM: 7 years fixed, then adjustable (default)
- 10/1 ARM: 10 years fixed, then adjustable

### Comparison Modes

**Mode 1: Full 30-Year**
- Compares total cost over entire loan
- Best for long-term homeowners
- Shows total savings over 30 years

**Mode 2: ARM Periods Only**
- Compares only years 1-7 (or 1-9 after refi)
- Best for those planning to sell/refi early
- Excludes adjustable period costs

**Mode 3: Custom Adjustable Rate**
- Use a specific rate for years 8-30
- Best for modeling future refi plans
- Removes cap rate advantage from comparison

---

## 🎯 Decision Making Framework

### Should I Refinance? (Full 30-Year View)

1. **Calculate breakeven rate**
   - If new rate < breakeven → Refinance ✓
   - If new rate > breakeven → Don't refinance ✗

2. **Check total savings**
   - Positive savings → Refinance ✓
   - Negative savings (additional cost) → Don't refinance ✗

3. **Consider monthly payment**
   - Calculate months to break even on closing costs
   - Ensure you'll stay long enough

---

### Should I Refinance? (Selling in 5-7 Years)

1. **Use ARM-only mode**
   - Check "Compare ARM periods only"

2. **Calculate ARM-only breakeven rate**
   - If new rate < ARM breakeven → Refinance ✓
   - If new rate > ARM breakeven → Don't refinance ✗

3. **Check ARM period costs**
   - Positive savings in ARM period → Refinance ✓
   - Additional cost in ARM period → Don't refinance ✗

---

## ⚙️ Assumptions & Limitations

### Assumptions
✓ Rates remain constant during each period  
✓ No prepayments or extra payments  
✓ Full 30-year term (or use ARM-only mode)  
✓ Refinance costs paid out of pocket (not rolled into loan)  

### Limitations
✗ Does NOT model actual ARM adjustments (uses max cap)  
✗ Does NOT account for tax deductions  
✗ Does NOT consider opportunity costs or inflation  
✗ Does NOT discount future payments to present value  
✗ Does NOT model lender credits or points  

**Note:** These are conservative estimates. Actual results may vary.

---

## 🆘 Troubleshooting

### Streamlit Issues

**Problem:** `streamlit: command not found`  
**Solution:** `pip install streamlit`

**Problem:** Port already in use  
**Solution:** `streamlit run streamlit_app.py --server.port 8502`

**Problem:** Browser doesn't open  
**Solution:** Manually go to `http://localhost:8501`

### Desktop GUI Issues

**Problem:** `ModuleNotFoundError: No module named 'tkinter'`  
**Solution:** Install tkinter for your Python distribution

**Problem:** Window doesn't open  
**Solution:** Ensure you have a GUI environment (not SSH/remote terminal)

### General Issues

**Problem:** Invalid input values  
**Solution:** Check all values are positive numbers, rates are percentages

**Problem:** Results seem wrong  
**Solution:** Verify you understand the comparison mode (30-year vs ARM-only)

---

## 📚 Learn More

### Documentation Files
- `QUICK_START_STREAMLIT.md` - Streamlit quick start (3 steps)
- `README_STREAMLIT.md` - Complete Streamlit documentation
- `ARM_CALCULATOR_GUI_README.md` - Desktop GUI documentation
- `ARM_CALCULATOR_FEATURES.md` - Feature explanations
- `COMPARISON_MODE_GUIDE.md` - Comparison mode details
- `ARM_TYPES_GUIDE.md` - **NEW!** Guide to different ARM types (3/1, 5/1, 7/1, 10/1)
- `CONFIGURABLE_ARM_PERIOD_ENHANCEMENT.md` - **NEW!** Details on configurable ARM periods

### Example Outputs
All versions produce similar results with different presentation:
- **Streamlit:** Tabbed interface, metrics, visual indicators
- **Desktop GUI:** Scrolled text output, multiple windows
- **Command Line:** Formatted terminal output

---

## 🤝 Contributing

This is a personal finance tool. Feel free to:
- Modify parameters for your use case
- Add new features
- Share with others who might find it useful

---

## 📄 License

Free to use and modify for personal use.

---

## 📞 Support

For questions or issues:
1. Read the documentation (see links above)
2. Check the Help section in the app
3. Review the example scenarios

---

## 🎉 Get Started Now!

Choose your preferred version:

**Streamlit Web App (Recommended):**
```bash
pip install streamlit
streamlit run streamlit_app.py
```

**Desktop GUI:**
```bash
python3 arm_refi_calculator_gui.py
```

**Command Line:**
```bash
python3 arm_refi_cost_calculator.py
```

---

**Happy Calculating! 🏠💰**

*Last Updated: November 1, 2025*

