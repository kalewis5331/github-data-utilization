import httpx
import numpy as np
from fastapi import APIRouter
import pandas as pd
import matplotlib.pyplot as plt

router = APIRouter(prefix="/languages", tags=["language", "github"])


@router.get("/")
async def languages_chart():
    query = """
  {
    repos {
      language
    }
  }
    """
    url = 'https://kalewis5331.com/api/graphql'
    r = httpx.post(url, json={"query": query})
    status = r.status_code
    if status == 200:
        data = r.json()["data"]
        print(data["repos"])
        df = pd.DataFrame(data["repos"])
        df_summed = df.groupby('language').size().reset_index(name='count')
        df_summed['count'] = df_summed['count']
        plt.bar(df_summed['language'], df_summed['count'])
        plt.xlabel('Language')
        plt.ylabel('Count')
        plt.title('Occurrences of Repository Languages')
        plt.yticks(np.arange(min(df_summed['count']), max(df_summed['count'])+1, 1.0))

        # Show plot
        plt.show()
        plt.savefig('./static/images/new_plot.png')

        return data["repos"]
    else:
        r.raise_for_status()
        return {"data": []}


@router.get("/overtime")
async def get_languages_overtime():
    return {"message": "Languages Here!"}
