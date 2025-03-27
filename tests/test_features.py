# test features

from recur_scan.features import (
    get_amount_std_dev,
    get_ends_in_99,
    get_is_always_recurring,
    get_is_insurance,
    get_is_phone,
    get_is_utility,
    get_is_weekend_transaction,
    get_median_transaction_amount,
    get_n_transactions_days_apart,
    get_n_transactions_same_amount,
    get_n_transactions_same_day,
    get_pct_transactions_days_apart,
    get_pct_transactions_same_day,
    get_percent_transactions_same_amount,
    get_transaction_frequency,
)
from recur_scan.transactions import Transaction


def test_get_is_always_recurring() -> None:
    transaction = Transaction(id=1, user_id="user1", name="Netflix", amount=15.99, date="2024-01-01")
    assert get_is_always_recurring(transaction)


def test_get_is_insurance() -> None:
    transaction = Transaction(id=1, user_id="user1", name="Health Insurance", amount=120.50, date="2024-02-01")
    assert get_is_insurance(transaction)


def test_get_is_utility() -> None:
    transaction = Transaction(id=1, user_id="user1", name="Electric Utility", amount=90.75, date="2024-03-01")
    assert get_is_utility(transaction)


def test_get_is_phone() -> None:
    transaction = Transaction(id=1, user_id="user1", name="Verizon", amount=60.00, date="2024-04-01")
    assert get_is_phone(transaction)


def test_get_n_transactions_days_apart() -> None:
    transactions = [
        Transaction(id=1, user_id="user1", name="Rent", amount=1000, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="Rent", amount=1000, date="2024-02-01"),
    ]
    assert get_n_transactions_days_apart(transactions[0], transactions, 30, 2) == 1


def test_get_n_transactions_same_day() -> None:
    transactions = [
        Transaction(id=1, user_id="user1", name="Subscription", amount=9.99, date="2024-03-01"),
        Transaction(id=2, user_id="user1", name="Subscription", amount=9.99, date="2024-03-01"),
    ]
    assert get_n_transactions_same_day(transactions[0], transactions, 0) == 2


def test_get_pct_transactions_same_day() -> None:
    transactions = [
        Transaction(id=1, user_id="user1", name="Subscription", amount=9.99, date="2024-03-01"),
        Transaction(id=2, user_id="user1", name="Subscription", amount=9.99, date="2024-03-01"),
    ]
    assert get_pct_transactions_same_day(transactions[0], transactions, 0) == 1.0


def test_get_ends_in_99() -> None:
    transaction = Transaction(id=1, user_id="user1", name="Product", amount=19.99, date="2024-03-15")
    assert get_ends_in_99(transaction)


def test_get_percent_transactions_same_amount() -> None:
    transactions = [
        Transaction(id=1, user_id="user1", name="Product A", amount=50.00, date="2024-03-01"),
        Transaction(id=2, user_id="user1", name="Product A", amount=50.00, date="2024-03-02"),
    ]
    assert get_percent_transactions_same_amount(transactions[0], transactions) == 1.0


def test_get_transaction_frequency() -> None:
    transactions = [
        Transaction(id=1, user_id="user1", name="Coffee", amount=5.00, date="2024-03-01"),
        Transaction(id=2, user_id="user1", name="Coffee", amount=5.00, date="2024-03-02"),
    ]
    assert get_transaction_frequency(transactions[0], transactions) == 2


def test_get_amount_std_dev() -> None:
    transactions = [
        Transaction(id=1, user_id="user1", name="Groceries", amount=100.00, date="2024-03-01"),
        Transaction(id=2, user_id="user1", name="Groceries", amount=120.00, date="2024-03-02"),
    ]
    assert get_amount_std_dev(transactions[0], transactions) > 0


def test_get_median_transaction_amount() -> None:
    """Test get_median_transaction_amount returns correct median value."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=200, date="2024-01-02"),
        Transaction(id=3, user_id="user1", name="name1", amount=300, date="2024-01-03"),
    ]
    assert get_median_transaction_amount(transactions[0], transactions) == 200

    transactions.append(Transaction(id=4, user_id="user1", name="name1", amount=400, date="2024-01-04"))
    assert get_median_transaction_amount(transactions[0], transactions) == 250


def test_get_is_weekend_transaction() -> None:
    """Test get_is_weekend_transaction correctly identifies weekend transactions."""
    assert get_is_weekend_transaction(
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-03-23")
    )  # Saturday
    assert get_is_weekend_transaction(
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-03-24")
    )  # Sunday
    assert not get_is_weekend_transaction(
        Transaction(id=3, user_id="user1", name="name1", amount=100, date="2024-03-25")
    )  # Monday


def test_get_n_transactions_same_amount() -> None:
    """Test that get_n_transactions_same_amount returns the correct number of transactions with the same amount."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-01-02"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-03"),
    ]
    assert get_n_transactions_same_amount(transactions[0], transactions) == 2
    assert get_n_transactions_same_amount(transactions[2], transactions) == 1


def test_get_percent_transactions_same_amount() -> None:
    """
    Test that get_percent_transactions_same_amount returns correct percentage.
    Tests that the function calculates the right percentage of transactions with matching amounts.
    """
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-01-02"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-03"),
    ]
    assert pytest.approx(get_percent_transactions_same_amount(transactions[0], transactions)) == 2 / 4


def test_get_ends_in_99() -> None:
    """Test that get_ends_in_99 returns True for amounts ending in 99."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-01-02"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-03"),
    ]
    assert not get_ends_in_99(transactions[0])
    assert get_ends_in_99(transactions[3])


def test_get_n_transactions_same_day() -> None:
    """Test that get_n_transactions_same_day returns the correct number of transactions on the same day."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-01-02"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-03"),
    ]
    assert get_n_transactions_same_day(transactions[0], transactions, 0) == 2
    assert get_n_transactions_same_day(transactions[0], transactions, 1) == 3
    assert get_n_transactions_same_day(transactions[2], transactions, 0) == 1


def test_get_pct_transactions_same_day() -> None:
    """Test that get_pct_transactions_same_day returns the correct percentage of transactions on the same day."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=100, date="2024-01-01"),
        Transaction(id=3, user_id="user1", name="name1", amount=200, date="2024-01-02"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-03"),
    ]
    assert get_pct_transactions_same_day(transactions[0], transactions, 0) == 2 / 4


def test_get_n_transactions_days_apart() -> None:
    """Test get_n_transactions_days_apart."""
    transactions = [
        Transaction(id=1, user_id="user1", name="name1", amount=2.99, date="2024-01-01"),
        Transaction(id=2, user_id="user1", name="name1", amount=2.99, date="2024-01-02"),
        Transaction(id=3, user_id="user1", name="name1", amount=2.99, date="2024-01-14"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-15"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-16"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-29"),
        Transaction(id=4, user_id="user1", name="name1", amount=2.99, date="2024-01-31"),
    ]
    assert get_n_transactions_days_apart(transactions[0], transactions, 14, 0) == 2
    assert get_n_transactions_days_apart(transactions[0], transactions, 14, 1) == 4


def test_get_is_insurance() -> None:
    """Test get_is_insurance."""
    assert get_is_insurance(
        Transaction(id=1, user_id="user1", name="Allstate Insurance", amount=100, date="2024-01-01")
    )
    assert not get_is_insurance(Transaction(id=2, user_id="user1", name="AT&T", amount=100, date="2024-01-01"))


def test_get_is_phone() -> None:
    """Test get_is_phone."""
    assert get_is_phone(Transaction(id=2, user_id="user1", name="AT&T", amount=100, date="2024-01-01"))
    assert not get_is_phone(Transaction(id=3, user_id="user1", name="Duke Energy", amount=200, date="2024-01-02"))


def test_get_is_utility() -> None:
    """Test get_is_utility."""
    assert get_is_utility(Transaction(id=3, user_id="user1", name="Duke Energy", amount=200, date="2024-01-02"))
    assert not get_is_utility(
        Transaction(id=4, user_id="user1", name="HighEnergy Soft Drinks", amount=2.99, date="2024-01-03")
    )


def test_get_is_always_recurring() -> None:
    """Test get_is_always_recurring."""
    assert get_is_always_recurring(Transaction(id=1, user_id="user1", name="netflix", amount=100, date="2024-01-01"))
    assert not get_is_always_recurring(
        Transaction(id=2, user_id="user1", name="walmart", amount=100, date="2024-01-01")
    )
