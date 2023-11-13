from dotenv import load_dotenv

load_dotenv()
import utils
# from functions import FUNCTIONS
from functions_zh import FUNCTIONS
from agent import Agent


import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_agent_loop(agent):
    while True:
        user_input = input("You: ")
        if user_input == "/exit":
            break
        user_input = user_input.rstrip()
        user_message = utils.package_user_message(user_input)
        agent.step(user_message)


if __name__ == "__main__":
    persona = utils.get_persona_text()
    human = utils.get_human_text()
    system = utils.get_system_text()

    print("system:",system)
    print("persona:", persona)
    print("human:", human)

    agent = Agent(model="gpt-3.5-turbo-16k-0613", system=system, functions_description=FUNCTIONS, persona_notes=persona,
                  human_notes=human)
    run_agent_loop(agent)
