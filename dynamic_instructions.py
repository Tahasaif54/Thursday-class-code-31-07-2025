from agents import RunContextWrapper

def dynamic_instruction(ctx:RunContextWrapper, agent):
    # print(agent)
    return f"User Name: {ctx.context["name"]}, you are a helpful assistant"

async def en(ctx:RunContextWrapper,agent):
    if ctx.context["age"] >= 18:
         return True
    return False