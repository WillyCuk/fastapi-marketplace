from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import pandas as pd
from app import api_blibli as sb
from app import api_bukalapak as bk
from app import api_lazada as lz
from app import api_tokopedia as tk
from app import filter_data as fd

app = FastAPI()

# Initialize all scraping classes
blibli_scrap = sb.blibli()
bukalapak_scrap = bk.bukalapak()
lazada_scrap = lz.lazada()
tokopedia_scrap = tk.tokopedia()
filter = fd.filteringData()

# Define the scraping function


def scrap_data(keyword):
    df_blibli = blibli_scrap.scrap(keyword)
    df_bukalapak = bukalapak_scrap.scrap(keyword)
    df_lazada = lazada_scrap.scrap(keyword)
    df_tokopedia = tokopedia_scrap.scrap(keyword)
    df = pd.concat([df_blibli, df_bukalapak, df_lazada,
                    df_tokopedia], ignore_index=True)
    return df

# Define the API route for scraping


@app.get('/api/scrape')
async def scrape(keyword: str = ""):
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword not provided")
    df = scrap_data(keyword)
    json_compatible_item_data = df.to_dict(orient='records')
    return JSONResponse(content=json_compatible_item_data)


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8080)
