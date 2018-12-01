from bot_database import DBOperator
from settings import NewsAggregatorClient
from settings import TelegramBotToken
from bot_core import BotCore
import os


port = int(os.environ.get("PORT", 5000))


from flask import Flask

app = Flask(__name__)
BotCore(job_interval=60, token=TelegramBotToken, db=DBOperator(NewsAggregatorClient))
app.run(debug=False, host='0.0.0.0', port=port)