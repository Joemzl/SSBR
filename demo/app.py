"""
SSBR 官能化方案智能推荐系统 - Web Demo
基于 RAG 语义检索和问答生成的绿色轮胎材料推荐

用于毕业项目演示

Usage:
    python demo/app.py
    
Then open http://localhost:7861 in browser

性能优化 (2026-03-19):
- 启动时预加载向量缓存
- 查询延迟从 25-30秒 降低到 1-2秒

功能增强 (2026-03-19 - 003-rag-qa-enhancement):
- 添加 AI 问答功能（自然语言回答生成）
- 集成交叉编码器重排
- 支持检索+回答和仅检索两种模式
"""

import sys
import time
import io
from pathlib import Path

# 修复 Windows 控制台 Unicode 编码问题
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import gradio as gr
from scripts.rag_search import RAGSearchEngine
from scripts.qa_engine import QAEngine, QAEngineConfig
from scripts.models import AnswerType
from demo.data_formatter import (
    format_result_for_display,
    format_results_as_markdown,
    format_detail_as_markdown,
    FriendlyResult,
    similarity_to_match_level
)

# 初始化检索引擎（启用向量缓存）
print("正在初始化检索引擎...")
engine = RAGSearchEngine(use_cache=True)

# 初始化 QA 引擎
print("正在初始化问答引擎...")
qa_config = QAEngineConfig(
    enable_rerank=False,  # 暂时禁用重排（模型加载问题）
    enable_quality_scoring=True
)
qa_engine = QAEngine(config=qa_config, search_engine=engine)

# 存储当前搜索结果（用于详情查看）
current_results: list[FriendlyResult] = []

# 启动时预加载缓存的标志
_cache_preloaded = False


def preload_cache():
    """预加载向量缓存（在首次访问前调用）"""
    global _cache_preloaded
    if _cache_preloaded:
        return
    
    print("正在预加载向量缓存...")
    start = time.time()
    
    try:
        updated = engine.ensure_cache()
        elapsed = time.time() - start
        
        stats = engine.get_cache_stats()
        print(f"✅ 向量缓存加载完成: {stats.get('total_documents', 0)} 个文档，"
              f"更新 {updated} 个，耗时 {elapsed:.1f} 秒")
        
        _cache_preloaded = True
    except Exception as e:
        print(f"⚠️ 向量缓存加载失败: {e}")


# ==================== 核心功能函数 ====================

def search_and_answer(query: str, top_k: int = 3) -> tuple:
    """
    执行语义检索并生成 AI 回答
    
    Returns:
        (answer_html, samples_html, dropdown_choices, stats_text)
    """
    global current_results
    
    # 确保缓存已加载
    preload_cache()
    
    if not query.strip():
        return (
            "❌ 请输入您的研究问题",
            "",
            gr.update(choices=[], value=None),
            ""
        )
    
    try:
        # 执行问答
        response = qa_engine.answer(query, top_k=int(top_k), include_samples=True)
        
        # 格式化 AI 回答
        answer = response.answer
        answer_type_label = {
            AnswerType.DIRECT: "✅ 高相关度回答",
            AnswerType.REFERENCE: "⚠️ 参考性回答",
            AnswerType.GUIDANCE: "💡 引导性回答"
        }.get(answer.answer_type, "回答")
        
        # 将样本ID转换为用户友好的官能团名称
        source_descriptions = []
        if answer.source_samples and response.samples:
            for sample_id in answer.source_samples:
                for r in response.samples:
                    if r.sample_id == sample_id:
                        content = engine.get_summary_content(sample_id)
                        if content:
                            fr = format_result_for_display(
                                sample_id=sample_id,
                                similarity=r.similarity,
                                summary_content=content,
                                index=0,
                                query=query
                            )
                            source_descriptions.append(fr.functional_group)
                        break
        
        # 置信度转换为用户友好描述
        confidence_label = {
            "high": "高",
            "medium": "中等",
            "low": "较低"
        }.get(answer.confidence.value, answer.confidence.value)
        
        answer_html = f"""### {answer_type_label}

{answer.answer_text}

---
**参考方案**: {', '.join(source_descriptions) if source_descriptions else '通用领域知识'}
**置信度**: {confidence_label}
"""
        
        # 格式化样本列表（用户友好格式，不暴露内部ID和分数）
        if response.samples:
            # 先转换为用户友好格式
            friendly_results = []
            for i, r in enumerate(response.samples, 1):
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
            
            # 使用用户友好的表格格式
            samples_html = "### 相关方案\n\n"
            samples_html += "| 排名 | 官能化方案 | 匹配度 | 官能化试剂 | 来源 |\n"
            samples_html += "|:----:|-----------|:------:|-----------|------|\n"
            
            for fr in friendly_results:
                match_emoji = {"高": "🟢", "中": "🟡", "低": "🔵"}.get(fr.match_level, "⚪")
                samples_html += f"| {fr.index} | **{fr.functional_group}** | {match_emoji} {fr.match_level} | {fr.reagent[:20]}... | {fr.source[:15]}... |\n" if len(fr.reagent) > 20 else f"| {fr.index} | **{fr.functional_group}** | {match_emoji} {fr.match_level} | {fr.reagent} | {fr.source[:20]}... |\n"
            
            dropdown_choices = [f"方案 {r.index}: {r.functional_group}" for r in friendly_results]
        else:
            samples_html = "*无相关样本*"
            current_results = []
            dropdown_choices = []
        
        # 性能统计（简化展示，隐藏技术细节）
        total_time = response.total_time_ms
        if total_time < 1000:
            stats_text = f"⏱️ 响应时间: {total_time}ms"
        else:
            stats_text = f"⏱️ 响应时间: {total_time/1000:.1f}s"
        
        return (
            answer_html,
            samples_html,
            gr.update(choices=dropdown_choices, value=dropdown_choices[0] if dropdown_choices else None),
            stats_text
        )
        
    except Exception as e:
        current_results = []
        error_msg = str(e)
        
        # 提供更友好的错误消息
        if "额度不足" in error_msg or "quota" in error_msg.lower():
            user_error = "❌ API 额度不足，请联系管理员充值"
        elif "网络" in error_msg or "timeout" in error_msg.lower():
            user_error = "❌ 网络连接超时，请稍后重试"
        elif "API" in error_msg:
            user_error = "❌ API 服务暂时不可用，请稍后重试"
        else:
            user_error = f"❌ 生成回答出错: {error_msg[:100]}"
        
        return (
            user_error,
            "",
            gr.update(choices=[], value=None),
            ""
        )


def search_samples(query: str, top_k: int = 5) -> tuple:
    """执行语义检索并返回格式化结果"""
    global current_results
    
    # 确保缓存已加载
    preload_cache()
    
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

# 简约学术风格主题
ACADEMIC_THEME = gr.themes.Base(
    primary_hue=gr.themes.colors.emerald,
    secondary_hue=gr.themes.colors.slate,
    neutral_hue=gr.themes.colors.slate,
    font=gr.themes.GoogleFont("IBM Plex Sans"),
    font_mono=gr.themes.GoogleFont("IBM Plex Mono"),
).set(
    # 深色背景
    body_background_fill="#0f172a",
    body_background_fill_dark="#0f172a",
    background_fill_primary="#1e293b",
    background_fill_primary_dark="#1e293b",
    background_fill_secondary="#334155",
    background_fill_secondary_dark="#334155",
    # 文字颜色
    body_text_color="#e2e8f0",
    body_text_color_dark="#e2e8f0",
    body_text_color_subdued="#94a3b8",
    body_text_color_subdued_dark="#94a3b8",
    # 边框
    border_color_primary="#475569",
    border_color_primary_dark="#475569",
    block_border_width="1px",
    # 按钮
    button_primary_background_fill="#10b981",
    button_primary_background_fill_dark="#10b981",
    button_primary_background_fill_hover="#059669",
    button_primary_background_fill_hover_dark="#059669",
    button_primary_text_color="#ffffff",
    button_primary_text_color_dark="#ffffff",
    # 输入框
    input_background_fill="#1e293b",
    input_background_fill_dark="#1e293b",
    input_border_color="#475569",
    input_border_color_dark="#475569",
    input_border_color_focus="#10b981",
    input_border_color_focus_dark="#10b981",
    # 块元素
    block_background_fill="#1e293b",
    block_background_fill_dark="#1e293b",
    block_label_background_fill="#334155",
    block_label_background_fill_dark="#334155",
    block_label_text_color="#e2e8f0",
    block_label_text_color_dark="#e2e8f0",
    block_title_text_color="#e2e8f0",
    block_title_text_color_dark="#e2e8f0",
)

# 学术简约风格 CSS
ACADEMIC_CSS = """
/* 学术简约风格 */
.main-header {
    text-align: center;
    padding: 32px 24px;
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    margin-bottom: 24px;
}
.main-header h1 {
    color: #f1f5f9 !important;
    font-weight: 600;
    font-size: 1.75rem;
    margin: 0 0 8px 0;
    letter-spacing: -0.02em;
}
.main-header p {
    color: #94a3b8 !important;
    font-size: 0.95rem;
    margin: 0;
}
.main-header .accent {
    color: #10b981;
}
/* 卡片样式 */
.result-card, .detail-card {
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 20px;
    background: #1e293b;
}
.query-section {
    background: #1e293b;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #334155;
}
/* Markdown 样式优化 */
.prose h3, .prose h4 {
    color: #f1f5f9 !important;
}
.prose p, .prose li {
    color: #cbd5e1 !important;
}
.prose strong {
    color: #10b981 !important;
}
.prose code {
    background: #334155 !important;
    color: #10b981 !important;
    padding: 2px 6px;
    border-radius: 4px;
}
/* 表格样式 */
.prose table {
    border-collapse: collapse;
    width: 100%;
}
.prose th {
    background: #334155 !important;
    color: #f1f5f9 !important;
    padding: 10px 12px;
    text-align: left;
    font-weight: 500;
    border-bottom: 2px solid #10b981;
}
.prose td {
    padding: 10px 12px;
    border-bottom: 1px solid #475569;
    color: #cbd5e1 !important;
}
.prose tr:hover td {
    background: #334155;
}
/* 状态指示 */
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.85rem;
    color: #10b981;
}
.status-dot {
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
}
/* 示例按钮 */
.examples-table button {
    background: #334155 !important;
    border: 1px solid #475569 !important;
    color: #e2e8f0 !important;
}
.examples-table button:hover {
    background: #475569 !important;
    border-color: #10b981 !important;
}
"""


def create_demo():
    """创建 Gradio 演示界面"""
    
    with gr.Blocks(title="SSBR 官能化方案推荐系统") as demo:
        
        # 标题区域 - 简约学术风格
        gr.HTML("""
        <div class="main-header">
            <h1>SSBR 官能化方案智能推荐系统</h1>
            <p>基于 RAG 语义检索与 AI 问答的绿色轮胎材料推荐</p>
        </div>
        """)
        
        with gr.Row():
            # 左侧：查询面板
            with gr.Column(scale=2):
                gr.Markdown("### 描述您的研究需求")
                
                with gr.Group(elem_classes="query-section"):
                    query_input = gr.Textbox(
                        label="",
                        placeholder="例如：改善白炭黑分散性、降低滚动阻力、提高湿地抓地力...",
                        lines=2,
                        show_label=False
                    )
                    
                    with gr.Row():
                        top_k_slider = gr.Slider(
                            minimum=1,
                            maximum=10,
                            value=3,
                            step=1,
                            label="返回方案数"
                        )
                    
                    with gr.Row():
                        qa_btn = gr.Button("🤖 检索并生成回答", variant="primary", size="lg")
                        search_btn = gr.Button("🔍 仅检索推荐", variant="secondary", size="lg")
                
                gr.Markdown("### 示例查询")
                gr.Examples(
                    examples=EXAMPLE_QUERIES,
                    inputs=query_input,
                    label="",
                    examples_per_page=7
                )
                
                # 系统状态和性能统计
                with gr.Row():
                    status_text = gr.Markdown(get_system_status())
                stats_output = gr.Markdown("", elem_id="stats-output")
            
            # 右侧：结果展示
            with gr.Column(scale=3):
                # AI 回答区域
                gr.Markdown("### 📝 AI 回答")
                answer_output = gr.Markdown(
                    value="*输入研究需求后点击「检索并生成回答」获取 AI 分析*",
                    elem_classes="result-card"
                )
                
                # 推荐列表区域
                gr.Markdown("### 📋 推荐方案")
                result_output = gr.Markdown(
                    value="*输入研究需求后点击「仅检索推荐」查看推荐结果*",
                    elem_classes="result-card"
                )
        
        # 详情区域
        gr.Markdown("---")
        gr.Markdown("### 方案详情")
        
        with gr.Row():
            with gr.Column(scale=1):
                sample_dropdown = gr.Dropdown(
                    label="选择方案",
                    choices=[],
                    interactive=True
                )
            with gr.Column(scale=3):
                detail_output = gr.Markdown(
                    value="*从下拉列表选择方案查看详细信息*",
                    elem_classes="detail-card"
                )
        
        # 底部说明
        gr.Markdown("""
        ---
        ### 使用说明
        
        | 模式 | 按钮 | 说明 |
        |:----:|------|------|
        | **问答模式** | 🤖 检索并生成回答 | 基于检索结果生成专业的 AI 回答，包含引用来源 |
        | **推荐模式** | 🔍 仅检索推荐 | 传统语义检索，返回最相关的官能化方案列表 |
        
        **回答类型**:
        - ✅ 高相关度回答：找到高度匹配的样本 (相似度 ≥ 0.7)
        - ⚠️ 参考性回答：找到中等相关的样本 (相似度 0.5-0.7)，建议进一步验证
        - 💡 引导性回答：未找到高相关样本，提供领域通用建议
        
        ---
        <p style="text-align: center; color: #64748b; font-size: 0.85rem;">
        SSBR 官能化知识库 · RAG QA Enhancement v1.0
        </p>
        """)
        
        # 绑定事件 - 问答模式
        qa_btn.click(
            search_and_answer,
            inputs=[query_input, top_k_slider],
            outputs=[answer_output, result_output, sample_dropdown, stats_output]
        )
        
        # 绑定事件 - 仅检索模式
        def search_only_wrapper(query, top_k):
            result, detail, dropdown = search_samples(query, top_k)
            return "*使用「检索并生成回答」获取 AI 分析*", result, dropdown, ""
        
        search_btn.click(
            search_only_wrapper,
            inputs=[query_input, top_k_slider],
            outputs=[answer_output, result_output, sample_dropdown, stats_output]
        )
        
        query_input.submit(
            search_and_answer,
            inputs=[query_input, top_k_slider],
            outputs=[answer_output, result_output, sample_dropdown, stats_output]
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
    print("RAG QA Enhancement v1.0")
    print("=" * 60)
    print()
    
    # 启动时预加载向量缓存
    print("正在预加载向量缓存（首次启动可能需要 1-2 分钟）...")
    preload_cache()
    print()
    
    # 显示缓存统计
    stats = engine.get_cache_stats()
    print(f"缓存状态: {stats.get('total_documents', 0)} 个文档已索引")
    
    # 预热 QA 引擎（可选，首次查询会自动加载）
    print()
    print("正在预热 QA 引擎...")
    try:
        warmup_times = qa_engine.warmup()
        print(f"  ✅ 搜索引擎: {warmup_times.get('search_engine', 0)}ms")
        print(f"  ✅ 质量评估: {warmup_times.get('quality_scorer', 0)}ms")
        if 'reranker' in warmup_times:
            print(f"  ✅ 重排模型: {warmup_times.get('reranker', 0)}ms")
        print("QA 引擎预热完成!")
    except Exception as e:
        print(f"  ⚠️ 重排模型将在首次使用时加载: {e}")
    print()
    
    demo = create_demo()
    
    # 启动服务
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,  # 设为 True 可生成公网分享链接
        show_error=True,
        theme=ACADEMIC_THEME,
        css=ACADEMIC_CSS
    )
