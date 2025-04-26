import ast
import logging
import math
import numpy as np
import psycopg2

from ..utilities.utils import get_embedder
from ..utilities.embeddings import HuggingFaceModelEmbeddings, OpenAIModelEmbeddings, ModelEmbeddings


def calc_euclidean_dist(with_review_date_embeddings, without_review_date_embeddings):
    return math.sqrt(sum((a - b) ** 2 for a, b
                         in zip(with_review_date_embeddings, without_review_date_embeddings)))


def calc_cosine_dist(with_review_date_embeddings, without_review_date_embeddings):
    u = np.array(with_review_date_embeddings)
    v = np.array(without_review_date_embeddings)

    # Compute cosine distance
    dot_product = np.dot(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    return 1 - (dot_product / (norm_u * norm_v))


def extract_embeddings(fsq_id, review_id, table_1, table_2):
    conn = psycopg2.connect("dbname=crowd_checker user=user1 password=user1 host=localhost")
    cur = conn.cursor()

    cur.execute(f"""
           SELECT t1.review_id as review_id, t1.name as restaurant_name, t1.embeddings AS with_review_date, t2.embeddings AS without_review_date
           FROM {table_1} t1
           JOIN {table_2} t2
           ON t1.fsq_id = t2.fsq_id
           AND t1.review_id = t2.review_id
           WHERE t1.fsq_id = '{fsq_id}' AND t1.review_id = '{review_id}'
           AND  t2.fsq_id = '{fsq_id}' AND t2.review_id = '{review_id}';
       """, )

    return cur.fetchone()


def extract_single_embeddings(fsq_id, review_id, table_1):
    conn = psycopg2.connect("dbname=crowd_checker user=user1 password=user1 host=localhost")
    cur = conn.cursor()

    cur.execute(f"""
           SELECT t1.review_id as review_id, t1.name as restaurant_name, t1.embeddings AS with_review_date
           FROM {table_1} t1
           WHERE t1.fsq_id = '{fsq_id}' AND t1.review_id = '{review_id}'
       """, )

    return cur.fetchone()



def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # review_id = "4f13e98ce4b0380205234acd"
    # fsq_id= "4b53a54ff964a5200da627e3"

    # review_id= "54fb0215498ea77361bf2294"
    # fsq_id= "4cffaa76f7b38cfa4eaacac3"

    review_id= "54fb0215498ea77361bf2294"
    fsq_id= "4cffaa76f7b38cfa4eaacac3"


    # table_1 = "crowd_checker_api_gtesmallwithreviewdate"
    table_1 = "crowd_checker_api_gtesmallwithreviewdate"

    # fsq_id = "4e50e24c7d8bd425e4a41c55"
    # review_id = "4e600e991f6ef7d079ab0bfd"
    # table_1 = "crowd_checker_api_gtesmallwithreviewdate"
    # table_2 = "crowd_checker_api_gtesmallwithoutreviewdate"

    result = extract_single_embeddings(fsq_id, review_id, table_1)
    print("embeddings from table")

    if result:
        # extract the embeddings from tuple, the query produces Tuple(<rev_id>, <name>, [], [])
        with_review_date_embeddings = ast.literal_eval(result[2])
        # without_review_date_embeddings = ast.literal_eval(result[3])

        question = "give me the best hotel based on recent reviews and feedback provided by customers."
        embedder = get_embedder("HUGGING_FACE")
        question_embeddings = np.array(embedder.gen_embeddings(question)).tolist()


        euclidean_distance = math.sqrt(sum((a - b) ** 2 for a, b
                                 in zip(with_review_date_embeddings, question_embeddings)))

        cosine_dist = calc_cosine_dist(with_review_date_embeddings, question_embeddings)

        # cosine is close to 0 - which means it didn't change much or didn't add much to context
        # euclidean is > 0 but very small, which means the change was detected but not that heavy.
        # I guess this is because the models I used are very stable - I might need to use BERT loc model
        # or maybe create my own reco model that specializes in POI recommendation and geo location
        # similar to the related literatures.
        logging.info(f"EUCLIDEAN DISTANCE for review_id {review_id} is {euclidean_distance}")
        logging.info(f"COSINE DISTANCE for review_id {review_id} is {cosine_dist}")




if __name__ == "__main__":
    main()

