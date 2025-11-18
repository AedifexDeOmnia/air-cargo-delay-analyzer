import csv

DATA_FILE = "data/cargo_data.csv"


def load_shipments(path):
    """
    Load shipment data from a CSV file and return a list of dicts.
    Each row in the CSV becomes one dictionary.
    """
    shipments = []

    with open(path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert delay_minutes from string to integer
            row["delay_minutes"] = int(row["delay_minutes"])
            shipments.append(row)

    return shipments


def get_basic_stats(shipments):
    """
    Calculate basic statistics for delay_minutes.
    Returns a dictionary with count, min, max, and average.
    """
    if not shipments:
        return None

    delays = [s["delay_minutes"] for s in shipments]

    total = 0
    for d in delays:
        total += d

    count = len(delays)
    min_delay = min(delays)
    max_delay = max(delays)
    avg_delay = total / count

    return {
        "count": count,
        "min_delay": min_delay,
        "max_delay": max_delay,
        "avg_delay": avg_delay,
    }


def get_delayed_shipments(shipments, threshold=0):
    """
    Return a list of shipments where delay_minutes > threshold.
    """
    delayed = []
    for s in shipments:
        if s["delay_minutes"] > threshold:
            delayed.append(s)
    return delayed


def get_airline_stats(shipments, airline_code):
    """
    Filter shipments by airline code and calculate average delay.
    """
    airline_shipments = []
    for s in shipments:
        if s["airline"] == airline_code:
            airline_shipments.append(s)

    if not airline_shipments:
        return None

    delays = [s["delay_minutes"] for s in airline_shipments]

    total = 0
    for d in delays:
        total += d

    avg_delay = total / len(delays)

    return {
        "airline": airline_code,
        "count": len(airline_shipments),
        "avg_delay": avg_delay,
    }


def show_sample_shipments(shipments, limit=5):
    """
    Show the first few shipments (uses list slicing).
    """
    print(f"\nShowing first {limit} shipments (sample):")
    sample = shipments[:limit]  # slicing
    for s in sample:
        print(
            f"- ID {s['shipment_id']} | Airline {s['airline']} | "
            f"{s['origin']} → {s['destination']} | Delay: {s['delay_minutes']} min"
        )


def main():
    print("=== Air Cargo Delay Analyzer ===")

    # 1. Load data
    shipments = load_shipments(DATA_FILE)
    print(f"Loaded {len(shipments)} shipments from {DATA_FILE}")

    # 2. Show a sample of the data
    show_sample_shipments(shipments, limit=5)

    # 3. Basic delay statistics
    stats = get_basic_stats(shipments)
    if stats:
        print("\nOverall Delay Statistics:")
        print(f"- Total Shipments: {stats['count']}")
        print(f"- Minimum Delay:   {stats['min_delay']} minutes")
        print(f"- Maximum Delay:   {stats['max_delay']} minutes")
        print(f"- Average Delay:   {stats['avg_delay']:.2f} minutes")
    else:
        print("No data found for statistics.")

    # 4. Delayed vs on-time/early
    delayed = get_delayed_shipments(shipments, threshold=0)
    on_time_or_early = len(shipments) - len(delayed)

    print("\nDelay Breakdown:")
    print(f"- Delayed Shipments (delay > 0): {len(delayed)}")
    print(f"- On-Time / Early Shipments:     {on_time_or_early}")

    # 5. Airline-specific stats (example airlines in the data: AF, KL, DL)
    for airline in ["AF", "KL", "DL"]:
        airline_stat = get_airline_stats(shipments, airline)
        if airline_stat:
            print(
                f"\nAirline {airline_stat['airline']} Stats:"
                f"\n- Shipments: {airline_stat['count']}"
                f"\n- Average Delay: {airline_stat['avg_delay']:.2f} minutes"
            )

    # 6. Simple decision based on average delay
    if stats:
        print("\nPerformance Summary:")
        if stats["avg_delay"] <= 10:
            print("Overall performance: ✅ Good (average delay at or below 10 minutes)")
        elif stats["avg_delay"] <= 30:
            print("Overall performance: ⚠️ Moderate (delays could be improved)")
        else:
            print("Overall performance: 🔴 Poor (significant delays detected)")

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
