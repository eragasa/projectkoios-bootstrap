from __future__ import annotations

import json

import requests


class ExampleTool:
    def encode(self, value: object) -> str:
        return json.dumps(value, sort_keys=True)

    def fetch_is_not_called_by_the_fixture(self, url: str) -> object:
        return requests.get(url, timeout=1)
