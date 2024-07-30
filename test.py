def main():
    import anthropic
    from dotenv import load_dotenv
    import os

    load_dotenv()
    api_key = os.getenv("ANTHROPIC_TOKEN")

    client = anthropic.Anthropic(
        api_key=api_key,
    )

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        # messages=[
        #     {"role": "user", "content": "hi how are you"},
        #     {"role": "assistant", "content": "good how are you?"},
        #     {"role": "user", "content": "my name is mike"},
        #     {"role": "assistant", "content": "nice to meet you!"},
        #     {"role": "user", "content": "what's my name?"}
        # ]
        messages=[{'role': 'user', 'content': "!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\nfailed with error: sequence item 0: expected str instance, Message found\n!summarize\nfailed with error: cannot access local variable 'message' where it is not associated with a value\n!summarize\n!summarize\n!summarize\n!summarize\nI can only summarize thread contents!\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize\n!summarize penis\n!summarize penis\n!summarize\n!summarize\n3\n!add 1 2\n!summarize this message\n!summarize\n!summarize this message\n!summarize\nPong! 65ms\n!ping\n<@1249843054785990767> summarize\n<@1249843054785990767>\n!summarize\n<@1249843054785990767> sup\npenis in the air\n<@1249843054785990767> print penis in the air\n<@1249843054785990767> sup\nyep, we in a thread: test thread\n<@1249843054785990767> is_thread\n<@1249843054785990767>\n/is_thread\n<@1249843054785990767> is_thread\nyep, we in a thread: test thread\n!is_thread\nno we are not in a thread\nyou just said: !is_thread\n!is_thread\n!is_thraed\nno we are not in a thread\nyou just said: !is_thread\n!is_thread\nthis is a test thread\n"}]
    )
    print(message.content)


if __name__ == "__main__":
    main()
