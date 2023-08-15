import connection as conn
from datetime import datetime
import time

# some functions to parse json date
class DateTimeEncoder(conn.json.JSONEncoder):
    def default(self, o):
        if isinstance(o, conn.datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return conn.json.JSONEncoder.default(self, o)



async def main(phone):
    await conn.client.start()
    print("Client Created")
    # Ensure you're authorized
    if await conn.client.is_user_authorized() == False:
        await conn.client.send_code_request(phone)
        try:
            await conn.client.sign_in(phone, input('Enter the code: '))
        except conn.SessionPasswordNeededError:
            await conn.client.sign_in(password=input('Password: '))

    me = await conn.client.get_me()

    # channel_messages = []
    all_messages = []
    channel = await conn.client.get_entity(conn.entity)
    limit = 100
    offset_id = 0   # ID of message to start retrieving messages
    start_date = datetime(2023, 8, 1)
    start_date = datetime.now()
    # start_date = int(time.mktime(start_date.timetuple()))
    total_messages = 0

    while True:
        print(f"Total messages: {total_messages}\noffset_id: {offset_id}")
        history = await conn.client(conn.GetHistoryRequest(
            peer = channel,
            offset_date = start_date,   # date to start retrieving messages from
            add_offset = 0,
            offset_id = offset_id,
            limit = limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages

        for message in messages:
            all_messages.append(message.to_dict())
        #     if message.reply_to_msg_id and message.text != "Typing...":
        #         prompt = await message.get_reply_message()
        #         print(f"prompt: {prompt.text}\n")
        #         print(f"reply: {message.text}")
        total_messages = len(all_messages)
        offset_id = messages[len(messages) - 1].id
        

    with open("channel_messages.json", "w") as channel_messages_file:
        conn.json.dump(all_messages, channel_messages_file, cls=DateTimeEncoder)


with conn.client:
    conn.client.loop.run_until_complete(main(conn.phone))


# # messages from chat history - channel_messages.json
# with open('./channel_messages.json') as file:
#     all_messages = conn.json.load(file)1001932824854


# unanswered_messages = []
# prompt_ids_before = []

# for message in all_messages:
#     try:
#         paal_reply = message.get('message')
#         if paal_reply.startswith("I'm sorry") or paal_reply.startswith("I apologize") or \
#             paal_reply.startswith("Timeout error!") or paal_reply.startswith("Error:") or \
#             paal_reply.startswith("Sorry, we encountered an error") or paal_reply.startswith("Unfortunately"):
#             reply_id = message.get('id')
#             reply_to_msgprmpt_id = message.get('reply_to', {}).get('reply_to_msg_id')
#             prompt_ids_before.append({
#                 'paal_reply_id': reply_id,
#                 'id_of_msg_being_replied': reply_to_msgprmpt_id,
#             })
#     except AttributeError:
#         pass

# # json file of paal_reply_ids and ids of message being replied to
# with open('prompt_ids_before.json', 'w') as promptIds:
#     conn.json.dump(prompt_ids_before, promptIds)

# size = 20
# serial_no = 1
# while size >= 1:
#     for ids in prompt_ids_before:
#         prompt_id = ids['id_of_msg_being_replied']
#         reply_id = ids['paal_reply_id']
#         for message_prompt in all_messages:
#             try:
#                 message_prompt_id = message_prompt.get('id')
#                 if message_prompt_id == prompt_id:
#                     for message_reply in all_messages:
#                         try:
#                             message_reply_id = message_reply.get('id')
#                             if message_reply_id == reply_id:
#                                 unanswered_messages.append({
#                                     's/n': serial_no,
#                                     'prompt_date': message_prompt.get('date'),
#                                     'prompt_id': prompt_id,
#                                     'user_prompt': message_prompt.get('message'),
#                                     'paal_reply': message_reply.get('message'),
#                                     'reply_date': message_reply.get('date'),
#                                     'reply_id': reply_id
#                                 })
#                         except AttributeError:
#                             pass
#             except AttributeError:
#                 pass
#         prompt_ids_before.remove(ids)
#         size = len(prompt_ids_before)
#         serial_no += 1
#         print(f"size: {size}")
#         print(f"length_of_prompt_ids: {len(prompt_ids_before)}")
#         print(f"length_of_unanswered_messages: {len(unanswered_messages)}")
#         print(f"Total: {len(prompt_ids_before)} + {len(unanswered_messages)} = {len(prompt_ids_before) + len(unanswered_messages)}") # 4706


#     # json file of paal_reply_ids and ids of message being replied to
#     with open('prompt_ids_after.json', 'w') as promptIds:
#         conn.json.dump(prompt_ids_before, promptIds)

# with open('unanswered_messages.json', 'w') as unanswered:
#     conn.json.dump(unanswered_messages, unanswered)