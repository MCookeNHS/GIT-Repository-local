import streamlit as st
import re


st.title("Monthly Budget Calculator")

# one or two decinam places
pattern = r'^\d+(\.\d{1,2})?$'


# Get inputs from user, cast as integers and store in variables
name = st.text_input("What's your name?")
if name:
    st.write("Hello", name)

monthly_take_home = st.text_input("What's your monthly take home income?",
value=0)
if monthly_take_home.isdigit():
    st.write("£",monthly_take_home," income per month")
else:
    st.write("Please Enter a Whole Number")

housing_costs = st.text_input("What's your monthly housing cost (rent/mortgage)?",
value=0)
# if housing_costs:
#     st.write("£",housing_costs," housing costs per month")
if re.match(pattern, housing_costs):
    housing_costs = float(housing_costs)  # Convert to float
    st.write("£", f"{housing_costs:.2f}", " housing costs per month")  # Display formatted to 2 decimal
else:
    st.write("Please enter a valid number with up to 2 decimal places.")

food_costs = st.text_input("How much do you spend on food per month?",
value=0)
if re.match(pattern, food_costs):
    food_costs = float(food_costs)  # Convert to float
    st.write("£", f"{food_costs:.2f}", " food costs per month")  # Display formatted to 2 decimal
else:
    st.write("Please enter a valid number with up to 2 decimal places.")

utility_costs = st.text_input("How much do you spend on utilities per month?",
value=0)
if re.match(pattern, utility_costs):
    utility_costs = float(utility_costs)  # Convert to float
    st.write("£", f"{utility_costs:.2f}", " utility costs per month")  # Display formatted to 2 decimal
else:
    st.write("Please enter a valid number with up to 2 decimal places.",
value=0)

# Calculate remaining money after housing, food and utility costs
remaining = (float(monthly_take_home) - float(housing_costs) - float(food_costs) - float(utility_costs))

# Calculate the percentage of take home that housing costs represent
# if all(isinstance(x, float) for x in [monthly_take_home, housing_costs, food_costs, utility_costs]):
if float(monthly_take_home) > 0:
    housing_perc = (float(housing_costs) / float(monthly_take_home))*100
else: housing_perc = 0

# Print the message to the user
if float(housing_perc) > 0:
    st.write(
        "Your monthly amount after housing, food and utility costs is",
        "£",f"{remaining}.  Your housing costs represent ",f"{housing_costs:.2f}%",
        "of your monthly take home.")




## go to file location in terminal then run file from commmane line
# cd "OneDrive - NHS\HSMA\Module 7 - GIT\23 - Web apps"
# py -m streamlit run test.py
# ctrl + c to quit streamlit