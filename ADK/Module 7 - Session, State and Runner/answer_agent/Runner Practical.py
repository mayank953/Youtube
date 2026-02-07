from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

import dotenv
dotenv.load_dotenv()

sessions_service_in_memory = InMemorySessionService()

initial_state = {
    "name": "Mayank",
    "data":'''
    I am mayank, a software developer with 5 years of experience in full-stack development.
    I love NBA, and my favourite player is Kobe Bryant
    '''
}

APP_NAME = "Answer Agent"
USER_ID = "mayank"
SESSION_ID = 'mayank_session'  # str(uuid.uuid4())  # Use a unique session ID in production


import asyncio

async def main():
    current_session = await sessions_service_in_memory.create_session(
        session_id=SESSION_ID,
        user_id=USER_ID,
        app_name=APP_NAME,
        state=initial_state
    )

    print(f"Session created with ID: {SESSION_ID}")

    created_sessions = await(sessions_service_in_memory.list_sessions(
        user_id=USER_ID,
        app_name=APP_NAME))
    print(f"Created sessions: {created_sessions}")

    runner = Runner(
        agent = root_agent,
        session_service = sessions_service_in_memory,
        app_name= APP_NAME
    )


    new_message = types.Content(
        role = 'user',
        parts = [types.Part(text='Which is the Favourite Player of User?')]
    )


    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print("Final response:", event.content.parts[0].text)



asyncio.run(main())

# print('Session state after interaction:')

# active_session= sessions_service_in_memory.get_session(
#     user_id=USER_ID,
#     session_id=SESSION_ID,
#     app_name=APP_NAME
# )
# print(active_session)

# for k,v in active_session.
#     print(f"{k}: {v}")
# # Note: The above code assumes that the agent.py file is in the same directory and contains the root_agent definition.