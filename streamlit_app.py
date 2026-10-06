# Import python packages

import streamlit as st
import requests
import pandas as pd

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

cnx = st.connection("snowflake")
session = cnx.session()


# Get the fruit options
# We now get BOTH FRUIT_NAME and SEARCH_ON

my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
)


# Convert the Snowpark DataFrame to a Pandas DataFrame

pd_df = my_dataframe.to_pandas()


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

        # Add the selected fruit to the ingredients string

        ingredients_string += fruit_chosen + " "


        # Find the SEARCH_ON value for the selected fruit

        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen,
            "SEARCH_ON"
        ].iloc[0]


        # Display the nutrition heading

        st.subheader(
            fruit_chosen + " Nutrition Information"
        )


        # Get nutrition information from SmoothieFroot API
        # Use SEARCH_ON instead of FRUIT_NAME

        smoothiefroot_response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )


        # Display nutrition information

        sf_df = st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )


    # Display selected ingredients

    st.write(ingredients_string)


    # Submit Order button

    time_to_insert = st.button("Submit Order")


    if time_to_insert:

        st.success(
            "Your Smoothie is ordered!",
            icon="✅"
        )
