import unittest

from recur_scan.features import (
    get_has_irregular_spike,
    get_is_common_subscription_amount,
    get_is_first_of_month,
    get_is_fixed_interval,
    get_is_similar_name,
    get_occurs_same_week,
)
from recur_scan.transactions import Transaction


class TestFeatureExtraction(unittest.TestCase):
    def setUp(self):
        """Set up test transactions for a single user"""
        self.user_id = "user1"
        self.transactions = [
            Transaction(id=1, user_id="user1", name="Netflix", amount=15.99, date="2024-01-01"),
            Transaction(id=2, user_id="user1", name="Hulu", amount=12.99, date="2024-01-15"),
            Transaction(id=3, user_id="user1", name="Spotify", amount=9.99, date="2024-02-01"),
            Transaction(id=4, user_id="user1", name="Auto Insurance", amount=100.00, date="2024-01-10"),
            Transaction(id=5, user_id="user1", name="T-Mobile Payment", amount=50.00, date="2024-01-20"),
            Transaction(id=6, user_id="user1", name="Electric Utility Bill", amount=75.00, date="2024-01-25"),
            Transaction(id=7, user_id="user1", name="Netflix", amount=15.99, date="2024-02-01"),
            Transaction(id=8, user_id="user1", name="Netflix", amount=15.99, date="2024-03-01"),
            Transaction(id=9, user_id="user2", name="Disney+", amount=10.99, date="2024-01-01"),
        ]
        self.test_transaction = Transaction(id=10, user_id="user1", name="Netflix", amount=15.99, date="2024-03-01")

    def get_user_transactions(self, transactions, user_id):
        """Filter transactions to only include those belonging to the same user."""
        return [t for t in transactions if t.user_id == user_id]

    def test_get_is_common_subscription_amount(self):
        assert get_is_common_subscription_amount(
            Transaction(id=20, user_id="user1", name="Hulu", amount=9.99, date="2024-01-01")
        )
        assert not get_is_common_subscription_amount(
            Transaction(id=21, user_id="user1", name="Store Purchase", amount=27.5, date="2024-01-15")
        )

    def test_get_occurs_same_week(self):
        user_transactions = self.get_user_transactions(self.transactions, "user1")
        assert get_occurs_same_week(
            Transaction(id=22, user_id="user1", name="Netflix", amount=15.99, date="2024-03-01"), user_transactions
        )
        assert not get_occurs_same_week(
            Transaction(id=23, user_id="user1", name="One-time Purchase", amount=99.99, date="2024-01-20"),
            user_transactions,
        )

    def test_get_is_similar_name(self):
        user_transactions = self.get_user_transactions(self.transactions, "user1")
        assert get_is_similar_name(
            Transaction(id=24, user_id="user1", name="Spotify Premium", amount=9.99, date="2024-02-01"),
            user_transactions,
        )
        assert not get_is_similar_name(
            Transaction(id=25, user_id="user1", name="Amazon Purchase", amount=50.0, date="2024-03-05"),
            user_transactions,
        )

    def test_get_is_fixed_interval(self):
        user_transactions = self.get_user_transactions(self.transactions, "user1")
        assert get_is_fixed_interval(
            Transaction(id=26, user_id="user1", name="Netflix", amount=15.99, date="2024-03-01"), user_transactions
        )
        assert not get_is_fixed_interval(
            Transaction(id=27, user_id="user1", name="Gas Station", amount=40.0, date="2024-02-10"), user_transactions
        )

    def test_get_has_irregular_spike(self):
        user_transactions = self.get_user_transactions(self.transactions, "user1")
        assert get_has_irregular_spike(
            Transaction(id=28, user_id="user1", name="Internet Bill", amount=100.0, date="2024-03-01"),
            user_transactions,
        )
        assert not get_has_irregular_spike(
            Transaction(id=29, user_id="user1", name="Spotify", amount=9.99, date="2024-02-01"), user_transactions
        )

    def test_get_is_first_of_month(self):
        assert get_is_first_of_month(
            Transaction(id=30, user_id="user1", name="Rent Payment", amount=1200.0, date="2024-02-01")
        )
        assert not get_is_first_of_month(
            Transaction(id=31, user_id="user1", name="Grocery", amount=75.0, date="2024-02-15")
        )


if __name__ == "__main__":
    unittest.main()
