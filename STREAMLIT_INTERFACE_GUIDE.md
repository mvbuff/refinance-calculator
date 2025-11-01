# Streamlit Interface Guide

A visual walkthrough of the ARM Refinance Calculator Streamlit web app.

---

## 🖼️ App Layout Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🏠 ARM Refinance Cost Calculator                                           │
├──────────────┬──────────────────────────────────────────────────────────────┤
│              │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  SIDEBAR     │  │   Original   │  │  Refinanced  │  │    Total     │        │
│  (Inputs)    │  │ Loan Total   │  │  Loan Total  │  │   Savings    │        │
│              │  │ $3,437,014   │  │ $3,031,347   │  │  $405,667    │        │
│  Loan Params │  └──────────────┘  └──────────────┘  └──────────────┘        │
│              │                                                                │
│  Loan Amount │  ─────────────────────────────────────────────────────        │
│  [1288000]   │  Results                                                      │
│              │  ─────────────────────────────────────────────────────        │
│  Current ARM │  [📊 Comparison] [📋 Original] [🔄 Refinance] [📈 Breakeven] │
│  Rate (%)    │                                                                │
│  [4.875]     │  ┌──────────────────────────────────────────────────────┐    │
│              │  │  MODE: FULL 30-YEAR COMPARISON                       │    │
│  New ARM     │  │                                                      │    │
│  Rate (%)    │  │  Original Loan:                                      │    │
│  [4.0]       │  │    Total Paid:      $3,437,013.65                   │    │
│              │  │    Total Interest:  $2,149,013.65                   │    │
│  Refinance   │  │    Total Principal: $1,288,000.00                   │    │
│  After       │  │                                                      │    │
│  [24] months │  │  Refinanced Loan:                                   │    │
│              │  │    Total Paid:      $3,031,346.85                   │    │
│  Refinance   │  │    Total Interest:  $1,745,346.85                   │    │
│  Cost ($)    │  │    Refinance Cost:      $2,000.00                   │    │
│  [2000]      │  │                                                      │    │
│              │  │  ✓ SAVINGS: $405,666.80 (11.80%)                    │    │
│  ─────────   │  │                                                      │    │
│              │  │  Monthly payment savings: $650.14                   │    │
│  Options     │  │  Months to break even: 3.1 months                   │    │
│              │  └──────────────────────────────────────────────────────┘    │
│  ☐ Compare   │                                                                │
│    ARM only  │  ┌──────────────────────────────────────────────────────┐    │
│              │  │  Important Notes                                     │    │
│  ☐ Custom    │  │  - All calculations assume constant rates           │    │
│    Rate      │  │  - Does not account for tax deductions              │    │
│  [4.5]       │  │  - Refinance costs paid out of pocket               │    │
│              │  └──────────────────────────────────────────────────────┘    │
│  ─────────   │                                                                │
│              │                                                                │
│  [Calculate] │                                                                │
│  (Primary)   │                                                                │
│              │                                                                │
│  [Show Help] │                                                                │
│              │                                                                │
└──────────────┴──────────────────────────────────────────────────────────────┘
```

---

## 🎨 Component Breakdown

### 1. Sidebar (Left Panel)

**Purpose:** All user inputs and controls

```
┌─────────────────────────┐
│  Loan Parameters        │
├─────────────────────────┤
│                         │
│  Loan Amount ($)        │
│  ┌───────────────────┐  │
│  │ 1288000           │  │
│  └───────────────────┘  │
│  Your original mortgage │
│                         │
│  Current ARM Rate (%)   │
│  ┌───────────────────┐  │
│  │ 4.875             │  │
│  └───────────────────┘  │
│  Initial fixed rate     │
│                         │
│  New ARM Rate (%)       │
│  ┌───────────────────┐  │
│  │ 4.0               │  │
│  └───────────────────┘  │
│  Offered refinance rate │
│                         │
│  Refinance After        │
│  ├───────────────────┤  │
│  │●──────────────24──│  │
│  └───────────────────┘  │
│  1 ─────────────── 84   │
│  When you plan to refi  │
│                         │
│  Refinance Cost ($)     │
│  ┌───────────────────┐  │
│  │ 2000              │  │
│  └───────────────────┘  │
│  Closing costs          │
│                         │
├─────────────────────────┤
│  Comparison Options     │
├─────────────────────────┤
│                         │
│  ☐ Compare ARM          │
│     periods only        │
│                         │
│  Exclude years 8-30     │
│                         │
│  ☐ Use custom rate      │
│     for Years 8-30      │
│                         │
│  Custom Rate (%)        │
│  ┌───────────────────┐  │
│  │ 4.5    (disabled) │  │
│  └───────────────────┘  │
│                         │
├─────────────────────────┤
│  ┏━━━━━━━━━━━━━━━━━┓    │
│  ┃    Calculate    ┃    │
│  ┗━━━━━━━━━━━━━━━━━┛    │
│                         │
│  ┌─────────────────┐    │
│  │   Show Help     │    │
│  └─────────────────┘    │
│                         │
└─────────────────────────┘
```

**Key Features:**
- Number inputs with min/max validation
- Slider for "Refinance After"
- Checkboxes for comparison modes
- Large primary "Calculate" button
- Secondary "Show Help" button

---

### 2. Summary Metrics (Top of Main Area)

**Purpose:** At-a-glance comparison

```
┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
│ Original Loan     │  │ Refinanced Loan   │  │ Total Savings     │
│ Total             │  │ Total             │  │                   │
│                   │  │                   │  │                   │
│ $3,437,013.65     │  │ $3,031,346.85     │  │ $405,666.80       │
│                   │  │                   │  │                   │
│                   │  │ ▼ -$405,666.80    │  │ ▲ 11.80%          │
└───────────────────┘  └───────────────────┘  └───────────────────┘
```

**Features:**
- Large numbers, easy to read
- Color-coded deltas (green = good, red = bad)
- Percentage change shown
- Responsive layout (stacks on mobile)

---

### 3. Tabbed Results Area

**Purpose:** Organize detailed results

```
┌──────────────────────────────────────────────────────────────┐
│ [📊 Comparison] [📋 Original Loan] [🔄 Refinance] [📈 Breakeven] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Tab content appears here                                   │
│  (different for each tab)                                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

### 3a. Comparison Tab

```
┌──────────────────────────────────────────────────────────────┐
│ 📊 Comparison                                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  MODE: FULL 30-YEAR COMPARISON (Including All Periods)      │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  Original Loan          │  Refinanced Loan                  │
│  ─────────────────      │  ────────────────                 │
│  Total Paid:            │  Total Paid:                      │
│  $3,437,013.65          │  $3,031,346.85                    │
│                         │                                   │
│  Total Interest:        │  Total Interest:                  │
│  $2,149,013.65          │  $1,745,346.85                    │
│                         │                                   │
│  Total Principal:       │  Refinance Cost:                  │
│  $1,288,000.00          │  $2,000.00                        │
│                                                              │
│  ┌─────────────────────────────────────────────────┐        │
│  │ ✓ SAVINGS from refinancing: $405,666.80        │        │
│  │   (11.80%)                                      │        │
│  └─────────────────────────────────────────────────┘        │
│                                                              │
│  ℹ️ Monthly payment savings: $650.14                        │
│     Months to break even: 3.1 (0.3 years)                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**With ARM-Only Mode:**
```
┌──────────────────────────────────────────────────────────────┐
│ 📊 Comparison                                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  MODE: ARM PERIODS ONLY - Interest & Refinance Costs        │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  ℹ️ Principal payments are the same in both scenarios.      │
│     This comparison focuses only on INTEREST and COSTS.     │
│                                                              │
│  Original (ARM Period - Months 1-84)                        │
│  ────────────────────────────────────                        │
│  Interest Paid:              $414,392.41                    │
│  Refinance Cost:                   $0.00                    │
│  Total Cost (Interest only): $414,392.41                    │
│                                                              │
│  Refinance (ARM Periods - Months 1-108)                     │
│  ────────────────────────────────────                        │
│  Before Refi Interest:        $96,734.28                    │
│  New ARM Interest:           $350,731.21                    │
│  Combined ARM Interest:      $447,465.49                    │
│  Refinance Cost:               $2,000.00                    │
│  Total Cost (Int + Refi):    $449,465.49                    │
│                                                              │
│  ┌─────────────────────────────────────────────────┐        │
│  │ ✗ ARM PERIOD ADDITIONAL COST: $35,073.09       │        │
│  │   (8.46%)                                       │        │
│  └─────────────────────────────────────────────────┘        │
│                                                              │
│  ARM-Only Breakeven Rate                                    │
│  ────────────────────────                                    │
│  Current ARM:     Breakeven:     Your New:                  │
│  ┌──────────┐    ┌──────────┐   ┌──────────┐               │
│  │ 4.875%   │    │ 3.584%   │   │ 4.000%   │               │
│  └──────────┘    └──────────┘   └──────────┘               │
│                                                              │
│  ✗ Your rate (4.000%) is ABOVE breakeven                    │
│    → Costs $35,073.09 more during ARM periods               │
│                                                              │
│  ℹ️ Any new rate below 3.584% saves money during ARM        │
│     periods                                                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

### 3b. Original Loan Tab

```
┌──────────────────────────────────────────────────────────────┐
│ 📋 Original Loan                                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Scenario 1: Keep Original Loan                             │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  Rate Information        │  Monthly Payments                │
│  ────────────────        │  ────────────────                │
│  Initial Rate            │  Years 1-7:                      │
│  (Years 1-7):            │  $6,804.98                       │
│  4.875%                  │                                  │
│                          │  Years 8-30:                     │
│  Capped Rate             │  $11,239.09                      │
│  (Years 8-30):           │                                  │
│  9.875%                  │                                  │
│                                                              │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  ┌───────────────┐  ┌────────────────┐  ┌────────────────┐  │
│  │ Total Amount  │  │ Total Interest │  │ Total Principal│  │
│  │ Paid          │  │ Paid           │  │ Paid           │  │
│  │               │  │                │  │                │  │
│  │ $3,437,014    │  │ $2,149,014     │  │ $1,288,000     │  │
│  └───────────────┘  └────────────────┘  └────────────────┘  │
│                                                              │
│  ────────────────────────────────────────────────────────    │
│  Interest Breakdown by Period                                │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  ARM Period (Months 1-84, Years 1-7)                        │
│  ───────────────────────────────────────                     │
│  Interest Paid:   $414,392.41                               │
│  Principal Paid:  $157,199.28                               │
│                                                              │
│  Adjustable Period (Months 85-360, Years 8-30)              │
│  ──────────────────────────────────────────                  │
│  Interest Paid:   $1,734,621.24                             │
│  Principal Paid:  $1,130,800.72                             │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

### 3c. Refinance Scenario Tab

```
┌──────────────────────────────────────────────────────────────┐
│ 🔄 Refinance Scenario                                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Scenario 2: Refinance After 24 Months (2.0 years)          │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  ┌────────────────┐                                          │
│  │ Refinance Cost │                                          │
│  │ $2,000.00      │                                          │
│  └────────────────┘                                          │
│                                                              │
│  ────────────────────────────────────────────────────────    │
│  Before Refinance                                            │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  ┌────────────────┐ ┌──────────────┐ ┌──────────────────┐   │
│  │ Monthly        │ │ Total Paid   │ │ Remaining        │   │
│  │ Payment        │ │ (Months 1-24)│ │ Balance          │   │
│  │                │ │              │ │                  │   │
│  │ $6,804.98      │ │ $163,319.50  │ │ $1,262,732.47    │   │
│  └────────────────┘ └──────────────┘ └──────────────────┘   │
│                                                              │
│  Interest Paid:   $96,734.28                                │
│  Principal Paid:  $25,267.53                                │
│                                                              │
│  ────────────────────────────────────────────────────────    │
│  After Refinance                                             │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  New Loan Amount:  $1,262,732.47                            │
│  New Initial Rate: 4.000%                                    │
│  New Capped Rate:  9.000%                                    │
│                                                              │
│  Monthly Payment (Phase 1): $6,154.84                       │
│  Monthly Payment (Phase 2): $10,330.02                      │
│                                                              │
│  ────────────────────────────────────────────────────────    │
│  Total Refinance Scenario                                    │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  ┌────────────────┐ ┌────────────────┐ ┌─────────────────┐  │
│  │ Loan Payments  │ │ Refinance Cost │ │ Total Amount    │  │
│  │                │ │                │ │ Paid            │  │
│  │                │ │                │ │                 │  │
│  │ $3,029,347     │ │ $2,000         │ │ $3,031,347      │  │
│  └────────────────┘ └────────────────┘ └─────────────────┘  │
│                                                              │
│  ────────────────────────────────────────────────────────    │
│  Interest Breakdown by Period                                │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  Original Loan (Months 1-24)                                │
│  Interest:   $96,734.28                                      │
│  Principal:  $25,267.53                                      │
│                                                              │
│  New ARM Period (Months 25-108)                             │
│  Interest:   $350,731.21                                     │
│  Principal:  $166,199.60                                     │
│                                                              │
│  New Adjustable Period (Months 109-360)                     │
│  Interest:   $1,295,881.36                                   │
│  Principal:  $1,096,532.87                                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

### 3d. Breakeven Analysis Tab

```
┌──────────────────────────────────────────────────────────────┐
│ 📈 Breakeven Analysis                                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Breakeven Rate Analysis (refinancing at month 24)          │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│  ┌───────────────┐  ┌────────────────┐  ┌────────────────┐  │
│  │ Current ARM   │  │ Current Cap    │  │ Breakeven NEW  │  │
│  │ Rate          │  │ Rate           │  │ ARM Rate       │  │
│  │               │  │                │  │                │  │
│  │ 4.875%        │  │ 9.875%         │  │ 5.368%         │  │
│  └───────────────┘  └────────────────┘  └────────────────┘  │
│                                                              │
│  Breakeven NEW cap rate: 10.368%                            │
│                                                              │
│  ℹ️ Refinancing at any NEW rate below 5.368% saves money    │
│     compared to keeping your current 4.875% ARM.            │
│                                                              │
│  ⚠️ Why breakeven (5.368%) > current rate (4.875%)?         │
│     Refinancing resets you to a new 7-year fixed period,    │
│     allowing you to avoid the high cap rate (9.875%)        │
│     sooner, even at a higher rate.                          │
│                                                              │
│  ┌─────────────────────────────────────────────────┐        │
│  │ ✓ Your new rate (4.000%) is 1.368% BELOW       │        │
│  │   breakeven → Refinancing is BENEFICIAL         │        │
│  └─────────────────────────────────────────────────┘        │
│                                                              │
│  ────────────────────────────────────────────────────────    │
│  Breakeven Rates for Different Refinance Timings            │
│  ────────────────────────────────────────────────────────    │
│  With refi cost of $2,000.00                                │
│                                                              │
│  ┌──────┬───────┬────────────────┬────────────┬──────────┐  │
│  │Month │ Years │ Breakeven Rate │ Your Rate  │ Decision │  │
│  ├──────┼───────┼────────────────┼────────────┼──────────┤  │
│  │  12  │  1.0  │     5.407%     │   4.000%   │ ✓ GOOD   │  │
│  │  24  │  2.0  │     5.368%     │   4.000%   │ ✓ GOOD   │  │
│  │  36  │  3.0  │     5.332%     │   4.000%   │ ✓ GOOD   │  │
│  │  48  │  4.0  │     5.299%     │   4.000%   │ ✓ GOOD   │  │
│  │  60  │  5.0  │     5.269%     │   4.000%   │ ✓ GOOD   │  │
│  │  72  │  6.0  │     5.242%     │   4.000%   │ ✓ GOOD   │  │
│  └──────┴───────┴────────────────┴────────────┴──────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

### 4. Help Section (Expandable)

**Activated by "Show Help" button in sidebar**

```
┌──────────────────────────────────────────────────────────────┐
│ 📖 Help Guide                                            [X] │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ARM Refinance Calculator - Help Guide                      │
│  ════════════════════════════════════════                    │
│                                                              │
│  Overview:                                                   │
│  This calculator helps you analyze whether refinancing...    │
│                                                              │
│  Loan Structure: 7/6 ARM                                     │
│  - Years 1-7 (84 months): Fixed rate period                 │
│  - Years 8-30 (276 months): Adjustable rate period          │
│  - Default assumption: Adjustable rate = Initial + 5%       │
│                                                              │
│  Comparison Modes:                                           │
│                                                              │
│  1. Full 30-Year Comparison (Default)                       │
│     - Compares total cost over entire loan term             │
│     - Best when planning to keep loan for full term         │
│                                                              │
│  2. ARM Periods Only                                         │
│     - Compares ONLY the ARM fixed-rate periods              │
│     - Best when planning to sell in 5-7 years               │
│                                                              │
│  3. Custom Adjustable Rate                                   │
│     - Use a specific rate for years 8-30                    │
│     - Useful for modeling future refinance plans            │
│                                                              │
│  Key Metrics:                                                │
│  - Breakeven Rate: New rate where refinancing is neutral    │
│  - Savings: Total amount saved by refinancing               │
│  - Monthly Payment: Changes in monthly payments             │
│                                                              │
│  Tips:                                                       │
│  - Get actual closing costs from lenders                    │
│  - Test different timing scenarios                          │
│  - Compare multiple offers                                  │
│                                                              │
│  ┌───────────────┐                                           │
│  │ Close Help    │                                           │
│  └───────────────┘                                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

### 5. Important Notes (Footer)

```
┌──────────────────────────────────────────────────────────────┐
│ 📌 Important Notes                                      [▼]  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  - All calculations assume rates remain constant            │
│  - Actual ARM adjustments may vary based on index + margin  │
│  - Does not account for tax deductions or opportunity costs │
│  - Refinance costs are paid out of pocket, NOT rolled in    │
│  - Does not account for potential future refinancing        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎨 Color Scheme

### Metrics (Summary Cards)
- **Green (↑)**: Positive changes (savings)
- **Red (↓)**: Negative changes (costs)
- **Neutral**: No delta

### Messages
- **Success (Green)**: ✓ Savings, beneficial decisions
- **Error (Red)**: ✗ Additional costs, bad decisions
- **Warning (Yellow)**: = Neutral, equal scenarios
- **Info (Blue)**: ℹ️ Explanations, tips

### Buttons
- **Primary (Blue)**: Calculate button
- **Secondary (Gray)**: Show Help button

---

## 📱 Responsive Design

### Desktop (> 1024px)
- Sidebar: 30% width
- Main area: 70% width
- 3 columns for metrics
- Full-width tabs

### Tablet (768px - 1024px)
- Sidebar: Full width (collapsible)
- Main area: Full width
- 2-3 columns for metrics
- Full-width tabs

### Mobile (< 768px)
- Sidebar: Full width (collapsible)
- Main area: Full width
- 1 column for metrics (stacked)
- Scrollable tabs

---

## 🖱️ User Interactions

### Input Changes
1. User modifies input → Streamlit detects change
2. No action needed, waits for "Calculate"

### Calculate Button
1. User clicks "Calculate" → Streamlit re-runs
2. Spinner appears: "Calculating..."
3. Results populate all tabs
4. Summary metrics update

### Tab Switching
1. User clicks tab → Content changes instantly
2. No recalculation needed
3. All tabs stay populated

### Help Toggle
1. User clicks "Show Help" → Expander opens
2. User clicks "Close Help" → Expander closes
3. Page refreshes

### Checkbox Toggles
1. User checks/unchecks → Input enables/disables
2. No recalculation until "Calculate" clicked

---

## ⌨️ Keyboard Navigation

- **Tab**: Navigate between inputs
- **Enter**: Submit form (same as Calculate)
- **Space**: Toggle checkboxes
- **Arrow keys**: Adjust slider
- **Ctrl/Cmd + R**: Refresh page

---

## 🎯 Visual Hierarchy

1. **Most important** (Largest, top): Summary metrics
2. **Important** (Prominent): Calculate button, Comparison tab
3. **Supporting** (Medium): Other tabs, inputs
4. **Reference** (Smaller): Help, notes, explanations

---

## 💡 UX Best Practices

### Input Validation
- Min/max values enforced
- Percentage format (%.3f)
- Currency format ($X,XXX.XX)

### Feedback
- Button states (hover, active)
- Loading spinners
- Success/error messages
- Colored indicators

### Clarity
- Labels for all inputs
- Help text tooltips
- Visual grouping (borders, spacing)
- Consistent formatting

### Accessibility
- High contrast colors
- Large click targets
- Keyboard navigation
- Screen reader friendly

---

## 🌟 Key Advantages Over Desktop GUI

1. **Better Organization**: Tabs vs scrolling
2. **Visual Metrics**: Colored cards vs text
3. **Mobile Support**: Responsive vs desktop-only
4. **Modern Look**: Clean web UI vs traditional widgets
5. **Easy Sharing**: URL vs script file
6. **Auto-refresh**: Instant vs manual
7. **Expandable Help**: In-place vs popup
8. **Persistent State**: Session-based vs restart

---

**This interface makes complex financial calculations accessible and easy to understand! 🎉**

