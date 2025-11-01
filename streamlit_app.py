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
        """Calculate total cost of original ARM loan (7/6 pattern)"""
        
        # Phase 1: First 7 years at initial rate
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
        
        # Phase 2: Remaining years at capped rate
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
    st.markdown("---")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Loan Parameters")
        
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
        
        # Calculate default value for slider, ensuring it doesn't exceed max
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
            
            1. **Full 30-Year Comparison (Default)**
               - Compares total cost over entire 360-month loan term
               - Includes both ARM period and adjustable rate period
               - Best when planning to keep the loan for the full term
            
            2. **ARM Periods Only**
               - Compares ONLY the ARM fixed-rate periods
               - Excludes adjustable rate periods (years 8-30)
               - Focuses on interest paid + refinance costs only
               - Best when planning to sell or refinance again in 5-7 years
            
            3. **Custom Adjustable Rate**
               - Use a specific rate for years 8-30 in BOTH scenarios
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
                help="Total amount paid over 30 years with original loan"
            )
        
        with col2:
            st.metric(
                "Refinanced Loan Total",
                format_currency(refinance['total_paid']),
                delta=format_currency(-savings) if savings > 0 else format_currency(abs(savings)),
                delta_color="normal" if savings > 0 else "inverse",
                help="Total amount paid over 30 years with refinancing"
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
        
        # Detailed comparison
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
                    st.markdown("**Original Loan (ARM Period - Months 1-84)**")
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
                st.subheader("Full 30-Year Comparison")
                
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
                st.write(f"Initial Rate (Years 1-7): {format_percentage(current_arm_rate_dec)}")
                if use_custom_adjustable_rate:
                    st.write(f"Custom Rate (Years 8-30): {format_percentage(original_adjustable_rate)} (User-specified)")
                else:
                    st.write(f"Capped Rate (Years 8-30): {format_percentage(original_adjustable_rate)}")
            
            with col2:
                st.markdown("**Monthly Payments**")
                st.write(f"Years 1-7: {format_currency(original['monthly_payment_phase1'])}")
                st.write(f"Years 8-30: {format_currency(original['monthly_payment_phase2'])}")
            
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
                st.markdown(f"**ARM Period (Months 1-{first_period_months}, Years 1-7)**")
                st.write(f"Interest Paid: {format_currency(original['total_paid_phase1'] - original['principal_paid_phase1'])}")
                st.write(f"Principal Paid: {format_currency(original['principal_paid_phase1'])}")
            
            with col2:
                st.markdown(f"**Adjustable Period (Months {first_period_months+1}-{full_term_months}, Years 8-30)**")
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
                    st.write(f"Custom Rate (Years 8-30): {format_percentage(new_adjustable_rate)} (User-specified)")
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
                new_phase2_end_month = months_before_refi + full_term_months  # New loan runs for full term
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
                    st.warning(f"Why breakeven ({format_percentage(breakeven_rate)}) > current rate ({format_percentage(current_arm_rate_dec)})? Refinancing resets you to a new 7-year fixed period, allowing you to avoid the high cap rate ({format_percentage(original_adjustable_rate)}) sooner, even at a higher rate.")
                
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
                st.info("💡 ARM-only breakeven rate is shown in the Comparison tab. (Full 30-year breakeven analysis is not shown in ARM-only mode)")
                
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


if __name__ == "__main__":
    main()

