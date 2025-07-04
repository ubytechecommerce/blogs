import pandas as pd
from datetime import datetime

planilha = "automacao_total_stephanie.xlsx"
df_posts = pd.read_excel(planilha, sheet_name="Postagens")
df_blogs = pd.read_excel(planilha, sheet_name="Blogs")

print("Blogs disponíveis:")
for idx, row in df_blogs.iterrows():
    print(f"{row['Blog ID']}: {row['Nome do Blog']}")

blog_id = input("Digite o Blog ID para o novo post: ")
titulo = input("Título do Post: ")
palavra_chave = input("Palavra-chave principal: ")
data_programada = input("Data Programada (YYYY-MM-DD, opcional): ")
if not data_programada:
    data_programada = datetime.today().date()
else:
    data_programada = pd.to_datetime(data_programada).date()

novo_post = {
    "Blog ID": blog_id,
    "Título do Post": titulo,
    "Palavra-chave principal": palavra_chave,
    "Status": "Pendente",
    "Data Programada": data_programada,
    "URL": "",
}

# Evita duplicatas
if ((df_posts["Título do Post"] == titulo) & (df_posts["Blog ID"] == int(blog_id))).any():
    print("Já existe um post com esse título para esse blog.")
else:
    df_posts = pd.concat([df_posts, pd.DataFrame([novo_post])], ignore_index=True)
    with pd.ExcelWriter(planilha, mode="a", if_sheet_exists="replace") as writer:
        df_posts.to_excel(writer, sheet_name="Postagens", index=False)
    print("Novo post adicionado!")
