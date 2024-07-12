import seaborn as sns
import pandas as pd

class Config:
    COLORS = ["#4caba4", "#d68c78", '#a3a2a2', '#ab90a0', '#e6daa3', '#6782a8', '#8ea677']
    FIGURE_FACE_COLOR = 'white'
    AXES_FACE_COLOR = 'white'
    TEXT_PROPS = {'size': 9, 'color': 'white', 'fontweight': 'bold'}
    #Seaborn settings for visualizations!
    rc = {
        "axes.facecolor": "#f7f9fc",
        "figure.facecolor": "#f7f9fc",
        "axes.edgecolor": "#000000",
        "grid.color": "#EBEBE7",
        "font.family": "serif",
        "axes.labelcolor": "#000000",
        "xtick.color": "#000000",
        "ytick.color": "#000000",
        "grid.alpha": 0.4
    }

    default_palette = 'YlOrRd'

    sns.set_theme(rc=rc)
    pd.set_option('display.max_columns',35)
    pd.options.display.float_format = '{:,.2f}'.format
