import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Carrega os blogs existentes
planilha = "automacao_total_stephanie.xlsx"
df_blogs = pd.read_excel(planilha, sheet_name="Blogs")

# Tópicos populares para blogs de Adsense (pode personalizar)
temas_gerais = [
    ("Como ganhar dinheiro online", "ganhar dinheiro online"),
    ("Ferramentas de IA para produtividade", "ferramentas de IA"),
    ("Dicas para trabalhar em casa", "trabalho remoto"),
    ("Como criar um blog de sucesso", "criar blog"),
    ("Tendências de marketing digital", "marketing digital"),
    ("Como usar o ChatGPT para negócios", "ChatGPT negócios"),
    ("Ideias de renda extra", "renda extra"),
    ("SEO para iniciantes", "SEO básico"),
    ("Como monetizar seu site", "monetizar site"),
    ("Erros comuns de blogueiros", "erros blogueiros")
]

# Carrega posts já existentes
if os.path.exists(planilha):
    df_posts = pd.read_excel(planilha, sheet_name="Postagens")
else:
    df_posts = pd.DataFrame()

novos_posts = []
hoje = datetime.today()

for _, blog in df_blogs.iterrows():
    blog_id = blog["Blog ID"]
    blog_nome = blog["Nome do Blog"]
    # Gera 5 ideias por blog
    for i in range(5):
        tema, palavra_chave = random.choice(temas_gerais)
        titulo = f"{tema} em {hoje.strftime('%Y')}" if random.random() > 0.5 else tema
        # Evita duplicatas
        if not df_posts.empty and ((df_posts["Título do Post"] == titulo) & (df_posts["Blog ID"] == blog_id)).any():
            continue
        novos_posts.append({
            "Blog ID": blog_id,
            "Título do Post": titulo,
            "Palavra-chave principal": palavra_chave,
            "Status": "Pendente",
            "Data Programada": (hoje + timedelta(days=7*i)).date(),
            "URL": "",
        })

# Adiciona à planilha
if novos_posts:
    df_novos = pd.DataFrame(novos_posts)
    df_final = pd.concat([df_posts, df_novos], ignore_index=True)
    with pd.ExcelWriter(planilha, mode="a", if_sheet_exists="replace") as writer:
        df_final.to_excel(writer, sheet_name="Postagens", index=False)
    print(f"{len(novos_posts)} ideias de posts adicionadas!")
else:
    print("Nenhuma nova ideia gerada (possíveis duplicatas).")
