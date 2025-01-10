# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruit that you want in your custom Smoothie!
    """
)

conection = st.connection("snowflake")
session = connection.session()
my_dataframe = session.table("smoothies.public.FRUIT_OPTIONS").select(col('FRUIT_NAME'))

#option = st.selectbox('What is your favourite fruit?', ('Banana','Strawberries', 'Peaches'))

#st.write('You have selected:', option)

#st.dataframe(data = my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on the Smoothie will be:', name_on_order)

ingredient_list = st.multiselect("Choose upto 5 ingridents: ", my_dataframe, max_selections=5)

time_to_insert = st.button("Submit Order")

if ingredient_list :
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredients = ''
    for fruit in ingredient_list:
        ingredients += fruit + ' '
    #st.write(ingredients)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, '+name_on_order+' !', icon="✅")
