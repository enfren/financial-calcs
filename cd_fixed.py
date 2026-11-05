"""
cd_fixed.py
Simulates a fixed-term CD where interest accrues daily but is
withdrawn (transferred to HYSA) at the end of each month.
The CD principal never changes — interest does NOT compound within the CD.

This mimics a "pay-out" or "interest-withdrawal" CD structure.
"""

from datetime import date, datetime
import calendar


def parse_date(prompt: str) -> date:
    while True:
        raw = input(prompt)
        try:
            return datetime.strptime(raw.strip(), "%Y-%m-%d").date()
        except ValueError:
            print("  Invalid. Use YYYY-MM-DD (e.g. 2026-11-05)")


def add_months(d: date, months: int) -> date:
    """Add N months to a date, clamping to last day of month if needed."""
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def main():
    print("=== CD — Fixed Term, Monthly Interest Payout ===\n")

    principal = float(input("CD principal ($): "))
    apy = float(input("APY (e.g. 3 for 3%): ")) / 100
    start_date = parse_date("CD start date (YYYY-MM-DD): ")
    term_months = int(input("Term (months): "))

    daily_rate = (1 + apy) ** (1 / 365) - 1

    print(f"\n--- Monthly Projection ---")
    print(f"{'Month':<6} {'Start':<12} {'End':<12} {'Days':<6} {'Interest':<10} {'Cumulative':<12}")
    print("-" * 60)

    cumulative = 0.0
    current = start_date

    for m in range(1, term_months + 1):
        # End of this month (the day before the next month's start)
        next_month_start = add_months(start_date, m)
        month_end = next_month_start  # interest accrues up to this date (exclusive)
        days = (next_month_start - current).days

        # Interest on the fixed principal for this month's exact day count
        interest = principal * ((1 + daily_rate) ** days - 1)
        cumulative += interest

        month_label = f"M{m}"
        print(f"{month_label:<6} {current.strftime('%Y-%m-%d'):<12} {next_month_start.strftime('%Y-%m-%d'):<12} {days:<6} ${interest:<9.4f} ${cumulative:<11.4f}")

        current = next_month_start

    print("-" * 60)
    print(f"\nTotal interest earned over {term_months} months: ${cumulative:,.4f}")
    print(f"Total transferred to HYSA:                     ${cumulative:,.4f}")
    print(f"CD principal at maturity (unchanged):         ${principal:,.2f}")
    print(f"\nEffective annual return: {cumulative / principal / (term_months / 12):.4%}")


if __name__ == "__main__":
    main()   