from bokeh.layouts import layout
from bokeh.embed import components

from .pressao_plot import PressaoPlot
from .graphs import LineGraph


class Pressao:
    def __init__(self):
        self.pressao_plot = PressaoPlot()
        self.pressao_plot.plot()
        self.plot = self.pressao_plot.plot

    def plot_graph(self):
        self.make_plots()
        self.make_components()

    def make_plots(self):
        source = self.pressao_plot.datasource

        self.make_line(x='date', y='pressao', line_color='blue',
                       legend='Pressão', name='pressao',
                       source=source.get('pressao'))

        self.make_line(x='date', y='pressao_hpa', line_color='gray',
                       legend='Pressão hpa', name='pressao_hpa',
                       source=source.get('pressao_hpa'))

    def make_line(self, x, y, line_color, legend, name, source):
        line_settings = dict(x=x, y=y, line_color=line_color,
                             legend=legend, plot=self.plot,
                             name=name, source=source)

        plot = LineGraph(**line_settings).get_line()
        setattr(self, 'plot', plot)

    def make_components(self):
        plot = layout([self.plot], sizing_mode='stretch_width')
        script, div = components(plot)
        plot_components = {'script': script, 'div': div}

        setattr(self, 'components', plot_components)

    def get_div(self):
        components = getattr(self, 'components')
        return components.get('div')

    def get_scripts(self):
        components = getattr(self, 'components')
        return components.get('script')
