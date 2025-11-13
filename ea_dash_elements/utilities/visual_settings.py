import itertools


class VisualSettings:
    """
    A class that defines chart settings and color themes.

    Attributes:
        THEME_1 (list): The color theme 1.
        THEME_2 (list): The color theme 2.
        THEME_3 (list): The color theme 3.
        THEME_4 (list): The color theme 4.
        BENCHMARK_COLOR (str): The color for the benchmark line.
        BENCHMARK_LINE_TYPE (str): The line type for the benchmark line.
        TOTAL_COLOR (str): The color for the total line.
        BACKGROUND_COLOR (str): The background color of the chart.

    Methods:
        __init__(): Initializes a new instance of the ChartSettings class.
        make_color_iterator(): Creates an iterator for generating colors from a specified theme.
        make_base_layout_dict(): Creates a base layout dictionary for the chart.

    """

    THEME_1 = ["#ac0b3d", "#266295", "#5ab220", "#710c9e", "#ee983a"]
    THEME_2 = ["#75eab6", "#2c4e2f", "#759a76", "#bfdad4", "#daa4f9"]
    THEME_3 = ["#e456d8", "#9959ab", "#5ca0f7", "#2524f9", "#d8dc35"]
    THEME_4 = ["#683c00", "#fd191f", "#fab5b5", "#9b7d73", "#2cf52b"]

    BENCHMARK_COLOR = "#000000"
    BENCHMARK_LINE_TYPE = "markers"
    TOTAL_COLOR = "#000000"
    BACKGROUND_COLOR = "#ffffff"
    STACKED_CHARTS_OPACITY = 0.65
    TABLE_HEADER_COLOR = "#ac0b3d"
    FIRST_FORECAST_LINE_COLOR = "#85888a"
    OUTLINE_BUTTON_COLOR = '#0D1219'
    EA_RED = '#ac0b3d'

    def __init__(self):
        """
        Initializes a new instance of the ChartSettings class.
        """
        self.continuous_scheme = list(
            itertools.chain(
                VisualSettings.THEME_1,
                VisualSettings.THEME_2,
                VisualSettings.THEME_3,
                VisualSettings.THEME_4,
            )
        )

    def make_color_iterator(self):
        """
        Creates an iterator for generating colors from a specified theme.

        Args:
            theme (list, optional): The color theme to use. If not specified, the continuous_scheme will be used.

        Yields:
            str: The next color in the theme.

        """
        theme = self.continuous_scheme
        for color in itertools.cycle(theme):
            yield color

    def make_rgba_color_iterator(self, opacity):
        """This genreates colors with transparency
        It is to be used this way in the doc:
        line=dict(color=f'rgba{color_rgba}')
        """
        theme = self.continuous_scheme
        for color in itertools.cycle(theme):
            hex = color.lstrip('#')
            lv = len(hex)
            colors = list(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
            color_rgba = (colors[0], colors[1], colors[2], opacity)
            yield f'rgba{color_rgba}'

    @staticmethod
    def make_rgba_color(color, opacity):
        hex = color.lstrip('#')
        lv = len(hex)
        colors = list(int(hex[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        color_rgba = (colors[0], colors[1], colors[2], opacity)
        return f'rgba{color_rgba}'

    def make_base_layout_dict(self):
        """
        Creates a base layout dictionary for the chart.

        Returns:
            dict: The base layout dictionary.

        """
        legend = dict(
            orientation="h",
        )
        return {
            "hovermode": "x unified",
            "paper_bgcolor": self.BACKGROUND_COLOR,
            "plot_bgcolor": self.BACKGROUND_COLOR,
            "hoverlabel_namelength": -1,
            "legend": legend,
        }
