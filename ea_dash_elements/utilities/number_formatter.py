import numpy as np


class NumberType:
    ABSOLUTE = 'Absolute'
    PERCENTAGE = 'Percentage'


class NumberFormatter:

    def __init__(self, number_type: NumberType):
        self.number_type = number_type

    def format(self, number: float):
        if self.number_type == NumberType.ABSOLUTE:
            return self._format_absolute(number)
        elif self.number_type == NumberType.PERCENTAGE:
            return self._format_percentage(number)

    @staticmethod
    def _format_absolute(x):
        if np.isnan(x):
            return ''
        if x >= 0:
            return f'{abs(x):,.0f}'
        else:
            return f'({abs(x):,.0f})'

    @staticmethod
    def _format_percentage(x):
        """
        House style is not to show the % sign and have it in the title
        """
        if np.isnan(x):
            return ''
        if x >= 0:
            return f'{abs(x) * 100:,.1f}'
        else:
            return f'({abs(x) * 100:,.1f})'


