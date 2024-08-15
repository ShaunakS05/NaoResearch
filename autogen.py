import os

from autogen import ConversableAgent

robot1 = ConversableAgent(
    "NaoRobot",
    system_message="You are a Nao humanoid robot assisting humans with various tasks.",
    llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.9, "api_key": os.environ.get("OPENAI_API_KEY")}]},
    human_input_mode = "NEVER",
)

human_proxy =  ConversableAgent(
    "human_proxy",
    llm_config = False,
    human_input_mode="ALWAYS",
)

result = robot1.initiate_chat(
    human_proxy,
    message="10",
)
