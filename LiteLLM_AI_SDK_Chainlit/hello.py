from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.extensions.models.litellm_model import LitellmModel
from agents.run import RunConfig
import chainlit as cl
import os
from dotenv import load_dotenv


load_dotenv()

model = os.getenv("MODEL")
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


@cl.on_chat_start
async def chat_start():
    cl.user_session.set("history", [])
    await cl.Message("I am an helpful Assistant. How can I assist you today ?").send()


@cl.on_message
async def main(message: cl.Message):
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=LitellmModel(api_key=GEMINI_API_KEY, model=model),
    )
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    response = await Runner.run(starting_agent=agent, input=history, run_config=RunConfig(tracing_disabled=True))
    history.append({"role": "assistant", "content": response.final_output})
    cl.user_session.set("history", history)
    await cl.Message(response.final_output).send()
    # print(response.final_output)

# asyncio.run(main())
