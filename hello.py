from preswald import text, plotly, connect, get_df, table, query, slider, checkbox, separator, selectbox
import pandas as pd
import plotly.express as px


connect()
df = get_df('cbb25_csv')

text("# 2024-25 NCAA Men's Basketball Season")
separator()
threshold = slider("Top N teams", min_val=1, max_val=364, default=25)
separator()
text("## Advanced Statistics")

ADJOE_shown = checkbox(label="ADJOE - Adjusted Offensive Efficiency", size=0.5)
ADJDE_shown = checkbox(label="ADJDE - Adjusted Defensive Efficiency", size=0.5)
BARTHAG_shown = checkbox(label="BARTHAG - Power Rating (chance to beat average D1 team)", size=0.5)
EFG_O_shown = checkbox(label="EFG_O - Effective Field Goal Percentage Shot", size=0.5)
EFG_D_shown = checkbox(label="EFG_D - Effective Field Goal Percentage Allowed", size=0.5)
TOR_shown = checkbox(label="TOR - Turnover Rate", size=0.5)

df.rename(columns={"RK": "Rank", "CONF": "Conference", "G": "Games", "W": "Wins"}, inplace=True)

columns = ["Rank", "Team", "Conference", "Games", "Wins"]
if ADJOE_shown:
    columns.append("ADJOE")
if ADJDE_shown:
    columns.append("ADJDE")
if BARTHAG_shown:
    columns.append("BARTHAG")
if EFG_O_shown:
    columns.append("EFG_O")
if EFG_D_shown:
    columns.append("EFG_D")
if TOR_shown:
    columns.append("TOR")

separator()
table(df[df["Rank"] <= threshold][columns], title="Dynamic Data View")
separator()
text("## Statistical Relationships")

possible_options = ["Offensive Efficiency", "Defensive Efficiency", "Power Rating", "EFG Shot", "EFG Allowed", "Turnover Rate"]
option_map = {"Offensive Efficiency":"ADJOE", "Defensive Efficiency":"ADJDE", "Power Rating":"BARTHAG", "EFG Shot":"EFG_O", "EFG Allowed":"EFG_D", "Turnover Rate":"TOR"}

choice_x = selectbox(
    label="Choose x-axis",
    options=possible_options,
    size=0.5
)

choice_y = selectbox(
    label="Choose y-axis",
    options=possible_options,
    size=0.5
)

x_col = option_map[choice_x]
y_col = option_map[choice_y]

sql = f"SELECT * FROM cbb25_csv WHERE RK <= {threshold}"
filtered_df = query(sql, "cbb25_csv")

# Create a scatter plot
fig = px.scatter(filtered_df, x=x_col, y=y_col, text='Team',
                 title=f'{choice_x} vs {choice_y}',
                 labels={x_col: choice_x, y_col: choice_y})

# Add labels for each point
fig.update_traces(textposition='top center', marker=dict(size=12, color='orange'))

# Style the plot
fig.update_layout(template='plotly_white')

# Show the plot
plotly(fig)
