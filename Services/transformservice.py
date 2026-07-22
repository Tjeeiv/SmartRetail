import pandas as pd
from Services.dbconnector import getconnection
from Services.ingestservice import getengine
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

def cleansales():
    engine = getengine()

    try:
        df= pd.read_sql("select * from bronze.sales" ,engine)
        logger.info(f"Sales data fetched {len(df)}")
        df = df[~df["Invoice"].str.lower().str.startswith("c")]
        logger.info(f"Cancelled  data Removed {len(df)}")

        df = df[ (df["Quantity"] >0)  & (df["Price"] > 0 )]

        df = df.dropna(subset=["Customer ID","Description"])

        df = df.drop_duplicates()

        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"]) 

        df["Revenue"] = df["Quantity"] * df["Price"]

        return df
    except Exception as e:

        logger.error(f"Clean Sales failed: {e}")
        return None   
    


def aggregatesale():
     
    try:
        df = cleansales()
        df['yearmonth'] = df["InvoiceDate"].dt.to_period('M').astype(str)
        df1 = df.groupby("yearmonth").agg(
            Invoicecount =  ("Invoice" , 'nunique'),
            MonthlyRevenue = ("Revenue",'sum'),
            monAvgRev = ("Revenue",'mean')

        )

        df1.to_sql("sales", getengine(), schema="gold", if_exists="replace", index=True)
        logger.info(f"sales data loaded in Gold")
        
    except Exception as e:

        logger.error(f"aggregate Sales failed: {e}")
        return e
    

def transformreviews():
    engine = getengine()

    try:
        df= pd.read_sql("select * from bronze.reviews" ,engine)
        logger.info(f"Reviews data fetched {len(df)}")
        df = df.dropna(subset=["review_body"])
        logger.info(f"After dropping nulls: {len(df)} rows") 
        df = df.drop_duplicates()
        logger.info(f"After dedup: {len(df)} rows")

        df.to_sql("reviews",engine, schema="gold", if_exists="replace", index=False)
        logger.info(f"Reviews loaded into gold.reviews") 
    except Exception as e:

        logger.error(f"Clean Reviews failed: {e}")
        return e
    


def transformall():
    logger.info("Starting transform pipeline")
    cleansales()        
    aggregatesale()     
    transformreviews()
    logger.info("Transform pipeline complete")
