import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time # to stimulate real time data

df = pd.read_csv('pop_worldometer_data.csv')

st.set_page_config(
    page_title='Live Population Analysis',
    page_icon='',
    layout='wide'
)

# dashboard title
st.title('Live Population Analysis')

# filters
country_filter = st.sidebar.selectbox("Select the Country", pd.unique(df['Country (or dependency)']))

# hold everything together by not changing the location
placeholder = st.empty()

# dataframe filter
df = df[df['Country (or dependency)'] == country_filter]

# near real time stimulation
for seconds in range(200):

    # metric
    df['New_Land_Area (Km²)'] = df['Land Area (Km²)'] * np.random.choice(range(1,10),  len(df))
    df['New_Urban_Pop %'] = df['Urban Pop %'] * np.random.choice(range(1,10),  len(df))

#     creating KPIs
    Population_Density = df['Population (2020)'] / df['New_Land_Area (Km²)']
    Urban_Population_Rate = df['New_Urban_Pop %']
    Median_Age = df['Med. Age']*np.random.choice(range(1,10))

    with placeholder.container():
        kpi1, kpi2, kpi3 = st.columns(3)

        # filling 3 columns with their respective KPIs
        kpi1.metric(label='Population Density', value=round(Population_Density.mean(), 2), delta=round(Population_Density.mean() - 10, 2))
        kpi2.metric(label='Urban Population Rate', value=round(Urban_Population_Rate.mean(), 2), delta=round(Urban_Population_Rate.mean() - 10, 2))
        kpi3.metric(label='Age', value=round(Median_Age.mean(), 2), delta=round(Median_Age.mean() - 10))

#       create two columns for charts
        kpi_data = pd.DataFrame({
            'Country': df['Country (or dependency)'],
            'Population Density': Population_Density,
            'Urban Population Rate': Urban_Population_Rate
        })

        # Melt the DataFrame for easier plotting
        kpi_data_melted = kpi_data.melt(id_vars='Country', value_vars=['Population Density', 'Urban Population Rate'])

        # Create the bar chart
        fig = px.bar(kpi_data_melted,
                     x='Country',
                     y='value',
                     color='variable',
                     title='Population Density and Urban Population Rate',
                     labels={'value': 'Value'},
                     barmode='group')

        # Display the chart with a unique key
        # To avoid the duplicate key issue, ensure the plot is only created once.
        if 'population_density_urban_rate_chart' not in st.session_state:
            st.session_state['population_density_urban_rate_chart'] = True  # Set a flag

        st.plotly_chart(fig, key=f'population_density_urban_rate_chart_{np.random.randint(1000)}')

        st.markdown('### Detailed Data View')
        st.dataframe(df)
        time.sleep(1)

