import os 
import json
API_KEY  = os.getenv('GLM_API_KEY')
BASE_URL="https://open.bigmodel.cn/api/paas/v4"
# MODEL="GLM-4.7-Flash"
# MODEL='GLM-4.6V'
MODEL='GLM-4.5-Air'


def format_messages(messages):
    # 将langchain消息列表转化为json 字符串，
    data = {
        "messages": [msg.model_dump() for msg in messages]
    }#转为dict再dump
    return json.dumps(data, ensure_ascii=False, indent=4)

def format_response(response):
    res_json = json.dumps(
        {
            **response,
            "messages": [message.model_dump(mode="json") for message in response["messages"]],
        },
        ensure_ascii=False,
        indent=4,
    )
    return res_json # 输出 JSON 格式的结果