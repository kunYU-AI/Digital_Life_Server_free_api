from openai import OpenAI    # openai的库发生了更新，调回原本代码需要重安装按requirements.txt
import os
import tune

client = OpenAI(
    api_key="your api key",
    base_url="your url"    # 国内tech 国外org
)

def gpt_35_api_stream(messages: list):
    """
    为提供的对话消息创建新的回答 (流式传输)
    """
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

if __name__ == '__main__':
    messages = [{"role": "system", "content": tune.get_tune("paimon", "gpt-3.5-turbo")}]
    messages.append({'role': 'user','content': '派蒙，你好，你可以介绍一下你自己吗？'})
    print(messages)
    # 流式调用
    gpt_35_api_stream(messages)