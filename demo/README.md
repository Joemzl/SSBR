# SSBR 智能推荐系统 - Web Demo

## 快速启动

```bash
# 1. 安装依赖
pip install -r demo/requirements.txt

# 2. 确保已配置 API Key (项目根目录 .env 文件)
# OPENAI_API_KEY=your-key
# OPENAI_BASE_URL=https://api.uiuiapi.com/v1

# 3. 启动演示
python demo/app.py
```

启动后访问 http://localhost:7860

## 功能特点

- 🔍 **语义检索**: 基于自然语言描述检索相关官能化方案
- 📊 **相似度排序**: 返回相似度最高的样本列表
- 📄 **详情查看**: 查看完整的官能化方案和表征数据
- 🌐 **Web 界面**: 交互式操作，无需命令行

## 组会演示建议

1. 先展示系统架构图
2. 现场演示几个典型查询
3. 展示样本详情和数据溯源
