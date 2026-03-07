"""
SSBR 官能化方案智能推荐系统 - Web Demo
基于 RAG 语义检索的绿色轮胎材料推荐

用于毕业项目演示

Usage:
    python demo/app.py
    
Then open http://localhost:7860 in browser
"""

import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import gradio as gr
from scripts.rag_search import RAGSearchEngine
from demo.data_formatter import (
    format_result_for_display,
    format_results_as_markdown,
    format_detail_as_markdown,
    FriendlyResult,
    similarity_to_match_level
)

# 初始化检索引擎
engine = RAGSearchEngine()

# 存储当前搜索结果（用于详情查看）
current_results: list[FriendlyResult] = []


# ==================== 核心功能函数 ====================

def search_samples(query: str, top_k: int = 5) -> tuple:
    """执行语义检索并返回格式化结果"""
    global current_results
    
    if not query.strip():
        return "❌ 请输入您的研究需求", "", gr.update(choices=[], value=None)
    
    if not engine.embedding_service.is_available():
        return "❌ 系统暂时不可用，请稍后再试", "", gr.update(choices=[], value=None)
    
    try:
        # 执行检索
        results = engine.search(query, k=int(top_k))
        
        if not results:
            current_results = []
            return "### 未找到相关方案\n\n请尝试调整查询关键词。", "", gr.update(choices=[], value=None)
        
        # 转换为用户友好格式
        friendly_results = []
        for i, r in enumerate(results, 1):
            content = engine.get_summary_content(r.sample_id)
            if content:
                fr = format_result_for_display(
                    sample_id=r.sample_id,
                    similarity=r.similarity,
                    summary_content=content,
                    index=i,
                    query=query
                )
                friendly_results.append(fr)
        
        current_results = friendly_results
        
        # 格式化主要结果
        main_output = format_results_as_markdown(friendly_results, query)
        
        # 构建下拉选项（使用官能团名称）
        dropdown_choices = [f"方案 {r.index}: {r.functional_group}" for r in friendly_results]
        
        # 默认显示第一个方案的详情
        first_detail = format_detail_as_markdown(friendly_results[0]) if friendly_results else ""
        
        return main_output, first_detail, gr.update(choices=dropdown_choices, value=dropdown_choices[0] if dropdown_choices else None)
        
    except Exception as e:
        current_results = []
        return f"❌ 检索出错，请稍后重试", "", gr.update(choices=[], value=None)


def get_sample_detail(selection: str) -> str:
    """获取选中方案的详细信息"""
    global current_results
    
    if not selection or not current_results:
        return ""
    
    # 从选项中提取方案编号
    try:
        index = int(selection.split(":")[0].replace("方案", "").strip())
        for r in current_results:
            if r.index == index:
                return format_detail_as_markdown(r)
    except:
        pass
    
    return "无法加载详情"


def get_system_status() -> str:
    """获取系统状态（简化版，不暴露内部信息）"""
    api_ok = engine.embedding_service.is_available()
    
    if api_ok:
        return "✅ 系统运行正常"
    else:
        return "⚠️ 系统维护中"


# ==================== 示例查询 ====================

EXAMPLE_QUERIES = [
    ["改善白炭黑分散性"],
    ["降低轮胎滚动阻力"],
    ["提高湿地抓地力"],
    ["同时提高抓地力和降低滚阻"],
    ["改善填料-橡胶界面结合"],
    ["优化低温性能"],
    ["提高拉伸强度"]
]


# ==================== 构建界面 ====================

def create_demo():
    """创建 Gradio 演示界面"""
    
    with gr.Blocks(
        title="SSBR 官能化方案推荐系统",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="slate"
        ),
        css="""
        .main-header {
            text-align: center;
            padding: 20px 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .main-header h1 {
            color: white !important;
            margin: 0;
        }
        .main-header p {
            color: rgba(255,255,255,0.9) !important;
            margin: 10px 0 0 0;
        }
        .result-card {
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 16px;
            background: #fafafa;
        }
        .detail-card {
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 20px;
            background: white;
        }
        .query-section {
            background: #f8fafc;
            padding: 20px;
            border-radius: 12px;
        }
        .status-badge {
            font-size: 12px;
            padding: 4px 12px;
            border-radius: 20px;
            background: #e8f5e9;
            color: #2e7d32;
        }
        """
    ) as demo:
        
        # 标题区域
        gr.HTML("""
        <div class="main-header">
            <h1>🧪 SSBR 官能化方案智能推荐系统</h1>
            <p>基于语义理解的绿色轮胎材料解决方案推荐</p>
        </div>
        """)
        
        with gr.Row():
            # 左侧：查询面板
            with gr.Column(scale=2):
                gr.Markdown("### 🔍 描述您的需求")
                
                with gr.Group(elem_classes="query-section"):
                    query_input = gr.Textbox(
                        label="",
                        placeholder="例如：改善白炭黑分散性、降低滚动阻力、提高抓地力...",
                        lines=2,
                        show_label=False
                    )
                    
                    with gr.Row():
                        top_k_slider = gr.Slider(
                            minimum=1,
                            maximum=10,
                            value=5,
                            step=1,
                            label="推荐方案数量"
                        )
                        search_btn = gr.Button("🚀 获取推荐", variant="primary", size="lg")
                
                gr.Markdown("### 💡 试试这些查询")
                gr.Examples(
                    examples=EXAMPLE_QUERIES,
                    inputs=query_input,
                    label="",
                    examples_per_page=7
                )
                
                # 系统状态（简化）
                with gr.Row():
                    status_text = gr.Markdown(get_system_status())
            
            # 右侧：结果展示
            with gr.Column(scale=3):
                gr.Markdown("### 📊 推荐方案")
                
                result_output = gr.Markdown(
                    value="*输入您的需求，点击「获取推荐」查看结果*",
                    elem_classes="result-card"
                )
        
        # 详情区域
        gr.Markdown("---")
        gr.Markdown("### 📋 方案详情")
        
        with gr.Row():
            with gr.Column(scale=1):
                sample_dropdown = gr.Dropdown(
                    label="选择查看详情",
                    choices=[],
                    interactive=True
                )
            with gr.Column(scale=3):
                detail_output = gr.Markdown(
                    value="*选择上方推荐方案查看详细信息*",
                    elem_classes="detail-card"
                )
        
        # 底部说明
        gr.Markdown("""
        ---
        ### 📖 使用指南
        
        1. **输入需求**: 用自然语言描述您希望解决的问题，如"改善分散性"、"降低滚阻"等
        2. **查看推荐**: 系统会返回最相关的官能化方案，按匹配度排序
        3. **方案详情**: 点击下拉菜单可查看每个方案的详细信息
        
        **匹配度说明**:
        - 🟢 **高**: 与您的需求高度相关
        - 🟡 **中**: 有一定参考价值
        - 🔵 **低**: 供参考，建议结合具体情况评估
        
        ---
        *SSBR 官能化知识库 | 基于语义检索的智能推荐系统*
        """)
        
        # 绑定事件
        search_btn.click(
            search_samples,
            inputs=[query_input, top_k_slider],
            outputs=[result_output, detail_output, sample_dropdown]
        )
        
        query_input.submit(
            search_samples,
            inputs=[query_input, top_k_slider],
            outputs=[result_output, detail_output, sample_dropdown]
        )
        
        sample_dropdown.change(
            get_sample_detail,
            inputs=sample_dropdown,
            outputs=detail_output
        )
    
    return demo


# ==================== 启动 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("SSBR 官能化方案智能推荐系统")
    print("=" * 60)
    print()
    
    demo = create_demo()
    
    # 启动服务
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # 设为 True 可生成公网分享链接
        show_error=True
    )
