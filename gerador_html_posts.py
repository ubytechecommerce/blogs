import pandas as pd
import os

# 1. Lê a planilha
df = pd.read_excel("automacao_total_stephanie.xlsx", sheet_name="Postagens")

# 2. Cria a pasta de saída se não existir
os.makedirs("posts_gerados", exist_ok=True)

# 3. Função para gerar HTML de cada post (com Adsense)
def gerar_html(post):
    titulo = post["Título do Post"]
    palavra_chave = str(post.get("Palavra-chave principal", "imagem"))
    imagem_nome = palavra_chave.lower().replace(" ", "-") + ".jpg"
    slug = "".join([c if c.isalnum() else "_" for c in titulo.lower()])[:40]
    caminho = f"posts_gerados/{slug}.html"
    # Script Adsense atualizado
    adsense = '''<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7347586768860662" crossorigin="anonymous"></script>'''
    # HTML melhorado e responsivo
    html = f"""
<!DOCTYPE html>
<html lang=\"pt-br\">
<head>
    <meta charset=\"UTF-8\">
    <title>{titulo}</title>
    {adsense}
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <style>
        body {{ font-family: Arial, Helvetica, sans-serif; background: #fafbfc; color: #222; margin: 0; padding: 0; }}
        .container {{ max-width: 700px; margin: 40px auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 32px 24px; }}
        h1 {{ color: #e67e22; font-size: 2.2em; margin-bottom: 0.5em; }}
        img {{ display: block; margin: 24px auto; max-width: 100%; border-radius: 6px; }}
        .content {{ font-size: 1.15em; line-height: 1.7; margin-bottom: 2em; }}
        .cta {{ background: #fff3e0; border-left: 5px solid #ff9800; padding: 18px 20px; margin: 32px 0; border-radius: 6px; text-align: center; }}
        .cta a {{ color: #e67e22; font-weight: bold; text-decoration: none; font-size: 1.1em; }}
        hr {{ margin: 40px 0 30px 0; border: none; border-top: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class=\"container\">
        <h1>{titulo}</h1>
        <img src=\"https://caminho-da-sua-imagem.com/{imagem_nome}\" alt=\"{palavra_chave}\" />
        <div class=\"content\">
            <!-- Cole aqui o texto do post gerado por IA, ChatGPT, ou escreva manualmente. -->
            <p>Este é um exemplo de parágrafo introdutório. Substitua este texto pelo conteúdo do seu post, gerado por IA ou editado manualmente para SEO e conversão.</p>
            <ul>
                <li>Use listas para destacar benefícios ou passos.</li>
                <li>Inclua subtítulos (h2, h3) para organizar o conteúdo.</li>
                <li>Adicione links internos e externos relevantes.</li>
            </ul>
            <p>Finalize com uma chamada para ação ou convite para comentar/compartilhar.</p>
        </div>
        <div class=\"cta\">
            <p>👉 Quer aprender a ganhar dinheiro com seu próprio blog usando inteligência artificial?</p>
            <a href=\"https://autonomodigitalpro.blogspot.com/p/servicos.html\" target=\"_blank\">Conheça nossos serviços exclusivos!</a>
        </div>
        <hr />
        <p style=\"font-size:0.95em; color:#888; text-align:center;\">Post gerado automaticamente. Edite este arquivo no VSCode ou navegador para personalizar o conteúdo.</p>
    </div>
</body>
</html>
"""
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Post salvo: {caminho}")

# 4. Gera todos os posts
for _, post in df.iterrows():
    gerar_html(post)
