import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')

# Clean data
df = df.set_index('date')
upper = df['value'] <= df['value'].quantile(0.975) 
lower = df['value'] >= df['value'].quantile(0.025)
df = df[upper & lower]


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(20,5))
    sns.lineplot(x=df.index, y='value', data=df)
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['Year'] = df_bar['date'].map(lambda x: int(x.split('-')[0]))
    df_bar['Month'] = df_bar['date'].map(lambda x: int(x.split('-')[1]))
    df_bar.drop(['date'], inplace=True, axis=1)
    df_bar = df_bar.groupby(['Year','Month'])['value'].mean().to_frame().sort_values(by=['Year','Month']).reset_index()
    
    # Draw bar plot
    fig = plt.figure(figsize=(8,8))
    sns.barplot(x='Year', y='value', hue='Month', data=df_bar)
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    import datetime
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['date'] = [datetime.datetime.strptime(d, "%Y-%m-%d") for d in df_box["date"]]
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1,2, figsize=(15,6))
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    axes[0].title.set_text("Year-wise Box Plot (Trend)")

    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    axes[1].title.set_text("Month-wise Box Plot (Seasonality)")




    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    
    return fig