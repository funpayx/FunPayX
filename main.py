import logging
import asyncio

from bot import botmain
from funpay_listener import funpaymain


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)

async def main():
    logging.info('Запускаем все компоненты...')
    task1 = asyncio.create_task(botmain())
    task2 = asyncio.create_task(funpaymain())
    done, pending = await asyncio.wait(
        [task1, task2],
        return_when=asyncio.FIRST_COMPLETED
    )
    logging.info("Один из компонентов завершился, закрываем остальное...")
    for task in pending:
        task.cancel()
    await asyncio.gather(*pending, return_exceptions=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Бот выключен')