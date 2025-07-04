import pandas as pd
import os

planilha = "automacao_total_stephanie.xlsx"

# Carrega a planilha de blogs
df_blogs = pd.read_excel(planilha, sheet_name="Blogs")

print("Blogs atuais:")
print(df_blogs[["Blog ID", "Nome do Blog"]])

novo_id = input("Digite o novo Blog ID (número único): ")
novo_nome = input("Digite o nome do novo blog: ")

if (df_blogs["Blog ID"] == int(novo_id)).any():
    print("Já existe um blog com esse ID.")
else:
    novo_blog = {"Blog ID": int(novo_id), "Nome do Blog": novo_nome}
    df_blogs = pd.concat([df_blogs, pd.DataFrame([novo_blog])], ignore_index=True)
    with pd.ExcelWriter(planilha, mode="a", if_sheet_exists="replace") as writer:
        df_blogs.to_excel(writer, sheet_name="Blogs", index=False)
    print("Novo blog adicionado!")
