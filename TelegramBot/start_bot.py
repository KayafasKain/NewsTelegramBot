from bot_database import DBOperator
from settings import NewsAggregatorClient
from settings import TelegramBotToken
from bot_core import BotCore
BotCore(job_interval=600, token=TelegramBotToken, db=DBOperator(NewsAggregatorClient))