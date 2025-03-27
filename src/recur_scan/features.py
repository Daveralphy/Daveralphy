import re
from datetime import datetime
from statistics import mean, stdev

from recur_scan.transactions import Transaction

# def is_recurring_deposit(transaction: Transaction, merchant_trans: list[Transaction]) -> bool:
#    """
#    Check if a transaction is a recurring deposit based on amount and frequency.
#    """
#    return transaction.amount > 0 and len(merchant_trans) >= 3


# def is_dynamic_recurring(interval_stats: dict[str, float], amount_stats: dict[str, float]) -> bool:
#    """
#    Check if a transaction is recurring with varying amounts but consistent intervals.
#    """
#    return (
#        interval_stats["std_dev_days_between_transactions"] < 45
#        and amount_stats["mean"] > 0
#        and (amount_stats["std"] / amount_stats["mean"]) > 0.002
#    )


# def matching_transaction_ratio(
#    transaction: Transaction, all_transactions: list[Transaction], merchant_trans: list[Transaction]
# ) -> float:
#    """
#    Calculate the ratio of merchant-specific transactions with the same amount and name to all transactions.
#    """
#    if not all_transactions:
#        return 0.0
#
#    identical_transaction_count = sum(
#        t.amount == transaction.amount and t.name == transaction.name for t in merchant_trans
#    )
#
#    return identical_transaction_count / len(all_transactions)


# def common_transaction_names(all_transactions: list[Transaction]) -> list[str]:
#    """
#    Extract transaction names that frequently appear for the same user with repeated amounts.
#    """
#    grouped_transactions = defaultdict(list)
#    for transaction in all_transactions:
#        grouped_transactions[(transaction.user_id, transaction.name)].append(transaction)
#    return [
#        name
#        for (_user_id, name), transactions in grouped_transactions.items()
#        if any(count > 1 for count in Counter(t.amount for t in transactions).values())
#    ]


def get_is_always_recurring(transaction: Transaction) -> bool:
    """
    Check if the transaction is from a known recurring vendor.
    All transactions from these vendors are considered recurring.
    """
    #    known_recurring_keywords = ["netflix","spotify","amazon prime","amazon music","google play",
    #        "hulu","disney+","youtube","comcast","adobe","microsoft","afterpay","walmart+"]

    #    vendor_name = transaction.name.lower()
    #    # Create a regex pattern to match any of the known recurring keywords
    #    pattern = r"\b(" + "|".join(re.escape(keyword) for keyword in known_recurring_keywords) + r")\b"
    #    # Check if the vendor name matches the pattern
    #    return bool(re.search(pattern, vendor_name, re.IGNORECASE))

    # Use a regular expression with boundaries to match case-insensitive company names
    match = re.search(
        r"\b(netflix|spotify|google play|hulu|disney\+|youtube|adobe|microsoft|walmart\+|amazon prime)\b",
        transaction.name,
        re.IGNORECASE,
    )
    return bool(match)


def get_is_insurance(transaction: Transaction) -> bool:
    """Check if the transaction is from a known insurance company."""
    #    insurance_companies = {"geico", "allstate", "state farm", "progressive", "renters insurance",
    # "health insurance","car insurance", "home insurance", "life insurance", "insurance", "auto insurance"}
    #    return any(term in transaction.name.lower() for term in insurance_companies)

    # Use a regular expression with boundaries to match case-insensitive company names
    match = re.search(
        r"\b(insur|geico|allstate|state farm|progressive|insur|insuranc)\b", transaction.name, re.IGNORECASE
    )
    return bool(match)


def get_is_utility(transaction: Transaction) -> bool:
    """Check if the transaction is from a known utility company."""
    #    utility_terms = {"water", "electricity", "gas", "internet", "cable", "energy", "utility", "light"}
    #    return any(term in transaction.name.lower() for term in utility_terms)

    # Use a regular expression with boundaries to match case-insensitive company names
    match = re.search(
        r"\b(water|electricity|gas|internet|cable|energy|utilit|utility|cable|electric|light|phone)\b",
        transaction.name,
        re.IGNORECASE,
    )
    return bool(match)


def _get_days(date: str) -> int:
    """Get the number of days since the epoch of the transaction date."""
    # Assuming date is in the format YYYY-MM-DD
    # use the datetime module for the accurate determination
    # of the number of days since the epoch
    return (datetime.strptime(date, "%Y-%m-%d") - datetime(1970, 1, 1)).days


def get_n_transactions_days_apart(
    transaction: Transaction,
    all_transactions: list[Transaction],
    n_days_apart: int,
    n_days_off: int,
) -> int:
    """
    Get the number of transactions in all_transactions that are within n_days_off of
    being n_days_apart from thr transaction
    """
    n_txs = 0
    transaction_days = _get_days(transaction.date)

    for t in all_transactions:
        t_days = _get_days(t.date)
        days_diff = abs(t_days - transaction_days)
        # skip if the deifference is less than n_days_apart - n_days_off
        if days_diff < n_days_apart - n_days_off:
            continue

        # Check if thye difference is close to any multiple of n_daus_apart
        # For example, with n_days_apart =14 and n_days_off = 1, we want to count
        # transactions that are 13-15, 27-29, 41-43, etc. days apart

        remainder = days_diff % n_days_apart

        if remainder <= n_days_off or (n_days_apart - remainder) <= n_days_off:
            n_txs += 1

    return n_txs


def get_pct_transactions_days_apart(
    transaction: Transaction, all_transactions: list[Transaction], n_days_apart: int, n_days_off: int
) -> float:
    """
    Get the percentage of transactions in all_transactions that are within
    n_days_off of being n_days_apart from transaction
    """
    return get_n_transactions_days_apart(transaction, all_transactions, n_days_apart, n_days_off) / len(
        all_transactions
    )


def _get_day(date: str) -> int:
    """Get the day of the month from a transaction date."""
    return int(date.split("-")[2])


def get_n_transactions_same_day(transaction: Transaction, all_transactions: list[Transaction], n_days_off: int) -> int:
    """Get the number of transactions in all_transactions that are on the same day of the month as transaction."""
    transaction_day = _get_day(transaction.date)
    return sum(1 for t in all_transactions if abs(_get_day(t.date) - transaction_day) <= n_days_off)


def get_pct_transactions_same_day(
    transaction: Transaction, all_transactions: list[Transaction], n_days_off: int
) -> float:
    """Get the percentage of transactions in all_transactions that are on the same day of the month as transaction"""
    return get_n_transactions_same_day(transaction, all_transactions, n_days_off) / len(all_transactions)


def get_ends_in_99(transaction: Transaction) -> bool:
    """Check if the transaction amount ends in 99."""
    return int(transaction.amount * 100) % 100 == 99


def get_year(transaction: Transaction) -> int:
    """Get the year for the transaction date."""
    try:
        return datetime.strptime(transaction.date, "%Y-%m-%d").year
    except ValueError:
        return -1


def get_month(transaction: Transaction) -> int:
    """Get the month for the transaction date."""
    try:
        return datetime.strptime(transaction.date, "%Y-%m-%d").month
    except ValueError:
        return -1


def get_day(transaction: Transaction) -> int:
    """Get the day for the transaction date."""
    try:
        return datetime.strptime(transaction.date, "%Y-%m-%d").day
    except ValueError:
        return -1


# def get_day_of_week(transaction: Transaction) -> int:
#    """Get the day of the week for the transaction date."""
#    try:
#        return datetime.strptime(transaction.date, "%Y-%m-%d").weekday()
#    except ValueError:
#        return -1


def is_recurring_mobile_transaction(transaction: Transaction) -> bool:
    """Check if the transaction is from a known mobile company."""
    mobile_companies = {"t-mobile", "at&t", "verizon", "boost mobile", "tello mobile", "spectrum"}
    return transaction.name.lower() in mobile_companies


def get_min_transaction_amount(all_transactions: list[Transaction]) -> float:
    """Get the minimum transaction amount."""
    return min((t.amount for t in all_transactions), default=0.0)


def get_max_transaction_amount(all_transactions: list[Transaction]) -> float:
    """Get the maximum transaction amount."""
    return max((t.amount for t in all_transactions), default=0.0)


def get_transaction_intervals(transactions: list[Transaction]) -> dict[str, float]:
    """
    Extracts time-based features for recurring transactions.
    - Computes average days between transactions.
    - Computes standard deviation of intervals.
    - Checks for flexible monthly recurrence (±7 days).
    - Identifies if transactions occur on the same weekday.
    - Checks if payment amounts are within ±5% of each other.
    """
    if len(transactions) < 2:
        return {
            "avg_days_between_transactions": 0.0,
            "std_dev_days_between_transactions": 0.0,
            "monthly_recurrence": 0,
            "same_weekday": 0,
            "same_amount": 0,
        }
    # Sort transactions by date
    dates = sorted([
        datetime.strptime(trans.date, "%Y-%m-%d") if isinstance(trans.date, str) else trans.date
        for trans in transactions
    ])

    # calculate days between each consecutive grouped transactions
    intervals = [(dates[i] - dates[i - 1]).days for i in range(1, len(dates))]

    # compute average and standard deviation of transaction intervals
    avg_days = mean(intervals) if intervals else 0.0
    std_dev_days = stdev(intervals) if len(intervals) > 1 else 0.0

    # check for flexible monthly recurrence (±7 days)
    monthly_count = sum(
        1
        for gap in intervals
        if 23 <= gap <= 38  # 30 ± 7 days
    )
    monthly_recurrence = monthly_count / len(intervals) if intervals else 0.0

    # check if transactions occur on the same weekday
    weekdays = [date.weekday() for date in dates]  # Monday = 0, Sunday = 6
    same_weekday = 1 if len(set(weekdays)) == 1 else 0  # 1 if all transactions happen on the same weekday

    # check if payment amounts are within ±5% of each other
    amounts = [trans.amount for trans in transactions]

    base_amount = amounts[0]
    if base_amount == 0:
        consistent_amount = 0.0
    else:
        consistent_amount = sum(1 for amt in amounts if abs(amt - base_amount) / base_amount <= 0.05) / len(amounts)

    return {
        "avg_days_between_transactions": avg_days,
        "std_dev_days_between_transactions": std_dev_days,
        "monthly_recurrence": monthly_recurrence,
        "same_weekday": same_weekday,
        "same_amount": consistent_amount,
    }


def get_n_transactions_same_vendor(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    """Get the number of transactions in all_transactions with the same vendor as transaction."""
    return sum(1 for t in all_transactions if t.name == transaction.name)


def get_percent_transactions_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> float:
    """Get the percentage of transactions in all_transactions with the same amount as transaction."""
    if not all_transactions:
        return 0.0
    n_same_amount = sum(1 for t in all_transactions if t.amount == transaction.amount)
    return n_same_amount / len(all_transactions)


def get_n_transactions_same_amount(transaction: Transaction, all_transactions: list[Transaction]) -> int:
    """Get the number of transactions in all_transactions with the same amount as transaction."""
    return sum(1 for t in all_transactions if t.amount == transaction.amount)


def get_features(transaction: Transaction, all_transactions: list[Transaction]) -> dict[str, float | int | bool]:
    """Extract features for a given transaction."""
    # merchant_trans = [t for t in all_transactions if t.name == transaction.name]
    # interval_stats = get_transaction_intervals(merchant_trans)
    # amount_stats = {
    #    "mean": mean(t.amount for t in merchant_trans),
    #    "std": stdev(t.amount for t in merchant_trans) if len(merchant_trans) > 1 else 0.0,
    # }

    features = {
        "n_transactions_same_amount": get_n_transactions_same_amount(transaction, all_transactions),
        "percent_transactions_same_amount": get_percent_transactions_same_amount(transaction, all_transactions),
        "n_transactions_same_vendor": get_n_transactions_same_vendor(transaction, all_transactions),
        "max_transaction_amount": get_max_transaction_amount(all_transactions),
        "min_transaction_amount": get_min_transaction_amount(all_transactions),
        "is_recurring_mobile_transaction": is_recurring_mobile_transaction(transaction),
        # "day_of_week": get_day_of_week(transaction),
        "month": get_month(transaction),
        "day": get_day(transaction),
        "year": get_year(transaction),
        "ends_in_99": get_ends_in_99(transaction),
        "amount": transaction.amount,
        "same_day_exact": get_n_transactions_same_day(transaction, all_transactions, 0),
        "same_day_off_1": get_n_transactions_same_day(transaction, all_transactions, 1),
        "same_day_off_2": get_n_transactions_same_day(transaction, all_transactions, 2),
        "pct_transactions_same_day": get_pct_transactions_same_day(transaction, all_transactions, 0),
        "same_day_off_by_1": get_n_transactions_same_day(transaction, all_transactions, 1),
        "same_day_off_by_2": get_n_transactions_same_day(transaction, all_transactions, 2),
        "14_days_apart_exact": get_n_transactions_days_apart(transaction, all_transactions, 14, 0),
        "pct_14_days_apart_exact": get_pct_transactions_days_apart(transaction, all_transactions, 14, 0),
        "14_days_apart_off_by_1": get_n_transactions_days_apart(transaction, all_transactions, 14, 1),
        "pct_14_days_apart_off_by_1": get_pct_transactions_days_apart(transaction, all_transactions, 14, 1),
        "7_days_apart_exact": get_n_transactions_days_apart(transaction, all_transactions, 7, 0),
        "pct_7_days_apart_exact": get_pct_transactions_days_apart(transaction, all_transactions, 7, 0),
        "7_days_apart_off_by_1": get_n_transactions_days_apart(transaction, all_transactions, 7, 1),
        "pct_7_days_apart_off_by_1": get_pct_transactions_days_apart(transaction, all_transactions, 7, 1),
        "is_insurance": get_is_insurance(transaction),
        "is_utility": get_is_utility(transaction),
        "is_always_recurring": get_is_always_recurring(transaction),
        # "is_recurring_deposit": is_recurring_deposit(transaction, merchant_trans),
        # "is_dynamic_recurring": is_dynamic_recurring(interval_stats, amount_stats),
        # "matching_transaction_ratio": matching_transaction_ratio(transaction, all_transactions, merchant_trans),
        # "common_transaction_names": common_transaction_names(all_transactions),
    }
    # Add transaction intervals features
    intervals_features = get_transaction_intervals(all_transactions)
    features.update(intervals_features)
    return features
