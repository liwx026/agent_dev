# 目标：能用 Python 调用大模型 API，掌握结构化输出控制。
# 学习内容：
    # - OpenAI API（Chat Completion）参数：temperature、top_p、role、function_call。
    # - 智谱 GLM / 通义千问 API 调用（任选其一，国内免费额度）。
    # - Prompt 工程：角色设定、分隔符、输出格式化（JSON、Markdown）。
#练习

from openai import OpenAI
from agent_dev.utils import API_KEY,BASE_URL,MODEL

class LLMApiCall:
    def __init__(self,base_url,api_key) -> None:
        self.client = OpenAI(api_key=api_key, base_url=base_url)
     
    def ask_llm(self,messages,model, tools=None):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

    def interpreter(self,model,text):
        prompt = f"""
        翻译```分割的文本，将其中的英文部分翻译为中文
        
        不添加任何额外字符
        
        ```{text}```
        """
        messages=[
            {"role":"system","content":"你是一位翻译官"},
            {"role":"user","content":prompt}
        ]
        response = self.ask_llm(messages,model)
        print(response)

    def email_generator(self,model,text):
        prompt = f"""
        根据```分割的文本，生成正式邮件
        输出JSON格式，包含字段：
        - 收件人
        - 主题
        - 内容
        字段可为空
        
        不添加任何额外字符
        
        
        ```{text}```
        """
        messages=[
            {"role":"system","content":"你是一个邮件生成器"},
            {"role":"user","content":prompt}
        ]
        response = self.ask_llm(messages,model)
        print(response)
        
if __name__ == "__main__":
    llm_api_call = LLMApiCall(BASE_URL,API_KEY)
    text = """
    ellen：where are you from? how old are you?
    
    小明: 我来自中国，我今年18岁了。
    """
    
    llm_api_call.interpreter(MODEL,text)
   