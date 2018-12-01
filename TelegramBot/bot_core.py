from telegram.ext import Updater, CommandHandler, Dispatcher
import re
import math

class BotCore():

    bot_dict = {
        'start': 'Wellcome! Here you can get some news. You can learn about commands when type: "/commands"',
        'commands': '''
            1) everypony.ru - "/watch everypony" to start recieving news from everypony or "/unwatch_everypony" to stop watching pony news 
        '''
    }

    watch_dict = {
        'everypony': r'ever[i|y]pon[i|y]'
    }

    preferences = [
        'everypony'
    ]

    def __init__(self, token, bot_dict=None, db=None, job_interval=600):
        self.token = token
        self.updater = Updater(token=token)
        self.jobs = self.updater.job_queue
        self.dispatcher = self.updater.dispatcher
        self.job_interval = job_interval

        if bot_dict:
            self.bot_dict = bot_dict
        if db:
            self.db = db
        else:
            raise ValueError('Please, provide db-collection instance')
        self.set_up_updaters()

        self.jobs.run_repeating(self.aggregate_news, interval=job_interval, first=0)

    def set_up_updaters(self):
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('commands', self.commands))
        self.dispatcher.add_handler(CommandHandler('watch', self.watch, pass_args=True))
        self.updater.start_polling()

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=self.bot_dict['start'])
        self.db.execute_task(self.db.create_subscriber({
            'chat_id': update.message.chat_id,
            'preferences': []
        }))

    def commands(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=self.bot_dict['commands'])

    def watch(self, bot, update, args):
        command = " ".join(args)
        if re.match(self.watch_dict['everypony'], command):
            subscriber = self.db.execute_task(self.db.find_subscriber(update.message.chat_id))
            if 'everypony' not in subscriber['preferences']:
                subscriber['preferences'].append('everypony')
                self.db.execute_task(self.db.update_subscriber(subscriber))

    def aggregate_news(self, bot, size, subscriber_size=10):
        news = {}
        for pref in self.preferences:
            news[pref] = self.db.execute_task(self.db.get_fresh_items(collection=pref))
        iterations = int(math.ceil(self.db.execute_task(self.db.get_collection_size(collection='subscribers'))/subscriber_size))
        last_id = None
        for i in range(iterations):
            subs = self.db.execute_task(self.db.get_interested_subscribers(limit=subscriber_size, last_id=last_id))
            last_id = subs[len(subs)-1]['_id']
            for sub in subs:
                for preference in sub['preferences']:
                    if news[preference]:
                        for post in news[preference]:
                            self.send_news(post, sub['chat_id'])

    def send_news(self, post, chat_id):
        self.updater.bot.send_message(chat_id=chat_id, text='''
            {title}
            {link}            
        '''.format(title=post['title'], link=post['link']))


