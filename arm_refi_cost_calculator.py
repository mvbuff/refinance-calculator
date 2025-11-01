#!/home/utils/Python/builds/3.11.9-20250401/bin/python3.11
"""
ARM Refinance Cost Calculator
Compares total costs between keeping original ARM vs refinancing at any point

USAGE:
    python3 arm_refi_cost_calculator.py

WHAT IT DOES:
    - Calculates total cost of an ARM loan over the full term with two rate periods:
      * Fixed period (configurable, e.g., 3, 5, 7, 10 years): Fixed initial rate
      * Adjustable period (remaining years): Adjustable rate (capped at initial rate + 5%)
    
    - Models refinancing scenario:
      * Pay on original loan until specified month
      * Refinance remaining balance + costs into new 7/6 ARM
      * Compare total costs between scenarios
    
    - Provides insights:
      * Monthly payment comparisons
      * Total interest savings
      * Break-even payback analysis
      * Breakeven interest rate calculation
      * Alternative timing scenarios
      * Rate threshold recommendations

HOW TO USE:
    1. Scroll down to "ADJUSTABLE VARIABLES" section (around line 380)
    2. Modify the following parameters:
       - loan_amount: Original loan amount ($1,288,000 by default)
       - loan_term_years: Total loan term (30 years by default)
       - arm_fixed_years: ARM fixed period (7 years by default, can be 3, 5, 7, 10, etc.)
       - current_arm_rate: Current ARM initial rate (4.875% = 0.04875)
       - months_before_refi: When to refinance (24 months = 2 years)
       - new_arm_rate: New ARM rate if refinancing (4% = 0.04)
       - refi_cost: Refinancing costs ($2,000 by default)
       - compare_arm_only: True for ARM periods only, False for full term
       - use_custom_adjustable_rate: True to use custom rate for adjustable period
       - custom_adjustable_rate: Rate for adjustable period in both scenarios
    3. Run the script
    4. Review comprehensive comparison and insights

KEY FEATURE - BREAKEVEN RATE ANALYSIS:
    The calculator automatically determines the "breakeven rate" - the new ARM rate 
    at which refinancing becomes neutral (neither saves nor costs more money).
    
    - If your offered rate is BELOW the breakeven rate → Refinance is beneficial ✓
    - If your offered rate is ABOVE the breakeven rate → Don't refinance ✗
    - The breakeven rate varies based on WHEN you refinance
    
    Example: If breakeven rate is 5.357% at month 24:
      - A 4.0% offer saves you $403,074 → Refinance!
      - A 6.0% offer costs you $197,810 more → Don't refinance!

EXAMPLES:
    # Compare refinancing at different times:
    months_before_refi = 12   # After 1 year
    months_before_refi = 36   # After 3 years
    months_before_refi = 72   # After 6 years
    
    # Test different new rates:
    new_arm_rate = 0.035      # 3.5% new rate
    new_arm_rate = 0.045      # 4.5% new rate
    
    # Adjust refinance costs:
    refi_cost = 5000          # Higher closing costs
    refi_cost = 0             # No-cost refinance

ASSUMPTIONS:
    - Rates remain constant during each period
    - No prepayments or extra payments
    - No tax considerations
    - Full loan term (configurable, default 30 years/360 months)
    - ARM fixed period (configurable, default 7 years/84 months) for both original and new ARMs
"""

def monthly_payment(principal, annual_rate, months):
    """Calculate fixed monthly payment for a loan"""
    if annual_rate == 0:
        return principal / months
    r = annual_rate / 12
    M = (principal * r * (1 + r) ** months) / ((1 + r) ** months - 1)
    return M

def loan_schedule(principal, annual_rate, total_months):
    """Generate complete amortization schedule"""
    r = annual_rate / 12
    monthly = monthly_payment(principal, annual_rate, total_months)
    schedule = []
    balance = principal
    total_interest_paid = 0.0
    total_principal_paid = 0.0
    
    for m in range(1, total_months + 1):
        interest = balance * r
        principal_paid = monthly - interest
        balance -= principal_paid
        total_interest_paid += interest
        total_principal_paid += principal_paid
        
        schedule.append({
            'Month': m,
            'Payment': monthly,
            'Principal': principal_paid,
            'Interest': interest,
            'Balance': max(0, balance),  # Avoid negative due to rounding
            'TotalInterest': total_interest_paid,
            'TotalPrincipal': total_principal_paid
        })
    
    return schedule

def calculate_original_loan(loan_amount, initial_rate, cap_rate, first_period_months, total_months):
    """Calculate total cost of original ARM loan (7/6 pattern)"""
    
    # Phase 1: First 7 years at initial rate
    # Monthly payment is calculated based on full 30-year term at initial rate
    monthly_payment_phase1 = monthly_payment(loan_amount, initial_rate, total_months)
    
    # Build amortization schedule for first 84 months
    r1 = initial_rate / 12
    balance = loan_amount
    total_interest_phase1 = 0
    total_principal_phase1 = 0
    
    for m in range(first_period_months):
        interest = balance * r1
        principal_paid = monthly_payment_phase1 - interest
        balance -= principal_paid
        total_interest_phase1 += interest
        total_principal_phase1 += principal_paid
    
    balance_after_phase1 = balance
    total_paid_phase1 = monthly_payment_phase1 * first_period_months
    
    # Phase 2: Remaining 23 years at capped rate
    # Recalculate payment based on remaining balance and remaining time
    remaining_months = total_months - first_period_months
    monthly_payment_phase2 = monthly_payment(balance_after_phase1, cap_rate, remaining_months)
    
    # Build amortization schedule for remaining months
    r2 = cap_rate / 12
    balance = balance_after_phase1
    total_interest_phase2 = 0
    total_principal_phase2 = 0
    
    for m in range(remaining_months):
        interest = balance * r2
        principal_paid = monthly_payment_phase2 - interest
        balance -= principal_paid
        total_interest_phase2 += interest
        total_principal_phase2 += principal_paid
    
    total_paid_phase2 = monthly_payment_phase2 * remaining_months
    
    return {
        'monthly_payment_phase1': monthly_payment_phase1,
        'monthly_payment_phase2': monthly_payment_phase2,
        'total_paid_phase1': total_paid_phase1,
        'total_paid_phase2': total_paid_phase2,
        'total_paid': total_paid_phase1 + total_paid_phase2,
        'total_interest': total_interest_phase1 + total_interest_phase2,
        'total_principal': loan_amount,
        'balance_after_phase1': balance_after_phase1,
        'principal_paid_phase1': total_principal_phase1,
        'principal_paid_phase2': total_principal_phase2
    }

def calculate_refinance_scenario(loan_amount, original_rate, original_cap, 
                                 new_rate, new_cap, refi_month, refi_cost,
                                 first_period_months, total_months):
    """Calculate total cost when refinancing at specified month"""
    
    # Step 1: Calculate payments on original loan until refinance
    # Monthly payment is based on full 30-year term at original rate
    monthly_before_refi = monthly_payment(loan_amount, original_rate, total_months)
    
    # Calculate balance at refinance point
    r = original_rate / 12
    balance = loan_amount
    total_interest_before_refi = 0
    total_principal_before_refi = 0
    
    for m in range(refi_month):
        interest = balance * r
        principal_paid = monthly_before_refi - interest
        balance -= principal_paid
        total_interest_before_refi += interest
        total_principal_before_refi += principal_paid
    
    balance_at_refi = balance
    total_paid_before_refi = monthly_before_refi * refi_month
    
    # Step 2: New loan = remaining balance only (refi cost is separate expense)
    new_loan_amount = balance_at_refi
    # New loan gets a full term (e.g., new 30-year loan)
    new_loan_term_months = total_months
    
    # Step 3: New loan Phase 1 - fixed period at new rate
    new_phase1_months = min(first_period_months, new_loan_term_months)
    monthly_new_phase1 = monthly_payment(new_loan_amount, new_rate, new_loan_term_months)
    
    # Calculate balance after new loan phase 1
    r_new = new_rate / 12
    balance = new_loan_amount
    total_interest_new_phase1 = 0
    total_principal_new_phase1 = 0
    
    for m in range(new_phase1_months):
        interest = balance * r_new
        principal_paid = monthly_new_phase1 - interest
        balance -= principal_paid
        total_interest_new_phase1 += interest
        total_principal_new_phase1 += principal_paid
    
    balance_after_new_phase1 = balance
    total_paid_new_phase1 = monthly_new_phase1 * new_phase1_months
    
    # Step 4: New loan Phase 2 - remaining time at capped rate
    if new_loan_term_months > new_phase1_months:
        new_phase2_months = new_loan_term_months - new_phase1_months
        monthly_new_phase2 = monthly_payment(balance_after_new_phase1, new_cap, new_phase2_months)
        
        # Calculate totals for phase 2
        r_cap = new_cap / 12
        balance = balance_after_new_phase1
        total_interest_new_phase2 = 0
        total_principal_new_phase2 = 0
        
        for m in range(new_phase2_months):
            interest = balance * r_cap
            principal_paid = monthly_new_phase2 - interest
            balance -= principal_paid
            total_interest_new_phase2 += interest
            total_principal_new_phase2 += principal_paid
        
        total_paid_new_phase2 = monthly_new_phase2 * new_phase2_months
    else:
        monthly_new_phase2 = 0
        total_paid_new_phase2 = 0
        total_interest_new_phase2 = 0
        total_principal_new_phase2 = 0
    
    # Total cost = payments before refi + payments on new loan + refi cost (one-time expense)
    total_cost = total_paid_before_refi + total_paid_new_phase1 + total_paid_new_phase2 + refi_cost
    total_interest = total_interest_before_refi + total_interest_new_phase1 + total_interest_new_phase2
    
    return {
        'monthly_before_refi': monthly_before_refi,
        'total_paid_before_refi': total_paid_before_refi,
        'interest_before_refi': total_interest_before_refi,
        'principal_before_refi': total_principal_before_refi,
        'balance_at_refi': balance_at_refi,
        'new_loan_amount': new_loan_amount,
        'refi_cost': refi_cost,
        'monthly_new_phase1': monthly_new_phase1,
        'monthly_new_phase2': monthly_new_phase2,
        'total_paid_new_phase1': total_paid_new_phase1,
        'total_paid_new_phase2': total_paid_new_phase2,
        'interest_new_phase1': total_interest_new_phase1,
        'principal_new_phase1': total_principal_new_phase1,
        'interest_new_phase2': total_interest_new_phase2,
        'principal_new_phase2': total_principal_new_phase2,
        'new_phase1_months': new_phase1_months,
        'new_phase2_months': new_phase2_months,
        'total_paid': total_cost,
        'total_interest': total_interest
    }

def find_breakeven_rate(loan_amount, original_rate, original_cap, target_total_cost,
                        refi_month, refi_cost, first_period_months, total_months,
                        tolerance=0.00001):
    """
    Find the new ARM rate that results in the same total cost as keeping original loan.
    Uses binary search to find the breakeven rate.
    
    Returns the breakeven rate (as decimal, e.g., 0.04 = 4%)
    """
    # Set search bounds
    rate_low = 0.0001  # 0.01%
    rate_high = 0.15   # 15%
    
    max_iterations = 100
    iteration = 0
    
    while iteration < max_iterations:
        rate_mid = (rate_low + rate_high) / 2
        cap_mid = rate_mid + 0.05  # Cap is always +5%
        
        # Calculate total cost with this rate
        scenario = calculate_refinance_scenario(
            loan_amount, original_rate, original_cap,
            rate_mid, cap_mid, refi_month, refi_cost,
            first_period_months, total_months
        )
        
        cost_diff = scenario['total_paid'] - target_total_cost
        
        # Check if we're close enough
        if abs(cost_diff) < tolerance:
            return rate_mid
        
        # Adjust search bounds
        if cost_diff > 0:
            # Cost is too high, need lower rate
            rate_high = rate_mid
        else:
            # Cost is too low, need higher rate
            rate_low = rate_mid
        
        iteration += 1
    
    # Return best estimate
    return (rate_low + rate_high) / 2

def find_breakeven_rate_arm_only(loan_amount, original_rate, target_arm_interest,
                                  refi_month, refi_cost, first_period_months, total_months,
                                  tolerance=0.00001):
    """
    Find the new ARM rate where ARM period costs equal the original ARM period interest.
    
    Formula: Original ARM interest = Interest before refi + New ARM interest + Refi cost
    
    Returns the breakeven rate (as decimal, e.g., 0.04 = 4%)
    """
    # Set search bounds
    rate_low = 0.0001  # 0.01%
    rate_high = 0.15   # 15%
    
    max_iterations = 100
    iteration = 0
    
    while iteration < max_iterations:
        rate_mid = (rate_low + rate_high) / 2
        
        # Calculate interest before refinance (on original loan)
        monthly_pmt = monthly_payment(loan_amount, original_rate, total_months)
        r_orig = original_rate / 12
        balance = loan_amount
        interest_before_refi = 0
        
        for m in range(refi_month):
            interest = balance * r_orig
            principal_paid = monthly_pmt - interest
            balance -= principal_paid
            interest_before_refi += interest
        
        # Calculate new ARM interest with test rate
        new_loan_amount = balance
        remaining_months = total_months - refi_month
        new_phase1_months = min(first_period_months, remaining_months)
        
        monthly_new = monthly_payment(new_loan_amount, rate_mid, remaining_months)
        r_new = rate_mid / 12
        balance = new_loan_amount
        interest_new_arm = 0
        
        for m in range(new_phase1_months):
            interest = balance * r_new
            principal_paid = monthly_new - interest
            balance -= principal_paid
            interest_new_arm += interest
        
        # Total ARM cost = interest before refi + new ARM interest + refi cost
        total_arm_cost = interest_before_refi + interest_new_arm + refi_cost
        
        cost_diff = total_arm_cost - target_arm_interest
        
        # Check if we're close enough
        if abs(cost_diff) < tolerance:
            return rate_mid
        
        # Adjust search bounds
        if cost_diff > 0:
            # Cost is too high, need lower rate
            rate_high = rate_mid
        else:
            # Cost is too low, need higher rate
            rate_low = rate_mid
        
        iteration += 1
    
    # Return best estimate
    return (rate_low + rate_high) / 2

# ============================================================================
# ADJUSTABLE VARIABLES - Modify these to run different scenarios
# ============================================================================

loan_amount = 1288000
loan_term_years = 30         # Total loan term (typically 30)
arm_fixed_years = 7          # ARM fixed rate period (e.g., 3, 5, 7, 10)

full_term_months = loan_term_years * 12       # Total months
first_period_months = arm_fixed_years * 12    # Fixed rate period in months

# Original ARM parameters
current_arm_rate = 0.04875   # 4.875% initial rate
current_max_cap = current_arm_rate + 0.05  # Capped at initial + 5%

# Refinance scenario parameters
months_before_refi = 24      # When to refinance (in months) - ADJUST THIS
new_arm_rate = 0.04          # New ARM initial rate - ADJUST THIS
new_max_cap = new_arm_rate + 0.05  # New cap
refi_cost = 2000             # Refinancing costs - ADJUST THIS

# Comparison mode
compare_arm_only = False     # True: Compare ARM periods only, False: Compare full loan term cost

# Custom rate for adjustable period (after fixed period ends)
use_custom_adjustable_rate = False  # True: Use custom rate instead of cap rates
custom_adjustable_rate = 0.045      # Rate to use for both scenarios after fixed period (e.g., 0.045 = 4.5%)

# ============================================================================
# CALCULATIONS
# ============================================================================

# Determine which rates to use for adjustable period
if use_custom_adjustable_rate:
    original_adjustable_rate = custom_adjustable_rate
    new_adjustable_rate = custom_adjustable_rate
else:
    original_adjustable_rate = current_max_cap
    new_adjustable_rate = new_max_cap

# Calculate original loan scenario
original = calculate_original_loan(
    loan_amount, 
    current_arm_rate, 
    original_adjustable_rate, 
    first_period_months, 
    full_term_months
)

# Calculate refinance scenario
refinance = calculate_refinance_scenario(
    loan_amount,
    current_arm_rate,
    original_adjustable_rate,
    new_arm_rate,
    new_adjustable_rate,
    months_before_refi,
    refi_cost,
    first_period_months,
    full_term_months
)

# Calculate breakeven rate - what rate would make refinancing neutral?
breakeven_rate = find_breakeven_rate(
    loan_amount,
    current_arm_rate,
    current_max_cap,
    original['total_paid'],  # Target: same cost as original
    months_before_refi,
    refi_cost,
    first_period_months,
    full_term_months
)

# ============================================================================
# OUTPUT RESULTS
# ============================================================================

print("=" * 80)
print("ARM REFINANCE COST CALCULATOR")
print("=" * 80)
print()

print("LOAN DETAILS:")
print(f"  Original Loan Amount:        ${loan_amount:,.2f}")
print(f"  Term:                        {full_term_months} months ({full_term_months//12} years)")
print(f"  Fixed Rate Period:           {first_period_months} months ({first_period_months//12} years)")
print()

print("-" * 80)
print("SCENARIO 1: KEEP ORIGINAL LOAN")
print("-" * 80)
print(f"  Initial Rate (Years 1-7):    {current_arm_rate*100:.3f}%")
if use_custom_adjustable_rate:
    print(f"  Custom Rate (Years 8-30):    {original_adjustable_rate*100:.3f}% (User-specified)")
else:
    print(f"  Capped Rate (Years 8-30):    {original_adjustable_rate*100:.3f}%")
print(f"  Monthly Payment (Years 1-7): ${original['monthly_payment_phase1']:,.2f}")
print(f"  Monthly Payment (Years 8-30):${original['monthly_payment_phase2']:,.2f}")
print()
print(f"  Total Amount Paid:           ${original['total_paid']:,.2f}")
print(f"  Total Interest Paid:         ${original['total_interest']:,.2f}")
print(f"  Total Principal Paid:        ${original['total_principal']:,.2f}")
print()
print("  INTEREST BREAKDOWN BY PERIOD:")
interest_phase1 = original['total_interest'] - (original['total_paid'] - original['total_paid_phase1'] - original['total_principal'])
print(f"    ARM Period (Months 1-{first_period_months}, Years 1-7):")
print(f"      Interest Paid:           ${original['total_paid_phase1'] - original['principal_paid_phase1']:,.2f}")
print(f"      Principal Paid:          ${original['principal_paid_phase1']:,.2f}")
print(f"    Adjustable Period (Months {first_period_months+1}-{full_term_months}, Years 8-30):")
print(f"      Interest Paid:           ${original['total_paid_phase2'] - original['principal_paid_phase2']:,.2f}")
print(f"      Principal Paid:          ${original['principal_paid_phase2']:,.2f}")
print()

print("-" * 80)
print(f"SCENARIO 2: REFINANCE AFTER {months_before_refi} MONTHS ({months_before_refi/12:.1f} years)")
print("-" * 80)
print(f"  Refinance Cost:              ${refi_cost:,.2f}")
print()
print("  BEFORE REFINANCE:")
print(f"    Monthly Payment:           ${refinance['monthly_before_refi']:,.2f}")
print(f"    Total Paid (Months 1-{months_before_refi}):  ${refinance['total_paid_before_refi']:,.2f}")
print(f"    Interest Paid:             ${refinance['interest_before_refi']:,.2f}")
print(f"    Principal Paid:            ${refinance['principal_before_refi']:,.2f}")
print(f"    Remaining Balance:         ${refinance['balance_at_refi']:,.2f}")
print()
print("  AFTER REFINANCE:")
print(f"    New Loan Amount:           ${refinance['new_loan_amount']:,.2f}")
print(f"    Refinance Cost (paid out of pocket): ${refinance['refi_cost']:,.2f}")
print(f"    New Initial Rate:          {new_arm_rate*100:.3f}%")
if use_custom_adjustable_rate:
    print(f"    Custom Rate (Years 8-30):  {new_adjustable_rate*100:.3f}% (User-specified)")
else:
    print(f"    New Capped Rate:           {new_adjustable_rate*100:.3f}%")
print(f"    Monthly Payment (Phase 1): ${refinance['monthly_new_phase1']:,.2f}")
if refinance['monthly_new_phase2'] > 0:
    print(f"    Monthly Payment (Phase 2): ${refinance['monthly_new_phase2']:,.2f}")
print()
print("  TOTAL REFINANCE SCENARIO:")
print(f"    Loan Payments:             ${refinance['total_paid'] - refinance['refi_cost']:,.2f}")
print(f"    Refinance Cost:            ${refinance['refi_cost']:,.2f}")
print(f"    Total Amount Paid:         ${refinance['total_paid']:,.2f}")
print(f"    Total Interest Paid:       ${refinance['total_interest']:,.2f}")
print()
print("  INTEREST BREAKDOWN BY PERIOD:")
print(f"    Original Loan (Months 1-{months_before_refi}):")
print(f"      Interest Paid:           ${refinance['interest_before_refi']:,.2f}")
print(f"      Principal Paid:          ${refinance['principal_before_refi']:,.2f}")

# Calculate month ranges for new loan phases
new_loan_start_month = months_before_refi + 1
new_phase1_end_month = months_before_refi + refinance['new_phase1_months']
print(f"    New ARM Period (Months {new_loan_start_month}-{new_phase1_end_month}):")
print(f"      Interest Paid:           ${refinance['interest_new_phase1']:,.2f}")
print(f"      Principal Paid:          ${refinance['principal_new_phase1']:,.2f}")

if refinance['new_phase2_months'] > 0:
    new_phase2_start_month = new_phase1_end_month + 1
    print(f"    New Adjustable Period (Months {new_phase2_start_month}-{full_term_months}):")
    print(f"      Interest Paid:           ${refinance['interest_new_phase2']:,.2f}")
    print(f"      Principal Paid:          ${refinance['principal_new_phase2']:,.2f}")
print()

print("=" * 80)
print("COMPARISON")
print("=" * 80)

if compare_arm_only:
    print("MODE: ARM PERIODS ONLY - Interest & Refinance Costs Comparison")
    print("-" * 80)
    print()
    print("  NOTE: Principal payments are the same in both scenarios.")
    print("        This comparison focuses only on INTEREST and REFINANCE COSTS.")
    print()
    
    # Original loan ARM interest: Interest during first 84 months
    original_arm_interest = original['total_paid_phase1'] - original['principal_paid_phase1']
    
    # Refinance ARM interest: Interest before refi + interest during new ARM period + refi cost
    refi_arm_interest = refinance['interest_before_refi'] + refinance['interest_new_phase1']
    refi_arm_total_cost = refi_arm_interest + refinance['refi_cost']
    
    print("  ORIGINAL LOAN (ARM Period - Months 1-84):")
    print(f"    Interest Paid:               ${original_arm_interest:,.2f}")
    print(f"    Refinance Cost:              $0.00")
    print(f"    Total Cost (Interest only):  ${original_arm_interest:,.2f}")
    print()
    
    print(f"  REFINANCE SCENARIO (ARM Periods - Months 1-{months_before_refi + refinance['new_phase1_months']}):")
    print(f"    Before Refi (Months 1-{months_before_refi}):")
    print(f"      Interest Paid:             ${refinance['interest_before_refi']:,.2f}")
    print(f"    New ARM Period (Months {months_before_refi+1}-{months_before_refi + refinance['new_phase1_months']}):")
    print(f"      Interest Paid:             ${refinance['interest_new_phase1']:,.2f}")
    print(f"    Combined ARM Interest:       ${refi_arm_interest:,.2f}")
    print(f"    Refinance Cost:              ${refinance['refi_cost']:,.2f}")
    print(f"    Total Cost (Interest + Refi): ${refi_arm_total_cost:,.2f}")
    print()
    
    # Calculate ARM-only breakeven rate
    breakeven_rate_arm = find_breakeven_rate_arm_only(
        loan_amount, current_arm_rate, original_arm_interest,
        months_before_refi, refi_cost, first_period_months, full_term_months
    )
    
    arm_cost_diff = refi_arm_total_cost - original_arm_interest
    if arm_cost_diff < 0:
        print(f"  ARM PERIOD SAVINGS:          ${abs(arm_cost_diff):,.2f}")
        print(f"  Percentage saved:            {(abs(arm_cost_diff)/original_arm_interest)*100:.2f}%")
        print(f"  ✓ Refinancing saves money during ARM periods")
    else:
        print(f"  ARM PERIOD ADDITIONAL COST:  ${arm_cost_diff:,.2f}")
        print(f"  Percentage increase:         {(arm_cost_diff/original_arm_interest)*100:.2f}%")
        print(f"  ✗ Refinancing costs more during ARM periods")
    
    print()
    print(f"  Original ARM interest cost:  ${original_arm_interest:,.2f}")
    print(f"  Refinanced total ARM cost:   ${refi_arm_total_cost:,.2f}")
    print()
    print("  BREAKEVEN RATE FOR ARM PERIODS ONLY:")
    print(f"    Current ARM rate:            {current_arm_rate*100:.3f}%")
    print(f"    Your new ARM rate:           {new_arm_rate*100:.3f}%")
    print(f"    Breakeven ARM rate:          {breakeven_rate_arm*100:.3f}%")
    print()
    if new_arm_rate < breakeven_rate_arm:
        print(f"    ✓ Your rate ({new_arm_rate*100:.3f}%) < Breakeven ({breakeven_rate_arm*100:.3f}%)")
        print(f"      → Saves ${abs(arm_cost_diff):,.2f} during ARM periods")
    elif new_arm_rate > breakeven_rate_arm:
        print(f"    ✗ Your rate ({new_arm_rate*100:.3f}%) > Breakeven ({breakeven_rate_arm*100:.3f}%)")
        print(f"      → Costs ${arm_cost_diff:,.2f} more during ARM periods")
    else:
        print(f"    = Your rate ({new_arm_rate*100:.3f}%) = Breakeven ({breakeven_rate_arm*100:.3f}%)")
        print(f"      → Neutral during ARM periods")
    print()
    print("  INTERPRETATION:")
    print("  - This comparison excludes adjustable rate periods (months 85-360)")
    print("  - Useful if you plan to refinance again or sell before rates adjust")
    print("  - Principal payments are identical in both scenarios, so they're excluded")
    print(f"  - Any new rate below {breakeven_rate_arm*100:.3f}% saves money during ARM periods")
    
    # Set savings for use in later sections (use full 30-year for breakeven analysis)
    savings = original['total_paid'] - refinance['total_paid']
else:
    print("MODE: FULL 30-YEAR COMPARISON (Including All Periods)")
    print("-" * 80)
    print()
    
    savings = original['total_paid'] - refinance['total_paid']
    if savings > 0:
        print(f"  SAVINGS from refinancing:    ${savings:,.2f}")
        print(f"  Percentage saved:            {(savings/original['total_paid'])*100:.2f}%")
    else:
        print(f"  ADDITIONAL COST from refi:   ${abs(savings):,.2f}")
        print(f"  Percentage increase:         {(abs(savings)/original['total_paid'])*100:.2f}%")

    print()
    print(f"  Original loan total:         ${original['total_paid']:,.2f}")
    print(f"  Refinanced loan total:       ${refinance['total_paid']:,.2f}")

print("=" * 80)
print()

# Additional helpful metrics
print("ADDITIONAL INSIGHTS:")
print("-" * 80)

# Only show full 30-year breakeven analysis if NOT in ARM-only mode
if not compare_arm_only:
    # Breakeven rate analysis (Full 30-year)
    print(f"  BREAKEVEN RATE ANALYSIS (refinancing at month {months_before_refi}):")
    print(f"    Current ARM rate:            {current_arm_rate*100:.3f}%")
    if use_custom_adjustable_rate:
        print(f"    Custom adjustable rate:      {original_adjustable_rate*100:.3f}%")
    else:
        print(f"    Current cap rate:            {original_adjustable_rate*100:.3f}%")
    print(f"    Breakeven NEW ARM rate:      {breakeven_rate*100:.3f}%")
    print(f"    Breakeven NEW cap rate:      {(breakeven_rate + 0.05)*100:.3f}%")
    print()
    print(f"    What this means: Refinancing at any NEW rate below {breakeven_rate*100:.3f}% saves money")
    print(f"                     compared to keeping your current {current_arm_rate*100:.3f}% ARM.")
    print()
    if breakeven_rate > current_arm_rate and not use_custom_adjustable_rate:
        print(f"    💡 Why breakeven ({breakeven_rate*100:.3f}%) > current rate ({current_arm_rate*100:.3f}%):")
        print(f"       Refinancing resets you to a new 7-year fixed period, allowing you to")
        print(f"       avoid the high cap rate ({original_adjustable_rate*100:.3f}%) sooner, even at a higher rate.")
    print()
    if new_arm_rate < breakeven_rate:
        rate_advantage = breakeven_rate - new_arm_rate
        print(f"    ✓ Your new rate ({new_arm_rate*100:.3f}%) is {rate_advantage*100:.3f}% BELOW breakeven")
        print(f"      → Refinancing is BENEFICIAL")
    elif new_arm_rate > breakeven_rate:
        rate_disadvantage = new_arm_rate - breakeven_rate
        print(f"    ✗ Your new rate ({new_arm_rate*100:.3f}%) is {rate_disadvantage*100:.3f}% ABOVE breakeven")
        print(f"      → Refinancing is NOT beneficial")
    else:
        print(f"    = Your new rate ({new_arm_rate*100:.3f}%) equals breakeven")
        print(f"      → Neutral (no financial advantage)")
    print()
else:
    # In ARM-only mode, the breakeven was already shown in the comparison section
    print(f"  NOTE: ARM-only breakeven rate is shown in the COMPARISON section above.")
    print(f"        (Breakeven analysis for full 30-year is not shown in ARM-only mode)")
    print()

# Break-even payback analysis
if savings > 0:
    months_to_breakeven = refi_cost / ((original['monthly_payment_phase1'] - refinance['monthly_new_phase1']) if refinance['monthly_new_phase1'] < original['monthly_payment_phase1'] else 1)
    if refinance['monthly_new_phase1'] < original['monthly_payment_phase1']:
        monthly_savings = original['monthly_payment_phase1'] - refinance['monthly_new_phase1']
        print(f"  Monthly payment savings:     ${monthly_savings:,.2f} (during new fixed period)")
        print(f"  Months to break even:        {months_to_breakeven:.1f} months ({months_to_breakeven/12:.1f} years)")
    
    # What if refinancing even later?
    alt_refi_months = [12, 36, 48, 60, 72]
    if months_before_refi not in alt_refi_months:
        print()
        print("  Alternative refinance timing scenarios:")
        for alt_month in alt_refi_months:
            if alt_month < first_period_months:  # Only show if within first period
                alt_scenario = calculate_refinance_scenario(
                    loan_amount, current_arm_rate, current_max_cap,
                    new_arm_rate, new_max_cap, alt_month, refi_cost,
                    first_period_months, full_term_months
                )
                alt_savings = original['total_paid'] - alt_scenario['total_paid']
                print(f"    Refinance at month {alt_month:2d} ({alt_month/12:3.1f} years): ${alt_scenario['total_paid']:,.2f} (saves ${alt_savings:,.2f})")

# Breakeven rates for different timing scenarios
if not compare_arm_only:
    print()
    print("-" * 80)
    print("  BREAKEVEN RATES FOR DIFFERENT REFINANCE TIMINGS:")
    print(f"  (With refi cost of ${refi_cost:,.2f})")
    print()
    print("    Month  Years   Breakeven Rate    Your Rate    Decision")
    print("    " + "-" * 60)

    timing_scenarios = [12, 24, 36, 48, 60, 72]
    for month in timing_scenarios:
        if month <= first_period_months:
            be_rate = find_breakeven_rate(
                loan_amount, current_arm_rate, original_adjustable_rate,
                original['total_paid'], month, refi_cost,
                first_period_months, full_term_months
            )
            decision = "✓ GOOD" if new_arm_rate < be_rate else ("✗ BAD" if new_arm_rate > be_rate else "= NEUTRAL")
            years = month / 12
            print(f"    {month:5d}  {years:5.1f}       {be_rate*100:5.3f}%        {new_arm_rate*100:5.3f}%      {decision}")
else:
    # Show ARM-only breakeven rates for different timings
    print()
    print("-" * 80)
    print("  ARM-ONLY BREAKEVEN RATES FOR DIFFERENT REFINANCE TIMINGS:")
    print(f"  (With refi cost of ${refi_cost:,.2f})")
    print()
    print("    Month  Years   ARM Breakeven     Your Rate    Decision")
    print("    " + "-" * 60)

    timing_scenarios = [12, 24, 36, 48, 60, 72]
    for month in timing_scenarios:
        if month <= first_period_months:
            be_rate_arm = find_breakeven_rate_arm_only(
                loan_amount, current_arm_rate, original['total_paid_phase1'] - original['principal_paid_phase1'],
                month, refi_cost, first_period_months, full_term_months
            )
            decision = "✓ GOOD" if new_arm_rate < be_rate_arm else ("✗ BAD" if new_arm_rate > be_rate_arm else "= NEUTRAL")
            years = month / 12
            print(f"    {month:5d}  {years:5.1f}       {be_rate_arm*100:5.3f}%        {new_arm_rate*100:5.3f}%      {decision}")

print()
print("=" * 80)
print()
print("NOTES:")
print("  - All calculations assume rates remain constant during each period")
print("  - Actual ARM adjustments may vary based on index + margin")
print("  - Does not account for tax deductions, opportunity costs, or inflation")
print("  - Modify variables at top of script to test different scenarios")
print("=" * 80)