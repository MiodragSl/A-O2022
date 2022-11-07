import streamlit as st
import pandas as pd
import io
import datetime as dt
pd.options.plotting.backend = 'plotly'
import plotly.express as px

customer_df = pd.read_csv('Customers.csv')
products_df = pd.read_csv('Products.csv')
superstore_df = pd.read_csv('SuperStore.csv')

customer_head = customer_df.head(3)
products_head = products_df.head(3)
superstore_head = superstore_df.head(3)

st.set_page_config(page_title="Superstore sales")
st.subheader("Tasks: ")
st.markdown(
    "1. Download file \"Sample-Superstore-Homework.xls\"\n"
    "2. Data capturing, cleaning and preparation\n"
    "3. Data analysis and visualization\n"
    "4. Diagnostic analytics\n\n"
    )
st.markdown(
    """
    Bonus:
    - Check contextual outliers (sales per Product category)
    - Prepare dashboard
    """
    )
st.markdown("""---""")
task_1 = st.header("Task 1 - CSV to Pandas dataframe")
st.markdown(
    """
    The file \"Sample-Superstore-Homework.xls\" was downloaded and every worksheet was converted into csv file.
    """
)

st.write(
    """
    Dataframes have been created from .csv files in Python with Pandas library. Example: 
    """
)

st.code(
    """
import pandas as pd
customer_df = pd.read_csv("customer.csv")
customer_head = customer_df.head(3)
...
    """
)

show_tables = st.checkbox("Click to show created dataframes")

if show_tables == True:
    st.subheader(
    """
        Customer.csv
    """
    )
    st.table(customer_head)

    st.subheader(
    """
        Products.csv
    """
    )
    st.table(products_head)

    st.subheader(
    """
        SuperStore.csv
    """
    )
    st.table(superstore_head)
st.markdown("""---""")

task_2 = st.header("Task 2 - Data Capturing, Clearing and Preparation")

st.markdown(
    """
    First of all, we need to see which kind of data we are dealing with. \n
    """
)

st.subheader("customer.csv")

show_meta1 = st.checkbox("Click to show metadata for customer.csv")
if show_meta1 == True:
    buffer = io.StringIO()
    customer_info = customer_df.info(buf=buffer)
    cus_info = buffer.getvalue()
    st.code(cus_info)

    
    
    info = customer_df.pivot_table(columns=['Segment'],aggfunc='size')
    st.code(info)

    info1 = customer_df.pivot_table(columns=['Country'],aggfunc='size')
    st.code(info1)

    info2 = customer_df.pivot_table(columns=['City'],aggfunc='size')
    st.code(info2)

    info3 = customer_df.pivot_table(columns=['State'],aggfunc='size')
    st.code(info3)

    info4 = customer_df.pivot_table(columns=['Postal Code'],aggfunc='size')
    st.code(info4)

    info5 = customer_df.pivot_table(columns=['Region'],aggfunc='size')
    st.code(info5)

st.markdown(
    """
    Customer dataframe contains 8 columns of data and all of them are NOMINAL. There are no missing data. \n
    """
)
st.subheader("products.csv")

show_meta2 = st.checkbox("Click to show metadata for products.csv")
if show_meta2 == True:
    buffer1 = io.StringIO()
    products_info = products_df.info(buf=buffer1)
    pro_info = buffer1.getvalue()
    st.code(pro_info)

st.markdown(
    """
    Products dataframe contains 4 columns of data and all of them are NOMINAL. There are no missing data. \n

    """
)

st.subheader("superstore.csv")

show_meta3 = st.checkbox("Click to show metadata for superstore.csv")
if show_meta3 == True:
    buffer2 = io.StringIO()
    superstore_info = superstore_df.info(buf=buffer2)
    sup_info = buffer2.getvalue()
    st.code(sup_info)

st.markdown(
    """
    Dataframe contains 11 columns of data and all of them are NOMINAL except Sales, Quantity, Discount, and Profit which are SCALE. There are no missing data. \n
    """
)

st.markdown("""---""")
st.header("Task 3 - Data analysis and visualization")
st.subheader("Lag time task")

superstore_df[['Order Date','Ship Date']] = superstore_df[['Order Date','Ship Date']].apply(pd.to_datetime)
superstore_df['Lag time'] = (superstore_df['Ship Date'] - superstore_df['Order Date']).dt.days
superstore_df['Year'] = pd.DatetimeIndex(superstore_df['Ship Date']).year
superstore_df['Ship Mode'] = superstore_df['Ship Mode'].str.replace('Stnadard Class','Standard Class')
superstore_df['Ship Mode'] = superstore_df['Ship Mode'].astype("string")


superstore_df = superstore_df.drop(superstore_df[superstore_df['Lag time'] > 8].index)


lag_df = superstore_df.groupby(["Year","Ship Mode"])["Lag time"].mean()

lagdf = pd.DataFrame(lag_df)

lagdf = lagdf.reset_index(level=[0,1])


st.markdown("""
    Firstly I have converted columns Order Date and Ship date to date format. Then I have
    added a new column which represent difference between Order Date and Ship date. After inspecting newly
    created column I have noticed that there is one shipment that last 16438 days. That must be some unsatisfied
    customer!

    There was a mistake with year input. 2061 corrected to 2016.

    I have also noticed that Ship Mode contains spelling error. So Stnadard Class was corrected to Standard Class.
""")

info6 = superstore_df.pivot_table(columns=['Lag time'],aggfunc='size')
st.code(info6)
st.write(lagdf)

fig = px.histogram(lagdf, x='Year', y='Lag time', color='Ship Mode', barmode='group')

st.plotly_chart(fig)

st.markdown("""
    We can see that Lag Time between classes is consistent throughout the years, but we can see that in year 2018
    there are only Second Class and Standard Class. \n

    Lets see how Lag time looks like by Ship Mode: 
""")

StandardClass_box = superstore_df[(superstore_df['Ship Mode'] == 'Standard Class')]
StandardClass_figure = px.box(StandardClass_box, title="Standard Class", y="Lag time")
st.plotly_chart(StandardClass_figure)

sameday_box = superstore_df[(superstore_df['Ship Mode'] == 'Same Day')]
sameday_figure = px.box(sameday_box, title="Same day", y="Lag time")
st.plotly_chart(sameday_figure)

firstClass_box = superstore_df[(superstore_df['Ship Mode'] == 'First Class')]
firstClass_figure = px.box(firstClass_box, title="First Class", y="Lag time")
st.plotly_chart(firstClass_figure)

secondClass_box = superstore_df[(superstore_df['Ship Mode'] == 'Second Class')]
secondClass_figure = px.box(secondClass_box, title="Second Class", y="Lag time")
st.plotly_chart(secondClass_figure)

st.subheader("Products by Order task")

order_df = superstore_df.groupby(["Order ID"])["Product ID"].count()
order_df = order_df.reset_index(level=[0])
order_df = order_df["Product ID"].value_counts()
order_df = order_df.reset_index(level=[0])
order_df.rename(columns={'index':'Number of Products'}, inplace = True)
order_df.rename(columns={'Product ID':'Frequency'}, inplace = True)
order_plot = px.bar(order_df, x='Number of Products', y='Frequency')
st.plotly_chart(order_plot)

st.markdown(
    """
    Number of products per order. 
    """
)

st.subheader("Number of orders per customer task")

cusor = superstore_df.drop_duplicates(subset=['Order ID'])
cusor = superstore_df.groupby(["Customer ID"])["Order ID"].count()
cusor = cusor.reset_index(level=[0])
num_cus = cusor['Order ID'].value_counts()
num_cus = num_cus.reset_index()
num_cus.rename(columns={'index':'Number of orders by a customer'}, inplace = True)
num_cus.rename(columns={'Order ID':'Number of customers'}, inplace = True)
num_cus = num_cus.sort_values(by=['Number of orders by a customer'])
num_cus_plot = px.bar(num_cus, x='Number of orders by a customer', y='Number of customers')
st.plotly_chart(num_cus_plot)

cusor = cusor.sort_values(by=['Order ID'], ascending=False)
newdf = cusor.merge(customer_df[['Customer ID','Customer Name']], left_on='Customer ID', right_on='Customer ID').drop('Customer ID', axis='columns')
ae = newdf.drop_duplicates()
ae = ae.reset_index(level=[0])
ae = ae[['Customer Name', 'Order ID']].head(10)

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.table(ae)


st.markdown("""
    William Brown is the customer with the most orders!
""")
