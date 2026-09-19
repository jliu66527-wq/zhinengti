# 智能体 · Octop 代码快照

本仓库从本机已安装的 Octop 1.0.1 提取应用代码，上传日期为 2026-09-19。
原项目：https://github.com/TencentCloud/Octop 。保留原 MIT 许可证及代码内的第三方许可。

## 内容与边界

- `octop/`：Python 应用源码、内置资源及已编译的 Dashboard 管理界面。
- `requirements.txt`：从安装包元数据提取的基础依赖约束。
- `pyproject.toml`：为此代码快照补充的安装配置。
- 不包含原项目 Git 历史、前端 TypeScript/Vue/React 开发工程或原项目测试集。
- 不包含本机凭据、用户配置、数据库、对话记录、日志、浏览器资料、下载模型和虚拟环境。
- 这是安装版本的代码快照，不是个人数据备份，也未修改原有服务重启逻辑。

## 安装与运行

需要 Python 3.12 或更高版本，在独立环境安装：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e .
octop --help
```

依赖保留上游的版本范围，未锁定全部间接依赖。私有或镜像尚未同步的包可能需要原项目使用的包源。
请使用独立的 `OCTOP_HOME` 初始化配置，避免与已有实例共享数据库；实际运行前按 CLI 帮助完成设置。
此快照仅完成静态检查，未在新环境验证安装或启动。
