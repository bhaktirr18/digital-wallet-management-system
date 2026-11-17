
class WalletError(Exception):
    """Base exception for wallet-related errors."""


class InsufficientBalanceError(WalletError):
    """Raised when the wallet does not have enough funds."""


class InvalidAmountError(WalletError):
    """Raised when an invalid transaction amount is provided."""


class DuplicateTransactionError(WalletError):
    """Raised when a duplicate transaction is detected."""


class RecipientNotFoundError(WalletError):
    """Raised when the recipient wallet does not exist."""
