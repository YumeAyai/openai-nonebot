import asyncio
import nonebot
from .config import *


from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (Message, MessageSegment)

# 读取配置
try:
    model_id = nonebot.get_driver().config.openai_api_modelid
    api_key = nonebot.get_driver().config.openai_api_key
    max_tokens = nonebot.get_driver().config.openai_max_tokens
    chatbot_on_command = nonebot.get_driver().config.openai_chatbot_on_command
    proxies = nonebot.get_driver().config.openai_proxies
    timeout = nonebot.get_driver().config.openai_timeout
except:
    model_id = "text-davinci-002"
    api_key = "############################"
    max_tokens = 2000
    chatbot_on_command = "gpt"
    proxies = ""
    timeout = ""
    


__plugin_meta__ = PluginMetadata(
    name="OpenAI chatbot",
    description="没有上下文关联的OpenAI对话机器人",
    usage=(
        f"OpenAI chatbot： \n"
        f"    没有上下文关联的OpenAI对话机器人 \n \n"
        f" 1. /oachat <对话内容>\n"
        f" 2. {chatbot_on_command} <对话内容> \n"
        f"        \n"
        f"model_id： {model_id}  \n"
    ),
)



chatbot = OpenApiChatbot(api_key, model_id)

# 定义命令
chat = on_command(rf"{chatbot_on_command}", aliases={
                    "/chat"}, block=True, priority=5)


chat_help = on_command(
    "/help", aliases={"/对话帮助"}, block=True, priority=5)


@chat_help.handle()
async def _(msg: Message = CommandArg()):
    await chat_help.finish(__plugin_meta__.usage)


@chat.handle()
async def _(msg: Message = CommandArg()):
    if api_key == "没有api":
        await chat.finish("请配置OPENAI_API_KEY")
    user_input = msg.extract_plain_text()
    if user_input == "" or user_input == None or user_input.isspace():
        await chat.finish("输入东西啊喂！")
    await chat.send(MessageSegment.text(user_input))
    await chat.send(MessageSegment.text("Loading..."))
    loop = asyncio.get_event_loop()
    # 不同转递方法
    # try:
    #     res = await loop.run_in_executor(None, chatbot.analyze_chat_responses, chatbot.generate_response(user_input))
    # except Exception as e:
    #     await chat.finish(str(e))
    # await chat.finish(MessageSegment.text(res))
    try:
        res = await loop.run_in_executor(None, chatbot.generate_response, user_input)
    except Exception as e:
        await chat.finish(str(e))
    await chat.finish(MessageSegment.text(chatbot.analyze_chat_responses(res)))