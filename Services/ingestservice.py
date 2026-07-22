from sqlalchemy import create_engine
from Services.dbconnector import getconnection
import logging
import pandas as pd
import os 
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

 

def getengine():
    load_dotenv()
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
    return engine

def setupschemas():
    conn = getconnection()
    try:
        cs = conn.cursor()
        cs.execute("CREATE SCHEMA IF NOT EXISTS bronze")
        logger.info("Bronze schema created/verified")
        cs.execute("CREATE SCHEMA IF NOT EXISTS gold")
        logger.info("Gold schema created/verified")
        conn.commit()
        cs.close()
        conn.close()
        logger.info("Schema setup complete")
    except Exception as e:
        conn.rollback()
        logger.error(f"Schema setup failed: {e}")
        return e
    
def ingestsales():
    try:
        df = pd.read_csv("data/sales.csv" )
        logger.info(f"sales file {len(df)} rows")

        df.to_sql("sales", getengine(), schema="bronze", if_exists="replace", index=False)
        logger.info(f"sales data loaded in DB")

    except Exception as e:
         
        logger.error(f"ingestsales failed :{e}")

def ingestreview():
    logger.info(f"logger step0")
    try:
        logger.info(f"logger step1")
        cols = ["review_id", "product_id", "product_title",
                "star_rating", "review_headline", "review_body", "review_date"]
        logger.info(f"logger step2 {cols}")
        df = pd.read_csv("data/review.tsv"  , sep="\t", usecols=cols)
        logger.info(f"logger step3")
        logger.info(f"Review file {len(df)} rows")
        logger.info(f"{df.head()}")

        df.to_sql("reviews", getengine(), schema="bronze", if_exists="replace", index=False)
        logger.info(f"Review data loaded in DB")

    except Exception as e:
        logger.info(f"logger step -1")
        logger.error(f"ingestReview failed :{e}")

def ingestall():
    logger.info(f"Entering into setup schemas") 
    setupschemas()
    logger.info(f"Exited setup schemas") 

    logger.info(f"Entering into review ingest") 
    ingestreview()
    logger.info(f"Exited review ingest")

    logger.info(f"Entering into sale ingest") 
    ingestsales()
    logger.info(f"Exited sale ingest") 

