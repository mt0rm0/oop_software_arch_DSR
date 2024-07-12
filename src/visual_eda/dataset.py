import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.config import Config

class Dataset:
    """
    A class to represent a dataset for analysis and visualization.

    Attributes
    ----------
    data : DataFrame
        The dataset loaded from a CSV file.
    name : str
        The name of the dataset derived from the filename.

    Methods
    -------
    __str__():
        Returns a string representation of the dataset.
    load_data(filename):
        Loads data from a CSV file.
    summary():
        Returns a summary DataFrame of the dataset.
    configure_plots():
        Configures the plot settings using the current configuration.
    colors():
        Property that returns the color palette from the Config.
    figure_face_color():
        Property that returns the figure face color from the Config.
    axes_face_color():
        Property that returns the axes face color from the Config.
    text_props():
        Property that returns the text properties from the Config.
    show_plot(column_name):
        Displays a donut and count plot for a specified column.
    _plot_donut_chart(ax, value_counts):
        Helper function to plot a donut chart.
    _plot_count_chart(ax, column_name, labels, value_counts):
        Helper function to plot a count chart.
    """

    def __init__(self, filename):
        """
        Constructs all the necessary attributes for the Dataset object.

        Parameters
        ----------
        filename : str
            The path to the CSV file containing the dataset.
        """
        self.data = self.load_data(filename)
        self.name = filename.split('.')[0].split('/')[-1]
        self.configure_plots()

    def __str__(self):
        """Returns a string representation of the dataset."""
        return f"The {self.name} dataset has {self.data.shape[0]} rows and {self.data.shape[1]} columns"

    def load_data(self, filename):
        """
        Loads data from a CSV file.
        TODO: Load data from an XLS file aswell.

        Parameters
        ----------
        filename : str
            The path to the CSV file.

        Returns
        -------
        DataFrame
            The loaded dataset.
        """
        return pd.read_csv(filename)

    def summary(self):
        """
        Returns a summary DataFrame of the dataset, excluding the 'id' column.

        Returns
        -------
        DataFrame
            A summary of the dataset.
        """
        df = self.data.drop(columns=["id"])
        summary = pd.DataFrame({
            'Data Type': df.dtypes,
            '# Missing': df.isnull().sum(),
            'Duplicate': [df.duplicated().sum()] * len(df.columns),
            '# Unique': df.nunique()
        })
        
        desc = df.describe(include='all').transpose()
        summary = summary.join(desc[['min', 'max', 'mean', 'std', 'top', 'freq']])
        summary.rename(columns={
            'mean': 'Avg',
            'std': 'Std Dev',
            'top': 'Top Value',
            'freq': 'Freq'
        }, inplace=True)
        
        return summary


    def configure_plots(self):
        """Configures the plot settings using the current configuration."""
        plt.rcParams['figure.facecolor'] = self.figure_face_color
        plt.rcParams['axes.facecolor'] = self.axes_face_color

    @property
    def colors(self):
        """
        Property that returns the color palette from the Config.
        
        The `@property` decorator allows a method to be accessed like an attribute.
        This means you can call 'self.colors' instead of 'self.colors()'.
        It is useful for:
            1. Encapsulation: Controlling access to private attributes.
            2. Read-Only Attributes: Making an attribute read-only.
            3. Dynamic Computation and Access: Calculating the attribute value 
            when accessed and allowing for accessing the updated value without 
            needing to reinstantiate the class. (Very useful for configurations that change a lot)
        
        Returns
        -------
        list
            The color palette.
        """
        return Config.COLORS

    @property
    def figure_face_color(self):
        """
        Returns the figure face color from the Config.

        Returns
        -------
        str
            The figure face color.
        """
        return Config.FIGURE_FACE_COLOR

    @property
    def axes_face_color(self):
        """
        Returns the axes face color from the Config.

        Returns
        -------
        str
            The axes face color.
        """
        return Config.AXES_FACE_COLOR

    @property
    def text_props(self):
        """
        Returns the text properties from the Config.

        Returns
        -------
        dict
            The text properties.
        """
        return Config.TEXT_PROPS

    def show_plot(self, column_name):
        """
        Displays a donut and count plot for a specified column.

        Parameters
        ----------
        column_name : str
            The name of the column to plot.
        """
        fig, ax = plt.subplots(1, 2, figsize=(10, 4))
        ax = ax.flatten()
        
        value_counts = self.data[column_name].value_counts()
        labels = value_counts.index.tolist()

        self._plot_donut_chart(ax[0], value_counts)
        self._plot_count_chart(ax[1], column_name, labels, value_counts)
        
        fig.suptitle(column_name, fontsize=15, fontweight='bold')
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        plt.show()

    def _plot_donut_chart(self, ax, value_counts):
        """
        Helper function to plot a donut chart.

        Parameters
        ----------
        ax : Axes
            The matplotlib axes object.
        value_counts : Series
            The value counts of the column.
        """
        wedges, texts, autotexts = ax.pie(
            value_counts, autopct='%1.1f%%', textprops=self.text_props, colors=self.colors,
            wedgeprops=dict(width=0.35), startangle=80, pctdistance=0.85)
        centre_circle = plt.Circle((0, 0), 0.6, fc='white')
        ax.add_artist(centre_circle)

    def _plot_count_chart(self, ax, column_name, labels, value_counts):
        """
        Helper function to plot a count chart.

        Parameters
        ----------
        ax : Axes
            The matplotlib axes object.
        column_name : str
            The name of the column to plot.
        labels : list
            The list of labels for the plot.
        value_counts : Series
            The value counts of the column.
        """
        palette = sns.color_palette(self.colors, len(labels))
        sns.countplot(data=self.data, y=column_name, ax=ax, hue=column_name, palette=palette, order=labels, legend=False)
        for i, v in enumerate(value_counts):
            ax.text(v + 1, i, str(v), color='black', fontsize=10, va='center')
        sns.despine(left=True, bottom=True)
        plt.yticks(fontsize=9, color='black')
        ax.set_ylabel(None)
        plt.xlabel("")
        plt.xticks([])