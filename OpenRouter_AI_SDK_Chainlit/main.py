from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from dotenv import find_dotenv, load_dotenv
import os
import asyncio

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


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant",
        model=model,
    )
    response = await Runner.run(starting_agent=agent, input="Who is the founder of Pakistan")
    print(response.final_output)

asyncio.run(main())
