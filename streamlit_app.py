# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruit that you want in your custom Smoothie!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write('The name on the Smoothie will be:', name_on_order)

connection = st.connection("snowflake")
session = connection.session()

my_dataframe = session.table("smoothies.public.FRUIT_OPTIONS").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

#option = st.selectbox('What is your favourite fruit?', ('Banana','Strawberries', 'Peaches'))

#st.write('You have selected:', option)

#st.dataframe(data = my_dataframe, use_container_width=True)

ingredient_list = st.multiselect("Choose upto 5 ingridents: ", my_dataframe, max_selections=5)

time_to_insert = st.button("Submit Order")

if ingredient_list :
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredients = ''
    for fruit in ingredient_list:
        ingredients += fruit + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit,' is ', search_on, '.')
        st.subheader(fruit+' Nutrition Information')
        my_smoothiee_fruit = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_df = st.dataframe(data=my_smoothiee_fruit.json(), use_container_width = True)
    #st.write(ingredients)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, '+name_on_order+' !', icon="✅")
