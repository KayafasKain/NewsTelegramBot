import asyncio
import logging
import motor.motor_asyncio


class DBOperator(object):

    loop = asyncio.get_event_loop()

    def __init__(self, db, limit=10):
        self.db = db
        self.limit = limit

    def execute_task(self, method):
        result = self.loop.run_until_complete(method)
        if result:
            return result

    async def create_subscriber(self, subscriber, collection='subscribers'):
        await self.db[collection].update_one(subscriber, { '$set': subscriber }, upsert=True)

    async def update_subscriber(self, subscriber, collection='subscribers'):
        await self.db[collection].update_one({'chat_id': subscriber['chat_id'] }, { '$set': subscriber }, upsert=True)

    async def update_item(self, item, collection='everypony'):
        await self.db[collection].update_one(item, {'$set': {'brodcasted': True}}, upsert=True)

    async def find_subscriber(self, chat_id, collection='subscribers'):
        return await self.db[collection].find_one({'chat_id': chat_id})

    async def get_interested_subscribers(self, limit=10, last_id=None, collection='subscribers'):
        if not last_id:
            subscribers = self.db[collection].find({'preferences': { '$exists': True, '$not': {'$size': 0}}}).limit(self.limit)
        else:
            subscribers = self.db[collection].find({'_id' > last_id},{ 'preferences': {'$exists': True, '$not': {'$size': 0}}}).limit(self.limit)

        result = []
        for subscriber in await subscribers.to_list(length=limit):
            result.append(subscriber)

        return result

    async def get_fresh_items(self, collection='everypony'):
        fresh_items = self.db[collection].find({'brodcasted': {'$ne': True} })
        result_list =[]
        for item in await fresh_items.to_list(length=10):
            await self.update_item(item, collection=collection)
            result_list.append(item)
        return result_list

    async def get_last_items(self, limit=10, collection='everypony'):
        return await self.db[collection].find().limit(limit)

    async def get_collection_size(self, collection='everypony'):
        return await self.db[collection].count_documents({})