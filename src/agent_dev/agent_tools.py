# 目标：用 LangChain 重构 Agent，简化工具接入和记忆管理。

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from agent_dev.utils import MODEL,BASE_URL,API_KEY
from pydantic import SecretStr
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage,HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import wrap_tool_call
@tool
def get_weather(location:str)->str:
    """Get the weather for a location."""
    return f"{location} 晴，28℃"
@tool
def caculater(expression: str)->str:
    """Calculate a numeric expression."""
    result = eval(expression)
    return str(result)
    
model = ChatOpenAI(
    model=MODEL,
    base_url=BASE_URL,
    api_key=SecretStr(API_KEY) if API_KEY else None, 
    temperature=0)

class TodoStore:
    def __init__(self):
        self.todos = []

todos = TodoStore()

@wrap_tool_call
def get_todos(request, handle):
    """Get the current todo list."""
    name = request.tool_call["name"]
    args = request.tool_call["args"]
    result = handle(request)
    
    print(f"{name}({args})={result.content}")
    return result

@tool
def add_todo(todo: str) -> str:
    """Add a todo item to the current todo list."""
    todos.todos.append(todo)
    return f"Added {todo}"


@tool
def list_todos() -> str:
    """List all current todo items."""
    return "\n".join(todos.todos) or "No todos"


@tool
def remove_todo(todo: str) -> str:
    """Remove a todo item from the current todo list."""
    if todo in todos.todos:
        todos.todos.remove(todo)
        return f"Removed {todo}"
    return f"{todo} not found"

agent = create_agent(
     model = model,
     tools = [
         get_weather,
         caculater,
         add_todo,
         list_todos,
         remove_todo,
     ],
     middleware=[get_todos],#添加中间件
     system_prompt = SystemMessage(content="你是一个AI助手,回答简洁明了"),
     checkpointer=InMemorySaver() # 保存会话
    ) # type: ignore

config = {"configurable": {"thread_id": "agent-demo"}}# 配置会话ID

while True:
    text = input("输入你的问题:")
    if text == "bye":
        break
    response = agent.invoke(
        {
            "messages": [HumanMessage(content=text)]
        },
        config=config, # type: ignore
    )
    print(response["messages"][-1].content)