from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner
from agents.run import RunConfig
from dotenv import find_dotenv, load_dotenv
import os
import asyncio
import chainlit as cl

load_dotenv()

Base_Url = os.getenv("BASE_URL")
Open_Router_Key = os.getenv('OPENROUTER_API_KEY')
model = os.getenv("MODEL")

external_client = AsyncOpenAI(
    base_url=Base_Url,
    api_key=Open_Router_Key
)

model = OpenAIChatCompletionsModel(
    model=model,
    openai_client=external_client,
)


@cl.on_chat_start
async def chat_start():
    cl.user_session.set("history", [])
    await cl.Message("I am an helpful Assistant. How can I assist you today ?").send()


@cl.on_message
async def main(message: cl.Message):
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=model,
    )
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    response = await Runner.run(starting_agent=agent, input=history, run_config=RunConfig(tracing_disabled=True))
    history.append({"role": "assistant", "content": response.final_output})
    cl.user_session.set("history", history)
    await cl.Message(response.final_output).send()
    # print(response.final_output)

# asyncio.run(main())
