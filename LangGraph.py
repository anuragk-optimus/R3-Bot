from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
import asyncio

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# Initialize the Azure OpenAI client
llm = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY_CHAT"),
    azure_endpoint= os.getenv("AZURE_OPENAI_ENDPOINT_CHAT"),
    model="gpt-4o",
    api_version='2025-02-01-preview'
)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Add the chatbot node to the graph
graph_builder.add_node("chatbot", chatbot)

# Define edges for the graph (flow between nodes)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile the graph
graph = graph_builder.compile()

# Function to stream updates based on user input
async def stream_graph_updates(user_input: str):
    # print('')
    for event in graph.astream_events({"messages": [HumanMessage(content = "tell a joke in 200 words")]}):
        # print(event.keys())
        if ('chunk' in event["data"].keys()):
         print(event['data']['chunk'].content)
        print(event['data'])
        

# Main loop for interacting with the chatbot
async def getGraph():
    return graph
    while True:
        try:
           
            user_input = input("give prompt")
            for msg, metadata in graph.stream(input={"messages": [HumanMessage(content = user_input)]}, stream_mode="messages"):
                print (msg.content)

        except Exception as e:
            print(f"An error occurred: {e}")
            break
# asyncio.run(main())