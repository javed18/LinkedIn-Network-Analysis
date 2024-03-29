import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
#from fuzzywuzzy import fuzz
import plotly.express as px

# You will get your LinkedIn Connections data in csv format
# df is your DataFrame with columns: First Name, Last Name, Company, Position
df = pd.read_csv('/path/Connections.csv')
connection_data = df.to_dict('records')

# Mapping of seniority levels to their respective weights
seniority_weights = {
    "CEO/Founder/Head": 7,
    "Vice President/Lead": 6,
    "Assistant Vice President/Scientist": 5,
    "Senior Manager/Senior Engineer": 4,
    "Manager/Analyst/Engineer": 3,
    "Assistant Manager/Deputy Manager": 2,
    "Staff/Unknown": 1,
}

# Function to map position strings to seniority levels
def map_position_to_seniority(position):
    if not isinstance(position, str):
        return "Staff/Unknown"  # Default to "Staff/Unknown" if position is not a string
    position = position.lower()
    if "head" in position or "chief" in position or "ceo" in position or "founder" in position:
        return "CEO/Founder/Head"
    elif "assistant vice president" in position or "scientist" in position:
        return "Assistant Vice President/Scientist"
    elif "vice president" in position or "lead" in position  or "vp" in position:
        return "Vice President/Lead"
    elif "senior manager" in position or "senior" in position:
        return "Senior Manager/Senior Engineer"
    elif "manager" in position or "analyst" in position or "engineer" in position:
        return "Manager/Analyst/Engineer"
    elif "assistant manager" in position or "deputy manager" in position:
        return "Assistant Manager/Deputy Manager"
    else:
        return "Staff/Unknown"

# Create a graph
G = nx.Graph()

# Dictionary to store actual person details
person_details = {}

# Add nodes for connections with attributes (company, position)
for idx, connection in enumerate(connection_data):
    person_id = "C" + str(idx + 1)
    name = connection["First Name"] + " " + connection["Last Name"]
    company = connection["Company"]
    position = connection["Position"]
    seniority_level = map_position_to_seniority(position)
    G.add_node(person_id, company=company, position=position, seniority=seniority_level)
    person_details[person_id] = {"name": name, "company": company, "position": position, "seniority": seniority_level}

# Create DataFrame from connection data
df_person = pd.DataFrame(connection_data)

# Company dominance treemap
company_counts = df_person['Company'].value_counts()
company_counts_df = pd.DataFrame({'Company': company_counts.index, 'Count': company_counts.values})
fig_company = px.treemap(company_counts_df, path=['Company'], values='Count')
fig_company.update_layout(
    title={
        'text': "Company Dominance in Network",
        'x': 0.5,
        'y': 0.9,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

# Position dominance treemap
position_counts = df_person['Position'].value_counts()
position_counts_df = pd.DataFrame({'Position': position_counts.index, 'Count': position_counts.values})
fig_position = px.treemap(position_counts_df, path=['Position'], values='Count')
fig_position.update_layout(
    title={
        'text': "Position Dominance in Network",
        'x': 0.5,
        'y': 0.9,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

# Seniority dominance treemap
df_person['Seniority'] = df_person['Position'].apply(map_position_to_seniority)
seniority_counts = df_person['Seniority'].value_counts()
seniority_counts_df = pd.DataFrame({'Seniority': seniority_counts.index, 'Count': seniority_counts.values})
fig_seniority = px.treemap(seniority_counts_df, path=['Seniority'], values='Count')
fig_seniority.update_layout(
    title={
        'text': "Seniority Dominance in Network",
        'x': 0.5,
        'y': 0.9,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

# Visualize
plt.figure(figsize=(14, 7))
plt.show()
fig_company.show()
fig_position.show()
fig_seniority.show()

# Output - person details for high seniority
high_seniority_dict = {k: v for k, v in person_details.items() if v['seniority'] in ["CEO/Founder/Head", "Vice President/Lead"]}
print("High Seniority Level:")
for person_id, details in high_seniority_dict.items():
    print(person_id + ":", details)

# Output - person details for low seniority
low_seniority_dict = {k: v for k, v in person_details.items() if v['seniority'] not in ["CEO/Founder/Head", "Vice President/Lead"]}
print("\nLow Seniority Level:")
for person_id, details in low_seniority_dict.items():
    print(person_id + ":", details)
