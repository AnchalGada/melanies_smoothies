import streamlit as st
from snowflake.snowpark.functions import col

# --------------------------------------------------
# App title
# --------------------------------------------------

st.title("🥤 Customize Your Smoothie! 🥤")

st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# --------------------------------------------------
# Get the name for the order
# --------------------------------------------------

name_on_order = st.text_input("Name on Smoothie")

st.write(
    "The name on your Smoothie will be:",
    name_on_order
)

# --------------------------------------------------
# Connect to Snowflake
# --------------------------------------------------

cnx = st.connection("snowflake")
session = cnx.session()

# --------------------------------------------------
# Get fruit options from Snowflake
# --------------------------------------------------

my_dataframe = (
    session.table("smoothies.public.fruit_options")
    .select(col("fruit_name"))
)

# Convert Snowpark result to a Python list
fruit_options = [
    row["FRUIT_NAME"]
    for row in my_dataframe.collect()
]

# --------------------------------------------------
# Select ingredients
# --------------------------------------------------

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

# --------------------------------------------------
# Create ingredient string
# --------------------------------------------------

if ingredients_list:

    ingredients_string = " ".join(ingredients_list)

    st.write("Your ingredients:", ingredients_string)

    # --------------------------------------------------
    # Submit Order
    # --------------------------------------------------

    if st.button("Submit Order"):

        # Escape single quotes
        safe_name = name_on_order.replace("'", "''")
        safe_ingredients = ingredients_string.replace("'", "''")

        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders
            (ingredients, name_on_order)
            VALUES ('{safe_ingredients}', '{safe_name}')
        """

        session.sql(my_insert_stmt).collect()

        st.success(
            "Your Smoothie is ordered!",
            icon="✅"
        )
