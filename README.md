## ⚙️ Enviroment setting

```bash
cd youtube_crawler
conda init
(base) .~/.bashrc
(base) conda create -n yt_crawl python=3.10 -y
(base) conda activate yt_crawl
(yt_crawl) pip install -r requirements.txt
```

## ⚒️ How to set pre-commit config

```bash
pip install pre-commit
# Used in case of locale related errors
# apt install locales locales-all
pre-commit install
```

## 🌟 How to run

```bash
python key_main.py
```
