import os
import asyncio
from agents import Agent, AsyncOpenAI, ModelSettings, OpenAIChatCompletionsModel, set_tracing_disabled, Runner, function_tool
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
set_tracing_disabled(True)

client_provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

Model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client_provider,
)

@function_tool
def plus(n1: int, n2: int) -> str:
    print("✅ Plus tool triggered")
    return f"Answer is: {n1 + n2}"

@function_tool
def subtract(n1: int, n2: int) -> str:
    print("✅ Subtract tool triggered")
    return f"Answer is: {n1 - n2}"

@function_tool
def multiply(n1: int, n2: int) -> str:
    print("✅ Multiply tool triggered")
    return f"Answer is: {n1 * n2}"

@function_tool
def divide(n1: int, n2: int) -> str:
    if n2 == 0:
        return "Error: Division by zero is not allowed."
    print("✅ Divide tool triggered")
    return f"Answer is: {n1 / n2}"


async def main():
    grammar_fixer_agent = Agent(
        name="Grammar Fixer",
        instructions="You correct grammar, punctuation, and spelling without changing the meaning.",
        model=Model,
        tools=[plus, subtract, multiply, divide],
        tool_use_behavior="run_llm_again",
        model_settings=ModelSettings(tool_choice="required")
        )

    math_agent = Agent(
    name="Math Agent",
    instructions="You solve math problems.",
    model=Model,
    tools=[plus, subtract, multiply, divide],
    tool_use_behavior="run_llm_again",
    model_settings=ModelSettings(tool_choice="required")
)

    summarizer_agent = Agent(
    name="Summarizer",
    instructions="You summarize the given text in 3–5 bullet points. Focus on clarity and key points.",
    model=Model,
    )

    idea_generator_agent = Agent(
    name="Idea Generator",
    instructions="You generate 3 unique and creative ideas based on the user's topic.",
    model=Model,
    )

    language_detector_agent = Agent(
    name="Language Detector",
    instructions="You detect and report the language of the given input.",
    model=Model,
    )

    politeness_converter_agent = Agent(
    name="Politeness Converter",
    instructions="You rewrite messages to sound polite and professional while keeping the meaning.",
    model=Model,
    )

    checklist_maker_agent = Agent(
    name="Checklist Maker",
    instructions="You turn the user's input into a detailed, step-by-step checklist.",
    model=Model,
    )

    comparison_agent = Agent(
    name="Comparison Agent",
    instructions="You compare the given items and list their pros and cons in a table format.",
    model=Model,
    )

    code_explainer_agent = Agent(
    name="Code Explainer",
    instructions="You explain what the given code does in simple, beginner-friendly terms.",
    model=Model,
    )

    tone_changer_agent = Agent(
    name="Tone Changer",
    instructions="You rewrite text in the tone requested by the user: casual, formal, fun, etc.",
    model=Model,
    )

    title_optimizer_agent = Agent(
    name="Title Optimizer",
    instructions="You generate 3 improved, more engaging, and SEO-friendly titles for the input.",
    model=Model,
    )

    orchestrator_agent = Agent(
        name="Orchestrator",
        instructions=(
        "You coordinate multiple agents to complete complex tasks efficiently.",
        "You decide which agents to use based on the user's input and the task requirements.",
        "You are responsible for determining which agent should handle the user's request. ",
        "Ask the user what they want, then hand off the request to the most relevant agent."),
        model=Model,
        handoffs=["grammar_fixer_agent", "summarizer_agent", "idea_generator_agent", "language_detector_agent", "politeness_converter_agent", "checklist_maker_agent", "comparison_agent", "code_explainer_agent", "tone_changer_agent", "title_optimizer_agent", "math_agent"],
    )

    result = Runner.run_streamed(
            starting_agent=orchestrator_agent,
            input="Can you sum this and deep answer : '1100+(100*23)-50/10'",
        )

    async for event in result.stream_events():
         if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
             print(event.data.delta, end="", flush=True)

asyncio.run(main())
