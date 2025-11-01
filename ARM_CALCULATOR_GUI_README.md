# ARM Refinance Calculator - GUI Version

An interactive graphical user interface for analyzing and comparing ARM (Adjustable Rate Mortgage) refinance scenarios.

![ARM Calculator GUI](https://img.shields.io/badge/Python-3.11-blue.svg)

## 🚀 Quick Start

### Running the GUI

**Option 1: Using the launcher script (macOS/Linux)**
```bash
./run_arm_calculator.sh
```

**Option 2: Direct Python execution**
```bash
python3 arm_refi_calculator_gui.py
```

**Option 3: Double-click (macOS)**
- Make the `.sh` file executable: `chmod +x run_arm_calculator.sh`
- Double-click `run_arm_calculator.sh` in Finder

## 📋 Features

### ✅ Easy Input Management
- **Visual Input Fields**: All loan parameters in one convenient form
- **Input Validation**: Real-time validation prevents calculation errors
- **Helpful Hints**: Gray text hints show example values

### ✅ Comprehensive Calculations
- **Original Loan Analysis**: Full breakdown of keeping your current ARM
- **Refinance Scenario**: Complete analysis of refinancing at any month
- **Breakeven Rate**: Automatically calculates the threshold rate for beneficial refinancing
- **Interest Breakdown**: See exactly where your interest dollars go in each period
- **Multiple Timing Scenarios**: Compare breakeven rates at 12, 24, 36, 48, 60, and 72 months

### ✅ Multiple Windows
- **New Window Button**: Open additional calculator windows for side-by-side comparison
- **Value Copying**: New windows automatically copy values from the current window
- **Independent Calculations**: Each window operates independently

### ✅ Professional Output
- **Formatted Results**: Easy-to-read, properly formatted output
- **Scrollable Display**: Full results visible with scroll support
- **Copy-Friendly**: Results are text-based and can be selected/copied

## 🎯 How to Use

### Step 1: Enter Your Loan Parameters

| Field | Description | Example |
|-------|-------------|---------|
| **Loan Amount** | Your original mortgage amount | 1288000 |
| **Current ARM Rate** | Your current ARM initial rate (%) | 4.875 |
| **New ARM Rate** | The new rate being offered (%) | 4.0 |
| **Refinance After** | When to refinance (in months) | 24 |
| **Refinance Cost** | Total closing costs ($) | 2000 |

### Step 2: Click "Calculate"

The calculator will:
1. Validate your inputs
2. Run comprehensive calculations
3. Display detailed results in the output window

### Step 3: Review Results

The output includes:

#### 📊 Scenario 1: Keep Original Loan
- Monthly payments for each period
- Total costs and interest
- Interest breakdown by ARM vs adjustable period

#### 📊 Scenario 2: Refinance
- Costs before refinancing
- New loan details
- Complete interest breakdown across all periods
- Total savings or additional cost

#### 📊 Comparison
- Total savings or cost increase
- Percentage difference
- Side-by-side totals

#### 📊 Breakeven Analysis
- **Breakeven rate** for your refinance timing
- ✓/✗ indicator showing if your rate is beneficial
- Breakeven rates for alternative timing (12-72 months)
- Monthly payment savings
- Months to break even on closing costs

### Step 4: Compare Scenarios (Optional)

1. Click **"New Window"** to open another calculator
2. Your current values are automatically copied
3. Modify any parameters in the new window
4. Compare results side-by-side

## 💡 Usage Examples

### Example 1: Should I Refinance Now?

**Situation**: You have a 4.875% ARM and are offered 4% after 2 years.

```
Inputs:
  Loan Amount: $1,288,000
  Current ARM Rate: 4.875%
  New ARM Rate: 4.0%
  Refinance After: 24 months
  Refinance Cost: $2,000

Result:
  ✓ Breakeven rate: 5.357%
  ✓ Your 4.0% is BELOW breakeven
  ✓ Savings: $403,074.83 (11.73%)
  → REFINANCE IS BENEFICIAL
```

### Example 2: What Rate Do I Need?

**Situation**: You want to refinance in 5 years but don't know what rate to target.

```
Inputs:
  Refinance After: 60 months

Output Shows:
  Breakeven rate: 6.300%
  
Interpretation:
  - Any rate below 6.300% → Beneficial
  - Any rate above 6.300% → Not beneficial
```

### Example 3: When Should I Refinance?

**Use Multiple Windows**:

1. Open 3 windows
2. Set refinance timing to: 24, 48, 72 months
3. Keep new rate at 4% in all windows
4. Compare total savings:
   - 24 months: $403k savings
   - 48 months: $511k savings
   - 72 months: $610k savings
5. **Conclusion**: Wait longer for better savings!

## 🎨 GUI Features

### Buttons

| Button | Function |
|--------|----------|
| **Calculate** | Run calculations with current parameters |
| **New Window** | Open new calculator with copied values |
| **Clear Results** | Clear the results display |

### Status Bar

Located at the bottom of the window:
- Shows current operation status
- Displays "Ready" when idle
- Shows "Calculating..." during computation
- Displays errors if they occur

### Results Area

- **Scrollable**: Full results with vertical scrolling
- **Monospaced Font**: Easy-to-read aligned columns
- **Selectable**: Click and drag to select text for copying
- **Search**: Use Cmd+F (Mac) or Ctrl+F (Windows) to search results

## 🔧 Technical Details

### Requirements
- Python 3.11 or higher
- tkinter (included with Python)
- No additional packages required!

### Platform Support
- ✅ macOS
- ✅ Linux
- ✅ Windows

### Performance
- Multi-threaded calculations keep GUI responsive
- Typical calculation time: < 1 second
- Supports unlimited simultaneous windows

## 📖 Understanding the Output

### Breakeven Rate Table

```
Month  Years   Breakeven Rate    Your Rate    Decision
------------------------------------------------------------
   12    1.0       5.098%        4.000%      ✓ GOOD
   24    2.0       5.357%        4.000%      ✓ GOOD
   36    3.0       5.642%        4.000%      ✓ GOOD
```

**Interpretation**:
- **Breakeven Rate**: The rate at which refinancing has no net benefit
- **Your Rate**: The new ARM rate you entered
- **Decision**: 
  - ✓ GOOD = Your rate beats breakeven (saves money)
  - ✗ BAD = Your rate is worse than breakeven (costs more)
  - = NEUTRAL = Exactly at breakeven

### Interest Breakdown

Shows how much interest you pay in each phase:

**Original Loan**:
- ARM Period (Years 1-7): Lower interest due to low rate
- Adjustable Period (Years 8-30): Higher interest due to rate cap

**Refinance Scenario**:
- Original Loan portion: Interest until refinance
- New ARM Period: Interest during new fixed period
- New Adjustable Period: Interest during new adjustable period

**Key Insight**: Most interest is paid in the adjustable periods!

## 🆘 Troubleshooting

### GUI Won't Start

**Error**: `ModuleNotFoundError: No module named '_tkinter'`

**Solution** (macOS):
```bash
brew install python-tk@3.11
```

**Solution** (Linux):
```bash
sudo apt-get install python3-tk
```

### Input Errors

| Error Message | Solution |
|---------------|----------|
| "Loan amount must be positive" | Enter a value greater than 0 |
| "Rate must be between 0 and 100" | Enter percentage (e.g., 4.5 not 0.045) |
| "Invalid input values" | Check all fields contain valid numbers |

### Window Issues

**Problem**: New window doesn't open
- **Cause**: Invalid values in current window
- **Solution**: Fix validation errors or use default values

**Problem**: Window is too small/large
- **Solution**: Resize by dragging corner; size persists within session

## 📝 Tips & Best Practices

### 🎯 Getting the Most Accurate Results

1. **Use Actual Loan Amount**: Enter your exact principal balance
2. **Check Your Rate**: Verify current ARM rate from loan documents
3. **Include All Costs**: Add appraisal, title, and closing fees to refi cost
4. **Consider Timing**: Run multiple scenarios with different timing

### 🎯 Comparing Multiple Offers

1. Open a new window for each lender offer
2. Use the same base parameters (loan amount, current rate, timing)
3. Only change the "New ARM Rate" and "Refinance Cost"
4. Compare breakeven analysis across all windows

### 🎯 Finding Optimal Timing

1. Set a target new rate (e.g., 4%)
2. Open windows for months 12, 24, 36, 48, 60, 72
3. Compare total savings across all scenarios
4. Check the breakeven table to see where your rate stands

### 🎯 Negotiating with Lenders

1. Calculate breakeven rate for your desired timing
2. Use this as your target in negotiations
3. Any rate below breakeven is worth considering
4. Factor in closing costs - higher costs increase breakeven rate

## 🔐 Privacy & Security

- **No Data Collection**: All calculations are performed locally
- **No Network Access**: Calculator works completely offline
- **No Data Storage**: Results are not saved automatically
- **Copy Results**: Save results by copying text to your own files

## 📞 Support

For issues with:
- **Calculations**: Review the original command-line script (`arm_refi_cost_calculator.py`)
- **GUI Issues**: Check Python and tkinter installation
- **Feature Requests**: Modify the source code as needed

## 📄 Files

| File | Purpose |
|------|---------|
| `arm_refi_calculator_gui.py` | Main GUI application |
| `arm_refi_cost_calculator.py` | Command-line version (original) |
| `run_arm_calculator.sh` | Launcher script (macOS/Linux) |
| `ARM_CALCULATOR_GUI_README.md` | This documentation |

## 🎓 Advanced Usage

### Custom Scenarios

You can modify the source code to:
- Change default term (currently 30 years/360 months)
- Adjust ARM fixed period (currently 7 years/84 months)
- Modify cap structure (currently +5%)
- Add additional output fields

### Automation

Create shell scripts to launch with specific values:
```bash
#!/bin/bash
# Launch calculator with preset values
python3 -c "
import arm_refi_calculator_gui
# Customize initial values here
"
```

---

## Summary

The ARM Refinance Calculator GUI provides a powerful, user-friendly interface for:
- ✅ Evaluating refinance opportunities
- ✅ Understanding interest breakdowns
- ✅ Finding breakeven rates
- ✅ Comparing multiple scenarios
- ✅ Making informed financial decisions

**Remember**: The breakeven rate is your most powerful tool. Any offer below this rate saves you money!

---

*Created with Python + tkinter | No external dependencies | 100% offline*

