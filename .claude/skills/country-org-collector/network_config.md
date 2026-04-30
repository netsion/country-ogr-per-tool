# 网络与工具配置

## 代理设置

本机网络环境需要通过代理访问 Wikipedia / Wikidata 等境外站点。

- **主代理**：`http://127.0.0.1:7890`
- **备用代理**：`http://10.11.204.68:8081`

所有批处理脚本（`atomic_write.py` 中的 `setup_proxy()`）自动执行主备切换：先尝试主代理，不通则回退到备用代理。

所有本地 HTTP 请求（curl / Python urllib）**必须配置代理**，否则会被网络层重置连接（`WinError 10054` / `curl:35 SSL connect error`）。浏览器通过 PAC 文件自动走代理，但命令行工具不会。

### curl 使用代理

```bash
curl -L --proxy "http://127.0.0.1:7890" "https://query.wikidata.org/sparql?..."
```

> **注意**：所有 curl 调用建议加 `-L` 参数（follow redirects）。Wikidata EntityData 等端点可能返回 HTTP redirect，缺少 `-L` 会保存 HTML 而非 JSON。

### Python urllib 使用代理

```python
from atomic_write import setup_proxy
setup_proxy()  # 自动主备切换
```

或手动配置：

```python
import urllib.request
proxy = urllib.request.ProxyHandler({
    'https': 'http://127.0.0.1:7890',
    'http': 'http://127.0.0.1:7890'
})
opener = urllib.request.build_opener(proxy)
# 注意：需同时设置 User-Agent，否则 Wikipedia REST API 返回 403
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with opener.open(req, timeout=30) as resp:
    data = json.loads(resp.read().decode())
```

### 设置环境变量（推荐，一次生效全局）

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

## Windows 编码注意事项

本机为 Windows 环境，Python 默认使用 GBK 编码，输出 CJK 字符会触发 `UnicodeEncodeError: 'gbk' codec can't encode character`。

**解决方案**（任选其一）：

```bash
# 方式1：设置环境变量
export PYTHONIOENCODING=utf-8
python script.py

# 方式2：脚本内设置（必须在任何 print 之前）
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## 工具选择策略

1. **Wikidata SPARQL** — 优先本地 curl + 代理（最稳定）；`mcp__search-read__read_url` 作备选
2. **Wikipedia REST API** — 三种方式均可，`mcp__search-read__read_url` 最便捷
3. **DBpedia SPARQL** — 仅本地 curl（MCP 工具对含 OPTIONAL/FILTER 的复杂查询会静默失败）
4. **普通网页** — `mcp__search-read__read_url` 优先，失败时用 `mcp__web_reader__webReader`
5. **本地 curl/Python 执行前** — 始终确认已设置代理
6. **Cloudflare JS Challenge** — 遇到 Cloudflare 防护（返回"Just a moment..."质询页）时，直接跳过该来源，改用 Wikipedia / 新闻搜索等其他数据源获取信息
