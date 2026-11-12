# 头像管线 SOP（新国家数据集标准流程）

> 沉淀自 2026-11-11~12 全局头像工程（54 数据集、12946 张图落地）。
> 问题全量台账见 [avatar-issues.md](avatar-issues.md)；网络细节见 skill 的 network_config.md。

## 标准流程（按序执行）

```
1. 采集（P1-P5 管线）
   └─ 头像源只收直链；profile 只能是 {source_url, local_path, minio_path} 对象
2. 批量下载      python scripts_tmp/a6_download.py --only person   # 然后 --only org
   └─ 双通道（28081 图片代理 + AnitCloud）+ FilePath API 路由 + 魔数校验
   └─ 直接写 minio-store/default/{popular-person|org-profile}/{cc}/<ID>.<ext>
   └─ 同时回写 local_path（相对项目根）+ minio_path（对象 key）
3. 审计          python scripts_tmp/avatar_audit.py
   └─ 检查 bad_source_url / bad_naming / local_missing / download_gap / malformed
4. 修复（按 audit_result.json 分类处置，脚本见下表）
5. 上传 MinIO    打包 upload_kit_stage/（upload_to_minio.py + minio-store）→ 生产执行
   └─ 纯标准库 SigV4，零依赖，Python 3.6+；--selftest/--dry/--verify 三件套
6. 对账关单      --verify 输出 ok=N missing=0 size-diff=0，N = minio_path 有值数
```

## 布局约定（2026-11-12 起）

| 层 | 值 |
|---|---|
| 本地镜像 | `minio-store/default/popular-person-profile/{cc}/<PERSON-ID>.<ext>`（org 用 popular-org-profile） |
| local_path | `minio-store/default/...`（**相对项目根**） |
| minio_path | `default/popular-person-profile/{cc}/<ID>.<ext>`（对象 key，无前导 `/`） |
| 桶 | `default` |

## 可复用脚本清单（scripts_tmp/）

| 脚本 | 用途 |
|---|---|
| `a6_download.py` | **主力下载器**：双通道 + FilePath 转换 + 断点 + 直接写 minio-store 布局 |
| `avatar_audit.py` | 全库审计（已兼容 minio-store 布局） |
| `fix_avatar_links.py` | File: 死链 / QID 页修复（P18 解析） |
| `fix_org_avatar_links.py` | 同上 org 版（P154 logo 优先） |
| `fix_social_avatars.py` | 社交链接处置（graph.facebook 可下载，主页置 null） |
| `a4_step1_probe.py` / `a4_step23_wiki.py` / `a4_step4_og.py` | html 链接四步漏斗（Content-Type / pageimages / P18 / og:image） |
| `a5_fix_malformed.py` | malformed profile 修复（文本备份后置 null） |
| `migrate_to_minio_store.py` | 旧布局 → minio-store 一次性迁移（已执行过，新数据集不需要） |
| `../upload_kit_stage/upload_to_minio.py` | 生产上传（纯 stdlib SigV4，py3.6+） |

## 踩坑速查

- Wikimedia 直连域名并发即封（robot policy 429，封出口 IP）→ 只走 FilePath API
- 多语言 wiki 文件不在 commons → `ar.wikipedia.org/wiki/Special:FilePath/...`
- Windows 杀软/索引器锁 JSON → os.replace 带 4 次重试（a6 内置）
- 后台管道 `| tail` 会吞进度日志 → 用 `-u` 直写文件
- 后端 28081 `/image` 走 nginx 路径分发；`/api/v1/image-to-base64` 对 Wikimedia 403（服务端出口被拒）不可用
