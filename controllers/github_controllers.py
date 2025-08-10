# 暴露api
from flask import Blueprint, request
from numpy import ufunc

from constants.constants import URL_PREFIX
from data_collectors.github import scrape_github_trending

github_bp = Blueprint('github', __name__, url_prefix=f"{URL_PREFIX}/github")

SINCE = {
    'daily': 'daily',
    'weekly': 'weekly',
    'monthly': 'monthly'
}


@github_bp.route('')
def save_trending_data():
    query_params = request.args.to_dict()
    _language = query_params.get('language', '')
    since_param = query_params.get('since', '').lower()
    if since_param:
        _since = SINCE.get(since_param)
        if _since is None:
            return 'Invalid since parameter', 400
    else:
        _since = ''
    return scrape_github_trending(_language, _since)
