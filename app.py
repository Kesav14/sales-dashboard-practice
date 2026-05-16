import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title='Sales Dashboard',
                   page_icon=':bar_chart:',
                   layout='wide')

def get_data_from_excel():
  df=pd.read_excel(
    io='supermarkt_sales.xlsx',
    engine='openpyxl',
    sheet_name='Sales',
    skiprows=3,
    usecols='B:R',
    nrows=1004,
  )

  df['hour']=pd.to_datetime(df['Time'],format='%H:%M:%S').dt.hour
  return df

df=get_data_from_excel()


st.sidebar.header('Please filter here:')
city= st.sidebar.multiselect(
  'Select the city:',
  options=df['City'].unique(),
  default=df['City'].unique()
)

customer_type= st.sidebar.multiselect(
  'Select customer type:',
  options=df['Customer_type'].unique(),
  default=df['Customer_type'].unique()
)


gender= st.sidebar.multiselect(
  'Select gender:',
  options=df['Gender'].unique(),
  default=df['Gender'].unique()
)

df_selection= df.query(
  'City in @city & Customer_type in @customer_type & Gender in @gender '
)

st.title(':bar_chart: Sales Dashboard')
st.markdown('##')


total_sales = df_selection['Total'].sum()
average_rating=round(df_selection['Rating'].mean(),1) if not df_selection.empty else 0
star_rating=':star:' * int(round(average_rating,0))
average_sales=round(df_selection['Total'].mean(),2) if not df_selection.empty else 0

left_column,middle_column,right_column=st.columns(3)
with left_column:
  st.subheader('Total sales:')
  st.subheader(f'US $ {total_sales:,}')

with middle_column:
  st.subheader('Average Rating:')
  st.subheader(f'{average_rating} {star_rating}')

with right_column:
  st.subheader('Average Sales:')
  st.subheader(f'US $ {average_sales}')

st.markdown('---')


sales_by_product=(
  df_selection.groupby(by=['Product line'])[['Total']].sum().sort_values(by='Total')

)

fig_product_sales = px.bar(
  sales_by_product,
  x='Total',
  y=sales_by_product.index,
  title='<b>Sales by Product Line</b>',
  color_discrete_sequence=['#0083B8'] * len(sales_by_product),
  template='plotly_white'
)

fig_product_sales.update_layout(
  plot_bgcolor='rgba(0,0,0,0)',
  xaxis=(dict(showgrid=False))
)



sales_by_hour=df_selection.groupby(by=['hour'])[['Total']].sum()
fig_hourly_sales=px.bar(
  sales_by_hour,
  x=sales_by_hour.index,
  y='Total',
  title='<b>Sales by hour</b>',
  color_discrete_sequence=['#0083B8'] * len(sales_by_hour),
  template='plotly_white',
)

fig_hourly_sales.update_layout(
  xaxis=dict(tickmode='linear'),
  plot_bgcolor='rgba(0,0,0,0)',
  yaxis=(dict(showgrid=False)),
)

left_column,right_column= st.columns(2)
left_column.plotly_chart(fig_hourly_sales,use_container_width=True)
right_column.plotly_chart(fig_product_sales,use_container_width=True)


hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)