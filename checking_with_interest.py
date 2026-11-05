"""
checking_with_interest.py
Simulates a checking account that pays interest only up to a balance cap.
Interest accrues daily on min(balance, cap).

You only input SEGMENTS — periods where the balance stayed constant.
Example: $900 from Nov 1–14, then $1000 from Nov 15–30 = 2 segments.
"""

from datetime import date, datetime, timedelta


def parse_date(prompt: str) -> date:
    while True:
        raw = input(prompt)
        try:
            return datetime.strptime(raw.strip(), "%Y-%m-%d").date()
        except ValueError:
            print("  Invalid. Use YYYY-MM-DD (e.g. 2026-11-05)")


def main():
    print("=== Checking Account — Interest with Cap ===\n")

    apy = float(input("APY (e.g. 0.5 for 0.5%): ")) / 100
    cap = float(input("Interest applies up to what balance? ($): "))
    statement_date = parse_date("Statement / interest credit date (YYYY-MM-DD): ")

    # Collect segments: each is (start_date, end_date, balance)
    print(f"\nEnter balance segments (periods where balance stayed the same).")
    print(f"Segments must be consecutive and end on {statement_date.strftime('%Y-%m-%d')}.")
    print(f"Type 'done' when finished.\n")

    segments = []
    current_start = parse_date("  First segment starts (YYYY-MM-DD): ")

    while True:
        balance = float(input(f"  Balance from {current_start.strftime('%Y-%m-%d')}: $"))
        next_seg = input(f"  Next segment starts (YYYY-MM-DD) or 'done': ")

        if next_seg.strip().lower() == "done":
            if statement_date < current_start:
                print(f"  Error: Statement date ({statement_date}) must be after {current_start}.")
                print(f"  Re-enter segments with a later statement date.")
                return
            end_date = statement_date
            segments.append((current_start, end_date, balance))
            break
        else:
            try:
                end_date = datetime.strptime(next_seg.strip(), "%Y-%m-%d").date()
            except ValueError:
                print("  Invalid date.")
                continue
            segments.append((current_start, end_date, balance))
            current_start = end_date

    # Calculate interest per segment
    daily_rate = (1 + apy) ** (1 / 365) - 1
    total_interest = 0

    print(f"\n--- Breakdown ---")
    print(f"{'Start':<12} {'End':<12} {'Days':<6} {'Balance':<10} {'Eligible':<10} {'Interest':<10}")
    print("-" * 60)

    for start, end, balance in segments:
        days = (end - start).days
        eligible = min(balance, cap)
        interest = eligible * ((1 + daily_rate) ** days - 1)
        total_interest += interest
        display_end = end - timedelta(days=1)
        print(f"{start.strftime('%Y-%m-%d'):<12} {display_end.strftime('%Y-%m-%d'):<12} {days:<6} ${balance:<9,.2f} ${eligible:<9,.2f} ${interest:<9.4f}")

    print("-" * 60)
    print(f"Total interest credited: ${total_interest:,.4f}")


if __name__ == "__main__":
    main()   