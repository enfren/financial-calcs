"""
savings_basic.py
Simulates a single savings deposit earning daily-compounding interest
until a payout date. Uses exact calendar days (not 30/31 assumptions).

How banks work:
  - Interest accrues daily: daily_rate = (1 + APY)^(1/365) - 1
  - Interest is credited on a set date (e.g., 1st of the month)
  - The number of days is simply (payout_date - deposit_date).days
"""

from datetime import date, datetime


def parse_date(prompt: str) -> date:
    """Prompt for a date in YYYY-MM-DD format with retry."""
    while True:
        raw = input(prompt)
        try:
            return datetime.strptime(raw.strip(), "%Y-%m-%d").date()
        except ValueError:
            print("  Invalid. Use YYYY-MM-DD (e.g. 2026-11-05)")


def main():
    print("=== Savings Account — Basic ===\n")

    deposit_date = parse_date("Date of deposit (YYYY-MM-DD): ")
    amount = float(input("Amount of deposit ($): "))
    apy = float(input("APY (e.g. 3 for 3%): ")) / 100
    payout_date = parse_date("Date interest is paid into account (YYYY-MM-DD): ")

    if payout_date <= deposit_date:
        print("\nError: Payout date must be after deposit date.")
        return

    days = (payout_date - deposit_date).days

    # Convert APY to a daily rate.
    # APY is the effective annual yield, so:
    #   (1 + daily_rate)^365 = 1 + APY
    #   daily_rate = (1 + APY)^(1/365) - 1
    daily_rate = (1 + apy) ** (1 / 365) - 1

    # Apply daily compounding for the exact number of days
    balance = amount * (1 + daily_rate) ** days
    interest_earned = balance - amount

    print(f"\n--- Results ---")
    print(f"Deposit:     ${amount:,.2f} on {deposit_date.strftime('%B %d, %Y')}")
    print(f"Payout:      {payout_date.strftime('%B %d, %Y')}")
    print(f"Days:        {days}")
    print(f"APY:         {apy:.4%}")
    print(f"Daily rate:  {daily_rate:.8%}")
    print(f"")
    print(f"Interest:    ${interest_earned:,.4f}")
    print(f"New balance: ${balance:,.2f}")


if __name__ == "__main__":
    main()   