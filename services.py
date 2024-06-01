import dbm
import json
from functools import lru_cache
from random import choice
from typing import Any


def host_is_valid(host_dict: dict[str, Any]) -> bool:
    # weighted instance score based on the availability
    # over the last 3h, 30 and 120 days, together with the version.
    # points > 50
    # whether the host has RSS feeds enabled.
    # rss is True
    # All Time % for all time percentage of the instance being healthy.
    # healthy_percentage_overall > 55
    return (host_dict["points"] > 50 and host_dict["rss"]) or (
        host_dict["rss"] and host_dict["healthy_percentage_overall"] > 55
    )


@lru_cache(maxsize=256)
def get_valid_instances() -> list[str]:
    with open("host_data/hosts.json", "r+") as f:
        host_data = json.loads(f.read())
    return [h["url"] for h in host_data["hosts"] if host_is_valid(h)]


def get_least_requested_host() -> str:
    with dbm.open("host_data/host_requests", "c") as db:
        host_request_items = [
            {"host": k.decode(), "requests": int(db[k])} for k in db.keys()
        ]

    if not host_request_items:
        hosts = get_valid_instances()
        host = choice(hosts)
    else:
        host = min(host_request_items, key=lambda x: x["requests"])["host"]
    return host


def update_host_requests(host: str) -> None:
    with dbm.open("host_data/host_requests", "c") as db:
        db[host] = str(int(db.get(host, 0)) + 1)
