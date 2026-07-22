
import pandas as pd
from Services.ingestservice import getengine
from Services.transformservice import cleansales
import matplotlib.pyplot as plt
import seaborn as sns
import logging


logger = logging.getLogger(__name__)

def fetchsalesdata():
    engine = getengine()

    try:
        df= pd.read_sql("select * from gold.sales" ,engine)
        logger.info(f"Sales data fetched {len(df)}")
         
        return df
    except Exception as e:

        logger.error(f"Fetch Sales failed: {e}")
        return e
    
def fetchreviewdata():
    engine = getengine()

    try:
        df= pd.read_sql("select * from gold.reviews" ,engine)
        logger.info(f"Review data fetched {len(df)}")
         
        return df
    except Exception as e:

        logger.error(f"Fetch Review failed: {e}")
        return e
    

def plottopproducts(top_n=10):
    df = cleansales()

    df1 = df.groupby("Description").agg (
                    ProductRevenue = ("Revenue",'sum')
    )

    df1 = df1.sort_values("ProductRevenue", ascending=False)

    top = df1.head(top_n)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top["ProductRevenue"], y=top.index, ax=ax, palette="viridis")
    ax.ticklabel_format(style='plain', axis='x')
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel("Product Category")
    ax.set_title(f"Top {top_n} Performing Product Categories by Revenue")
    plt.tight_layout()
    return fig

def plotmonthlytrend():

    data = fetchsalesdata()
    data = data.sort_values("yearmonth")

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(data["yearmonth"], data["MonthlyRevenue"], marker="o")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Revenue")
    ax.set_title("Monthly Revenue Trend"    )
    plt.xticks(rotation = 45)
    plt.tight_layout()
    return fig

def plotratingdist():

    data = fetchreviewdata()
    fig,ax = plt.subplots(figsize = (10,5))
    sns.countplot(data=data, x="star_rating", ax=ax, order=[1,2,3,4,5]) 
    ax.set_xlabel("Review")
    ax.set_ylabel("Total count")
    ax.set_title("Review Distribution"    )     
    return fig