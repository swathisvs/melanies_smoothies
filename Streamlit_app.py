# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)
import streamlit as st

name_on_order = st.text_input("Name on Smooothie:")
st.write("The name on your smoothie will be :", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop 

#convert the snowpark dataframe to pandas dataframe so we can use LOC functions
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
   
    ingredients_string =''
    
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width = True)


