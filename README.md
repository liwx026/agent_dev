# agent-dev

一个使用 Python 调用大模型 API 的学习项目，当前以智谱 GLM 兼容 OpenAI SDK 的接口为例，练习基础 API 调用、Prompt 设计和 Function Calling。

## 功能

- `llm_api_call.py`
	- 调用 Chat Completions API。
	- 将英文内容翻译为中文。
	- 根据输入生成包含收件人、主题和内容字段的 JSON 邮件草稿。
- `function_call.py`
	- 向模型注册 `get_weather` 和 `caculater` 两个工具。
	- 根据模型返回的 `tool_calls` 执行 Python 函数。
	- 将工具结果以 `role: tool` 消息传回模型，直到模型生成最终回复。

## 环境要求

- Python 3.12 至 4.0 以下版本
- 智谱 API Key
- 项目依赖：`openai >= 3.3.1, < 4.0.0`、`langchain >= 1.3.17, < 2.0.0`、`langchain-openai >= 1.1.0, < 2.0.0`

## 安装

使用 Poetry：

```bash
poetry install
```

或在虚拟环境中安装依赖：

```bash
python -m pip install "openai>=3.3.1,<4.0.0"
```

## 配置

在当前终端设置 API Key：

```bash
export GLM_API_KEY="你的智谱API_KEY"
```

配置集中在 `src/agent_dev/utils.py`：

| 配置 | 当前值 | 说明 |
| --- | --- | --- |
| `API_KEY` | `GLM_API_KEY` 环境变量 | API 密钥，不应写入代码或提交到仓库 |
| `BASE_URL` | `https://open.bigmodel.cn/api/paas/v4` | 智谱 OpenAI 兼容接口地址 |
| `MODEL` | `glm-5.2` | 默认模型名称，需与账号可用模型一致 |

## 运行

从项目根目录执行：

```bash
python src/agent_dev/llm_api_call.py
```

该命令会执行一个翻译示例。

运行 Function Calling 交互示例：

```bash
python src/agent_dev/function_call.py
```

输入问题后，模型可以选择天气或计算器工具；输入 `bye` 退出。例如：

```text
北京天气怎么样？
计算 12 * 8
bye
```

## Function Calling 流程

1. 程序通过 `tools` 参数向模型提供函数名称、描述和参数 Schema。
2. 模型返回普通消息或一个或多个 `tool_calls`。
3. 程序根据函数名从 `self.funcs` 中找到 Python 函数，并解析 JSON 参数。
4. 程序把函数结果作为工具消息追加到历史消息。
5. 再次请求模型，直到模型不再要求调用工具并输出最终结果。

计算器支持 `+`、`-`、`*`、`/`；其他运算符会抛出 `ValueError`，除数为零会抛出 `ZeroDivisionError`。

## 项目结构

```text
.
├── pyproject.toml
├── README.md
├── src/
│   └── agent_dev/
│       ├── __init__.py
│       ├── function_call.py
│       ├── llm_api_call.py
│       └── utils.py
└── tests/
		└── __init__.py
```

## 当前注意事项

- 两个示例脚本使用相对脚本目录可用的直接导入方式，推荐按上面的命令直接运行，不要使用 `python -m agent_dev...`。
- `function_call.py` 会把多轮对话保存在内存中，程序退出后不会持久化。
- 工具执行异常目前会直接终止当前交互轮次。
- `llm_api_call.py` 中的 `tools` 参数已保留在方法签名中，但当前示例只演示普通文本请求。
- 没有配置 API Key 时，远程请求无法正常完成；README 不包含任何真实密钥。

## 检查语法

不发送 API 请求的基础检查：

```bash
python -m compileall -q src
```
