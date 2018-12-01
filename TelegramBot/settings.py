import logging
import motor.motor_asyncio

TelegramBotToken = '690368266:AAHi0TvxKCbXbpSZp_6ine8UGoL6X0BPPrs'
LoggingKeeper = logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
MONGO_CLIENT = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb://Admin1:Admin1@ds129926.mlab.com:29926/news_aggregator'
)
NewsAggregatorClient = MONGO_CLIENT.news_aggregator