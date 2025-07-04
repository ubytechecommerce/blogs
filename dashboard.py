import os
import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Carrega os dados da planilha gerada pelo seu script
posts_path = "automacao_total_stephanie.xlsx"
df = pd.read_excel(posts_path, sheet_name="Postagens")
df_blogs = pd.read_excel(posts_path, sheet_name="Blogs")

def get_html_path(row):
    blog_name = df_blogs[df_blogs["Blog ID"] == row["Blog ID"]]["Nome do Blog"].values[0]
    folder = os.path.join("posts_html", blog_name.replace(" ", "_"), str(row["Data Programada"]))
    slug = "".join([c if c.isalnum() else "_" for c in row["Título do Post"]])[:40]
    return os.path.join(folder, slug + ".html")

df["HTML Path"] = df.apply(get_html_path, axis=1)

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Painel de Posts dos Blogs"),
    html.Label("Filtrar por Blog:"),
    dcc.Dropdown(
        id='blog-filter',
        options=[{"label": n, "value": n} for n in df_blogs["Nome do Blog"]],
        value=None,
        multi=True,
        placeholder="Selecione o(s) blog(s)"
    ),
    html.Label("Filtrar por Status:"),
    dcc.Dropdown(
        id='status-filter',
        options=[{"label": s, "value": s} for s in df["Status"].unique()],
        value=None,
        multi=True,
        placeholder="Selecione status"
    ),
    html.Br(),
    html.Div(id="post-count"),
    dash_table.DataTable(
        id='posts-table',
        columns=[
            {"name": "Blog", "id": "Blog"},
            {"name": "Data", "id": "Data Programada"},
            {"name": "Título", "id": "Título do Post"},
            {"name": "Status", "id": "Status"},
            {"name": "HTML", "id": "HTML Link", "presentation": "markdown"}
        ],
        data=[],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
    )
])

@app.callback(
    [Output('posts-table', 'data'),
     Output('post-count', 'children')],
    [Input('blog-filter', 'value'),
     Input('status-filter', 'value')]
)
def update_table(blog_filter, status_filter):
    dff = df.copy()
    if blog_filter:
        blog_ids = df_blogs[df_blogs["Nome do Blog"].isin(blog_filter)]["Blog ID"].tolist()
        dff = dff[dff["Blog ID"].isin(blog_ids)]
    if status_filter:
        dff = dff[dff["Status"].isin(status_filter)]
    dff = dff.sort_values("Data Programada", ascending=False)
    dff["Blog"] = dff["Blog ID"].map(lambda x: df_blogs[df_blogs["Blog ID"] == x]["Nome do Blog"].values[0])
    dff["HTML Link"] = dff["HTML Path"].map(lambda p: f"[Abrir]({p})" if os.path.exists(p) else "")
    count = f"Total de posts exibidos: {len(dff)}"
    return dff[["Blog", "Data Programada", "Título do Post", "Status", "HTML Link"]].to_dict("records"), count

if __name__ == '__main__':
    app.run(debug=True)
