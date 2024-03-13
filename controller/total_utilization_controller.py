import io
import httpx
from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
import json

router = APIRouter(prefix="/repository", tags=["repository", "github"])
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


async def create_multi_bar_chart(repo_id: int):
    query = """
  {
    repos {
        id
        language
        languages_url
    }
  }
    """
    url = 'https://kalewis5331.com/api/graphql'
    r = httpx.post(url, json={"query": query})
    status = r.status_code
    if status == 200:
        data = r.json()["data"]
        repos = data["repos"]
        filtered_repo = [item for item in repos if item['id'] == repo_id]
        repo = filtered_repo[0]
        lang_url = repo["languages_url"]
        res = httpx.get(lang_url)
        status2 = res.status_code
        if status2 == 200:
            langs_array = res.json()
            langs = list(langs_array.keys())
            colorful_bars = create_color_labels(langs)
            total_sum = sum(langs_array.values())
            fig, ax = plt.subplots()
            columns = [(item / total_sum) * 100 for item in langs_array.values()]
            bars = ax.bar(langs, columns, color=colorful_bars)
            ax.set_xlabel('Language')
            ax.set_ylabel('% of Languages Used')
            ax.set_title('Occurrences of Repository Languages')
            plt.xticks(rotation=45, ha='right')
            plt.yticks([0, 25, 50, 75, 100], ['0', '25%', '50%', '75%', '100%'])
            plt.tight_layout()
            # Add labels with values above each bar
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width() / 2, height, '{:.3f}'.format(height), ha='center', va='bottom')

            # Show plot
            # plt.show()
            # plt.savefig('./static/images/bar.png')
            # Convert the plot to a PNG image
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            plt.close(fig)
            return buffer
        else:
            print(r.raise_for_status())
            print('Error Creating Bar Graph')


@router.get("/{repo_id}")
async def languages_chart(request: Request, repo_id: int):
    b = await create_multi_bar_chart(repo_id)
    # Return the PNG image as a response
    return Response(content=b.getvalue(), media_type='image/png')
