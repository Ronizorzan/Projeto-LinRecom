# api.py
from flask import Flask, request, jsonify
import pickle
import pandas as pd
import gc

app = Flask(__name__)

# Carregar modelo SVD
with open("svd_model.pkl", "rb") as f:
    model = pickle.load(f)

# Carregar metadados dos filmes
items_df = pd.read_parquet("data/movies.parquet")

# Carregar base de similaridade entre usuários
user_sim_df = pd.read_parquet("data/user_similarity_top3.parquet")  # userId, similarUserId, similarity

# Carregar recomendações pré-calculadas dos usuários similares
top3_by_user = pd.read_parquet("data/top3_by_user.parquet")


def get_similar_user_recommendations(user_id, top_n=3):
    """Retorna filmes que usuários similares provavelmente gostariam, ou usa SVD como fallback."""
    user_id = int(user_id)
    similar_users = user_sim_df[user_sim_df["userId"] == user_id] \
        .sort_values("similarity", ascending=False)["similarUserId"].tolist()

    if user_id in top3_by_user["userId"].values:
        user_top3 = top3_by_user[top3_by_user["userId"] == user_id]
        scored = [
            (row["movieId"], row["rating"])
            for _, row in user_top3.iterrows()
        ]
        
    else:
        # Fallback: usar SVD para prever os filmes que usuários similares gostariam
        scored = []
        for sim_user in similar_users:
            for movie_id in items_df['movieId'].unique():
                est = model.predict(sim_user, movie_id).est
                scored.append((movie_id, est))

    # Ordenar por score e pegar top_n
    scored.sort(key=lambda x: x[1], reverse=True)
    top_scored = scored[:top_n]

    result = []
    for movie_id, score in top_scored:
        title = items_df.loc[items_df['movieId'] == movie_id, 'title'].values[0]
        result.append({"title": str(title), "score": float(round(score, 2))})

    return result


@app.route("/recommend", methods=["GET"])
def recommend():
    user_id = int(request.args.get("userId"))
    n = int(request.args.get("n", 10))

    gc.collect()

    # Predições principais via SVD
    predictions = [
        (int(iid), float(model.predict(user_id, iid).est))
        for iid in items_df['movieId'].unique()
    ]
    predictions.sort(key=lambda x: x[1], reverse=True)
    top_n = predictions[:n]

    # Recomendação baseada em usuários similares
    similar_recs = get_similar_user_recommendations(user_id, top_n=3)

    result = []
    for iid, score in top_n:
        title = items_df.loc[items_df['movieId'] == iid, 'title'].values[0]
        result.append({
            "movieId": int(iid),
            "title": str(title),
            "score": float(round(score, 2)),
            "similar_users_liked": similar_recs
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=False, port=5000)