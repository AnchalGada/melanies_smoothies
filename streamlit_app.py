# Import python packages

import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app

st.title("🥤 Customize Your Smoothie! 🥤")

st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Get the name for the order

name_on_order = st.text_input("Name on Smoothie")

st.write(
    "The name on your Smoothie will be:",
    name_on_order
)

# Get the active Snowflake session

session = get_active_session()

# Get the fruit options

my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(
    col("fruit_name")
)

# Uncomment this if you want to see the dataframe

# st.dataframe(data=my_dataframe, use_container_width=True)

# Multiselect

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# Create a string from the selected ingredients

if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    st.write(ingredients_string)

    # Create the INSERT statement
    # The table has two columns:
    # INGREDIENTS and NAME_ON_ORDER

    my_insert_stmt = """
        INSERT INTO smoothies.public.orders
        (ingredients, name_on_order)
        VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')
    """

    # Show the SQL statement for testing

    st.write(my_insert_stmt)

    # Submit Order button

    time_to_insert = st.button("Submit Order")

    if time_to_insert:

        session.sql(my_insert_stmt).collect()

        st.success(
            "Your Smoothie is ordered!",
            icon="✅"
        )

   
