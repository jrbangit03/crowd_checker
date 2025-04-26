
import ast
import math

import psycopg2
import pandas as pd

def main():
    conn = psycopg2.connect("dbname=crowd_checker user=user1 password=user1 host=localhost")
    cur = conn.cursor()

    fsq_id = "4e50e24c7d8bd425e4a41c55"
    review_id = "4ffc2593e4b0dfc828b34e29"
    table = "crowd_checker_api_gtesmallwithoutreviewdate"

    cur.execute(f"""
           SELECT t1.review_id as review_id, t1.name as restaurant_name, t1.embeddings AS embeddings
           FROM {table} t1
       """, )

    # cur.execute(f"""
    #     SELECT t1.review_id as review_id, t1.name as restaurant_name, t1.embeddings AS with_review_date, t2.embeddings AS without_review_date
    #     FROM crowd_checker_api_gtesmallwithreviewdate t1
    #     JOIN crowd_checker_api_gtesmallwithoutreviewdate t2
    #     ON t1.fsq_id = t2.fsq_id
    #     AND t1.review_id = t2.review_id
    # """,)

    result = cur.fetchall()

    if result:
        import numpy as np
        from sklearn.decomposition import PCA
        import plotly.express as px

        # df = pd.DataFrame(result, columns=["review_id", "restaurant_name", "with_review_date", "without_review_date"])
        # to make sure each element is a list
        df = pd.DataFrame(result, columns=["review_id", "restaurant_name", "embeddings"])
        df['embeddings'] = df['embeddings'].apply(lambda x: ast.literal_eval(x))
        # df['without_review_date'] = df['without_review_date'].apply(lambda y: ast.literal_eval(y))

        embeddings = np.array(df['embeddings'].tolist())
        # embedding_without_review_date = np.array(df['without_review_date'].tolist())

        # combined_embeddings = np.hstack((embedding_with_review_date, embedding_without_review_date))

        # n_components = 2 (because we want to create a 2D visualisation)
        pca = PCA(n_components=2)

        # notes:
        #  change from id (the visualization)
        #  tables (results) that answers the research question. - this will be discussed by panelists
        #  slides - prepare draft for may-3
        #  threshold whether 0.15 is unacceptable

        # since the embeddings from gte-small (huggingface) produces 384 dimension
        # and embeddings from openAI small produces 1536 dimension
        # it's hard to visualize them so I used PCA to reduce the dimension ** while maintaining integrity - check variance **
        # PCA will drop the data with less relevance to the context making the embeddings smaller and avoid overfitting.
        # some reference: https://www.youtube.com/watch?v=jPmV3j1dAv4&t=41s

        # pca_embeddings = pca.fit_transform(combined_embeddings)
        pca_embeddings = pca.fit_transform(embeddings)

        df_pca = pd.DataFrame(pca_embeddings, columns=['PC1', 'PC2'])
        df_pca['review_id'] = df['review_id']
        df_pca['restaurant_name'] = df['restaurant_name']


        # ** need to cross check again PC1 and PC2 - and check if we can separate the embeddings **
        # PC1 - This component captures the largest variance direction in your combined dataset, incorporating information from both embedding sources
        # PC2 - This component captures the second-largest variance direction, orthogonal to PC1, also integrating information from both embeddings.
        fig = px.scatter(df_pca, x='PC1', y='PC2',
                         text='review_id',
                         color='restaurant_name',
                         title="PCA of Combined Embeddings")
        fig.show()


if __name__ == "__main__":
    main()