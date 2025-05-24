"""
Custom Exceptions to hanlde app specific behavior on errors.
"""


class CalculatorException(Exception):
    """
    Calculator base exception. Handled at the outermost level.
    All other exception types are subclasses of this exception type.
    """


class OperationalException(CalculatorException):
    """
    Requires manual intervention and will stop the bot.
    Most of the time, this is caused by an invalid Configuration.
    """


class ConfigurationError(OperationalException):
    """
    Configuration error. Usually caused by invalid configuration.
    """


class AdditionError(CalculatorException):
    """
    Addition error. Usually caused by invalid configuration.
    """


class SubstractionError(CalculatorException):
    """
    Substraction error. Usually caused by invalid configuration.
    """


class MultiplicationError(CalculatorException):
    """
    Multiplication error. Usually caused by invalid configuration.
    """


class DivisionError(CalculatorException):
    """
    Division error. Usually caused by invalid configuration.
    """
