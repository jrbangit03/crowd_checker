# import ast
import ast

import plotly
import psycopg2
import plotly.express as px
import numpy as np
import pandas as pd
# from scipy.spatial.distance import euclidean
# from scipy.spatial.distance import cosine
#
#
# from sklearn.metrics.pairwise import cosine_distances, euclidean_distances
# import matplotlib.pyplot as plt
# import numpy as np
# # import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.metrics.pairwise import euclidean_distances
#
from sklearn.decomposition import PCA
# from sklearn.metrics.pairwise import cosine_similarity
#
# import numpy as np
# from sklearn.decomposition import PCA
# import plotly.express as px
# import plotly.io as pio


# def test():
#     import numpy as np
#     import matplotlib.pyplot as plt
#     from sklearn.metrics.pairwise import euclidean_distances
#
#     # Example embeddings (replace with actual embeddings)
#     embedding_1 = np.random.randn(1, 1536)
#     embedding_2 = np.random.randn(1, 1536)
#
#     # Compute Euclidean distance
#     distance = euclidean_distances(embedding_1, embedding_2)[0][0]
#
#     # Plotting
#     plt.figure(figsize=(6, 4))
#     plt.bar(['Text 1 vs Text 2'], [distance], color='skyblue')
#     plt.ylabel('Euclidean Distance')
#     plt.title('Similarity between Text 1 and Text 2 Embeddings')
#     plt.show()

def main():
    conn = psycopg2.connect("dbname=crowd_checker user=user1 password=user1 host=localhost")
    cur = conn.cursor()

    fsq_id = "4e50e24c7d8bd425e4a41c55"
    review_id = "4ffc2593e4b0dfc828b34e29"


    cur.execute(f"""
        SELECT t1.review_id as review_id, t1.name as restaurant_name, t1.embeddings AS with_review_date, t2.embeddings AS without_review_date
        FROM crowd_checker_api_gtesmallwithreviewdate t1
        JOIN crowd_checker_api_gtesmallwithoutreviewdate t2
        ON t1.fsq_id = t2.fsq_id
        AND t1.review_id = t2.review_id
    """,)
    # WHERE t1.fsq_id = '{fsq_id}' AND t1.review_id = '{review_id}'
    # AND  t2.fsq_id = '{fsq_id}' AND t2.review_id = '{review_id}';


    result = cur.fetchall()

    if result:
        import numpy as np
        from sklearn.decomposition import PCA
        import plotly.express as px

        df = pd.DataFrame(result, columns=["review_id", "restaurant_name", "with_review_date", "without_review_date"])
        # to make sure each element is a list
        df['with_review_date'] = df['with_review_date'].apply(lambda x: ast.literal_eval(x))
        df['without_review_date'] = df['without_review_date'].apply(lambda y: ast.literal_eval(y))

        embedding_with_review_date = np.array(df['with_review_date'].tolist())
        embedding_without_review_date = np.array(df['without_review_date'].tolist())

        combined_embeddings = np.hstack((embedding_with_review_date, embedding_without_review_date))

        # n_components = 2 (because we want to create a 2D visualisation)
        pca = PCA(n_components=2)

        # # since the embeddings from gte-small (huggingface) produces 384 dimension
        # and embeddings from openAI small produces 1536 dimension
        # it's hard to visualize them so I used PCA to reduce the dimension while maintaining integrity
        # PCA will drop the data with less relevance to the context making the embeddings smaller and avoid over fitting.
        # some reference: https://www.youtube.com/watch?v=jPmV3j1dAv4&t=41s

        pca_embeddings = pca.fit_transform(combined_embeddings)

        df_pca = pd.DataFrame(pca_embeddings, columns=['PC1', 'PC2'])
        df_pca['review_id'] = df['review_id']
        df_pca['restaurant_name'] = df['restaurant_name']

        fig = px.scatter(df_pca, x='PC1', y='PC2',
                         text='review_id',
                         color='restaurant_name',
                         title="PCA of Combined Embeddings")
        fig.show()


        # combine 2 separate PCA results to capture variance on both separated embeddings
        # combined_pca = np.hstack((pca_embedding_1, pca_embedding_2))
        # print(combined_pca)

        # df_pca = pd.DataFrame(combined_pca, columns=['PC1', 'PC2', 'PC3', 'PC4'])
        # df_pca['review_id'] = df['review_id']
        #
        # # Plot the PCA results
        # fig = px.scatter(df_pca, x='PC1', y='PC2', text='review_id', title='PCA of Combined Embeddings of Data with vs without Review Date')
        # fig.show()



        import plotly.io as pio

        # extract the embeddings from tuple, the query produces [Tuple([], []), Tuple2([], [])]
        # with_review_date_embeddings = [ast.literal_eval(i[0]) for i in result]
        # without_review_date_embeddings = [ast.literal_eval(i[1]) for i in result]
        #
        # # Combine all embeddings into one array for PCA
        # all_embeddings = np.array(with_review_date_embeddings + without_review_date_embeddings)
        # print(all_embeddings.shape)
        # pca = PCA(n_components=2)
        # reduced = pca.fit_transform(all_embeddings)
        #
        # # Dynamic labels and colors
        # labels = [f'e1[{i}]' for i in range(len(with_review_date_embeddings))] + [f'e2[{i}]' for i in range(len(without_review_date_embeddings))]
        # colors = ['Embedding 1'] * len(with_review_date_embeddings) + ['Embedding 2'] * len(without_review_date_embeddings)
        #
        # # Plot using Plotly Express
        # fig = px.scatter(
        #     x=reduced[:, 0],
        #     y=reduced[:, 1],
        #     text=labels,
        #     color=colors,
        #     labels={'x': 'PCA 1', 'y': 'PCA 2'},
        #     title='PCA Visualization of Embeddings'
        # )
        # fig.update_traces(textposition='top center')
        # fig.show()



        # need to calculate cosine and eucliedean apart from this -- *****
        # with_review_date_embeddings = ast.literal_eval(result[0])
        # without_review_date_embeddings = ast.literal_eval(result[1])
        #
        # embedding_1_np = np.array(with_review_date_embeddings)
        # embedding_2_np = np.array(without_review_date_embeddings)
        #
        # embeddings_test = np.array([embedding_1_np, embedding_2_np])
        # print(embeddings_test.shape)
        #
        # # n_components = 2 (because we want to create a 2D visualisation)
        # pca_model = PCA(n_components=2)
        #
        # # since the embeddings from gte-small (huggingface) produces 384 dimension
        # # and embeddings from openAI small produces 1536 dimension
        # # it's hard to visualize them so I used PCA to reduce the dimension while maintaining integrity
        # # PCA will drop the data with less relevance to the context making the embeddings smaller and avoid over fitting.
        # # some reference: https://www.youtube.com/watch?v=jPmV3j1dAv4&t=41s
        # pca_model.fit_transform(embeddings_test)
        # pca_embeddings_values = pca_model.transform(embeddings_test)
        # print(pca_embeddings_values.shape)
        #
        # fig = px.scatter(
        #     x=pca_embeddings_values[:, 0],
        #     y=pca_embeddings_values[:, 1],
        #     # color=["with_review_date", "without_review_date"],
        #     # hover_name=["with_review_date", "without_review_date"],
        #     # title='PCA embeddings', width=800, height=600,
        #     # color_discrete_sequence=plotly.colors.qualitative.Alphabet_r
        # )
        #
        # fig.update_layout(
        #     xaxis_title='with_review_date',
        #     yaxis_title='without_review_date')
        # fig.show()











        # print(embedding_1_np)


        # embeddings from gte-small model produces 384 dimensionality,
        # to visualize it we need to reduce the dimensionality and convert the embeddings into a 2D numpy array
        # using PCA so we can visualize through sklearn


        # embeddings_test = np.array([embedding_1_np, embedding_2_np])
        # print(embeddings_test.shape)
        # pca_model = PCA(n_components=2)
        # pca_model.fit(embeddings_test)
        #
        # pca_embeddings_values = pca_model.transform(embeddings_test)
        # print(pca_embeddings_values.shape)
        #
        # fig = px.scatter(
        #     x=pca_embeddings_values[:, 0],
        #     y=pca_embeddings_values[:, 1],
        #     color=["with_review_date", "without_review_date"],
        #     hover_name=["with_review_date", "without_review_date"],
        #     title='PCA embeddings', width=800, height=600,
        #     color_discrete_sequence=plotly.colors.qualitative.Alphabet_r
        # )
        #
        # fig.update_layout(
        #     xaxis_title='with_review_date',
        #     yaxis_title='without_review_date')
        # fig.show()





        # plt.scatter(embedding_1_np, embedding_2_np)
        # plt.title("Line Plot with Matplotlib")
        # plt.xlabel("X Axis")
        # plt.ylabel("Y Axis")
        # plt.show()


        # print(embedding_1_np)
        # print(embedding_2_np)


        # distance = np.linalg.norm(embedding_1_np - embedding_2_np)
        # print(distance)
        #
        # euclidean_distance = euclidean(embedding_1_np, embedding_2_np)
        # cosine_distance = cosine(embedding_1_np, embedding_2_np)
        # print(euclidean_distance)
        # print(cosine_distance)

        # embeddings_test = np.array([embedding_1_np, embedding_2_np])
        # pca = PCA(n_components=2)
        # reduced_embeddings = pca.fit_transform(embeddings_test)
        # #
        # dist = euclidean(reduced_embeddings[0], reduced_embeddings[1])
        # #
        # # # Create a scatter plot to visualize the reduced embeddings
        # plt.figure(figsize=(8, 6))
        # plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=['r', 'b'], label="Embeddings")
        # #
        # # # Annotate points with their indices or labels
        # for i, txt in enumerate(['Embedding 1', 'Embedding 2']):
        #     plt.annotate(txt, (reduced_embeddings[i, 0], reduced_embeddings[i, 1]))
        # #
        # # # Draw a line between the two embeddings to represent the Euclidean distance
        # plt.plot([reduced_embeddings[0, 0], reduced_embeddings[1, 0]],
        #          [reduced_embeddings[0, 1], reduced_embeddings[1, 1]],
        #          'k--', label=f'Euclidean Distance: {dist:.2f}')
        # #
        # # # Title and labels
        # plt.title('PCA Visualization of 1-D Embeddings with Euclidean Distance')
        # plt.xlabel('PCA Component 1')
        # plt.ylabel('PCA Component 2')
        # plt.legend()
        # plt.grid(True)
        # plt.show()

        # distance_matrix = cosine_distances(embeddings_test)


### action items tomorrow
### - test using euclidean distance - understand if do we need a baseline embedding?
### - test using cosine distance - understand if do we need a baseline embedding?
### - visualize the vectors (neo4j?) - clean up the code, make matplotlib and sklearn as standard
### - related literature - read and understand if do we only need to extract and re-quote?


if __name__ == "__main__":
    main()