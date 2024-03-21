import io
import json

import httpx
import matplotlib.pyplot as plt
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/repositories", tags=["repository", "github"])


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
        name
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
        if len(repos) > 0:
            filtered_repo = [item for item in repos if item['id'] == repo_id]
            if filtered_repo:
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
                        plt.text(bar.get_x() + bar.get_width() / 2, height, '{:.3f}%'.format(height), ha='center',
                                 va='bottom')

                    # Show plot
                    # plt.show()
                    plt.savefig('./static/images/repo.png')

                    # Convert the plot to a PNG image
                    buffer = io.BytesIO()
                    # plt.savefig(buffer, format='png')
                    # buffer.seek(0)
                    # FigureCanvas(fig).print_png(buffer)
                    plt.close(fig)
                    graphdict = {
                        "buffer": buffer.getvalue(),
                        "name": repo["name"]
                    }

                    return graphdict
                else:
                    print(r.raise_for_status())
                    print('Error Creating Bar Graph')


async def get_repos():
    query = """
  {
    repos {
        id
        name
        language
        description
        languages_url
        private
        visibility
    }
  }
    """
    url = 'https://kalewis5331.com/api/graphql'
    r = httpx.post(url, json={"query": query})
    status = r.status_code
    if status == 200:
        data = r.json()["data"]
        repos = data["repos"]
        if len(repos) > 0:
            return repos
        else:
            print(r.raise_for_status())
            print('Error Creating Bar Graph')
            return []
    else:
        return []


@router.get("/")
async def languages_chart(request: Request):
    repos = await get_repos()
    return templates.TemplateResponse(request=request, name="repos.html", context={"repos": repos})


@router.get("/{repo_id}")
async def languages_chart(request: Request, repo_id: int):
    repo = await create_multi_bar_chart(repo_id)
    if repo:
        return templates.TemplateResponse(request=request, name="total_util.html", context={"repo_name": repo["name"]})
    else:
        return {"message": "Error Loading GitHub Repository"}
