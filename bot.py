# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount,Attachment
# from GetChat import chat
import os
import json
from LangGraph import getGraph
from langchain_core.messages import HumanMessage


class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    def create_adaptive_card_attachment(self):
        # read the .json file
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, "welcomecard.json")
        with open(path) as in_file:
            card_template = json.load(in_file)
        
       
        
        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card_template
        )


    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.value:
            action_data = turn_context.activity.value
            if action_data =="submitAction":
                await turn_context.send_activity(action_data.get("title"))
            else:
                await turn_context.send_activity(str(turn_context.activity))
        else:
            graph = await getGraph()
            prev = 0
            str = ""
            initial_message = MessageFactory.text("...")
            response = await turn_context.send_activity(initial_message)
            message_id = response.id
            for msg, metadata in graph.stream(input={"messages": [HumanMessage(content = turn_context.activity.text)]}, stream_mode="messages"):
                # print (msg.content)
                str = str+ msg.content
                if (len(str) - prev) > 100:
                    prev = len(str)
                    # print("sending update")
                    message = MessageFactory.text(str)
                    message.id = message_id
                    await turn_context.update_activity(message)
            message = MessageFactory.text(str)
            message.id = message_id
            await turn_context.update_activity(message)
                # print(message)
                
            
        # await turn_context.send_activity("hi")
      

    
    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        card = self.create_adaptive_card_attachment()
        response = MessageFactory.attachment(card)
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:

                await turn_context.send_activity(response)
