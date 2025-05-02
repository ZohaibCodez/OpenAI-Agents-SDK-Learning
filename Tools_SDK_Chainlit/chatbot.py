from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    FunctionTool,
    function_tool,
    set_tracing_disabled,
)
import os
from dotenv import find_dotenv, load_dotenv
import requests
import chainlit as cl
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(find_dotenv())

set_tracing_disabled(True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
Base_URL = "https://openrouter.ai/api/v1"
MODEL: str = "google/gemini-2.0-flash-001"

external_client = AsyncOpenAI(
    base_url=Base_URL,
    api_key=OPENROUTER_API_KEY,
)

model = OpenAIChatCompletionsModel(openai_client=external_client, model=MODEL)


@function_tool
async def fetch_weather(location: str) -> str:
    """
    Fetch the weather for a given location.

    Args:
        location:The location to fetch weather for.
    """

    response = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={OPENWEATHER_API_KEY}&q={location}"
    )
    if response.status_code == 200:
        data = response.json()
        location_name = data["location"]["name"]
        region = data["location"]["region"]
        country = data["location"]["country"]
        current = data["current"]
        description = (
            f"Weather report for {location_name}, {region}, {country}:\n"
            f"- Temperature: {current['temp_c']}°C\n"
            f"- Condition: {current['condition']['text']}\n"
            f"- Wind Speed: {current['wind_kph']} kph\n"
            f"- Humidity: {current['humidity']}%\n"
            f"- Feels Like: {current['feelslike_c']}°C\n"
            f"- Last Updated: {current['last_updated']}\n"
        )
        return description
    else:
        return f"Failed to fetch weather data for '{location}': {response.status_code} {response.text}"


@cl.on_chat_start
async def chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="I am a weather assistant. How can i assist you today."
    ).send()


@cl.on_message
async def message_handle(message: cl.Message):
    weather_agent = Agent(
        name="Weather Assistant",
        instructions="You are a helpful assistant for a user and you also fetch the current weather updates by using the tools provided to user . Location or city name anything about weather ask from user You have to ans in a very well-behaved manner .",
        model=model,
        tools=[fetch_weather],
    )

    msg = cl.Message(content="")
    await msg.send()

    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    response = Runner.run_streamed(starting_agent=weather_agent, input=history)

    async for event in response.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            await msg.stream_token(event.data.delta)

    await msg.update()
    history.append({"role": "assistant", "content": response.final_output})
    # await cl.Message(content=response.final_output).send()
