# container-mirror

外部レジストリのコンテナイメージを ghcr.io にミラーする GitHub Actions 置き場。

## ミラー一覧

| 元 | ミラー先 | ワークフロー |
|---|---|---|
| `mcr.microsoft.com/playwright/python` | `ghcr.io/suwa-sh/playwright-python` | [mirror-playwright-python.yml](.github/workflows/mirror-playwright-python.yml) |

## 使い方

```bash
docker pull ghcr.io/suwa-sh/playwright-python:v1.61.0-noble
```

## 動作

- **手動実行**: Actions → `mirror-playwright-python` → Run workflow。`tags` に空白区切りでタグを指定する(例: `v1.61.0-noble`)。空なら MCR の最新バージョンを自動検出する。
- **定期実行**: 毎週火曜 05:00 JST。MCR の最新 `vX.Y.Z` とそのディストロ亜種(`-jammy` / `-noble` / `-resolute`)を追従する。
- **冪等**: コピー前に元と先の digest を比較し、一致していればスキップする。
- **マルチアーキ**: `crane copy` が manifest list をそのままコピーするので amd64 / arm64 の両方が入る。`-amd64` / `-arm64` の単一アーキタグはミラーしない。

## 設計上の前提

- push は `GITHUB_TOKEN`(`permissions: packages: write`)で行う。この経路だとパッケージが本 repo に自動リンクされるため、`org.opencontainers.image.source` ラベルを書き換えられないミラーでも権限管理が破綻しない。
- ghcr のパッケージは**初期状態が private**。公開する場合は Package settings → Danger Zone → Change visibility で public にする(**public 化は不可逆**)。
