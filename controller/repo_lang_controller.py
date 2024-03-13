import httpx
import numpy as np
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import matplotlib.pyplot as plt
import json

router = APIRouter(prefix="/languages", tags=["language", "github"])
templates = Jinja2Templates(directory="templates")


def create_color_labels(languages: [str]):
    with open("static/colors.json", "r") as file:
        colors = json.load(file)
    labels = []
    for language in languages:
        if language in colors:
            labels.append(colors[language]['color'])
        else:
            labels.append('grey')

    return labels


async def create_bar_chart():
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
        repos = data["repos"]
        df = pd.DataFrame(repos)
        total_items = len(df)
        df_count = df.groupby('language').size().reset_index(name='count')
        df_count['percentage'] = (df_count['count'] / total_items) * 100
        language_column = df_count['language']
        labels = create_color_labels(language_column)
        fig, ax = plt.subplots()
        ax.bar(df_count['language'], df_count['percentage'], color=labels)
        ax.set_xlabel('Language')
        ax.set_ylabel('% of Languages Used')
        ax.set_title('Occurrences of Repository Languages')
        ax.set_yticks(np.arange(0, max(df_count['percentage']) + 25, 5))
        # # Show plot
        # ax.show()
        plt.savefig('./static/images/new_plot.png')
        plt.close(fig)
    else:
        print(r.raise_for_status())


@router.get("/", response_class=HTMLResponse)
async def languages_chart(request: Request):
    await create_bar_chart()
    return templates.TemplateResponse(request=request, name="language.html")
