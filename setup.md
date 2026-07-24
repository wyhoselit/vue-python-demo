步驟 1：準備環境

安裝必要工具Bash# 安裝 OpenSpec CLI（全局）
npm install -g @fission-ai/openspec@latest

# 確認安裝
openspec --version


建立專案根目錄Bashmkdir vuetify-fastapi-ai-demo
cd vuetify-fastapi-ai-demo
git init

步驟 2：初始化 Open
openspec init



** LLM Wiki 2.0 
https://github.com/langchain-ai/openwiki

```bash
sudo npm install -g openwiki
```



## 9router

```bash
~/.openwiki/.env
```



Personal mode builds a local personal brain wiki in ~/.openwiki/wiki from configured sources like local repositories, Gmail, Notion, Web Search, Hacker News, and X/Twitter.
```bash
openwiki personal --init
openwiki personal --update
```

Code mode builds repository documentation in openwiki/ for the current codebase.
```bash
openwiki --init
openwiki --update
```

## Understand Anything
```bash
curl -fsSL https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/main/install.sh | bash
```

```opencode
/plugin marketplace add Egonex-AI/Understand-Anything
/plugin install understand-anything
```