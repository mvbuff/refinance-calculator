#!/home/utils/Python/builds/3.11.9-20250401/bin/python3.11
"""
ARM Refinance Cost Calculator - GUI Version
Interactive graphical interface for comparing ARM refinance scenarios
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading


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
        remaining_months = total_months - refi_month
        
        # Step 3: New loan Phase 1
        new_phase1_months = min(first_period_months, remaining_months)
        monthly_new_phase1 = ARMCalculator.monthly_payment(new_loan_amount, new_rate, remaining_months)
        
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
        if remaining_months > new_phase1_months:
            new_phase2_months = remaining_months - new_phase1_months
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


class ARMCalculatorGUI:
    """GUI interface for ARM Refinance Calculator"""
    
    def __init__(self, root, initial_values=None):
        self.root = root
        self.root.title("ARM Refinance Calculator")
        self.root.geometry("1200x900")
        
        # Default values
        defaults = {
            'loan_amount': 1288000,
            'current_arm_rate': 4.875,
            'months_before_refi': 24,
            'new_arm_rate': 4.0,
            'refi_cost': 2000
        }
        
        # Use initial values if provided, otherwise use defaults
        if initial_values:
            defaults.update(initial_values)
        
        self.create_widgets(defaults)
    
    def create_widgets(self, defaults):
        """Create all GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="ARM Refinance Cost Calculator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text="Loan Parameters", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        row = 0
        
        # Loan Amount
        ttk.Label(input_frame, text="Loan Amount ($):").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.loan_amount = tk.StringVar(value=str(defaults['loan_amount']))
        ttk.Entry(input_frame, textvariable=self.loan_amount, width=20).grid(row=row, column=1, sticky=tk.W, padx=5)
        ttk.Label(input_frame, text="e.g., 1288000", foreground="gray").grid(row=row, column=2, sticky=tk.W)
        row += 1
        
        # Current ARM Rate
        ttk.Label(input_frame, text="Current ARM Rate (%):").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.current_arm_rate = tk.StringVar(value=str(defaults['current_arm_rate']))
        ttk.Entry(input_frame, textvariable=self.current_arm_rate, width=20).grid(row=row, column=1, sticky=tk.W, padx=5)
        ttk.Label(input_frame, text="e.g., 4.875", foreground="gray").grid(row=row, column=2, sticky=tk.W)
        row += 1
        
        # New ARM Rate
        ttk.Label(input_frame, text="New ARM Rate (%):").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.new_arm_rate = tk.StringVar(value=str(defaults['new_arm_rate']))
        ttk.Entry(input_frame, textvariable=self.new_arm_rate, width=20).grid(row=row, column=1, sticky=tk.W, padx=5)
        ttk.Label(input_frame, text="e.g., 4.0", foreground="gray").grid(row=row, column=2, sticky=tk.W)
        row += 1
        
        # Months Before Refi
        ttk.Label(input_frame, text="Refinance After (months):").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.months_before_refi = tk.StringVar(value=str(defaults['months_before_refi']))
        ttk.Entry(input_frame, textvariable=self.months_before_refi, width=20).grid(row=row, column=1, sticky=tk.W, padx=5)
        ttk.Label(input_frame, text="e.g., 24 (2 years)", foreground="gray").grid(row=row, column=2, sticky=tk.W)
        row += 1
        
        # Refi Cost
        ttk.Label(input_frame, text="Refinance Cost ($):").grid(row=row, column=0, sticky=tk.W, pady=3)
        self.refi_cost = tk.StringVar(value=str(defaults['refi_cost']))
        ttk.Entry(input_frame, textvariable=self.refi_cost, width=20).grid(row=row, column=1, sticky=tk.W, padx=5)
        ttk.Label(input_frame, text="e.g., 2000", foreground="gray").grid(row=row, column=2, sticky=tk.W)
        row += 1
        
        # Comparison Mode
        row += 1  # Add some spacing
        self.compare_arm_only = tk.BooleanVar(value=defaults.get('compare_arm_only', False))
        ttk.Checkbutton(input_frame, text="Compare ARM periods only (exclude adjustable rate periods)", 
                       variable=self.compare_arm_only).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        ttk.Label(input_frame, text="ℹ️  Useful if you plan to refinance or sell before the adjustable period starts", 
                 foreground="blue", font=('Arial', 9, 'italic')).grid(row=row, column=0, columnspan=3, sticky=tk.W, padx=20)
        row += 1
        
        # Custom Adjustable Rate
        row += 1  # Add some spacing
        self.use_custom_adjustable_rate = tk.BooleanVar(value=defaults.get('use_custom_adjustable_rate', False))
        ttk.Checkbutton(input_frame, text="Use custom rate for adjustable period (Years 8-30) in both scenarios", 
                       variable=self.use_custom_adjustable_rate).grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(input_frame, text="Custom Adjustable Rate (%):").grid(row=row, column=0, sticky=tk.W, pady=3, padx=20)
        self.custom_adjustable_rate = tk.StringVar(value=str(defaults.get('custom_adjustable_rate', 4.5)))
        ttk.Entry(input_frame, textvariable=self.custom_adjustable_rate, width=20).grid(row=row, column=1, sticky=tk.W, padx=5)
        ttk.Label(input_frame, text="e.g., 4.5 (if planning to refi at year 7)", foreground="gray").grid(row=row, column=2, sticky=tk.W)
        row += 1
        ttk.Label(input_frame, text="ℹ️  Uses this rate instead of cap rates for years 8-30 in BOTH scenarios", 
                 foreground="blue", font=('Arial', 9, 'italic')).grid(row=row, column=0, columnspan=3, sticky=tk.W, padx=20)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="New Window", command=self.open_new_window).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Clear Results", command=self.clear_results).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Help", command=self.show_help).grid(row=0, column=3, padx=5)
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(3, weight=1)
        
        # Scrolled text for results
        self.results_text = scrolledtext.ScrolledText(results_frame, width=110, height=32, 
                                                       font=('Courier', 12), wrap=tk.WORD)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def get_current_values(self):
        """Get current input values as a dictionary"""
        try:
            return {
                'loan_amount': float(self.loan_amount.get()),
                'current_arm_rate': float(self.current_arm_rate.get()),
                'new_arm_rate': float(self.new_arm_rate.get()),
                'months_before_refi': int(self.months_before_refi.get()),
                'refi_cost': float(self.refi_cost.get()),
                'compare_arm_only': self.compare_arm_only.get(),
                'use_custom_adjustable_rate': self.use_custom_adjustable_rate.get(),
                'custom_adjustable_rate': float(self.custom_adjustable_rate.get())
            }
        except ValueError as e:
            raise ValueError(f"Invalid input values: {e}")
    
    def validate_inputs(self):
        """Validate all input values"""
        try:
            values = self.get_current_values()
            
            if values['loan_amount'] <= 0:
                raise ValueError("Loan amount must be positive")
            if values['current_arm_rate'] <= 0 or values['current_arm_rate'] >= 100:
                raise ValueError("Current ARM rate must be between 0 and 100")
            if values['new_arm_rate'] <= 0 or values['new_arm_rate'] >= 100:
                raise ValueError("New ARM rate must be between 0 and 100")
            if values['months_before_refi'] <= 0 or values['months_before_refi'] >= 360:
                raise ValueError("Refinance timing must be between 1 and 359 months")
            if values['refi_cost'] < 0:
                raise ValueError("Refinance cost cannot be negative")
            if values['custom_adjustable_rate'] <= 0 or values['custom_adjustable_rate'] >= 100:
                raise ValueError("Custom adjustable rate must be between 0 and 100")
            
            return True
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return False
    
    def calculate(self):
        """Perform calculations and display results"""
        if not self.validate_inputs():
            return
        
        self.status_var.set("Calculating...")
        self.root.update()
        
        # Run calculation in separate thread to keep GUI responsive
        thread = threading.Thread(target=self._perform_calculation)
        thread.daemon = True
        thread.start()
    
    def _perform_calculation(self):
        """Actual calculation logic (runs in separate thread)"""
        try:
            values = self.get_current_values()
            
            # Convert percentages to decimals
            loan_amount = values['loan_amount']
            current_arm_rate = values['current_arm_rate'] / 100
            current_max_cap = current_arm_rate + 0.05
            new_arm_rate = values['new_arm_rate'] / 100
            new_max_cap = new_arm_rate + 0.05
            months_before_refi = values['months_before_refi']
            refi_cost = values['refi_cost']
            use_custom_adjustable_rate = values['use_custom_adjustable_rate']
            custom_adjustable_rate = values['custom_adjustable_rate'] / 100
            
            full_term_months = 360
            first_period_months = 84
            
            # Determine which rates to use for adjustable period
            if use_custom_adjustable_rate:
                original_adjustable_rate = custom_adjustable_rate
                new_adjustable_rate = custom_adjustable_rate
            else:
                original_adjustable_rate = current_max_cap
                new_adjustable_rate = new_max_cap
            
            # Calculate scenarios
            original = ARMCalculator.calculate_original_loan(
                loan_amount, current_arm_rate, original_adjustable_rate,
                first_period_months, full_term_months
            )
            
            refinance = ARMCalculator.calculate_refinance_scenario(
                loan_amount, current_arm_rate, original_adjustable_rate,
                new_arm_rate, new_adjustable_rate, months_before_refi, refi_cost,
                first_period_months, full_term_months
            )
            
            breakeven_rate = ARMCalculator.find_breakeven_rate(
                loan_amount, current_arm_rate, original_adjustable_rate,
                original['total_paid'], months_before_refi, refi_cost,
                first_period_months, full_term_months
            )
            
            # Format output
            output = self._format_results(
                loan_amount, current_arm_rate, original_adjustable_rate,
                new_arm_rate, new_adjustable_rate, months_before_refi, refi_cost,
                first_period_months, full_term_months,
                original, refinance, breakeven_rate, values['compare_arm_only'],
                use_custom_adjustable_rate
            )
            
            # Update GUI in main thread
            self.root.after(0, self._update_results, output)
            self.root.after(0, self.status_var.set, "Calculation complete")
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Calculation Error", str(e))
            self.root.after(0, self.status_var.set, "Error occurred")
    
    def _format_results(self, loan_amount, current_arm_rate, original_adjustable_rate,
                       new_arm_rate, new_adjustable_rate, months_before_refi, refi_cost,
                       first_period_months, full_term_months,
                       original, refinance, breakeven_rate, compare_arm_only=False,
                       use_custom_adjustable_rate=False):
        """Format calculation results as text"""
        
        output = []
        output.append("=" * 100)
        output.append("ARM REFINANCE COST CALCULATOR - RESULTS")
        output.append("=" * 100)
        output.append("")
        
        output.append("LOAN DETAILS:")
        output.append(f"  Original Loan Amount:        ${loan_amount:,.2f}")
        output.append(f"  Term:                        {full_term_months} months ({full_term_months//12} years)")
        output.append(f"  Fixed Rate Period:           {first_period_months} months ({first_period_months//12} years)")
        output.append("")
        
        output.append("-" * 100)
        output.append("SCENARIO 1: KEEP ORIGINAL LOAN")
        output.append("-" * 100)
        output.append(f"  Initial Rate (Years 1-7):    {current_arm_rate*100:.3f}%")
        if use_custom_adjustable_rate:
            output.append(f"  Custom Rate (Years 8-30):    {original_adjustable_rate*100:.3f}% (User-specified)")
        else:
            output.append(f"  Capped Rate (Years 8-30):    {original_adjustable_rate*100:.3f}%")
        output.append(f"  Monthly Payment (Years 1-7): ${original['monthly_payment_phase1']:,.2f}")
        output.append(f"  Monthly Payment (Years 8-30):${original['monthly_payment_phase2']:,.2f}")
        output.append("")
        output.append(f"  Total Amount Paid:           ${original['total_paid']:,.2f}")
        output.append(f"  Total Interest Paid:         ${original['total_interest']:,.2f}")
        output.append(f"  Total Principal Paid:        ${original['total_principal']:,.2f}")
        output.append("")
        output.append("  INTEREST BREAKDOWN BY PERIOD:")
        output.append(f"    ARM Period (Months 1-{first_period_months}, Years 1-7):")
        output.append(f"      Interest Paid:           ${original['total_paid_phase1'] - original['principal_paid_phase1']:,.2f}")
        output.append(f"      Principal Paid:          ${original['principal_paid_phase1']:,.2f}")
        output.append(f"    Adjustable Period (Months {first_period_months+1}-{full_term_months}, Years 8-30):")
        output.append(f"      Interest Paid:           ${original['total_paid_phase2'] - original['principal_paid_phase2']:,.2f}")
        output.append(f"      Principal Paid:          ${original['principal_paid_phase2']:,.2f}")
        output.append("")
        
        output.append("-" * 100)
        output.append(f"SCENARIO 2: REFINANCE AFTER {months_before_refi} MONTHS ({months_before_refi/12:.1f} years)")
        output.append("-" * 100)
        output.append(f"  Refinance Cost:              ${refi_cost:,.2f}")
        output.append("")
        output.append("  BEFORE REFINANCE:")
        output.append(f"    Monthly Payment:           ${refinance['monthly_before_refi']:,.2f}")
        output.append(f"    Total Paid (Months 1-{months_before_refi}):  ${refinance['total_paid_before_refi']:,.2f}")
        output.append(f"    Interest Paid:             ${refinance['interest_before_refi']:,.2f}")
        output.append(f"    Principal Paid:            ${refinance['principal_before_refi']:,.2f}")
        output.append(f"    Remaining Balance:         ${refinance['balance_at_refi']:,.2f}")
        output.append("")
        output.append("  AFTER REFINANCE:")
        output.append(f"    New Loan Amount:           ${refinance['new_loan_amount']:,.2f}")
        output.append(f"    Refinance Cost (paid out of pocket): ${refinance['refi_cost']:,.2f}")
        output.append(f"    New Initial Rate:          {new_arm_rate*100:.3f}%")
        if use_custom_adjustable_rate:
            output.append(f"    Custom Rate (Years 8-30):  {new_adjustable_rate*100:.3f}% (User-specified)")
        else:
            output.append(f"    New Capped Rate:           {new_adjustable_rate*100:.3f}%")
        output.append(f"    Monthly Payment (Phase 1): ${refinance['monthly_new_phase1']:,.2f}")
        if refinance['monthly_new_phase2'] > 0:
            output.append(f"    Monthly Payment (Phase 2): ${refinance['monthly_new_phase2']:,.2f}")
        output.append("")
        output.append("  TOTAL REFINANCE SCENARIO:")
        output.append(f"    Loan Payments:             ${refinance['total_paid'] - refinance['refi_cost']:,.2f}")
        output.append(f"    Refinance Cost:            ${refinance['refi_cost']:,.2f}")
        output.append(f"    Total Amount Paid:         ${refinance['total_paid']:,.2f}")
        output.append(f"    Total Interest Paid:       ${refinance['total_interest']:,.2f}")
        output.append("")
        output.append("  INTEREST BREAKDOWN BY PERIOD:")
        output.append(f"    Original Loan (Months 1-{months_before_refi}):")
        output.append(f"      Interest Paid:           ${refinance['interest_before_refi']:,.2f}")
        output.append(f"      Principal Paid:          ${refinance['principal_before_refi']:,.2f}")
        
        new_loan_start_month = months_before_refi + 1
        new_phase1_end_month = months_before_refi + refinance['new_phase1_months']
        output.append(f"    New ARM Period (Months {new_loan_start_month}-{new_phase1_end_month}):")
        output.append(f"      Interest Paid:           ${refinance['interest_new_phase1']:,.2f}")
        output.append(f"      Principal Paid:          ${refinance['principal_new_phase1']:,.2f}")
        
        if refinance['new_phase2_months'] > 0:
            new_phase2_start_month = new_phase1_end_month + 1
            output.append(f"    New Adjustable Period (Months {new_phase2_start_month}-{full_term_months}):")
            output.append(f"      Interest Paid:           ${refinance['interest_new_phase2']:,.2f}")
            output.append(f"      Principal Paid:          ${refinance['principal_new_phase2']:,.2f}")
        output.append("")
        
        output.append("=" * 100)
        output.append("COMPARISON")
        output.append("=" * 100)
        
        if compare_arm_only:
            output.append("MODE: ARM PERIODS ONLY - Interest & Refinance Costs Comparison")
            output.append("-" * 100)
            output.append("")
            output.append("  NOTE: Principal payments are the same in both scenarios.")
            output.append("        This comparison focuses only on INTEREST and REFINANCE COSTS.")
            output.append("")
            
            # Original loan ARM interest: Interest during first 84 months
            original_arm_interest = original['total_paid_phase1'] - original['principal_paid_phase1']
            
            # Refinance ARM interest: Interest before refi + interest during new ARM period + refi cost
            refi_arm_interest = refinance['interest_before_refi'] + refinance['interest_new_phase1']
            refi_arm_total_cost = refi_arm_interest + refinance['refi_cost']
            
            output.append("  ORIGINAL LOAN (ARM Period - Months 1-84):")
            output.append(f"    Interest Paid:               ${original_arm_interest:,.2f}")
            output.append(f"    Refinance Cost:              $0.00")
            output.append(f"    Total Cost (Interest only):  ${original_arm_interest:,.2f}")
            output.append("")
            
            output.append(f"  REFINANCE SCENARIO (ARM Periods - Months 1-{months_before_refi + refinance['new_phase1_months']}):")
            output.append(f"    Before Refi (Months 1-{months_before_refi}):")
            output.append(f"      Interest Paid:             ${refinance['interest_before_refi']:,.2f}")
            output.append(f"    New ARM Period (Months {months_before_refi+1}-{months_before_refi + refinance['new_phase1_months']}):")
            output.append(f"      Interest Paid:             ${refinance['interest_new_phase1']:,.2f}")
            output.append(f"    Combined ARM Interest:       ${refi_arm_interest:,.2f}")
            output.append(f"    Refinance Cost:              ${refinance['refi_cost']:,.2f}")
            output.append(f"    Total Cost (Interest + Refi): ${refi_arm_total_cost:,.2f}")
            output.append("")
            
            # Calculate ARM-only breakeven rate
            breakeven_rate_arm = ARMCalculator.find_breakeven_rate_arm_only(
                loan_amount, current_arm_rate, original_arm_interest,
                months_before_refi, refi_cost, first_period_months, full_term_months
            )
            
            arm_cost_diff = refi_arm_total_cost - original_arm_interest
            if arm_cost_diff < 0:
                output.append(f"  ARM PERIOD SAVINGS:          ${abs(arm_cost_diff):,.2f}")
                output.append(f"  Percentage saved:            {(abs(arm_cost_diff)/original_arm_interest)*100:.2f}%")
                output.append(f"  ✓ Refinancing saves money during ARM periods")
            else:
                output.append(f"  ARM PERIOD ADDITIONAL COST:  ${arm_cost_diff:,.2f}")
                output.append(f"  Percentage increase:         {(arm_cost_diff/original_arm_interest)*100:.2f}%")
                output.append(f"  ✗ Refinancing costs more during ARM periods")
            
            output.append("")
            output.append(f"  Original ARM interest cost:  ${original_arm_interest:,.2f}")
            output.append(f"  Refinanced total ARM cost:   ${refi_arm_total_cost:,.2f}")
            output.append("")
            output.append("  BREAKEVEN RATE FOR ARM PERIODS ONLY:")
            output.append(f"    Current ARM rate:            {current_arm_rate*100:.3f}%")
            output.append(f"    Your new ARM rate:           {new_arm_rate*100:.3f}%")
            output.append(f"    Breakeven ARM rate:          {breakeven_rate_arm*100:.3f}%")
            output.append("")
            if new_arm_rate < breakeven_rate_arm:
                output.append(f"    ✓ Your rate ({new_arm_rate*100:.3f}%) < Breakeven ({breakeven_rate_arm*100:.3f}%)")
                output.append(f"      → Saves ${abs(arm_cost_diff):,.2f} during ARM periods")
            elif new_arm_rate > breakeven_rate_arm:
                output.append(f"    ✗ Your rate ({new_arm_rate*100:.3f}%) > Breakeven ({breakeven_rate_arm*100:.3f}%)")
                output.append(f"      → Costs ${arm_cost_diff:,.2f} more during ARM periods")
            else:
                output.append(f"    = Your rate ({new_arm_rate*100:.3f}%) = Breakeven ({breakeven_rate_arm*100:.3f}%)")
                output.append(f"      → Neutral during ARM periods")
            output.append("")
            output.append("  INTERPRETATION:")
            output.append("  - This comparison excludes adjustable rate periods (months 85-360)")
            output.append("  - Useful if you plan to refinance again or sell before rates adjust")
            output.append("  - Principal payments are identical in both scenarios, so they're excluded")
            output.append(f"  - Any new rate below {breakeven_rate_arm*100:.3f}% saves money during ARM periods")
            
            # Set savings for use in later sections (use full 30-year for breakeven analysis)
            savings = original['total_paid'] - refinance['total_paid']
        else:
            output.append("MODE: FULL 30-YEAR COMPARISON (Including All Periods)")
            output.append("-" * 100)
            output.append("")
            
            savings = original['total_paid'] - refinance['total_paid']
            if savings > 0:
                output.append(f"  SAVINGS from refinancing:    ${savings:,.2f}")
                output.append(f"  Percentage saved:            {(savings/original['total_paid'])*100:.2f}%")
            else:
                output.append(f"  ADDITIONAL COST from refi:   ${abs(savings):,.2f}")
                output.append(f"  Percentage increase:         {(abs(savings)/original['total_paid'])*100:.2f}%")
            
            output.append("")
            output.append(f"  Original loan total:         ${original['total_paid']:,.2f}")
            output.append(f"  Refinanced loan total:       ${refinance['total_paid']:,.2f}")
        
        output.append("=" * 100)
        output.append("")
        
        output.append("ADDITIONAL INSIGHTS:")
        output.append("-" * 100)
        
        # Only show full 30-year breakeven analysis if NOT in ARM-only mode
        if not compare_arm_only:
            # Breakeven rate analysis (Full 30-year)
            output.append(f"  BREAKEVEN RATE ANALYSIS (refinancing at month {months_before_refi}):")
            output.append(f"    Current ARM rate:            {current_arm_rate*100:.3f}%")
            if use_custom_adjustable_rate:
                output.append(f"    Custom adjustable rate:      {original_adjustable_rate*100:.3f}%")
            else:
                output.append(f"    Current cap rate:            {original_adjustable_rate*100:.3f}%")
            output.append(f"    Breakeven NEW ARM rate:      {breakeven_rate*100:.3f}%")
            output.append(f"    Breakeven NEW cap rate:      {(breakeven_rate + 0.05)*100:.3f}%")
            output.append("")
            output.append(f"    What this means: Refinancing at any NEW rate below {breakeven_rate*100:.3f}% saves money")
            output.append(f"                     compared to keeping your current {current_arm_rate*100:.3f}% ARM.")
            output.append("")
            
            if breakeven_rate > current_arm_rate and not use_custom_adjustable_rate:
                output.append(f"    💡 Why breakeven ({breakeven_rate*100:.3f}%) > current rate ({current_arm_rate*100:.3f}%):")
                output.append(f"       Refinancing resets you to a new 7-year fixed period, allowing you to")
                output.append(f"       avoid the high cap rate ({original_adjustable_rate*100:.3f}%) sooner, even at a higher rate.")
            output.append("")
            
            if new_arm_rate < breakeven_rate:
                rate_advantage = breakeven_rate - new_arm_rate
                output.append(f"    ✓ Your new rate ({new_arm_rate*100:.3f}%) is {rate_advantage*100:.3f}% BELOW breakeven")
                output.append(f"      → Refinancing is BENEFICIAL")
            elif new_arm_rate > breakeven_rate:
                rate_disadvantage = new_arm_rate - breakeven_rate
                output.append(f"    ✗ Your new rate ({new_arm_rate*100:.3f}%) is {rate_disadvantage*100:.3f}% ABOVE breakeven")
                output.append(f"      → Refinancing is NOT beneficial")
            else:
                output.append(f"    = Your new rate ({new_arm_rate*100:.3f}%) equals breakeven")
                output.append(f"      → Neutral (no financial advantage)")
            
            output.append("")
        else:
            # In ARM-only mode, the breakeven was already shown in the comparison section
            output.append(f"  NOTE: ARM-only breakeven rate is shown in the COMPARISON section above.")
            output.append(f"        (Full 30-year breakeven analysis is not shown in ARM-only mode)")
            output.append("")
        
        if savings > 0:
            if refinance['monthly_new_phase1'] < original['monthly_payment_phase1']:
                monthly_savings = original['monthly_payment_phase1'] - refinance['monthly_new_phase1']
                months_to_breakeven = refi_cost / monthly_savings
                output.append(f"  Monthly payment savings:     ${monthly_savings:,.2f} (during new fixed period)")
                output.append(f"  Months to break even:        {months_to_breakeven:.1f} months ({months_to_breakeven/12:.1f} years)")
        
        # Breakeven rates for different timing scenarios
        if not compare_arm_only:
            output.append("")
            output.append("-" * 100)
            output.append("  BREAKEVEN RATES FOR DIFFERENT REFINANCE TIMINGS:")
            output.append(f"  (With refi cost of ${refi_cost:,.2f})")
            output.append("")
            output.append("    Month  Years   Breakeven Rate    Your Rate    Decision")
            output.append("    " + "-" * 76)
            
            timing_scenarios = [12, 24, 36, 48, 60, 72]
            for month in timing_scenarios:
                if month <= first_period_months:
                    be_rate = ARMCalculator.find_breakeven_rate(
                        loan_amount, current_arm_rate, original_adjustable_rate,
                        original['total_paid'], month, refi_cost,
                        first_period_months, full_term_months
                    )
                    decision = "✓ GOOD" if new_arm_rate < be_rate else ("✗ BAD" if new_arm_rate > be_rate else "= NEUTRAL")
                    years = month / 12
                    output.append(f"    {month:5d}  {years:5.1f}       {be_rate*100:5.3f}%        {new_arm_rate*100:5.3f}%      {decision}")
        else:
            # Show ARM-only breakeven rates for different timings
            output.append("")
            output.append("-" * 100)
            output.append("  ARM-ONLY BREAKEVEN RATES FOR DIFFERENT REFINANCE TIMINGS:")
            output.append(f"  (With refi cost of ${refi_cost:,.2f})")
            output.append("")
            output.append("    Month  Years   ARM Breakeven     Your Rate    Decision")
            output.append("    " + "-" * 76)
            
            timing_scenarios = [12, 24, 36, 48, 60, 72]
            for month in timing_scenarios:
                if month <= first_period_months:
                    be_rate_arm = ARMCalculator.find_breakeven_rate_arm_only(
                        loan_amount, current_arm_rate, original['total_paid_phase1'] - original['principal_paid_phase1'],
                        month, refi_cost, first_period_months, full_term_months
                    )
                    decision = "✓ GOOD" if new_arm_rate < be_rate_arm else ("✗ BAD" if new_arm_rate > be_rate_arm else "= NEUTRAL")
                    years = month / 12
                    output.append(f"    {month:5d}  {years:5.1f}       {be_rate_arm*100:5.3f}%        {new_arm_rate*100:5.3f}%      {decision}")
        
        output.append("")
        output.append("=" * 100)
        
        return "\n".join(output)
    
    def _update_results(self, text):
        """Update results text widget (must be called from main thread)"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, text)
    
    def clear_results(self):
        """Clear the results text area"""
        self.results_text.delete(1.0, tk.END)
        self.status_var.set("Results cleared")
    
    def open_new_window(self):
        """Open a new calculator window with current values"""
        try:
            current_values = self.get_current_values()
            new_window = tk.Toplevel(self.root)
            ARMCalculatorGUI(new_window, initial_values=current_values)
            self.status_var.set("New window opened")
        except ValueError as e:
            messagebox.showwarning("Warning", f"Could not copy values: {e}\nOpening window with default values.")
            new_window = tk.Toplevel(self.root)
            ARMCalculatorGUI(new_window)
    
    def show_help(self):
        """Display help information in a new window"""
        help_window = tk.Toplevel(self.root)
        help_window.title("ARM Refinance Calculator - Help")
        help_window.geometry("900x700")
        
        # Create scrolled text for help content
        help_frame = ttk.Frame(help_window, padding="10")
        help_frame.pack(fill=tk.BOTH, expand=True)
        
        help_text = scrolledtext.ScrolledText(help_frame, width=90, height=38, 
                                              font=('Arial', 12), wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True)
        
        # Help content
        help_content = """
ARM REFINANCE CALCULATOR - COMPREHENSIVE HELP GUIDE
==================================================

OVERVIEW
--------
This calculator helps you analyze whether refinancing your Adjustable Rate Mortgage (ARM) 
makes financial sense by comparing total costs over the full loan term or just the ARM periods.

LOAN STRUCTURE: 7/6 ARM
------------------------
• Years 1-7 (84 months): Fixed rate period
• Years 8-30 (276 months): Adjustable rate period
• Default assumption: Adjustable rate = Initial rate + 5% (cap)

INPUT PARAMETERS
---------------

1. Loan Amount ($)
   - Your original mortgage principal
   - Example: 1,288,000

2. Current ARM Rate (%)
   - Your current loan's initial fixed rate for years 1-7
   - Example: 4.875 means 4.875%

3. New ARM Rate (%)
   - The new fixed rate being offered if you refinance
   - Example: 4.0 means 4.0%

4. Refinance After (months)
   - When you plan to refinance
   - Example: 24 = 2 years from now
   - Must be between 1-359 months

5. Refinance Cost ($)
   - One-time closing costs paid out of pocket
   - NOT added to loan principal
   - Example: 2000 = $2,000

COMPARISON MODES
---------------

MODE 1: Full 30-Year Comparison (Default)
==========================================
☐ Compare ARM periods only (unchecked)

What it does:
• Compares total cost over entire 360-month loan term
• Includes both ARM period and adjustable rate period
• Shows total payments, interest, and principal for full 30 years

When to use:
• You plan to keep the loan for the full term
• You want to see lifetime costs
• You care about the long-term financial impact

Breakeven Rate:
• Shows what NEW rate would equal the cost of keeping current loan
• Accounts for the benefit of lower cap rates in years 8-30
• Typically HIGHER than current rate due to cap rate benefits

Example Output:
  Original loan total:  $3,437,013.65
  Refinanced total:     $3,031,346.85
  SAVINGS:              $405,666.80 (11.80%)


MODE 2: ARM Periods Only
=========================
☑ Compare ARM periods only (checked)

What it does:
• Compares ONLY the ARM fixed-rate periods (months 1-84 for original)
• For refinance: months 1-24 on original + months 25-108 on new loan
• Excludes all adjustable rate periods (years 8-30)
• Focuses on interest paid + refinance costs only
• Principal payments are identical, so they're excluded

When to use:
• You plan to sell the property in 5-7 years
• You'll refinance again before year 7-9
• You want to minimize short-term costs
• You only care about ARM period expenses

Breakeven Rate:
• Shows what NEW rate makes ARM periods cost the same
• Typically LOWER than current rate
• Formula: Original ARM interest = Interest before refi + New ARM interest + Refi cost

Example Output:
  Original ARM interest:  $414,392.41
  Refinanced ARM cost:    $449,465.49
  ADDITIONAL COST:        $35,073.09 (8.46%)
  
  Breakeven ARM rate: 3.584%
  Your 4.0% is ABOVE breakeven → costs more during ARM periods

IMPORTANT: ARM-only mode often shows refinancing costs MORE because you're 
extending from 84 to 108 total months at fixed rates!


MODE 3: Custom Adjustable Rate
==============================
☑ Use custom rate for adjustable period (Years 8-30)

What it does:
• Instead of using cap rates (current+5%, new+5%), use a SINGLE custom rate
• This custom rate is used for BOTH scenarios in years 8-30
• Removes the cap rate advantage from comparison
• Useful for modeling specific future refinance plans

When to use:
• You plan to refinance again at year 7 to a specific rate
• You want to test "what if" scenarios with different future rates
• You want to isolate ARM period differences from cap rate differences

Example:
  Custom rate = 4.5%
  
  Original scenario:  4.875% for years 1-7, then 4.5% for years 8-30
  Refinance scenario: 4.0% for years 1-7, then 4.5% for years 8-30
  
  This focuses comparison on the 0.875% difference during ARM periods only.


CALCULATION DETAILS
------------------

Original Loan Cost:
1. Calculate monthly payment based on 4.875% over 360 months
2. Apply that payment for months 1-84 (ARM period)
3. Calculate remaining balance after month 84
4. Recalculate payment for remaining balance at cap rate (9.875%)
5. Apply new payment for months 85-360
6. Sum all payments

Refinance Scenario Cost:
1. Pay original loan for months 1-24 at 4.875%
2. Pay refinance cost ($2,000) out of pocket
3. New loan = remaining balance (NOT balance + refi cost)
4. Calculate new payment based on 4.0% for remaining 336 months
5. Apply that payment for months 25-108 (new ARM period)
6. Calculate remaining balance after month 108
7. Recalculate payment at new cap rate (9.0%)
8. Apply new payment for months 109-360
9. Sum all payments + refi cost

Breakeven Rate (Full 30-Year):
• Uses binary search to find new ARM rate where:
  Total refinance cost = Total original cost
• Accounts for entire 30-year period
• Considers cap rate differences

Breakeven Rate (ARM Only):
• Uses binary search to find new ARM rate where:
  Interest before refi + New ARM interest + Refi cost = Original ARM interest
• Only considers ARM fixed-rate periods
• Ignores adjustable rate periods completely


KEY ASSUMPTIONS
--------------

1. CONSTANT RATES
   ✓ Rates remain fixed during each period
   ✗ Does NOT model actual ARM adjustments based on index + margin
   ✗ Cap rates are maximum possible, not guaranteed actual rates

2. NO PREPAYMENTS
   ✓ Assumes standard monthly payments only
   ✗ Does NOT account for extra principal payments
   ✗ Does NOT model early payoff scenarios

3. FULL TERM
   ✓ Calculates for full 360 months (30 years)
   ✗ If you sell/refi early, use "ARM periods only" mode

4. NO TAX BENEFITS
   ✗ Does NOT account for mortgage interest tax deductions
   ✗ Does NOT consider opportunity costs of capital

5. REFINANCE COSTS
   ✓ Paid out of pocket, NOT added to loan principal
   ✓ One-time expense added to total cost
   ✗ Does NOT account for potential future refinancing

6. TIME VALUE OF MONEY
   ✗ Does NOT discount future payments to present value
   ✗ A dollar today equals a dollar in 30 years in these calculations

7. NO CLOSING CREDITS
   ✗ Does NOT model lender credits or points buydown


BREAKEVEN INTERPRETATION
-----------------------

Full 30-Year Breakeven: 5.368%
Current ARM rate: 4.875%
Your new rate: 4.0%

Interpretation:
→ Any new rate below 5.368% saves money over 30 years
→ Your 4.0% is 1.368% below breakeven = GOOD ✓
→ Even rates HIGHER than your current 4.875% can save money
→ Why? Because you escape the 9.875% cap sooner, even at a higher initial rate

ARM-Only Breakeven: 3.584%
Current ARM rate: 4.875%
Your new rate: 4.0%

Interpretation:
→ Any new rate below 3.584% saves money during ARM periods
→ Your 4.0% is 0.416% above breakeven = BAD ✗
→ You need a VERY LOW rate to offset the extra 24 months + refi cost
→ Why? You're extending from 84 to 108 total months at fixed rates


STRATEGIC USAGE EXAMPLES
------------------------

Example 1: Long-Term Homeowner
Goal: Minimize total 30-year cost
Settings:
  ☐ ARM periods only (unchecked)
  ☐ Custom adjustable rate (unchecked)
Action:
  Compare full 30-year costs
  Focus on total savings and breakeven rate
Decision:
  If new rate < breakeven rate → Refinance

Example 2: Planning to Sell in 5 Years
Goal: Minimize costs until sale
Settings:
  ☑ ARM periods only (checked)
  ☐ Custom adjustable rate (unchecked)
Action:
  Compare only ARM period costs
  Check ARM-only breakeven rate
Decision:
  If new rate < ARM breakeven → Refinance
  Otherwise, keep current loan

Example 3: Planning to Refi Again at Year 7
Goal: Compare assuming specific future rate
Settings:
  ☐ ARM periods only (unchecked)
  ☑ Custom adjustable rate (checked at 4.5%)
Action:
  Model both scenarios with same future rate
  Isolate ARM period advantage
Decision:
  Compare total costs with equal adjustable rates

Example 4: Multiple Offers Comparison
Goal: Compare 3 different lender offers
Action:
  1. Enter first offer, calculate
  2. Click "New Window"
  3. Change only the new ARM rate and refi cost
  4. Calculate in new window
  5. Repeat for third offer
  6. Compare results side-by-side


TIPS FOR BEST RESULTS
---------------------

✓ Get actual closing costs from lenders (not estimates)
✓ Verify your current ARM rate from loan documents
✓ Consider both comparison modes for complete picture
✓ Use multiple windows to compare different offers
✓ Test different timing scenarios (refinance at 12, 24, 36 months)
✓ Remember: Breakeven rates change based on timing
✓ Lower refinance costs → lower breakeven rate needed


LIMITATIONS
----------

This calculator:
✗ Cannot predict actual future ARM adjustment rates
✗ Does not account for tax implications
✗ Assumes you have cash for closing costs
✗ Does not model points or credits
✗ Does not consider credit score impacts
✗ Assumes standard amortization (no interest-only, balloon, etc.)


GETTING STARTED
--------------

Step 1: Enter your current loan details
Step 2: Enter the refinance offer details
Step 3: Click "Calculate" to see basic comparison
Step 4: Try "ARM periods only" if planning to sell/refi early
Step 5: Use "New Window" to compare multiple scenarios
Step 6: Make informed decision based on your timeline and goals


QUESTIONS?
---------

• Breakeven rate higher than current rate? Normal! You escape high cap rates sooner.
• ARM-only shows additional cost? Normal! You're extending the fixed-rate period.
• Savings different between modes? Normal! They measure different things.
• Custom rate reduces savings? Normal! You removed the cap rate advantage.


For more details, see the documentation files in the project directory.
"""
        
        help_text.insert(1.0, help_content)
        help_text.configure(state='disabled')  # Make read-only
        
        # Close button
        close_button = ttk.Button(help_frame, text="Close", command=help_window.destroy)
        close_button.pack(pady=10)
        
        self.status_var.set("Help window opened")


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = ARMCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

