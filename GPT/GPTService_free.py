import argparse
import logging
import os
import time
from openai import OpenAI

import GPT.tune as tune

class GPTService():
    def __init__(self, args):
        logging.info('Initializing ChatGPT Service...')
        self.tune = tune.get_tune(args.character, args.model)
        # self.tune = "You are a helpful assistant."    # test case
        self.counter = 0

        self.brainwash = args.brainwash
        self.api_key = args.APIKey
        self.url = args.url
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.url
        )
        
        # Store system message
        self.messages = [{"role": "system", "content": self.tune}]
        logging.info('OpenAI API Chatbot initialized.')

    def ask(self, text):
        stime = time.time()
        
        # Add user message
        self.messages.append({"role": "user", "content": text})
        
        # Get completion
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        
        # Get response
        response = completion.choices[0].message.content
        
        # Add assistant response to message history
        self.messages.append({"role": "assistant", "content": response})
        
        logging.info('ChatGPT Response: %s, time used %.2f' % (response, time.time() - stime))
        return response

    def ask_stream(self, text):
        prev_text = ""
        complete_text = ""
        stime = time.time()
        
        # Handle tune injection
        if self.counter % 5 == 0:
            if self.brainwash:
                logging.info('Brainwash mode activated, reinforce the tune.')
            else:
                logging.info('Injecting tunes')
            # Reset messages with system prompt
            self.messages = [{"role": "system", "content": self.tune}]
            
        self.counter += 1
        
        # Add user message
        self.messages.append({"role": "user", "content": text})
        
        # Create streaming completion
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                message = chunk.choices[0].delta.content
                
                if ("。" in message or "！" in message or "？" in message or "\n" in message) and len(complete_text) > 3:
                    complete_text += message
                    logging.info('ChatGPT Stream Response: %s, @Time %.2f' % (complete_text, time.time() - stime))
                    yield complete_text.strip()
                    complete_text = ""
                else:
                    complete_text += message
                
                prev_text += message

        if complete_text.strip():
            logging.info('ChatGPT Stream Response: %s, @Time %.2f' % (complete_text, time.time() - stime))
            yield complete_text.strip()
            
        # Add complete response to message history
        self.messages.append({"role": "assistant", "content": prev_text})


if __name__ == '__main__':
    # 设置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # 创建参数解析器
    parser = argparse.ArgumentParser(description='GPT Service Demo')
    parser.add_argument('--brainwash', action='store_true', help='Enable brainwash mode')
    parser.add_argument('--APIKey', type=str, nargs='?', required=True,
                        help='free api key')
    parser.add_argument('--url', type=str, nargs='?', required=True,
                        help='host name: 海外org 国内tech')
    args = parser.parse_args()

    service = GPTService(args)
    # 测试普通对话
    print("\n=== Testing normal chat ===")
    response = service.ask("介绍一下你自己")
    print("Response:", response)

    # 测试流式对话
    print("\n=== Testing streaming chat ===")
    prompt = "讲一个简短的故事"
    print(f"Prompt: {prompt}")
    print("Streaming response:")
    for response_chunk in service.ask_stream(prompt):
        print(response_chunk, end='\n')
