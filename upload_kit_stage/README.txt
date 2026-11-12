# MinIO 头像上传包（离线自包含，零依赖）

## 内容

- upload_to_minio.py   上传脚本（纯 Python 标准库，Python >= 3.6，无需 pip）
- minio-store/default/ 全部图片（12946 张 / 约 2.2GB）
  - 人物: popular-person-profile/{国家码}/<PERSON-ID>.<ext>  (8981)
  - 组织: popular-org-profile/{国家码}/<ORG-ID>.<ext>        (3965)
- minio.conf.example   配置模板

对象 key = minio-store/default/ 下的相对路径，与数据集中 profile.minio_path
字段严格一致；桶名默认 default（path-style 直传，S3 SigV4 协议）。

## 使用步骤

1. 解压: tar -xf minio-upload-kit.tar
2. 配置: cp minio.conf.example minio.conf && vi minio.conf
   填 MINIO_ENDPOINT / MINIO_ACCESS_KEY / MINIO_SECRET_KEY
   （也可用环境变量，env 优先于 conf）
3. 自检: python3 upload_to_minio.py --selftest   # 签名算法自测，应输出 PASS
4. 试运行: python3 upload_to_minio.py --dry       # 应显示 12946 objects
5. 上传:   python3 upload_to_minio.py
   - 断点续传：中断后重跑自动跳过已传（upload_state.json）
   - 4 线程、单文件 3 次重试、每 100 个打 checkpoint
6. 对账:   python3 upload_to_minio.py --verify
   预期: ok=12946 missing=0 size-diff=0

## 配置项

MINIO_ENDPOINT   host:port，不带 http://（例 10.1.2.3:9000）
MINIO_ACCESS_KEY / MINIO_SECRET_KEY
MINIO_SECURE     1=https（默认） 0=http（内网常见）
MINIO_BUCKET     默认 default
MINIO_REGION     默认 us-east-1（MinIO 一般不用改）
MINIO_INSECURE   1=自签证书跳过校验（仅 https 时用）
