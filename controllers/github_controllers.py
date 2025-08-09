# 暴露api
from flask import Blueprint

from constants.constants import URL_PREFIX
from data_collectors.github import scrape_github_trending

github_bp = Blueprint('github', __name__, url_prefix=f"{URL_PREFIX}/github")

@github_bp.route()
def save_trending_data():
    scrape_github_trending()

    return 200