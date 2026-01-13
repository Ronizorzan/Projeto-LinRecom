# app.py
import streamlit as st
import requests
import pandas as pd

st.set_page_config("🎬 Sistema de Recomendação de Filmes", layout="wide")

# 🎛️ Inputs do usuário
with st.sidebar:
    st.markdown("## 🎯 Personalize sua recomendação")
    user_id = st.number_input("👤 ID do usuário:", min_value=1, value=1, step=1, max_value=40000)
    n = st.slider("🎬 Quantidade de recomendações:", min_value=1, max_value=4, value=2)
    button = st.button("🔍 Obter recomendações")
    
    # Rodapé na barra lateral com as informações do desenvolvedor
    st.markdown("""
<style>
.footer {
    background-color: #f8f9fa;
    padding: 20px 25px;
    border-radius: 10px;
    border-left: 9px solid #972328;
    text-align: center;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin-top: 20px;
    color: #343a40;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
.footer p {
    font-size: 16px;
    margin-bottom: 15px;
}
.footer a {
    margin: 0 12px;
    display: inline-block;
}
.footer img {
    height: 36px;
    width: 36px;
    border-radius: 6px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.footer img:hover {
    transform: scale(1.1);
    box-shadow: 0 0 8px rgba(151, 35, 40, 0.4);
}
</style>

<div class="footer">
    <p><strong>Desenvolvido por: Ronivan</strong></p>
    <a href="http://107.22.129.114:5678/webhook/4091fa09-fb9a-4039-9411-7104d213f601/chat" target="_blank">
        <img src="https://cdn-icons-gif.flaticon.com/12205/12205168.gif" alt="Film Reel Icon">
    </a>
    <a href="https://github.com/Ronizorzan/Projeto-LinRecom" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/128/2504/2504911.png" alt="GitHub">
    </a>
    <a href="https://www.linkedin.com/in/ronivan-zorzan-barbosa" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/128/1384/1384072.png" alt="LinkedIn">
    </a>
    <a href="mailto:ronizorzan1992@gmail.com" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/128/5968/5968534.png" alt="Email">
    </a>
    
</div>
""", unsafe_allow_html=True)

# 🔄 Requisição à API
if button and user_id:
    with st.spinner("🔄 Buscando recomendações personalizadas..."):
        response = requests.get("http://localhost:5000/recommend", params={"userId": user_id, "n": n})

    if response.status_code == 200:
        recs = response.json()

        col1, col2 = st.columns([0.5, 0.5], gap="medium", border=True, vertical_alignment="center")
        with col1:
            # 🎬 Cabeçalho principal
            st.markdown(
                f"<h2 style='color:#F9F9F9;'>🎬 Filmes recomendados para o usuário <span style='color:#2E8B57;'>{user_id}</span></h1>",
                unsafe_allow_html=True
            )

            # Lista de recomendações principais
            for i, rec in enumerate(recs, start=1):
                st.markdown(
                    f"<div style='background-color:#F9F9F9;padding:10px;border-radius:8px;margin-bottom:10px;'>"
                    f"<h4 style='color:#2E8B57;'>Recomendação nº{i}</h4>"
                    f"<b style='color:#C2BC88;textsize:25px'>🎥<b>{rec['title']}</b>"
                    f"<span style='color:#3CCFDD;'>(Score: {rec['score']})</span></p>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        with col2:
            # Consolida todas as recomendações de usuários similares
            all_similar = []
            for rec in recs:
                for s in rec['similar_users_liked']:
                    all_similar.append(s)
            df_similar = pd.DataFrame(all_similar).drop_duplicates()

            # Exibe tabela única
            st.markdown("<h3 style='color:#F9F9F9;'>👥Baseado na preferência de usuários semelhantes:</h3>", unsafe_allow_html=True)
            st.table(df_similar)

            # Explicações importantes

            st.markdown("""<div style='background-color:#2C5C5C;padding:15px;border-radius:8px;margin-top:20px; margin-bottom:20px;'>
                    <h3 style='color:#B22222;'>💡 Por que essas recomendações?</h3>
                    <ul style='font-size:16px;'>
                        <li>🔗 <b> Conexão real:</b> Os filmes listados acima foram avaliados positivamente por usuários com gostos muito semelhantes ao usuário atual.</li>
                        <li>🎯 <b> Relevância:</b> O modelo identificou padrões que conectam as preferências do usuário a esses títulos.</li>
                        <li>✨ <b> Descoberta:</b> O modelo recomenda obras que não tinham sido exploradas, mas que combinam com esse perfil.</li>
                        <li>🔍 <b> Exploração Inteligente:</b> Mesmo que o usuário não tenha avaliado certos filmes,
                        o modelo sugere títulos com alta probabilidade de aceitação com base em padrões compartilhados.</li>
                        <li>📐 <b>Sugestão Precisa:</b> O Score à esquerda são as notas previstas pelo modelo para o filme atual. 
                        Já o Score acima são as notas atribuídas aos filmes por usuários semelhantes (os scores vão de 0.5 a 5.0).</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True)

    else:
        st.error("❌ Erro ao obter recomendações da API.")