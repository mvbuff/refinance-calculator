#!/home/utils/Python/builds/3.11.9-20250401/bin/python3.11
"""
ARM Refinance Cost Calculator - Streamlit Web App
Interactive web interface for comparing ARM refinance scenarios
"""

import streamlit as st


class ARMCalculator:
    """Core calculation functions for ARM refinance analysis"""
    
    @staticmethod
    def monthly_payment(principal, annual_rate, months):
        """Calculate fixed monthly payment for a loan"""
        if annual_rate == 0:
            return principal / months
        r = annual_rate / 12
        M = (principal * r * (1 + r) ** months) / ((1 + r) ** months - 1)
        return M

    @staticmethod
    def calculate_original_loan(loan_amount, initial_rate, cap_rate, first_period_months, total_months):
        """Calculate total cost of original ARM loan"""
        
        # Phase 1: Fixed rate period
        monthly_payment_phase1 = ARMCalculator.monthly_payment(loan_amount, initial_rate, total_months)
        
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
        
        # Phase 2: Adjustable rate period
        remaining_months = total_months - first_period_months
        monthly_payment_phase2 = ARMCalculator.monthly_payment(balance_after_phase1, cap_rate, remaining_months)
        
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

    @staticmethod
    def calculate_refinance_scenario(loan_amount, original_rate, original_cap, 
                                     new_rate, new_cap, refi_month, refi_cost,
                                     first_period_months, total_months):
        """Calculate total cost when refinancing at specified month"""
        
        # Step 1: Calculate payments on original loan until refinance
        monthly_before_refi = ARMCalculator.monthly_payment(loan_amount, original_rate, total_months)
        
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
        
        # Step 3: New loan Phase 1
        new_phase1_months = min(first_period_months, new_loan_term_months)
        monthly_new_phase1 = ARMCalculator.monthly_payment(new_loan_amount, new_rate, new_loan_term_months)
        
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
        
        # Step 4: New loan Phase 2
        if new_loan_term_months > new_phase1_months:
            new_phase2_months = new_loan_term_months - new_phase1_months
            monthly_new_phase2 = ARMCalculator.monthly_payment(balance_after_new_phase1, new_cap, new_phase2_months)
            
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
            new_phase2_months = 0
        
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

    @staticmethod
    def find_breakeven_rate(loan_amount, original_rate, original_cap, target_total_cost,
                           refi_month, refi_cost, first_period_months, total_months,
                           tolerance=0.00001):
        """Find the new ARM rate that results in same total cost as keeping original loan"""
        rate_low = 0.0001
        rate_high = 0.15
        max_iterations = 100
        iteration = 0
        
        while iteration < max_iterations:
            rate_mid = (rate_low + rate_high) / 2
            cap_mid = rate_mid + 0.05
            
            scenario = ARMCalculator.calculate_refinance_scenario(
                loan_amount, original_rate, original_cap,
                rate_mid, cap_mid, refi_month, refi_cost,
                first_period_months, total_months
            )
            
            cost_diff = scenario['total_paid'] - target_total_cost
            
            if abs(cost_diff) < tolerance:
                return rate_mid
            
            if cost_diff > 0:
                rate_high = rate_mid
            else:
                rate_low = rate_mid
            
            iteration += 1
        
        return (rate_low + rate_high) / 2
    
    @staticmethod
    def find_breakeven_rate_arm_only(loan_amount, original_rate, target_arm_interest,
                                      refi_month, refi_cost, first_period_months, total_months,
                                      tolerance=0.00001):
        """Find the new ARM rate where ARM period costs equal the original ARM period interest"""
        rate_low = 0.0001
        rate_high = 0.15
        max_iterations = 100
        iteration = 0
        
        while iteration < max_iterations:
            rate_mid = (rate_low + rate_high) / 2
            
            # Calculate interest before refinance
            monthly_pmt = ARMCalculator.monthly_payment(loan_amount, original_rate, total_months)
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
            
            monthly_new = ARMCalculator.monthly_payment(new_loan_amount, rate_mid, remaining_months)
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
            
            if abs(cost_diff) < tolerance:
                return rate_mid
            
            if cost_diff > 0:
                rate_high = rate_mid
            else:
                rate_low = rate_mid
            
            iteration += 1
        
        return (rate_low + rate_high) / 2


class PrepaymentCalculator:
    """Calculator for extra payments and prepayment analysis"""
    
    @staticmethod
    def calculate_with_extra_payments(loan_amount, annual_rate, total_months, 
                                      extra_monthly=0, lump_sums=None,
                                      is_arm=False, arm_fixed_months=0, 
                                      adjustable_rate=None,
                                      extra_only_during_arm=False,
                                      extra_start_month=1, extra_stop_month=None):
        """Calculate loan with extra payments (supports both fixed-rate and ARM)"""
        if lump_sums is None:
            lump_sums = []
        
        lump_sums = sorted(lump_sums, key=lambda x: x[0])
        
        regular_payment = ARMCalculator.monthly_payment(loan_amount, annual_rate, total_months)
        
        balance = loan_amount
        total_paid = 0
        total_interest = 0
        total_principal = 0
        total_extra_payments = 0
        total_interest_arm_period = 0
        total_interest_adjustable = 0
        month = 0
        schedule = []
        payment_recalculated = False
        
        while balance > 0.01 and month < total_months * 2:
            month += 1
            
            # Determine current interest rate
            if is_arm and month > arm_fixed_months and adjustable_rate is not None:
                current_rate = adjustable_rate
                if not payment_recalculated and balance > 0:
                    remaining_months = total_months - month + 1
                    if remaining_months > 0:
                        regular_payment = ARMCalculator.monthly_payment(balance, adjustable_rate, remaining_months)
                    payment_recalculated = True
            else:
                current_rate = annual_rate
            
            r = current_rate / 12
            interest = balance * r
            
            # Track interest by period
            if is_arm and month <= arm_fixed_months:
                total_interest_arm_period += interest
            elif is_arm:
                total_interest_adjustable += interest
            
            # Regular principal payment
            if balance + interest < regular_payment:
                principal = balance
                payment = balance + interest
            else:
                principal = regular_payment - interest
                payment = regular_payment
            
            # Add extra monthly payment
            # Check if we should apply extra payment this month
            should_apply_extra = True
            
            # Check start/stop month boundaries
            if month < extra_start_month:
                should_apply_extra = False
            if extra_stop_month is not None and month > extra_stop_month:
                should_apply_extra = False
            
            # Check ARM-only constraint
            if extra_only_during_arm and is_arm and month > arm_fixed_months:
                should_apply_extra = False  # Stop extra payments after ARM fixed period
            
            if should_apply_extra:
                extra_this_month = min(extra_monthly, balance - principal) if balance > principal else 0
                if extra_this_month > 0:
                    principal += extra_this_month
                    payment += extra_this_month
                    total_extra_payments += extra_this_month
            
            # Check for lump sum payment this month
            for lump_month, lump_amount in lump_sums:
                if lump_month == month:
                    lump_payment = min(lump_amount, balance - principal) if balance > principal else 0
                    if lump_payment > 0:
                        principal += lump_payment
                        payment += lump_payment
                        total_extra_payments += lump_payment
            
            # Update balances
            balance -= principal
            total_paid += payment
            total_interest += interest
            total_principal += principal
            
            schedule.append({
                'month': month,
                'payment': payment,
                'principal': principal,
                'interest': interest,
                'balance': max(0, balance),
                'extra_payment': payment - regular_payment if payment > regular_payment else 0,
                'rate': current_rate,
                'period': 'ARM Fixed' if (is_arm and month <= arm_fixed_months) else ('Adjustable' if is_arm else 'Fixed')
            })
            
            if balance <= 0.01:
                break
        
        months_to_payoff = month
        
        return {
            'regular_payment': regular_payment,
            'months_to_payoff': months_to_payoff,
            'total_paid': total_paid,
            'total_interest': total_interest,
            'total_principal': total_principal,
            'total_extra_payments': total_extra_payments,
            'total_interest_arm_period': total_interest_arm_period,
            'total_interest_adjustable': total_interest_adjustable,
            'final_balance': balance,
            'schedule': schedule,
            'is_arm': is_arm,
            'arm_fixed_months': arm_fixed_months if is_arm else 0
        }


def format_currency(value):
    """Format value as currency"""
    return f"${value:,.2f}"


def format_percentage(value):
    """Format value as percentage"""
    return f"{value*100:.3f}%"


def main():
    st.set_page_config(
        page_title="ARM Refinance Calculator",
        page_icon="🏠",
        layout="wide"
    )
    
    st.title("🏠 ARM Refinance Cost Calculator")
    
    # Create main tabs for different calculators
    calc_tab1, calc_tab2 = st.tabs(["💰 Refinance Analysis", "⚡ Extra Payments & Prepayment"])
    
    # ================================================================
    # SIDEBAR - Common inputs
    # ================================================================
    active_tab = st.session_state.get('active_tab', 'refinance')
    
    with st.sidebar:
        st.header("Calculator Selection")
        st.info("Use the tabs above to switch between calculators")
        st.markdown("---")
        
        # Determine which set of inputs to show
        if calc_tab1:
            st.header("Refinance Parameters")
            
            loan_amount = st.number_input(
                "Loan Amount ($)",
                min_value=0,
                value=1288000,
                step=1000,
                help="Your original mortgage principal"
            )
            
            loan_term_years = st.number_input(
                "Loan Term (years)",
                min_value=1,
                max_value=50,
                value=30,
                step=1,
                help="Total loan term in years (typically 30)"
            )
            
            arm_fixed_years = st.number_input(
                "ARM Fixed Period (years)",
                min_value=1,
                max_value=30,
                value=7,
                step=1,
                help="Number of years at fixed rate before adjustment (e.g., 3, 5, 7, 10)"
            )
            
            current_arm_rate = st.number_input(
                "Current ARM Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=4.875,
                step=0.001,
                format="%.3f",
                help=f"Your current loan's initial fixed rate for years 1-{int(arm_fixed_years)}"
            )
            
            new_arm_rate = st.number_input(
                "New ARM Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=4.0,
                step=0.001,
                format="%.3f",
                help="The new fixed rate being offered if you refinance"
            )
            
            arm_fixed_months = int(arm_fixed_years * 12)
            default_refi_months = min(24, arm_fixed_months)
            
            months_before_refi = st.slider(
                "Refinance After (months)",
                min_value=1,
                max_value=arm_fixed_months,
                value=default_refi_months,
                help=f"When you plan to refinance (max {arm_fixed_months} months for {int(arm_fixed_years)}-year ARM)"
            )
            
            refi_cost = st.number_input(
                "Refinance Cost ($)",
                min_value=0,
                value=2000,
                step=100,
                help="One-time closing costs paid out of pocket"
            )
            
            st.markdown("---")
            st.subheader("Comparison Options")
            
            compare_arm_only = st.checkbox(
                "Compare ARM periods only",
                value=False,
                help="Exclude adjustable rate periods (useful if planning to sell/refi before year 7-9)"
            )
            
            use_custom_adjustable_rate = st.checkbox(
                "Use custom rate for adjustable period",
                value=False,
                help=f"Use a specific rate for years {int(arm_fixed_years)+1}-{int(loan_term_years)} in both scenarios"
            )
            
            custom_adjustable_rate = st.number_input(
                "Custom Adjustable Rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=4.5,
                step=0.001,
                format="%.3f",
                disabled=not use_custom_adjustable_rate,
                help=f"Rate to use for years {int(arm_fixed_years)+1}-{int(loan_term_years)} in both scenarios"
            )
            
            st.markdown("---")
            calculate_button = st.button("Calculate", type="primary", use_container_width=True)
            
            if st.button("Show Help", use_container_width=True):
                st.session_state['show_help'] = True
    
    # ================================================================
    # TAB 1: REFINANCE ANALYSIS
    # ================================================================
    with calc_tab1:
        # Help section
        if st.session_state.get('show_help', False):
            with st.expander("📖 Help Guide", expanded=True):
                st.markdown("""
                ### ARM Refinance Calculator - Help Guide
                
                **Overview:**
                This calculator helps you analyze whether refinancing your Adjustable Rate Mortgage (ARM) 
                makes financial sense by comparing total costs over the full loan term or just the ARM periods.
                
                **Loan Structure: ARM**
                - Configurable fixed rate period (e.g., 3, 5, 7, 10 years)
                - Remaining term: Adjustable rate period
                - Default assumption: Adjustable rate = Initial rate + 5% (cap)
                
                **Comparison Modes:**
                
                1. **Full Loan Term Comparison (Default)**
                   - Compares total cost over entire loan term
                   - Includes both ARM period and adjustable rate period
                   - Best when planning to keep the loan for the full term
                
                2. **ARM Periods Only**
                   - Compares ONLY the ARM fixed-rate periods
                   - Excludes adjustable rate periods
                   - Best when planning to sell or refinance again in 5-7 years
                
                3. **Custom Adjustable Rate**
                   - Use a specific rate for adjustable period in BOTH scenarios
                   - Removes the cap rate advantage from comparison
                   - Useful for modeling specific future refinance plans
                
                **Key Metrics:**
                - **Breakeven Rate**: The new ARM rate at which refinancing becomes neutral
                - **Savings**: Total amount saved by refinancing
                - **Monthly Payment**: Changes in monthly payment amounts
                
                **Tips:**
                - Get actual closing costs from lenders (not estimates)
                - Verify your current ARM rate from loan documents
                - Test different timing scenarios
                - Compare multiple lender offers using different rate inputs
                """)
                
                if st.button("Close Help"):
                    st.session_state['show_help'] = False
                    st.rerun()
        
        # Main calculation area
        if calculate_button or st.session_state.get('last_calculated', False):
            st.session_state['last_calculated'] = True
            
            # Convert percentages to decimals
            current_arm_rate_dec = current_arm_rate / 100
            current_max_cap = current_arm_rate_dec + 0.05
            new_arm_rate_dec = new_arm_rate / 100
            new_max_cap = new_arm_rate_dec + 0.05
            custom_adjustable_rate_dec = custom_adjustable_rate / 100
            
            full_term_months = int(loan_term_years * 12)
            first_period_months = int(arm_fixed_years * 12)
            
            # Determine which rates to use for adjustable period
            if use_custom_adjustable_rate:
                original_adjustable_rate = custom_adjustable_rate_dec
                new_adjustable_rate = custom_adjustable_rate_dec
            else:
                original_adjustable_rate = current_max_cap
                new_adjustable_rate = new_max_cap
            
            # Calculate scenarios
            with st.spinner('Calculating...'):
                original = ARMCalculator.calculate_original_loan(
                    loan_amount, current_arm_rate_dec, original_adjustable_rate,
                    first_period_months, full_term_months
                )
                
                refinance = ARMCalculator.calculate_refinance_scenario(
                    loan_amount, current_arm_rate_dec, original_adjustable_rate,
                    new_arm_rate_dec, new_adjustable_rate, months_before_refi, refi_cost,
                    first_period_months, full_term_months
                )
                
                breakeven_rate = ARMCalculator.find_breakeven_rate(
                    loan_amount, current_arm_rate_dec, original_adjustable_rate,
                    original['total_paid'], months_before_refi, refi_cost,
                    first_period_months, full_term_months
                )
            
            # Display results
            st.header("Results")
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            
            savings = original['total_paid'] - refinance['total_paid']
            
            with col1:
                st.metric(
                    "Original Loan Total",
                    format_currency(original['total_paid']),
                    help="Total amount paid over full term with original loan"
                )
            
            with col2:
                st.metric(
                    "Refinanced Loan Total",
                    format_currency(refinance['total_paid']),
                    delta=format_currency(-savings) if savings > 0 else format_currency(abs(savings)),
                    delta_color="normal" if savings > 0 else "inverse",
                    help="Total amount paid with refinancing"
                )
            
            with col3:
                if savings > 0:
                    st.metric(
                        "Total Savings",
                        format_currency(savings),
                        delta=f"{(savings/original['total_paid'])*100:.2f}%",
                        help="Amount saved by refinancing"
                    )
                else:
                    st.metric(
                        "Additional Cost",
                        format_currency(abs(savings)),
                        delta=f"{(abs(savings)/original['total_paid'])*100:.2f}%",
                        delta_color="inverse",
                        help="Additional cost from refinancing"
                    )
            
            st.markdown("---")
            
            # Detailed comparison tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Comparison",
                "📋 Original Loan",
                "🔄 Refinance Scenario",
                "📈 Breakeven Analysis"
            ])
            
            with tab1:
                if compare_arm_only:
                    st.subheader("ARM Periods Only - Interest & Refinance Costs Comparison")
                    st.info("💡 Principal payments are the same in both scenarios. This comparison focuses only on INTEREST and REFINANCE COSTS.")
                    
                    # Original loan ARM interest
                    original_arm_interest = original['total_paid_phase1'] - original['principal_paid_phase1']
                    
                    # Refinance ARM interest
                    refi_arm_interest = refinance['interest_before_refi'] + refinance['interest_new_phase1']
                    refi_arm_total_cost = refi_arm_interest + refinance['refi_cost']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Original Loan (ARM Period - Months 1-{first_period_months})**")
                        st.write(f"Interest Paid: {format_currency(original_arm_interest)}")
                        st.write(f"Refinance Cost: $0.00")
                        st.write(f"**Total Cost: {format_currency(original_arm_interest)}**")
                    
                    with col2:
                        st.markdown(f"**Refinance Scenario (ARM Periods - Months 1-{months_before_refi + refinance['new_phase1_months']})**")
                        st.write(f"Before Refi Interest: {format_currency(refinance['interest_before_refi'])}")
                        st.write(f"New ARM Interest: {format_currency(refinance['interest_new_phase1'])}")
                        st.write(f"Refinance Cost: {format_currency(refinance['refi_cost'])}")
                        st.write(f"**Total Cost: {format_currency(refi_arm_total_cost)}**")
                    
                    arm_cost_diff = refi_arm_total_cost - original_arm_interest
                    
                    if arm_cost_diff < 0:
                        st.success(f"✓ ARM PERIOD SAVINGS: {format_currency(abs(arm_cost_diff))} ({(abs(arm_cost_diff)/original_arm_interest)*100:.2f}%)")
                    else:
                        st.error(f"✗ ARM PERIOD ADDITIONAL COST: {format_currency(arm_cost_diff)} ({(arm_cost_diff/original_arm_interest)*100:.2f}%)")
                    
                    # ARM-only breakeven rate
                    breakeven_rate_arm = ARMCalculator.find_breakeven_rate_arm_only(
                        loan_amount, current_arm_rate_dec, original_arm_interest,
                        months_before_refi, refi_cost, first_period_months, full_term_months
                    )
                    
                    st.markdown("---")
                    st.subheader("ARM-Only Breakeven Rate")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Current ARM Rate", format_percentage(current_arm_rate_dec))
                    with col2:
                        st.metric("Your New ARM Rate", format_percentage(new_arm_rate_dec))
                    with col3:
                        st.metric("Breakeven ARM Rate", format_percentage(breakeven_rate_arm))
                    
                    if new_arm_rate_dec < breakeven_rate_arm:
                        st.success(f"✓ Your rate ({format_percentage(new_arm_rate_dec)}) is BELOW breakeven → Saves {format_currency(abs(arm_cost_diff))} during ARM periods")
                    elif new_arm_rate_dec > breakeven_rate_arm:
                        st.error(f"✗ Your rate ({format_percentage(new_arm_rate_dec)}) is ABOVE breakeven → Costs {format_currency(arm_cost_diff)} more during ARM periods")
                    else:
                        st.warning(f"= Your rate ({format_percentage(new_arm_rate_dec)}) equals breakeven → Neutral during ARM periods")
                    
                    st.info(f"Any new rate below {format_percentage(breakeven_rate_arm)} saves money during ARM periods")
                
                else:
                    st.subheader("Full Loan Term Comparison")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Original Loan**")
                        st.write(f"Total Paid: {format_currency(original['total_paid'])}")
                        st.write(f"Total Interest: {format_currency(original['total_interest'])}")
                        st.write(f"Total Principal: {format_currency(original['total_principal'])}")
                    
                    with col2:
                        st.markdown("**Refinanced Loan**")
                        st.write(f"Total Paid: {format_currency(refinance['total_paid'])}")
                        st.write(f"Total Interest: {format_currency(refinance['total_interest'])}")
                        st.write(f"Refinance Cost: {format_currency(refinance['refi_cost'])}")
                    
                    if savings > 0:
                        st.success(f"✓ SAVINGS from refinancing: {format_currency(savings)} ({(savings/original['total_paid'])*100:.2f}%)")
                        
                        if refinance['monthly_new_phase1'] < original['monthly_payment_phase1']:
                            monthly_savings = original['monthly_payment_phase1'] - refinance['monthly_new_phase1']
                            months_to_breakeven = refi_cost / monthly_savings
                            st.info(f"📅 Monthly payment savings: {format_currency(monthly_savings)} | Months to break even: {months_to_breakeven:.1f} ({months_to_breakeven/12:.1f} years)")
                    else:
                        st.error(f"✗ ADDITIONAL COST from refinancing: {format_currency(abs(savings))} ({(abs(savings)/original['total_paid'])*100:.2f}%)")
            
            with tab2:
                st.subheader("Scenario 1: Keep Original Loan")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Rate Information**")
                    st.write(f"Initial Rate (Years 1-{int(arm_fixed_years)}): {format_percentage(current_arm_rate_dec)}")
                    if use_custom_adjustable_rate:
                        st.write(f"Custom Rate (Years {int(arm_fixed_years)+1}-{int(loan_term_years)}): {format_percentage(original_adjustable_rate)} (User-specified)")
                    else:
                        st.write(f"Capped Rate (Years {int(arm_fixed_years)+1}-{int(loan_term_years)}): {format_percentage(original_adjustable_rate)}")
                
                with col2:
                    st.markdown("**Monthly Payments**")
                    st.write(f"Years 1-{int(arm_fixed_years)}: {format_currency(original['monthly_payment_phase1'])}")
                    st.write(f"Years {int(arm_fixed_years)+1}-{int(loan_term_years)}: {format_currency(original['monthly_payment_phase2'])}")
                
                st.markdown("---")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Amount Paid", format_currency(original['total_paid']))
                with col2:
                    st.metric("Total Interest Paid", format_currency(original['total_interest']))
                with col3:
                    st.metric("Total Principal Paid", format_currency(original['total_principal']))
                
                st.markdown("---")
                st.subheader("Interest Breakdown by Period")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**ARM Period (Months 1-{first_period_months}, Years 1-{int(arm_fixed_years)})**")
                    st.write(f"Interest Paid: {format_currency(original['total_paid_phase1'] - original['principal_paid_phase1'])}")
                    st.write(f"Principal Paid: {format_currency(original['principal_paid_phase1'])}")
                
                with col2:
                    st.markdown(f"**Adjustable Period (Months {first_period_months+1}-{full_term_months}, Years {int(arm_fixed_years)+1}-{int(loan_term_years)})**")
                    st.write(f"Interest Paid: {format_currency(original['total_paid_phase2'] - original['principal_paid_phase2'])}")
                    st.write(f"Principal Paid: {format_currency(original['principal_paid_phase2'])}")
            
            with tab3:
                st.subheader(f"Scenario 2: Refinance After {months_before_refi} Months ({months_before_refi/12:.1f} years)")
                
                st.metric("Refinance Cost", format_currency(refi_cost))
                
                st.markdown("---")
                st.markdown("**Before Refinance**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Monthly Payment", format_currency(refinance['monthly_before_refi']))
                with col2:
                    st.metric(f"Total Paid (Months 1-{months_before_refi})", format_currency(refinance['total_paid_before_refi']))
                with col3:
                    st.metric("Remaining Balance", format_currency(refinance['balance_at_refi']))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"Interest Paid: {format_currency(refinance['interest_before_refi'])}")
                with col2:
                    st.write(f"Principal Paid: {format_currency(refinance['principal_before_refi'])}")
                
                st.markdown("---")
                st.markdown("**After Refinance**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"New Loan Amount: {format_currency(refinance['new_loan_amount'])}")
                    st.write(f"New Initial Rate: {format_percentage(new_arm_rate_dec)}")
                    if use_custom_adjustable_rate:
                        st.write(f"Custom Rate (Years {int(arm_fixed_years)+1}-{int(loan_term_years)}): {format_percentage(new_adjustable_rate)} (User-specified)")
                    else:
                        st.write(f"New Capped Rate: {format_percentage(new_adjustable_rate)}")
                
                with col2:
                    st.write(f"Monthly Payment (Phase 1): {format_currency(refinance['monthly_new_phase1'])}")
                    if refinance['monthly_new_phase2'] > 0:
                        st.write(f"Monthly Payment (Phase 2): {format_currency(refinance['monthly_new_phase2'])}")
                
                st.markdown("---")
                st.subheader("Total Refinance Scenario")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Loan Payments", format_currency(refinance['total_paid'] - refinance['refi_cost']))
                with col2:
                    st.metric("Refinance Cost", format_currency(refinance['refi_cost']))
                with col3:
                    st.metric("Total Amount Paid", format_currency(refinance['total_paid']))
                
                st.markdown("---")
                st.subheader("Interest Breakdown by Period")
                
                new_loan_start_month = months_before_refi + 1
                new_phase1_end_month = months_before_refi + refinance['new_phase1_months']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Original Loan (Months 1-{months_before_refi})**")
                    st.write(f"Interest Paid: {format_currency(refinance['interest_before_refi'])}")
                    st.write(f"Principal Paid: {format_currency(refinance['principal_before_refi'])}")
                
                with col2:
                    st.markdown(f"**New ARM Period (Months {new_loan_start_month}-{new_phase1_end_month})**")
                    st.write(f"Interest Paid: {format_currency(refinance['interest_new_phase1'])}")
                    st.write(f"Principal Paid: {format_currency(refinance['principal_new_phase1'])}")
                
                if refinance['new_phase2_months'] > 0:
                    new_phase2_start_month = new_phase1_end_month + 1
                    new_phase2_end_month = months_before_refi + full_term_months
                    st.markdown(f"**New Adjustable Period (Months {new_phase2_start_month}-{new_phase2_end_month})**")
                    st.write(f"Interest Paid: {format_currency(refinance['interest_new_phase2'])}")
                    st.write(f"Principal Paid: {format_currency(refinance['principal_new_phase2'])}")
            
            with tab4:
                if not compare_arm_only:
                    st.subheader(f"Breakeven Rate Analysis (refinancing at month {months_before_refi})")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Current ARM Rate", format_percentage(current_arm_rate_dec))
                    with col2:
                        if use_custom_adjustable_rate:
                            st.metric("Custom Adjustable Rate", format_percentage(original_adjustable_rate))
                        else:
                            st.metric("Current Cap Rate", format_percentage(original_adjustable_rate))
                    with col3:
                        st.metric("Breakeven NEW ARM Rate", format_percentage(breakeven_rate))
                    
                    st.write(f"Breakeven NEW cap rate: {format_percentage(breakeven_rate + 0.05)}")
                    
                    st.info(f"💡 Refinancing at any NEW rate below {format_percentage(breakeven_rate)} saves money compared to keeping your current {format_percentage(current_arm_rate_dec)} ARM.")
                    
                    if breakeven_rate > current_arm_rate_dec and not use_custom_adjustable_rate:
                        st.warning(f"Why breakeven ({format_percentage(breakeven_rate)}) > current rate ({format_percentage(current_arm_rate_dec)})? Refinancing resets you to a new {int(arm_fixed_years)}-year fixed period, allowing you to avoid the high cap rate ({format_percentage(original_adjustable_rate)}) sooner, even at a higher rate.")
                    
                    if new_arm_rate_dec < breakeven_rate:
                        rate_advantage = breakeven_rate - new_arm_rate_dec
                        st.success(f"✓ Your new rate ({format_percentage(new_arm_rate_dec)}) is {format_percentage(rate_advantage)} BELOW breakeven → Refinancing is BENEFICIAL")
                    elif new_arm_rate_dec > breakeven_rate:
                        rate_disadvantage = new_arm_rate_dec - breakeven_rate
                        st.error(f"✗ Your new rate ({format_percentage(new_arm_rate_dec)}) is {format_percentage(rate_disadvantage)} ABOVE breakeven → Refinancing is NOT beneficial")
                    else:
                        st.warning(f"= Your new rate ({format_percentage(new_arm_rate_dec)}) equals breakeven → Neutral (no financial advantage)")
                    
                    st.markdown("---")
                    st.subheader("Breakeven Rates for Different Refinance Timings")
                    st.caption(f"With refi cost of {format_currency(refi_cost)}")
                    
                    timing_scenarios = [12, 24, 36, 48, 60, 72]
                    timing_data = []
                    
                    for month in timing_scenarios:
                        if month <= first_period_months:
                            be_rate = ARMCalculator.find_breakeven_rate(
                                loan_amount, current_arm_rate_dec, original_adjustable_rate,
                                original['total_paid'], month, refi_cost,
                                first_period_months, full_term_months
                            )
                            decision = "✓ GOOD" if new_arm_rate_dec < be_rate else ("✗ BAD" if new_arm_rate_dec > be_rate else "= NEUTRAL")
                            years = month / 12
                            timing_data.append({
                                "Month": month,
                                "Years": f"{years:.1f}",
                                "Breakeven Rate": format_percentage(be_rate),
                                "Your Rate": format_percentage(new_arm_rate_dec),
                                "Decision": decision
                            })
                    
                    st.table(timing_data)
                
                else:
                    st.info("💡 ARM-only breakeven rate is shown in the Comparison tab. (Full loan term breakeven analysis is not shown in ARM-only mode)")
                    
                    st.markdown("---")
                    st.subheader("ARM-Only Breakeven Rates for Different Refinance Timings")
                    st.caption(f"With refi cost of {format_currency(refi_cost)}")
                    
                    timing_scenarios = [12, 24, 36, 48, 60, 72]
                    timing_data = []
                    
                    for month in timing_scenarios:
                        if month <= first_period_months:
                            be_rate_arm = ARMCalculator.find_breakeven_rate_arm_only(
                                loan_amount, current_arm_rate_dec, 
                                original['total_paid_phase1'] - original['principal_paid_phase1'],
                                month, refi_cost, first_period_months, full_term_months
                            )
                            decision = "✓ GOOD" if new_arm_rate_dec < be_rate_arm else ("✗ BAD" if new_arm_rate_dec > be_rate_arm else "= NEUTRAL")
                            years = month / 12
                            timing_data.append({
                                "Month": month,
                                "Years": f"{years:.1f}",
                                "ARM Breakeven": format_percentage(be_rate_arm),
                                "Your Rate": format_percentage(new_arm_rate_dec),
                                "Decision": decision
                            })
                    
                    st.table(timing_data)
            
            st.markdown("---")
            
            # Notes section
            with st.expander("📌 Important Notes"):
                st.markdown("""
                - All calculations assume rates remain constant during each period
                - Actual ARM adjustments may vary based on index + margin
                - Does not account for tax deductions, opportunity costs, or inflation
                - Refinance costs are paid out of pocket, NOT added to loan principal
                - Does not account for potential future refinancing opportunities
                """)
    
    # ================================================================
    # TAB 2: EXTRA PAYMENTS & PREPAYMENT ANALYSIS
    # ================================================================
    with calc_tab2:
        st.markdown("""
        ### ⚡ Extra Payments & Prepayment Savings Calculator
        
        Calculate how much you can save by making extra payments towards your loan principal.
        This analysis shows the impact of:
        - **Extra monthly payments** towards principal
        - **One-time lump sum payments** at specific times
        - **Works with both ARM and Fixed-rate loans**
        """)
        
        # Prepayment sidebar inputs
        with st.sidebar:
            st.markdown("---")
            st.header("Extra Payments Settings")
            
            prep_loan_amount = st.number_input(
                "Loan Amount ($)",
                min_value=0,
                value=1288000,
                step=1000,
                key="prep_loan_amount",
                help="Your loan principal amount"
            )
            
            prep_loan_term_years = st.number_input(
                "Loan Term (years)",
                min_value=1,
                max_value=50,
                value=30,
                step=1,
                key="prep_loan_term",
                help="Total loan term"
            )
            
            st.markdown("---")
            st.subheader("Loan Type")
            
            prep_is_arm = st.checkbox(
                "ARM Loan",
                value=True,
                key="prep_is_arm",
                help="Check if this is an ARM loan with different rates for fixed and adjustable periods"
            )
            
            if prep_is_arm:
                prep_arm_fixed_years = st.number_input(
                    "ARM Fixed Period (years)",
                    min_value=1,
                    max_value=30,
                    value=7,
                    step=1,
                    key="prep_arm_fixed",
                    help="Number of years at fixed rate (e.g., 3, 5, 7, 10)"
                )
                
                prep_arm_rate = st.number_input(
                    "ARM Fixed Rate (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=4.875,
                    step=0.001,
                    format="%.3f",
                    key="prep_arm_rate",
                    help="Interest rate during ARM fixed period"
                )
                
                prep_adjustable_rate = st.number_input(
                    "Adjustable Period Rate (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=9.875,
                    step=0.001,
                    format="%.3f",
                    key="prep_adj_rate",
                    help=f"Estimated rate for years {int(prep_arm_fixed_years)+1}-{int(prep_loan_term_years)} (e.g., capped rate)"
                )
            else:
                prep_interest_rate = st.number_input(
                    "Interest Rate (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=4.875,
                    step=0.001,
                    format="%.3f",
                    key="prep_fixed_rate",
                    help="Annual interest rate (fixed for entire term)"
                )
            
            st.markdown("---")
            st.subheader("Extra Payment Options")
            
            extra_monthly_payment = st.number_input(
                "Extra Monthly Payment ($)",
                min_value=0,
                value=500,
                step=100,
                key="extra_monthly",
                help="Additional amount to pay each month towards principal"
            )
            
            # Option to limit extra payments to ARM period only
            if prep_is_arm and extra_monthly_payment > 0:
                apply_extra_entire_term = st.radio(
                    "Apply extra monthly payments:",
                    options=["Throughout entire loan term", "Only during ARM fixed period", "Custom date range"],
                    index=0,
                    key="extra_payment_period",
                    help="Choose when to apply extra payments"
                )
                
                if apply_extra_entire_term == "Only during ARM fixed period":
                    st.info(f"💡 Extra monthly payments will stop after month {int(prep_arm_fixed_years * 12)} (end of ARM fixed period)")
            else:
                if extra_monthly_payment > 0:
                    apply_extra_entire_term = st.radio(
                        "Apply extra monthly payments:",
                        options=["Throughout entire loan term", "Custom date range"],
                        index=0,
                        key="extra_payment_period_fixed",
                        help="Choose when to apply extra payments"
                    )
                else:
                    apply_extra_entire_term = "Throughout entire loan term"
            
            # Custom date range for extra payments
            if extra_monthly_payment > 0 and apply_extra_entire_term == "Custom date range":
                st.markdown("**Custom Extra Payment Period**")
                
                col1, col2 = st.columns(2)
                with col1:
                    extra_start_month = st.number_input(
                        "Start Month",
                        min_value=1,
                        max_value=int(prep_loan_term_years * 12),
                        value=1,
                        step=1,
                        key="extra_start_month",
                        help="First month to start making extra payments"
                    )
                with col2:
                    extra_stop_month = st.number_input(
                        "Stop Month",
                        min_value=1,
                        max_value=int(prep_loan_term_years * 12),
                        value=min(60, int(prep_loan_term_years * 12)),
                        step=1,
                        key="extra_stop_month",
                        help="Last month to make extra payments (leave as-is for no end date)"
                    )
                
                # Validate
                if extra_stop_month < extra_start_month:
                    st.error("⚠️ Stop month must be after start month!")
                else:
                    duration_months = extra_stop_month - extra_start_month + 1
                    duration_years = duration_months / 12
                    st.caption(f"Extra payments from month {extra_start_month} to {extra_stop_month} ({duration_months} months / {duration_years:.1f} years)")
            else:
                extra_start_month = 1
                extra_stop_month = None
            
            st.markdown("---")
            st.subheader("Lump Sum Payments")
            
            num_lump_sums = st.number_input(
                "Number of Lump Sum Payments",
                min_value=0,
                max_value=10,
                value=1,
                step=1,
                key="num_lumps",
                help="How many one-time lump sum payments you plan to make"
            )
            
            lump_sum_payments = []
            for i in range(int(num_lump_sums)):
                st.markdown(f"**Lump Sum #{i+1}**")
                col1, col2 = st.columns(2)
                with col1:
                    lump_month = st.number_input(
                        f"Month",
                        min_value=1,
                        max_value=int(prep_loan_term_years * 12),
                        value=min(12 * (i+1), int(prep_loan_term_years * 12)),
                        step=1,
                        key=f"lump_month_{i}"
                    )
                with col2:
                    lump_amount = st.number_input(
                        f"Amount ($)",
                        min_value=0,
                        value=10000,
                        step=1000,
                        key=f"lump_amount_{i}"
                    )
                lump_sum_payments.append((int(lump_month), float(lump_amount)))
            
            st.markdown("---")
            calculate_prep_button = st.button("Calculate Savings", type="primary", use_container_width=True, key="calc_prep")
        
        # Main prepayment results area
        if calculate_prep_button or st.session_state.get('prep_calculated', False):
            st.session_state['prep_calculated'] = True
            
            # Check if any extra payments are configured
            # Filter out lump sums with 0 amount
            valid_lump_sums = [(m, a) for m, a in lump_sum_payments if a > 0]
            has_extra_payments = extra_monthly_payment > 0 or len(valid_lump_sums) > 0
            
            if not has_extra_payments:
                st.warning("⚠️ No extra payments configured. Please set an extra monthly payment or add lump sum payments to see savings analysis.")
                st.info("👈 Use the sidebar to configure:\n- Extra Monthly Payment (e.g., $500)\n- Or add Lump Sum Payments")
            else:
                prep_total_months = int(prep_loan_term_years * 12)
                
                # Prepare loan parameters based on type
                if prep_is_arm:
                    prep_rate_decimal = prep_arm_rate / 100
                    prep_adj_rate_decimal = prep_adjustable_rate / 100
                    prep_arm_fixed_months = int(prep_arm_fixed_years * 12)
                else:
                    prep_rate_decimal = prep_interest_rate / 100
                    prep_adj_rate_decimal = None
                    prep_arm_fixed_months = 0
                
                # Determine if extra payments should only apply during ARM period
                extra_only_during_arm = (apply_extra_entire_term == "Only during ARM fixed period")
                
                # Set start/stop months based on selection
                if apply_extra_entire_term == "Custom date range":
                    final_start_month = int(extra_start_month)
                    final_stop_month = int(extra_stop_month)
                else:
                    final_start_month = 1
                    final_stop_month = None
                
                with st.spinner('Calculating prepayment savings...'):
                    # Calculate regular payment schedule
                    regular = PrepaymentCalculator.calculate_with_extra_payments(
                        prep_loan_amount,
                        prep_rate_decimal,
                        prep_total_months,
                        extra_monthly=0,
                        lump_sums=[],
                        is_arm=prep_is_arm,
                        arm_fixed_months=prep_arm_fixed_months,
                        adjustable_rate=prep_adj_rate_decimal,
                        extra_only_during_arm=False,
                        extra_start_month=1,
                        extra_stop_month=None
                    )
                    
                    # Calculate with extra payments (use only valid lump sums)
                    with_extra = PrepaymentCalculator.calculate_with_extra_payments(
                        prep_loan_amount,
                        prep_rate_decimal,
                        prep_total_months,
                        extra_monthly=extra_monthly_payment,
                        lump_sums=valid_lump_sums,
                        is_arm=prep_is_arm,
                        arm_fixed_months=prep_arm_fixed_months,
                        adjustable_rate=prep_adj_rate_decimal,
                        extra_only_during_arm=extra_only_during_arm,
                        extra_start_month=final_start_month,
                        extra_stop_month=final_stop_month
                    )
                
                # Summary metrics
                st.subheader("📊 Savings Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                
                interest_saved = regular['total_interest'] - with_extra['total_interest']
                months_saved = regular['months_to_payoff'] - with_extra['months_to_payoff']
                years_saved = months_saved / 12
                
                with col1:
                    st.metric(
                        "Interest Saved",
                        format_currency(interest_saved),
                        delta=f"{(interest_saved/regular['total_interest'])*100:.1f}%",
                        help="Total interest saved by making extra payments"
                    )
                
                with col2:
                    st.metric(
                        "Time Saved",
                        f"{months_saved:.0f} months",
                        delta=f"{years_saved:.1f} years",
                        help="Loan paid off earlier"
                    )
                
                with col3:
                    st.metric(
                        "Regular Payoff",
                        f"{regular['months_to_payoff']:.0f} months",
                        help="Time to pay off with regular payments"
                    )
                
                with col4:
                    st.metric(
                        "With Extra Payments",
                        f"{with_extra['months_to_payoff']:.0f} months",
                        help="Time to pay off with extra payments"
                    )
                
                st.markdown("---")
                
                # Detailed comparison tabs
                tab1, tab2, tab3 = st.tabs(["📋 Comparison", "📊 Regular Schedule", "⚡ With Extra Payments"])
                
                with tab1:
                    st.subheader("Side-by-Side Comparison")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Regular Payment Schedule**")
                        if prep_is_arm:
                            st.write(f"Loan Type: {int(prep_arm_fixed_years)}/{int(prep_loan_term_years-prep_arm_fixed_years)} ARM")
                            st.write(f"ARM Rate: {prep_arm_rate:.3f}% (Years 1-{int(prep_arm_fixed_years)})")
                            st.write(f"Adjustable Rate: {prep_adjustable_rate:.3f}% (Years {int(prep_arm_fixed_years)+1}-{int(prep_loan_term_years)})")
                        else:
                            st.write(f"Loan Type: Fixed Rate")
                            st.write(f"Interest Rate: {prep_interest_rate:.3f}%")
                        st.write(f"Monthly Payment: {format_currency(regular['regular_payment'])}")
                        st.write(f"Months to Payoff: {regular['months_to_payoff']:.0f} ({regular['months_to_payoff']/12:.1f} years)")
                        st.write(f"Total Paid: {format_currency(regular['total_paid'])}")
                        st.write(f"Total Interest: {format_currency(regular['total_interest'])}")
                        if prep_is_arm:
                            st.write(f"  - ARM Period: {format_currency(regular['total_interest_arm_period'])}")
                            st.write(f"  - Adjustable Period: {format_currency(regular['total_interest_adjustable'])}")
                        st.write(f"Total Principal: {format_currency(regular['total_principal'])}")
                    
                    with col2:
                        st.markdown("**With Extra Payments**")
                        st.write(f"Base Monthly Payment: {format_currency(with_extra['regular_payment'])}")
                        if extra_monthly_payment > 0:
                            st.write(f"+ Extra Monthly: {format_currency(extra_monthly_payment)}")
                            if apply_extra_entire_term == "Custom date range":
                                st.caption(f"(Applied from month {final_start_month} to {final_stop_month})")
                            elif extra_only_during_arm and prep_is_arm:
                                st.caption(f"(Applied only during ARM fixed period: Months 1-{prep_arm_fixed_months})")
                            else:
                                st.caption("(Applied throughout loan term)")
                        st.write(f"Months to Payoff: {with_extra['months_to_payoff']:.0f} ({with_extra['months_to_payoff']/12:.1f} years)")
                        
                        # Show if paid off before adjustable period
                        if prep_is_arm and with_extra['months_to_payoff'] <= prep_arm_fixed_months:
                            st.success(f"✅ Paid off during ARM fixed period! (Avoided adjustable rate entirely)")
                        
                        st.write(f"Total Paid: {format_currency(with_extra['total_paid'])}")
                        st.write(f"Total Interest: {format_currency(with_extra['total_interest'])}")
                        if prep_is_arm:
                            st.write(f"  - ARM Period: {format_currency(with_extra['total_interest_arm_period'])}")
                            st.write(f"  - Adjustable Period: {format_currency(with_extra['total_interest_adjustable'])}")
                            adjustable_saved = regular['total_interest_adjustable'] - with_extra['total_interest_adjustable']
                            if adjustable_saved > 0:
                                st.info(f"💡 Avoided {format_currency(adjustable_saved)} in adjustable period interest!")
                        st.write(f"Total Extra Payments: {format_currency(with_extra['total_extra_payments'])}")
                    
                    st.markdown("---")
                    
                    # Savings breakdown
                    st.subheader("💰 Savings Breakdown")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Interest Savings", format_currency(interest_saved))
                    
                    with col2:
                        st.metric("Time Savings", f"{months_saved:.0f} months ({years_saved:.1f} years)")
                    
                    with col3:
                        roi = (interest_saved / with_extra['total_extra_payments'] * 100) if with_extra['total_extra_payments'] > 0 else 0
                        st.metric("ROI on Extra Payments", f"{roi:.1f}%")
                    
                    # Lump sum summary
                    if valid_lump_sums:
                        st.markdown("---")
                        st.subheader("Lump Sum Payments")
                        
                        lump_data = []
                        total_lump = 0
                        for month, amount in sorted(valid_lump_sums):
                            years = month / 12
                            lump_data.append({
                                "Month": month,
                                "Year": f"{years:.1f}",
                                "Amount": format_currency(amount)
                            })
                            total_lump += amount
                        
                        st.table(lump_data)
                        st.write(f"**Total Lump Sum Payments:** {format_currency(total_lump)}")
                
                with tab2:
                    st.subheader(f"Regular Payment Schedule (All {regular['months_to_payoff']:.0f} Months)")
                    
                    schedule_data = []
                    for entry in regular['schedule']:
                        row = {
                            "Month": entry['month'],
                            "Payment": format_currency(entry['payment']),
                            "Principal": format_currency(entry['principal']),
                            "Interest": format_currency(entry['interest']),
                            "Balance": format_currency(entry['balance'])
                        }
                        if prep_is_arm:
                            row["Period"] = entry['period']
                        schedule_data.append(row)
                    
                    st.dataframe(schedule_data, use_container_width=True, height=600)
                
                with tab3:
                    st.subheader(f"Payment Schedule with Extra Payments (All {with_extra['months_to_payoff']:.0f} Months)")
                    
                    schedule_data = []
                    for entry in with_extra['schedule']:
                        row = {
                            "Month": entry['month'],
                            "Payment": format_currency(entry['payment']),
                            "Principal": format_currency(entry['principal']),
                            "Interest": format_currency(entry['interest']),
                            "Extra": format_currency(entry['extra_payment']),
                            "Balance": format_currency(entry['balance'])
                        }
                        if prep_is_arm:
                            row["Period"] = entry['period']
                        schedule_data.append(row)
                    
                    st.dataframe(schedule_data, use_container_width=True, height=600)
                
                st.markdown("---")
                
                # Additional insights
                with st.expander("💡 Key Insights"):
                    # Build extra payment period description
                    if apply_extra_entire_term == "Custom date range":
                        extra_period_desc = f"months {final_start_month} to {final_stop_month} ({final_stop_month - final_start_month + 1} months / {(final_stop_month - final_start_month + 1)/12:.1f} years)"
                    elif extra_only_during_arm and prep_is_arm:
                        extra_period_desc = f"months 1 to {prep_arm_fixed_months} (ARM fixed period only)"
                    else:
                        extra_period_desc = "throughout entire loan term"
                    
                    st.markdown(f"""
                    ### Analysis Results
                    
                    **Your Extra Payments:**
                    - Extra Monthly Payment: {format_currency(extra_monthly_payment)}
                    - Payment Period: {extra_period_desc}
                    - Number of Lump Sums: {len(valid_lump_sums)}
                    - Total Extra Payments: {format_currency(with_extra['total_extra_payments'])}
                    
                    **Savings:**
                    - **Interest Saved: {format_currency(interest_saved)}** ({(interest_saved/regular['total_interest'])*100:.1f}% reduction)
                    - **Time Saved: {months_saved:.0f} months** ({years_saved:.1f} years)
                    - **Payoff Date: {with_extra['months_to_payoff']/12:.1f} years** instead of {regular['months_to_payoff']/12:.1f} years
                    
                    **Return on Investment:**
                    - For every extra dollar paid towards principal, you save ${interest_saved/with_extra['total_extra_payments'] if with_extra['total_extra_payments'] > 0 else 0:.2f} in interest
                    - Effective ROI: {roi:.1f}%
                    
                    {'**ARM Loan Benefit:**' if prep_is_arm else ''}
                    {f'- Paid off in {with_extra["months_to_payoff"]:.0f} months ({with_extra["months_to_payoff"]/12:.1f} years)' if prep_is_arm else ''}
                    {f'- {"✅ Completely avoided adjustable period!" if with_extra["months_to_payoff"] <= prep_arm_fixed_months else f"Reduced adjustable period exposure by {months_saved:.0f} months"}' if prep_is_arm else ''}
                    
                    **Recommendation:**
                    {'✅ Excellent strategy! Your extra payments will save significant interest.' if interest_saved > with_extra['total_extra_payments'] * 0.2 else '⚠️ Consider if the savings justify the extra payments based on your financial goals.'}
                    """)
        
        else:
            st.info("👈 Configure your extra payment options in the sidebar and click 'Calculate Savings' to see results.")


if __name__ == "__main__":
    main()
