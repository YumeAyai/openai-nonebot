import openai


class OpenApiChatbot:
    def __init__(self, api_key, model_id):
        # 初始化 OpenApiChatbot 类的实例
        # 参数 api_key 表示 OpenAI API 的凭据
        # 参数 model_id 表示要使用的模型 ID
        openai.api_key = api_key  # 设置 API 凭据
        self.model_id = model_id  # 设置模型 ID
        self.headers = {  # 构造请求头
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai.api_key}"
        }

    def generate_response(self, user_input):
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"}
            ]
        )

        # 返回消息体
        # {
        # 'id': 'chatcmpl-6p9XYPYSTTRi0xEviKjjilqrWU2Ve',
        # 'object': 'chat.completion',
        # 'created': 1677649420,
        # 'model': 'gpt-3.5-turbo',
        # 'usage': {'prompt_tokens': 56, 'completion_tokens': 31, 'total_tokens': 87},
        # 'choices': [
        # {
        #     'message': {
        #     'role': 'assistant',
        #     'content': 'The 2020 World Series was played in Arlington, Texas at the Globe Life Field, which was the new home stadium for the Texas Rangers.'},
        #     'finish_reason': 'stop',
        #     'index': 0
        # }
        # ]
        # }

        # 
        #    response[‘choices’][0][‘message’][‘content’]

        
        # 根据输入的提示 prompt 生成 OpenApiChatbot 的回复文本
        
        response_text = response.choices[0].text.strip()
        self.history.append(response_text)
        print (response)
        return response_text  # 返回响应中的完整文本

    # 定义一个函数，用于解析 ChatGPT API 的响应

    def analyze_chat_responses(self, resp):

        chatResp = resp.choices[0].text
        # 移除所有开头的\n
        while (chatResp.startswith("\n") != chatResp.startswith("？")):
            chatResp = chatResp[1:]
        print(str(chatResp))

        return chatResp

    # 定义一个函数，用于解析 ChatGPT API 的响应并获取所有输出结果

    def analyze_all_responses(self, resp):
        # 获取 def generate_response 响应的数据，并解析
        choices = resp['choices']
        # 创建一个列表，存储所有 ChatGPT 的输出结果
        allResp = []
        # 对响应中的 choices 列表进行迭代，获取所有结果的文本
        for choice in choices:
            allResp.append(choice['text'].strip())
        print(str(allResp))

        return allResp