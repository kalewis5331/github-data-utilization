import httpx
from fastapi import APIRouter

router = APIRouter(prefix="/languages", tags=["language", "github"])


@router.get("/")
async def get_languages():
    query = """
  {
    repos {
      id
      language
      name
      description
      stargazers_count
      forks
      html_url
    }
  }
    """
    url = 'https://kalewis5331.com/api/graphql'
    r = httpx.post(url, json={"query": query})
    status = r.status_code
    if status == 200:
        data = r.json()["data"]
        print(data["repos"])
        return data["repos"]
    else:
        r.raise_for_status()
        return {"data": []}


@router.get("/overtime")
async def get_languages_overtime():
    return {"message": "Languages Here!"}
