# 目标：让模型自主选择调用你写的 Python 函数，形成基础 Agent。

# 学习内容：
    # - OpenAI Function Calling 机制：定义 tools schema，解析 tool_calls 响应。
    # A- gent 基本循环：用户输入 → LLM 决策（回复 or 调用工具）→ 执行工具 → 将结果传回 LLM → 最终回复。
    
from openai import OpenAI
from agent_dev.utils import API_KEY,BASE_URL,MODEL
import json

class FunCall:
    def __init__(self,base_url,api_key) -> None:
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.funcs = {
            "get_weather":self.get_weather,
            "caculater":self.caculater
        }
        self.tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of a location, the user should supply a location first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
     {
        "type": "function",
        "function": {
            "name": "caculater",
            "description": "计算两个数的运算结果",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "description": "第一个运算数",
                    },
                    "b": {
                        "type": "string",
                        "description": "第二个运算数",
                    },
                    "operator": {
                        "type": "string",
                        "description": "运算符号",
                    }
                    
                },
                "required": ["a","b","operator"]
            },
        }
    },
    
]
    def get_weather(self,location):
        return f"{location} 晴，28℃"
    def caculater(self,a,b,operator):
        a,b = float(a),float(b)
        match operator:
            case "+":
                result = a+b
            case "-":
                result = a-b
            case "*":
                result = a * b
            case "/":
                result = a / b
            case _:
                raise ValueError(f"不支持的运算符: {operator}")
        return str(result)
    
   
    def funcall(self,round,messages):
        steps = 1
        while True:
            res = self.client.chat.completions.create(
                model = MODEL,
                messages = messages,
                tools = self.tools # type: ignore
            )
            messages.append(res.choices[0].message) 
            print(f"第{round}.{steps}轮的思考：{res.choices[0].message.reasoning_content}") # type: ignore
            tools = res.choices[0].message.tool_calls
            if tools is None:
                print(f"第{round}.{steps}轮的结果：{res.choices[0].message.content}")
                break
            for tool in tools:
                
                f = self.funcs[tool.function.name]# type: ignore
                r = f(**json.loads(tool.function.arguments))# type: ignore
                messages.append({
                    "role":"tool",
                    "tool_call_id":tool.id,
                    "content":r
                })
            steps+=1
            
        print()
        
        
        
if __name__ == "__main__":
    funcall = FunCall(BASE_URL,API_KEY)
    round = 1
    messages=[
        {"role":"system","content":"你是一个AI助手"}
    ]
   
    while True:
        text = input("输入你的问题:")
        if text == "bye":
            break
        prompt = f"""
            处理```分隔的内容
                    
            不要加额外的字符
                    
            ```{text}```
        """
        messages.append(
            {"role":"user","content":prompt}
        )
        funcall.funcall(round,messages)
        round +=1
        
        
        
   
    