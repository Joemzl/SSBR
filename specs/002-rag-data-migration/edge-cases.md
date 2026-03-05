# 边界情况处理文档

**Date**: 2026-03-05 | **Branch**: `002-rag-data-migration`

---

## 概述

本文档定义 RAG 推荐系统在边界情况下的处理策略。

---

## 1. 空查询处理

### 场景
用户输入为空或仅包含空白字符。

### 处理策略

```python
# scripts/utils/query_preprocessor.py
def preprocess_query(query: str) -> str:
    if not query or not query.strip():
        raise ValueError("查询内容不能为空，请输入您的需求描述")
    return query.strip()
```

### 用户提示
```
错误：查询内容不能为空，请输入您的需求描述。

示例查询：
- "我需要改善白炭黑分散性"
- "寻找低滚阻高抓地力的官能化方案"
- "羧基官能化 SSBR 的性能数据"
```

---

## 2. 超长查询处理

### 场景
用户输入超过 500 字符。

### 处理策略

```python
MAX_QUERY_LENGTH = 500

def preprocess_query(query: str) -> str:
    query = query.strip()
    if len(query) > MAX_QUERY_LENGTH:
        # 截断并提示
        truncated = query[:MAX_QUERY_LENGTH]
        logger.warning(f"查询过长，已截断至 {MAX_QUERY_LENGTH} 字符")
        return truncated
    return query
```

### 用户提示
```
提示：您的查询已截断至 500 字符。建议使用更简洁的描述以获得更精准的推荐。
```

---

## 3. 特殊字符处理

### 场景
查询包含可能干扰检索的特殊字符。

### 处理策略

```python
import re

def preprocess_query(query: str) -> str:
    # 保留中英文、数字、常用标点
    # 移除控制字符和不可见字符
    query = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', query)
    
    # 标准化空白
    query = re.sub(r'\s+', ' ', query)
    
    return query.strip()
```

### 保留字符
- 中文字符
- 英文字母和数字
- 常用标点：`，。、；：？！（）-_+=%`
- 化学符号：`-OH`, `-COOH`, `Si(OEt)₃`

---

## 4. YAML 解析失败

### 场景
解读文档的 YAML front matter 格式错误。

### 处理策略

```python
# scripts/utils/yaml_parser.py
def read_interpretation_file(filepath: Path) -> dict:
    try:
        content = filepath.read_text(encoding='utf-8')
        yaml_part, body = parse_yaml_frontmatter(content)
        return {'yaml': yaml_part, 'body': body}
    
    except yaml.YAMLError as e:
        logger.error(f"YAML 解析失败 ({filepath}): {e}")
        # 返回空 YAML，保留正文
        return {
            'yaml': {'_parse_error': str(e)},
            'body': content
        }
```

### 用户提示
```
警告：文件 SSBR-001/mechanical.md 的 YAML 格式存在问题，部分结构化数据可能无法读取。
建议使用 YAML 验证器检查文件格式：https://www.yamllint.com/
```

### 常见 YAML 错误
| 错误类型 | 示例 | 修复方法 |
|----------|------|----------|
| 缩进不一致 | 混用空格和制表符 | 统一使用 2 空格 |
| 缺少引号 | `value: 10.1039/xxx` | `value: "10.1039/xxx"` |
| 冒号后无空格 | `key:value` | `key: value` |
| 特殊字符未转义 | `name: SSBR-g-MUA` | `name: "SSBR-g-MUA"` |

---

## 5. 文件缺失处理

### 场景
- summary.md 不存在
- mechanical.md 或 dsc.md 不存在
- 整个样本目录不存在

### 处理策略

```python
def get_sample_summary(sample_id: str) -> Optional[str]:
    summary_path = INTERPRETATIONS_DIR / sample_id / "summary.md"
    
    if not summary_path.exists():
        logger.warning(f"样本 {sample_id} 缺少 summary.md，跳过检索")
        return None
    
    return summary_path.read_text(encoding='utf-8')
```

### RAG 检索行为
- 缺少 summary.md 的样本**不参与检索**
- 在验证脚本中报告缺失情况
- 推荐结果中不包含不完整样本

### 用户提示
```
提示：以下样本缺少 summary.md，未参与本次检索：
- SSBR-018
- SSBR-019

请先为这些样本生成综合档案：
python scripts/generate_summaries.py --sample SSBR-018
```

---

## 6. Embedding API 失败

### 场景
- 网络不可用
- API Key 无效
- 配额用尽
- 超时

### 处理策略

```python
class EmbeddingService:
    MAX_RETRIES = 3
    RETRY_DELAY = 2
    
    def embed(self, text: str) -> List[float]:
        for attempt in range(self.MAX_RETRIES):
            try:
                return self._call_api(text)
            except RateLimitError:
                time.sleep(self.RETRY_DELAY * (attempt + 1))
                continue
            except NetworkError:
                time.sleep(self.RETRY_DELAY)
                continue
        
        raise EmbeddingError("API 调用失败，请检查网络和 API Key")
```

### 降级策略

| 错误类型 | 重试次数 | 降级行为 |
|----------|----------|----------|
| Rate Limit | 3 次 | 等待后重试，指数退避 |
| Network Error | 3 次 | 等待后重试 |
| Invalid API Key | 0 次 | 立即报错 |
| Quota Exceeded | 0 次 | 报错并建议等待 |

### 用户提示
```
错误：Embedding API 调用失败
原因：API 配额已用尽

解决方案：
1. 检查 OpenAI API 使用量
2. 等待配额重置（通常为次日）
3. 或升级 API 计划

当前推荐功能暂时不可用，其他功能不受影响。
```

---

## 7. 低相似度结果处理

### 场景
所有检索结果的相似度都低于阈值 0.5。

### 处理策略

```python
def classify_results(results: List[dict]) -> dict:
    high = [r for r in results if r['similarity'] >= 0.7]
    medium = [r for r in results if 0.5 <= r['similarity'] < 0.7]
    low = [r for r in results if r['similarity'] < 0.5]
    
    if not high and not medium:
        # 全部为低相似度
        return {
            'results': low[:3],  # 仍返回 Top-3
            'confidence': 'low',
            'message': '知识库中无高度相关案例，以下为参考'
        }
    
    return {
        'results': high + medium,
        'confidence': 'high' if high else 'medium',
        'message': None
    }
```

### 用户提示
```
提示：知识库中未找到高度相关的案例。

以下结果仅供参考（相关度 < 50%）：
1. SSBR-004 (相关度: 42%)
2. SSBR-007 (相关度: 38%)
3. SSBR-012 (相关度: 35%)

建议：
- 尝试更具体的查询描述
- 或使用不同的关键词
```

---

## 8. 数值范围异常

### 场景
解读文档中的数值超出合理范围。

### 验证规则

| 字段 | 最小值 | 最大值 | 单位 |
|------|--------|--------|------|
| stress_* | 0 | 50 | MPa |
| tensile_strength | 0 | 100 | MPa |
| elongation | 0 | 1000 | % |
| tg | -100 | 50 | ℃ |
| tan_delta_* | 0 | 2 | - |

### 处理策略

```python
def validate_mechanical_data(data: dict) -> List[str]:
    warnings = []
    
    if data.get('tensile_strength', {}).get('value', 0) > 100:
        warnings.append("拉伸强度超过合理范围 (>100 MPa)")
    
    if data.get('tg', {}).get('value', 0) > 50:
        warnings.append("Tg 超过合理范围 (>50℃)")
    
    return warnings
```

### 用户提示
```
警告：SSBR-005/mechanical.md 中存在可疑数据：
- 拉伸强度 (150 MPa) 超出合理范围 (0-100 MPa)

建议检查数据来源，确认数值是否正确。
```

---

## 9. 并发访问处理

### 场景
MVP 版本不支持多用户并发。

### 处理策略

```python
# 文件锁（简单实现）
import fcntl

def with_file_lock(filepath: Path):
    lock_file = filepath.with_suffix('.lock')
    
    with open(lock_file, 'w') as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            yield
        except BlockingIOError:
            raise ConcurrencyError("文件正在被其他进程使用，请稍后重试")
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
```

### 用户提示
```
错误：数据文件正在被其他进程使用

可能原因：
- 另一个终端正在执行脚本
- Excel 文件正在编辑中

解决方案：
- 等待其他操作完成
- 关闭正在编辑的 Excel 文件
```

---

## 测试清单

- [ ] 空查询返回友好提示
- [ ] 超长查询正确截断
- [ ] 特殊字符不影响检索
- [ ] YAML 错误不导致程序崩溃
- [ ] 缺失文件有明确提示
- [ ] API 失败有重试和降级
- [ ] 低相似度结果有明确标注
- [ ] 异常数值有警告提示
