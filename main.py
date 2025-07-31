import os
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, Runner
from dotenv import load_dotenv
from tools import plus,subtract,get_weather
from dynamic_instructions import dynamic_instruction
import asyncio

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(True)

client_provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

Model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client_provider
)


my_agent = Agent(
    name = "Assistant",
    instructions=dynamic_instruction,
    # tools=[plus],
    tools=[subtract],
    model=Model
)

weather_agent = Agent(
    name="weather agent",
    instructions="use the weather tool to find weather of the provided city",
    tools=[get_weather],
    model=Model
)


result = Runner.run_sync(
    starting_agent=my_agent,
    #input="Hello?"
    input="10-7=?",
    #context={"name":"User1","age":16,"role":"student"}, #Subtract tool will not run because age is less than 18
    context={"name":"User2","age":23,"role":"student"}  #Subtract tool will run because age is greater than 18
)

print(result.final_output)

async def main():
    #prompt=input("Enter your question:")
    #runner = await Runner.run(starting_agent=weather_agent, input=prompt)
    runner = await Runner.run(starting_agent=weather_agent, input="weather in karachi")
    print(runner.final_output)

if __name__ == "__main__":
    asyncio.run(main())
# This code initializes an agent and runs it with a specific input, demonstrating the use of tools and dynamic instructions.