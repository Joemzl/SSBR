# SSBR 快速入门指南

> 本指南帮助你在 **5 分钟内** 完成项目配置并运行。

---

## 前置条件

- ✅ Python 3.10+
- ✅ OpenAI API Key（用于 Embedding）
- ✅ 网络能访问 `api.openai.com` 和 `huggingface.co`

---

## 一键初始化（复制粘贴即可）

### Windows PowerShell

```powershell
# 进入项目目录
cd SSBR

# 安装依赖
pip install -r requirements.txt

# 配置 API Key（替换为你的 Key）
$env:OPENAI_API_KEY = "sk-xxx"

# 构建向量缓存（必须，约 1 分钟）
python scripts/build_vector_cache.py --force

# 预下载重排模型（推荐，约 2-5 分钟，1.1GB）
python scripts/reranker.py --warmup

# 启动 Web Demo
python demo/app.py
```

### Linux / Mac

```bash
# 进入项目目录
cd SSBR

# 安装依赖
pip install -r requirements.txt

# 配置 API Key（替换为你的 Key）
export OPENAI_API_KEY="sk-xxx"

# 构建向量缓存（必须，约 1 分钟）
python scripts/build_vector_cache.py --force

# 预下载重排模型（推荐，约 2-5 分钟，1.1GB）
python scripts/reranker.py --warmup

# 启动 Web Demo
python demo/app.py
```

---

## 验证安装

启动 Web Demo 后，打开浏览器访问：

```
http://localhost:7861
```

尝试输入查询：
- "改善白炭黑分散性"
- "降低轮胎滚动阻力"
- "提高湿地抓地力"

---

## 需要下载的内容

| 内容 | 大小 | 下载时机 | 存储位置 |
|------|------|----------|----------|
| Python 依赖 | ~600 MB | `pip install` | `venv/` 或系统 Python |
| 向量数据库 | ~50 MB | `build_vector_cache.py` | `.cache/chroma_db/` |
| 重排模型 | **~1.1 GB** | 首次使用或 `--warmup` | `~/.cache/huggingface/` |

---

## 常见问题

### ❓ 向量缓存报错 "OPENAI_API_KEY not found"

配置环境变量：

```powershell
# Windows
$env:OPENAI_API_KEY = "sk-xxx"
```

### ❓ 重排模型下载太慢

配置 Hugging Face 镜像：

```powershell
# Windows
$env:HF_ENDPOINT = "https://hf-mirror.com"
python scripts/reranker.py --warmup
```

### ❓ Web Demo 无法访问

确保端口 7861 未被占用，或指定其他端口：

```bash
python demo/app.py --port 7862
```

---

## 下一步

- 阅读 [README.md](../README.md) 了解完整功能
- 查看 [新样本录入 SOP](../specs/002-rag-data-migration/new-sample-sop.md)
- 探索 `skills/` 目录中的 AI Skills

---

*SSBR 官能化知识库 · 快速入门 · 2026*
