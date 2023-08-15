import connection as conn

# messages from chat history - channel_messages.json
with open('./telegram-analysis/channel_messages.json') as file:
    all_messages = conn.json.load(file)


unanswered_messages = []
prompt_ids_before = []

for message in all_messages:
    try:
        paal_reply = message.get('message')
        if paal_reply.startswith("I'm sorry") or paal_reply.startswith("I apologize") or \
            paal_reply.startswith("Timeout error!") or paal_reply.startswith("Error:") or \
            paal_reply.startswith("Sorry, we encountered an error") or paal_reply.startswith("Unfortunately"):
            reply_id = message.get('id')
            reply_to_msgprmpt_id = message.get('reply_to', {}).get('reply_to_msg_id')
            prompt_ids_before.append({
                'paal_reply_id': reply_id,
                'id_of_msg_being_replied': reply_to_msgprmpt_id,
            })
    except AttributeError:
        pass

# json file of paal_reply_ids and ids of message being replied to
with open('prompt_ids_before.json', 'w') as promptIds:
    conn.json.dump(prompt_ids_before, promptIds)

size = 20
serial_no = 1
while size >= 1:
    for ids in prompt_ids_before:
        prompt_id = ids['id_of_msg_being_replied']
        reply_id = ids['paal_reply_id']
        for message_prompt in all_messages:
            try:
                message_prompt_id = message_prompt.get('id')
                if message_prompt_id == prompt_id:
                    for message_reply in all_messages:
                        try:
                            message_reply_id = message_reply.get('id')
                            if message_reply_id == reply_id:
                                unanswered_messages.append({
                                    's/n': serial_no,
                                    'prompt_date': message_prompt.get('date'),
                                    'prompt_id': prompt_id,
                                    'user_prompt': message_prompt.get('message'),
                                    'paal_reply': message_reply.get('message'),
                                    'reply_date': message_reply.get('date'),
                                    'reply_id': reply_id
                                })
                        except AttributeError:
                            pass
            except AttributeError:
                pass
        prompt_ids_before.remove(ids)
        size = len(prompt_ids_before)
        serial_no += 1
        print(f"size: {size}")
        print(f"length_of_prompt_ids: {len(prompt_ids_before)}")
        print(f"length_of_unanswered_messages: {len(unanswered_messages)}")
        print(f"Total: {len(prompt_ids_before)} + {len(unanswered_messages)} = {len(prompt_ids_before) + len(unanswered_messages)}") # 4706


    # json file of paal_reply_ids and ids of message being replied to
    with open('prompt_ids_after.json', 'w') as promptIds:
        conn.json.dump(prompt_ids_before, promptIds)

with open('unanswered_messages.json', 'w') as unanswered:
    conn.json.dump(unanswered_messages, unanswered)