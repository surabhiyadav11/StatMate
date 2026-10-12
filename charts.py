import plotly.express as px
import plotly.graph_objects as go

# Common Layout settings for academic white theme
LAYOUT_CONFIG = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color="#111827"),
    margin=dict(l=40, r=40, t=40, b=40),
)

def apply_academic_axes(fig):
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E7EB', zeroline=True, zerolinecolor='#E5E7EB')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E7EB', zeroline=True, zerolinecolor='#E5E7EB')
    fig.update_layout(**LAYOUT_CONFIG)
    return fig

def plot_histogram(df, column, title, x_label):
    fig = px.histogram(
        df, 
        x=column, 
        title=title,
        color_discrete_sequence=['#4F46E5'],
        opacity=0.8
    )
    fig.update_layout(xaxis_title=x_label, yaxis_title="Frequency")
    return apply_academic_axes(fig)

def plot_boxplot(df, x_col, y_col, title):
    fig = px.box(
        df, 
        x=x_col, 
        y=y_col, 
        title=title,
        color_discrete_sequence=['#4F46E5']
    )
    return apply_academic_axes(fig)

def plot_line_chart(df, x_col, y_col, title, group_col=None):
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=group_col,
        title=title,
        color_discrete_sequence=px.colors.sequential.Indigo
    )
    return apply_academic_axes(fig)

def plot_bar_chart(df, x_col, y_col, title):
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title,
        color_discrete_sequence=['#4F46E5']
    )
    return apply_academic_axes(fig)

def plot_distribution_curve(df, x_col, y_col, title, is_discrete=False):
    if is_discrete:
        fig = px.bar(df, x=x_col, y=y_col, title=title, color_discrete_sequence=['#4F46E5'])
    else:
        fig = px.line(df, x=x_col, y=y_col, title=title, color_discrete_sequence=['#4F46E5'])
        fig.update_traces(fill='tozeroy')
    
    fig.update_layout(xaxis_title="Value (x)", yaxis_title="Probability Density / Mass")
    return apply_academic_axes(fig)
