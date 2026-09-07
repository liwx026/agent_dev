# agent-dev

一个用于学习大模型应用开发的 Python 项目。项目以智谱 GLM 的 OpenAI 兼容接口为例，记录从基础 Chat Completions 调用到 Function Calling 的实现过程。

README 只覆盖当前仓库中已纳入 Git 的公开文件；被 `.gitignore` 排除的本地实验目录不属于项目的公开入口。

## 内容概览

- **基础 API 调用**：使用 OpenAI Python SDK 调用 Chat Completions，练习翻译和邮件草稿生成。
- **Function Calling**：注册天气查询和计算器工具，解析模型返回的 `tool_calls`，执行工具后继续请求模型。
- **LangChain Agent 示例**：`agent_tools.py` 展示工具、Middleware 和内存 Checkpointer 的组合用法。
- **配置与消息处理**：`utils.py` 集中管理 API 配置，并提供 LangChain 消息格式化辅助函数。

这是一个学习和实验项目，不是生产级 Agent 框架。示例代码会直接打印结果，暂未提供稳定的 CLI、持久化会话或完整测试套件。

## 环境要求

- Python `3.12` 或更高版本，且低于 `4.0`
- Poetry `2.x`
- 一个兼容 OpenAI API 的模型服务账号。本项目默认使用智谱 GLM

## 安装

在项目根目录执行：

```bash
poetry install
```

该命令会根据 `pyproject.toml` 和 `poetry.lock` 安装完整依赖，包括 OpenAI SDK、LangChain、LangGraph 和 PostgreSQL Checkpointer 相关包。

## 配置 API

不要把 API Key 写入源码或提交到仓库。在当前终端设置环境变量：

```bash
export GLM_API_KEY="你的智谱 API Key"
```

项目默认配置位于 `src/agent_dev/utils.py`：

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `API_KEY` | 读取 `GLM_API_KEY` | API 密钥，缺少时无法完成远程请求 |
| `BASE_URL` | `https://open.bigmodel.cn/api/paas/v4` | 智谱 OpenAI 兼容接口地址 |
| `MODEL` | `GLM-4.5-Air` | 使用前确认模型名称和账号权限 |

## 运行示例

安装项目后，从根目录使用模块方式运行：

### 基础调用

```bash
poetry run python -m agent_dev.llm_api_call
```

该示例会向模型发送一段中英文文本，并输出中文翻译。

### Function Calling

```bash
poetry run python -m agent_dev.function_call
```

程序启动后输入问题，模型可以选择天气工具或计算器工具；输入 `bye` 退出：

```text
北京天气怎么样？
计算 12 * 8
bye
```

计算器支持 `+`、`-`、`*`、`/`。工具调用和对话历史只保存在当前进程内，程序退出后不会持久化。

### LangChain Agent

```bash
poetry run python -m agent_dev.agent_tools
```

该示例包含天气、计算器和 Todo 工具，并使用 `InMemorySaver` 保存当前进程内的会话状态。它仍是实验代码，运行前建议先阅读源码。

## Function Calling 流程

1. 客户端通过 `tools` 参数向模型提供工具名称、描述和参数 Schema。
2. 模型返回普通消息，或返回一个或多个 `tool_calls`。
3. 程序根据工具名称找到 Python 函数，并解析模型提供的 JSON 参数。
4. 程序把工具结果作为 `role: tool` 消息追加到对话历史。
5. 程序再次请求模型，直到模型输出最终回复。

## 项目结构

```text
.
├── .gitignore
├── .python-version
├── README.md
├── poetry.lock
├── pyproject.toml
└── src/
    └── agent_dev/
        ├── __init__.py
        ├── agent_tools.py
        ├── function_call.py
        ├── llm_api_call.py
        ├── system_prompt.py
        └── utils.py
```

| 文件 | 作用 |
| --- | --- |
| `pyproject.toml` | 项目元数据、Python 版本和依赖声明 |
| `src/agent_dev/utils.py` | API 配置和消息格式化辅助函数 |
| `src/agent_dev/llm_api_call.py` | 基础 Chat Completions 调用示例 |
| `src/agent_dev/function_call.py` | OpenAI 兼容 Function Calling 示例 |
| `src/agent_dev/agent_tools.py` | LangChain Agent、工具和内存示例 |
| `src/agent_dev/system_prompt.py` | 系统提示词和动态提示词的学习片段 |

## 检查

以下检查不会发送 API 请求：

```bash
poetry check
poetry run python -m compileall -q src
```

运行需要模型服务的示例前，请确认 `GLM_API_KEY` 已配置，并注意相关调用可能产生费用。

## 安全说明

- API Key 仅通过环境变量读取，不要提交真实密钥、`.env` 文件或日志。
- 示例中的天气工具返回固定文本，并不会访问真实天气服务。
- `agent_tools.py` 中的计算器使用了 `eval`，仅适合受控学习环境，不要直接暴露给不可信输入。
