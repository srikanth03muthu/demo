# from fastapi import FastAPI 

# from fastapi.middleware.cors import CORSMiddleware

# app=FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# # @app.get("/")
# # def root():
# #     return {"Hello":"World"}

# @app.route("/http://127.0.0.1:8000/", methods=["GET"])
# def get_all_guides():
#     guides = Guide.query.all()
#     guide_list = [{"id": guide.id, "title": guide.title, "content": guide.content} for guide in guides]
#     return jsonify(guide_list), 200

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Example model
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool

# Example routes
@app.get("/")
async def root():
    print("hello")
    yesterday_data=pd.read_csv("C:/Users/chell/OneDrive/Desktop/T-1.csv")
    today_data=pd.read_csv("C:/Users/chell/OneDrive/Desktop/T.csv")
    merged_data = pd.merge(yesterday_data, today_data,on="ID_GLOBAL",suffixes=("_yesterday", "_today"),how="outer")
    comparison_results=pd.DataFrame()
    comparison_results["ID_GLOBAL"]=merged_data["ID_GLOBAL"]
    for column in yesterday_data.columns:
        if column !="ID_GLOBAL":
            comparison_results[column]=np.where(
                (merged_data[f"{column}_yesterday"].isna()) & (merged_data[f"{column}_today"].isna()),
                True,
                np.where(
                    (merged_data[f"{column}_yesterday"].notna()) & (merged_data[f"{column}_today"].notna()) &
                    (merged_data[f"{column}_yesterday"]==merged_data[f"{column}_today"]),
                    True,
                    False
                )
            )
    comparison_results.to_csv("comparison_results.csv",index=False)

    # Delta download
    today_data=pd.read_csv("C:/Users/chell/OneDrive/Desktop/T.csv")
    comparison_results=pd.read_csv("C:/Users/chell/OneDrive/Pictures/bnp_python/comparison_results.csv")
    mismatched_ids=comparison_results.loc[comparison_results.drop(columns="ID_GLOBAL").eq(False).any(axis=1),"ID_GLOBAL"]
    delta_values=today_data[today_data["ID_GLOBAL"].isin(mismatched_ids)]
    delta_values.to_csv("delta_values.csv", index=False)

# **Segregation**
    today_data=pd.read_csv("C:/Users/chell/OneDrive/Desktop/T.csv")
    comparison_results=pd.read_csv("C:/Users/chell/OneDrive/Pictures/bnp_python/comparison_results.csv")
    mismatched_ids=comparison_results.loc[comparison_results.drop(columns="ID_GLOBAL").eq(False).any(axis=1),"ID_GLOBAL"]
    delta_values=today_data[today_data["ID_GLOBAL"].isin(mismatched_ids)]
    market_sector_groups=delta_values.groupby("MARKET_SECTOR_DES")
    for market_sector,group in market_sector_groups:
        filename=f"delta_values_{market_sector}.csv"
        group.to_csv(filename,index=False)


        return {"message": "Hello from FastAPI!"}

@app.post("/items/")
async def create_item(item: Item):
    return {"name": item.name, "price": item.price, "in_stock": item.in_stock}

