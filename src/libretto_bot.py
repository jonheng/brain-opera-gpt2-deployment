class LibrettoBot:
    MAX_HISTORY = 10
    CHAT_SEP = '\n\n'

    def __init__(self, model):
        self.model = model
        self.actor_name = 'EVA'
        self.bot_name = 'BOT'
        self.chat_history = []

    def display_history(self):
        print('=========================')
        print(self.history_as_string())
        print('=========================')

    def history_as_string(self):
        return self.CHAT_SEP.join(self.chat_history)

    def actor_prompt(self, prompt):
        self.chat_history.append(self.actor_name + '\n' + prompt)
        self.chat_history.append(self.bot_name + '\n')

        while len(self.chat_history) > MAX_HISTORY:
            self.chat_history.pop(0)

        bot_reply = self.model.run(self.history_as_string())[0]
        bot_reply = self.postprocess_reply(bot_reply)

        self.chat_history[-1] = self.bot_name + '\n' + bot_reply

    def postprocess_reply(self, reply_str):
        eol_chars = '!.?'
        reply_str = reply_str.replace('\t', '')
        reply_str = reply_str.replace('\n', '')

        truncated_str = ''
        for char in reply_str:
            if char not in eol_chars:
                truncated_str += char
            else:
                truncated_str += char
                break

        return truncated_str

    def clear_history(self):
        self.chat_history = []

    def get_last_response(self):
        return self.chat_history[-1].lstrip(self.bot_name + '\n')