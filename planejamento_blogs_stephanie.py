import os
import re
import pandas as pd
import feedparser
from datetime import datetime

# 1. LISTA DE BLOGS (adicione novos blogs aqui quando criar)
blogs_info = [
    {
        'id': 1,
        'nome': 'Autônomo Digital Pro',
        'rss': 'https://autonomodigitalpro.blogspot.com/feeds/posts/default?alt=rss',
        'url': 'https://autonomodigitalpro.blogspot.com',
        'tema': 'Renda extra, IA, marketing',
        'status': 'Ativo',
        'data_criacao': '01/07/2025',
        'obs': 'Foco inicial do projeto'
    },
    {
        'id': 2,
        'nome': 'Sabedoria Suave',
        'rss': 'https://sabedoriasuave.blogspot.com/feeds/posts/default?alt=rss',
        'url': 'https://sabedoriasuave.blogspot.com',
        'tema': 'Autoconhecimento feminino',
        'status': 'Planejado',
        'data_criacao': '',
        'obs': 'Criar após aprovação do AdSense'
    },
    {
        'id': 3,
        'nome': 'Vida Leve & Livre',
        'rss': 'https://vidaleveelivre.blogspot.com/feeds/posts/default?alt=rss',
        'url': 'https://vidaleveelivre.blogspot.com',
        'tema': 'Estilo de vida e bem-estar',
        'status': 'Planejado',
        'data_criacao': '',
        'obs': 'Pensar conteúdo evergreen'
    }
]

# Função para limpar nomes de arquivos/pastas
slugify = lambda s: re.sub(r'[^a-zA-Z0-9_-]', '_', s.replace(' ', '_'))

# 2. IMPORTAÇÃO DOS POSTS DE TODOS OS BLOGS E GERAÇÃO DE HTML
all_blogs = []
all_posts = []
base_dir = 'posts_html'
os.makedirs(base_dir, exist_ok=True)

for blog in blogs_info:
    feed = feedparser.parse(blog['rss'])
    blog_dir = os.path.join(base_dir, slugify(blog['nome']))
    os.makedirs(blog_dir, exist_ok=True)
    for i, entry in enumerate(feed.entries):
        titulo = entry.title
        data_pub = entry.published
        link = entry.link
        resumo = entry.summary
        palavras_chave = entry.tags[0]['term'] if 'tags' in entry and entry.tags else "sem palavra-chave"
        tipo = "Conteúdo do Blog"
        # Status automático: se data de publicação for futura, status = 'Pendente', senão 'Publicado'
        data_pub_dt = datetime.strptime(data_pub, "%a, %d %b %Y %H:%M:%S %z")
        hoje = datetime.now(data_pub_dt.tzinfo)
        if data_pub_dt > hoje:
            status = "Pendente"
        else:
            status = "Publicado"
        data_fmt = data_pub_dt.strftime("%Y-%m-%d")
        pasta_data = os.path.join(blog_dir, data_fmt)
        os.makedirs(pasta_data, exist_ok=True)
        # Imagem do post (se houver)
        imagem = ''
        if 'media_content' in entry and entry.media_content:
            imagem = entry.media_content[0]['url']
        # HTML do post
        html = f'''<html>\n<head>\n<meta charset="utf-8">\n<title>{titulo}</title>\n</head>\n<body>\n<h1>{titulo}</h1>\n<p><i>Publicado em {data_fmt}</i></p>\n{'<img src="'+imagem+'" style="max-width:400px;">' if imagem else ''}\n<div>{resumo}</div>\n<p><b>Palavra-chave:</b> {palavras_chave}</p>\n<p><a href="{link}" target="_blank">Ver post original</a></p>\n<hr>\n<div style="background:#f0f0f0;padding:16px;margin-top:32px;"><b>CTA:</b> Conheça mais em <a href="https://ubytech.com.br" target="_blank">ubytech.com.br</a></div>\n</body>\n</html>'''
        # Salvar HTML
        file_name = slugify(titulo)[:40] + '.html'
        file_path = os.path.join(pasta_data, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        all_posts.append([
            blog['id'], i+1, titulo, palavras_chave, tipo, status,
            data_fmt, "✅", "Inserir CTA", imagem or "Imagem a gerar"
        ])
    all_blogs.append([
        blog['id'], blog['nome'], blog['url'], blog['tema'], blog['status'], blog['data_criacao'], "Automático", blog['obs']
    ])

# 3. CRIANDO PLANILHAS
blogs_df = pd.DataFrame(all_blogs, columns=["Blog ID", "Nome do Blog", "URL", "Tema Principal", "Status", "Data de Criação", "Última Postagem", "Observações"])
posts_df = pd.DataFrame(all_posts, columns=[
    "Blog ID", "Nº", "Título do Post", "Palavra-chave principal", "Tipo de conteúdo", "Status",
    "Data Programada", "Publicado?", "CTA", "Imagem"
])
social_df = pd.DataFrame(columns=["#", "Data", "Rede", "Tipo de Conteúdo", "Formato", "Link p/ Postagem", "Blog Relacionado", "Status", "CTA", "Observações"])
adsense_df = pd.DataFrame(columns=["Item", "Blog relacionado", "Status", "Observações"])
calendar_df = pd.DataFrame(columns=["Data", "Canal", "Tipo de ação", "Relacionado a", "Status", "Observações"])

# 4. SALVANDO PLANILHA
with pd.ExcelWriter("automacao_total_stephanie.xlsx", engine="openpyxl") as writer:
    blogs_df.to_excel(writer, sheet_name="Blogs", index=False)
    posts_df.to_excel(writer, sheet_name="Postagens", index=False)
    social_df.to_excel(writer, sheet_name="Redes Sociais", index=False)
    adsense_df.to_excel(writer, sheet_name="Monetização", index=False)
    calendar_df.to_excel(writer, sheet_name="Calendário", index=False)

print("✅ Planilha com dados de múltiplos blogs gerada com sucesso: automacao_total_stephanie.xlsx")
print("✅ HTMLs dos posts gerados em pastas por blog e data. Pronto para versionar no GitHub!")
