from preswald import connect, get_df, query, table, text, plotly
import plotly.express as px
import pandas as pd

# Load dataset
connect()
df = get_df("my_dataset")

# Dashboard intro
text("# Education Cost Analysis Dashboard")
text("This dashboard analyzes the cost of higher education globally. It includes tuition, rent, visa, and insurance data across universities.")

table(df, title="Dataset Preview")

# Query (optional filter)
sql = "SELECT * FROM my_dataset WHERE Tuition_USD > 60000"
filtered_df = query(sql, "my_dataset")

# Scatter plot
text("## Tuition vs Rent")
text("This chart compares tuition fees and monthly rent for universities by country to examine relative education and living costs.")
fig = px.scatter(df, x="Tuition_USD", y="Rent_USD", color="Country", text="University", title="Tuition vs Rent by Country")
plotly(fig)



# Prepare numeric columns and compute total cost
text("## Total Cost Calculation")
text("Total cost is calculated by summing tuition, 12 months rent, visa fees, and insurance for each university entry.")
df["Tuition_USD"] = pd.to_numeric(df["Tuition_USD"], errors="coerce")
df["Rent_USD"] = pd.to_numeric(df["Rent_USD"], errors="coerce")
df["Visa_Fee_USD"] = pd.to_numeric(df["Visa_Fee_USD"], errors="coerce")
df["Insurance_USD"] = pd.to_numeric(df["Insurance_USD"], errors="coerce")
df["Total_Cost_USD"] = df["Tuition_USD"] + (df["Rent_USD"] * 12) + df["Visa_Fee_USD"] + df["Insurance_USD"]

# Pie chart by city
text("## Total Cost by City")
text("This pie chart displays the top 7 cities where total education cost is highest based on all combined expense components.")
city_costs = df.groupby("City")["Total_Cost_USD"].sum().reset_index()
city_costs = city_costs.sort_values(by="Total_Cost_USD", ascending=False).head(7)
table(city_costs, title="Top Cities by Cost")
pie = px.pie(city_costs, values="Total_Cost_USD", names="City", title="Top 7 Cities by Total Cost", hole=0.4, template="plotly_white")
pie.update_traces(textinfo='percent+label')
plotly(pie)

# Choropleth heatmap
text("## Avg Cost by Country")
text("This choropleth map shows the average total education cost per country and highlights geographic cost differences worldwide.")
country_costs = df.groupby("Country")["Total_Cost_USD"].mean().reset_index()
heatmap = px.choropleth(
    country_costs,
    locations="Country",
    locationmode="country names",
    color="Total_Cost_USD",
    color_continuous_scale="OrRd",
    title="Average Total Cost by Country",
    labels={"Total_Cost_USD": "Avg Cost (USD)"},
    template="plotly_white"
)
heatmap.update_layout(geo=dict(showframe=False, showcoastlines=True))
plotly(heatmap)



# Bar chart for tuition
text("## Avg Tuition by Country")
text("This bar chart ranks the top 10 countries by their average tuition costs to identify expensive education destinations.")
tuition_by_country = df.groupby("Country")["Tuition_USD"].mean().reset_index()
tuition_by_country = tuition_by_country.sort_values(by="Tuition_USD", ascending=False).head(10)
bar = px.bar(tuition_by_country, x="Country", y="Tuition_USD", title="Top 10 Countries by Tuition", template="plotly_white")
bar.update_layout(xaxis_tickangle=-45)
plotly(bar)

# Maplibre-themed choropleth
text("## Maplibre Visualization")
text("A map using a thermal scale and dark theme to visualize average total cost by country with a distinct stylized appearance.")
maplibre_map = px.choropleth(
    country_costs,
    locations="Country",
    locationmode="country names",
    color="Total_Cost_USD",
    color_continuous_scale="thermal",
    title="Maplibre Style Cost Map",
    labels={"Total_Cost_USD": "Avg Cost (USD)"},
    template="plotly_dark"
)
maplibre_map.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='natural earth'
    )
)
plotly(maplibre_map)

