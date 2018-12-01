from bot_database import DBOperator
from settings import NewsAggregatorClient
from settings import TelegramBotToken
from bot_core import BotCore
import socket

BotCore(job_interval=60, token=TelegramBotToken, db=DBOperator(NewsAggregatorClient))