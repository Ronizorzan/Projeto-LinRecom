# 🎬 Projeto LinRecom
## Sistema de Recomendação de Filmes com álgebra linear

Este projeto entrega uma solução completa de recomendação de filmes, desde a construção do modelo no Kaggle até o deploy com API e interface interativa via Streamlit. Utilizando técnicas de filtragem colaborativa com SVD e similaridade do cosseno, o sistema oferece sugestões personalizadas com alta precisão e impacto real na experiência do usuário.

🚀 Visão Geral
Objetivo: Criar um sistema de recomendação que sugira filmes relevantes para o usuário com base em previsões de um modelo validado e nas preferências de usuários semelhantes.

Tecnologias: Python, Pandas, Scikit-learn, Surprise, Streamlit, Flask, Kaggle.

Modelo: SVD (Singular Value Decomposition) + Similaridade do Cosseno.

Interface: Aplicação interativa com Streamlit.

## ***🧠 Etapas do Projeto***

### 1. 📊 Construção do Modelo no Kaggle

Dataset: https://www.kaggle.com/datasets/parasharmanas/movie-recommendation-system?select=movies.csv
Treinamento do Modelo: https://www.kaggle.com/code/ronivanzorzanbarbosa/linrecom-linear-recommendation

Pré-processamento: Normalização, transformação de tipos, filtragem de usuários e filmes com poucas avaliações.

Treinamento com SVD: Redução de dimensionalidade para extrair padrões latentes.

#### Avaliação:
+ RMSE: 0.7746
+ MAE: 0.5836

> **Precision@10: 0.8058 (a cada 10 previsões 8 eram de fato relevantes para o usuário)**
> **Recall@10: 0.5688 (identificou quase 57% das opções relevantes para os usuários)**

### 2. 📐 Similaridade do Cosseno

Cálculo da Similaridade: https://www.kaggle.com/code/ronivanzorzanbarbosa/linrecom-similarities

Cálculo entre vetores de usuários no espaço latente.
Identificação de perfis semelhantes para gerar recomendações mais assertivas.

### 3. 🔌 API com Flask

Endpoint para receber o ID do usuário e retornar recomendações.
Integração com o modelo treinado e banco de dados de filmes.

### 4. 🖥️ Interface com Streamlit

Entrada de ID do usuário e número de recomendações.
Visualização dos filmes recomendados com scores previstos.
Explicações claras sobre o funcionamento do modelo e métricas de desempenho.

***💡 Diferenciais***

1) Recomendação baseada em padrões reais de comportamento.

2) Interface intuitiva e responsiva.

3) Explicações embutidas para transparência do modelo.

4) Métricas robustas para validação da qualidade das sugestões.

📬 Contato

- 📧 Desenvolvido por Ronivan ronizorzan@gmail.com
- 🔗 LinkedIn: www.linkedin.com/in/ronivan-zorzan-barbosa
- 🚀 Interface Web do Projeto: 192.168.1.70:8503

> "Recomendar é conectar. Este sistema transforma dados em experiências memoráveis."