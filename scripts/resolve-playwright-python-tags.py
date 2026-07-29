#!/usr/bin/env python3
"""mcr.microsoft.com/playwright/python の最新バージョンに属するタグ群を解決する。

出力: ミラー対象タグを空白区切りで 1 行に出す。
  例) v1.61.0 v1.61.0-jammy v1.61.0-noble v1.61.0-resolute

-amd64 / -arm64 の単一アーキタグは対象にしない。
manifest list をそのままコピーすれば両アーキが入るため。
"""

import json
import re
import urllib.request

TAGS_URL = "https://mcr.microsoft.com/v2/playwright/python/tags/list"

# 素のタグ + ディストロ亜種。MCR 側に存在するものだけを採用する。
VARIANTS = ["", "-jammy", "-noble", "-resolute"]

SEMVER = re.compile(r"v(\d+)\.(\d+)\.(\d+)")


def main() -> None:
    with urllib.request.urlopen(TAGS_URL, timeout=30) as res:
        tags = set(json.load(res)["tags"])

    versions = {
        tuple(int(g) for g in m.groups())
        for t in tags
        if (m := SEMVER.fullmatch(t))
    }
    if not versions:
        raise SystemExit("no semver tag found in MCR tag list")

    base = "v%d.%d.%d" % max(versions)
    print(" ".join(base + v for v in VARIANTS if base + v in tags))


if __name__ == "__main__":
    main()
