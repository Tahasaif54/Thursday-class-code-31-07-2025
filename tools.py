from agents import function_tool, RunContextWrapper, FunctionTool
from subtract_schema import SubtractSchema
from dynamic_instructions import en
from pydantic import BaseModel


@function_tool(description_override="This is a plus function This add two numbers", name_override="plus_function", is_enabled=True)
def plus(ctx:RunContextWrapper,n1,n2):
    """Plus Function"""
    print("<--- Plus Tool Fired ---->")
    print(f"ctx ---> {ctx.context["name"]} ")
    return f'Your result is {n1+n2}'

async def subtract_func(ctx:RunContextWrapper,arg):
    print("<--- Subtract Tool Fired --->")
    obj = SubtractSchema.model_validate_json(arg)
    return f"your answer is {obj.n1 - obj.n2}"

subtract = FunctionTool(
    name="subtract",
    description="Substract Function",
    params_json_schema=SubtractSchema.model_json_schema(),
    on_invoke_tool=subtract_func,
    is_enabled=en
)


class WeatherSchema(BaseModel):
    city:str

def get_weather(data: WeatherSchema):
    "Get the weather of the provided city."
    return f"City: {data.city}, Temperature: 35°C"


