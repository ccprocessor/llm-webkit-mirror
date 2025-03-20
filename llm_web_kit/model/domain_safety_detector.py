from typing import Dict
import re
import os

from llm_web_kit.config.cfg_reader import load_config
from llm_web_kit.libs.standard_utils import json_loads
from llm_web_kit.model.resource_utils import (CACHE_DIR, download_auto_file,
                                              singleton_resource_manager)

re_domain_w_port = re.compile(r"^(.+):(\d+)$")
# see: https://en.wikipedia.org/wiki/Second-level_domain
# see: https://raw.githubusercontent.com/gavingmiller/second-level-domains/master/SLDs.csv
generic_domains = set(["com", "net", "gov", "edu", "org", "int", "mil", "info", "xyz"])
less_generic_domains = set(["co", "ac", "biz", "name", "nom", "sch", "gob", "pro", "or", "go", "web", "mi", "in"])
secondary_domains = set(["me.uk", "us.com", "gc.ca", "on.ca", "bc.ca", "my.id"])

def get_url_parts(url: str):
    "return (scheme, host, port, path, param, fragments)"

    url = (url or "").strip()
    if not url:
        return None

    scheme = "http"
    if url.startswith("http://"):
        url = url[len("http://") :]
    elif url.startswith("https://"):
        url = url[len("https://") :]
        scheme = "https"

    def _split(url: str, sep: str):
        i = url.find(sep)
        return (url[:i], url[i:]) if i > 0 else (url, "")

    url, fragments = _split(url, "#")
    url, param = _split(url, "?")
    url, path = _split(url, "/")

    m = re_domain_w_port.match(url)
    host, port = m.groups() if m else (url, "")
    host, port = str(host), str(port)

    return (scheme, host, port, path, param, fragments)

def get_url_domain(url: str):
    parts = get_url_parts(url)
    if not parts:
        return None
    return parts[1]


def is_ip_address(domain: str):
    return domain and bool(re.match(r"^\d+\.\d+\.\d+\.\d+$", domain))

def get_domain_seq(domain: str):
    if not domain:
        return []
    if is_ip_address(domain):
        return [domain]
    parts = domain.split(".")
    if len(parts) <= 2:
        return [domain]
    end_idx = len(parts) - 1
    if ".".join(parts[-2:]) in secondary_domains:
        end_idx -= 1
    elif parts[-2] in generic_domains:
        end_idx -= 1
    elif parts[-2] in less_generic_domains and parts[-1] not in generic_domains:
        end_idx -= 1
    return [".".join(parts[idx:]) for idx in range(end_idx)]

def get_url_domain_seq(url: str):
    if not url:
        return []
    domain = get_url_domain(url)
    if not domain:
        return []
    return get_domain_seq(domain)


def domain_type_val(domain_type):
    m = {"whitelist": 1, "blacklist": 2, "silverlist": 3, "graylist": 4}
    if domain_type in m:
        return m[domain_type]
    return 100

class DomainChecker:
    def __init__(self) -> None:
        self.domain_dict = get_domain_dict()

    def get_domain_level(self, domain_seq: list) -> str:
        if not domain_seq:
            return ""
        domain_seq_levels = [self.domain_dict.get(domain_str, "") for domain_str in domain_seq]
        domain_seq_vals = [domain_type_val(domain_level) for domain_level in domain_seq_levels]
        min_val = min(domain_seq_vals)
        min_idx = domain_seq_vals.index(min_val)
        return domain_seq_levels[min_idx]

def auto_download():
    resource_config = load_config()['resources']
    resource_name = "domain_blacklist"
    domain_list_config: Dict = resource_config[resource_name]
    download_path = domain_list_config['download_path']
    md5 = domain_list_config['md5']
    local_path = os.path.join(CACHE_DIR, f"{resource_name}.json")
    domain_list_file_path = download_auto_file(download_path, local_path, md5)
    return domain_list_file_path


def get_domain_dict():
    domain_list_file_path=auto_download()
    with open(domain_list_file_path, "rb") as file:
        domain_list = file.readlines()

    domain_dict_list = [json_loads(domain_json) for domain_json in domain_list]

    domain_dict = {}
    for i in range(len(domain_dict_list)):
        domain = domain_dict_list[i]["domain"]
        if domain in domain_dict:
            if domain_type_val(domain_dict_list[i]["type"]) < domain_type_val(domain_dict[domain]):
                domain_dict[domain] = domain_dict_list[i]["type"]
        else:
            domain_dict[domain] = domain_dict_list[i]["type"]
    return domain_dict


def get_domain_level_checker() -> DomainChecker:
    if not singleton_resource_manager.has_name("domain_level_checker"):
        singleton_resource_manager.add_resource("domain_level_checker", DomainChecker())
    return singleton_resource_manager.get_resource("domain_level_checker")


def release_domain_level_detecter():
    singleton_resource_manager.release_resource("domain_level_checker")



def decide_domain_level(url: str) -> str:
    domainChecker = get_domain_level_checker()
    domain_seq = get_url_domain_seq(url)
    domain_level = domainChecker.get_domain_level(domain_seq)
    return domain_level


class DomainFilter:
    def __init__(self):
        pass

    def filter(
        self,
        content_str: str,
        language: str,
        url: str,
        language_details: str,
        content_style: str,
    ) -> dict:
        domain_level = decide_domain_level(url)
        if domain_level == "blacklist":
            return False, {"domain_level": domain_level}
        return True, {"domain_level": domain_level}
