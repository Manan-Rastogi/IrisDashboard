from sklearn import datasets
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Load the Iris dataset
iris = datasets.load_iris()
df = pd.DataFrame(data=iris['data'], columns=iris['feature_names'])
df['species'] = iris['target']
df['species'] = df['species'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})

def generate_histogram():
    fig = px.histogram(df, x='species', color='species', labels={'species': 'Species'}, title='Histogram of Species Counts')
    fig.show()
    return fig.to_html()

def generate_line_chart(species, feature):
    filtered_df = df[df['species'] == species]
    fig = px.line(filtered_df, x=feature, y=feature)
    return fig.to_json()

def generate_csv_data(species, feature, bin_start, bin_end):
    filtered_df = df[(df['species'] == species) & (df[feature] >= bin_start) & (df[feature] < bin_end)]
    csv_data = filtered_df.to_csv(index=False)
    return csv_data

