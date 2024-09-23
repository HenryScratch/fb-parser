from src.facebook_login import check_user
from src.proxy_checker import check_proxy_account_pairs

check_proxy_account_pairs(
    accounts_file="data/accounts.json",
    proxies_file="data/proxies.json",
)
