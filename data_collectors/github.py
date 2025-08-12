import base64
import logging

import requests
from bs4 import BeautifulSoup

from tools import mongo_dao
from tools import utils

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def scrape_github_trending(language=None, since='weekly'):
    if language is None or language == '':
        trending_url = f'https://github.com/trending?since={since}'
    else:
        trending_url = f'https://github.com/trending/{language}?since={since}'
    try:
        response = requests.get(url=trending_url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        repos = soup.find_all('article', class_='Box-row')

        _trending_repo = []

        for item in repos:
            try:
                repo_name = item.find('h2', class_='h3')
                if repo_name:
                    repo_name = repo_name.get_text(strip=True).replace('\n', '').replace(' ', '')
                else:
                    continue
                # 获取仓库描述
                description_elem = item.find('p', class_='col-9')
                description = description_elem.get_text(strip=True) if description_elem else "No description"

                # 获取编程语言
                language_elem = item.find('span', itemprop='programmingLanguage')
                language = language_elem.get_text(strip=True) if language_elem else "Unknown"

                # 获取星标数
                stars_elem = item.find('a', href=lambda x: x and '/stargazers' in x)
                stars = stars_elem.get_text(strip=True) if stars_elem else "0"

                # 获取今日星标数
                today_stars_elem = item.find('span', class_='d-inline-block float-sm-right')
                today_stars = today_stars_elem.get_text(strip=True) if today_stars_elem else "0"

                # 获取 Fork 数
                fork_elem = item.find('a', href=lambda x: x and '/forks' in x)
                forks = fork_elem.get_text(strip=True) if fork_elem else "0"
                read_me = get_readme(repo_name)
                repo_info = {'name': repo_name, 'description': description, 'language': language, 'stars': stars,
                             'today_stars': today_stars, 'forks': forks, 'url': f"https://github.com/{repo_name}",
                             'readme': read_me, '_id': utils.generate_id_str(repo_name)}
                mongo_dao.save_github_trending_data(repo_info)
                logger.info(repo_info)
                _trending_repo.append(repo_info)
            except Exception as e:
                logger.error(f"处理仓库信息时出错: {e}")
                continue
        return _trending_repo
    except requests.RequestException as e:
        logger.error(f"请求错误: {e}")
        return []
    except Exception as e:
        logger.error(f"解析错误: {e}")
        return []


def get_readme(repo_name: str):
    repo_url = f'https://api.github.com/repos/{repo_name}/readme'
    try:
        response = requests.get(url=repo_url, headers=headers, timeout=30)
        base64_content = response.json()['content'].replace('\n', '')
        return base64.b64decode(base64_content).decode('utf-8')
    except requests.RequestException as e:
        logger.error(f"请求错误: {e}")
        return ""
    except Exception as e:
        logger.error(f"解析错误: {e}")
        return ""


if __name__ == '__main__':
    scrape_github_trending()
