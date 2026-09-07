from langchain.agents import create_agent,AgentState

from langchain_openai import ChatOpenAI
from agent_dev.lang_chain_test  import API_KEY, BASE_URL,MODEL
from pydantic import SecretStr,BaseModel
from langchain.agents.middleware import dynamic_prompt, ModelRequest

model = ChatOpenAI(model=MODEL, temperature=0, api_key=SecretStr(API_KEY), base_url=BASE_URL)

## 6. System Prompt（系统提示词）

### 6.1 基础用法
agent = create_agent(
    model=model,
    system_prompt="你是一个乐于助人的助手。回答需简洁且准确。",
)
### 6.2 带角色的 System Prompt

SYSTEM_PROMPT = """你是一名高级数据分析师。你的职责：

1. 理解用户的数据分析需求
2. 使用提供的工具查询并分析数据
3. 以清晰、有条理的格式展示分析结果
4. 输出结果前务必核对计算过程
"""

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
)


### 6.3 动态 Prompt

# 运行时动态修改 prompt，
@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest)-> str:
    """根据用户上下文动态修改系统提示词"""
    user_id = request.runtime.context.get("user_id", "guest")
    return f"你是一名数据分析师。当前用户 ID: {user_id}。"
    

    
agent = create_agent(
    model=model,
    middleware=[dynamic_system_prompt],
)

res = agent.invoke(
    {"messages": [{"role": "user", "content": "请根据用户需求提供分析建议。"}]},
    context={"user_id": "alice_123"},
)
print(res) # 输出结果将包含动态修改后的系统提示词