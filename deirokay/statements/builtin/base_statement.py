"""
The base statement that all other statements inherit from.
"""
from abc import ABC, abstractmethod
from typing import List

from deirokay._typing import (DeirokayDataSource, DeirokayOption,
                              DeirokayStatement)
from deirokay.backend import MultiBackendMixin


class BaseStatement(MultiBackendMixin, ABC):
    """Base abstract statement class for all Deirokay statements.

    Attributes
    ----------
    options : dict
        Statement parameters provided by user.
    """

    name: str = 'base_statement'
    """str: Statement name when referred in Validation Documents
    (only valid for Deirokay built-in statements)."""
    expected_parameters: List[str] = ['type', 'severity', 'location']
    """List[str]: Parameters expected for this statement."""

    def __init_subclass__(cls) -> None:
        """Validate subclassed statement."""
        assert cls.name != BaseStatement.name, (
            'You should specify a `name` attribute for your statement class.'
        )

    def __init__(self, options: DeirokayOption) -> None:
        self._validate_options(options)
        self.options = options

    @classmethod
    def _validate_options(cls, options: DeirokayOption) -> None:
        """Make sure all provided statement parameters are expected
        by statement classes"""
        unexpected_parameters = [
            option for option in options
            if option not in (cls.expected_parameters +
                              BaseStatement.expected_parameters)
        ]
        if unexpected_parameters:
            raise ValueError(
                f'Invalid parameters passed to {cls.__name__} statement: '
                f'{unexpected_parameters}\n'
                f'The valid parameters are: {cls.expected_parameters}'
            )

    def __call__(self, df: DeirokayDataSource, /) -> dict:
        """Run statement instance."""
        internal_report = self.report(df)
        result = self.result(internal_report)

        final_report = {
            'detail': internal_report,
            'result': result
        }
        return final_report

    def report(self, df: DeirokayDataSource, /) -> dict:
        """Receive a DataFrame containing only columns on the scope of
        validation and returns a report of related metrics that can
        be used later to declare this Statement as fulfilled or
        failed.

        Parameters
        ----------
        df : DataFrame
            The scoped DataFrame columns to be analysed in this report
            by this statement.

        Returns
        -------
        dict
            A dictionary of useful statistics about the target columns.
        """
        raise NotImplementedError

    @abstractmethod
    def result(self, report: dict, /) -> bool:
        """Receive the report previously generated and declare this
        statement as either fulfilled (True) or failed (False).

        Parameters
        ----------
        report : dict
            Report generated by `report` method. Should ideally
            contain all statistics necessary to evaluate the statement
            validity.

        Returns
        -------
        bool
            Whether or not this statement passed.
        """

    @staticmethod
    def profile(df: DeirokayDataSource, /) -> DeirokayStatement:
        """Given a template data table, generate a statement dict
        from it.

        Parameters
        ----------
        df : DataFrame
            The DataFrame to be used as template.

        Returns
        -------
        dict
            Statement dict.

        Raises
        ------
        NotImplementedError
            If this method is not implemented by the subclass or the
            profile generation for this statement was intentionally
            skipped.
        """
        raise NotImplementedError