import os
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, Runner, SQLiteSession
from dotenv import load_dotenv
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

agent = Agent(
    name="General Purpose Agent",
    instructions="you are a helpful agent",
    model=Model
)

# result = Runner.run(starting_agent=agent, input="Hello?") # Error 
async def main():
    #result = await Runner.run(starting_agent=agent, input="what is capital of pakistan?")
    my_session = SQLiteSession("mysession_123","my_conversation.db") # "my_conversation.db" is  memory path the chat history will be stored in this manually  
    prompt = input("Enter your Question:")
    result = await Runner.run(starting_agent=agent, input=prompt, session=my_session)
    print(result.final_output)

    prompt = input("Enter your Question:")
    result = await Runner.run(starting_agent=agent, input=prompt, session=my_session)
    print(result.final_output)

    #print(result.final_output) # prints final output
    #print(result.last_agent) # print last agents
    #print(result.to_input_list()) #pit imprves session history context mantained


asyncio.run(main())
