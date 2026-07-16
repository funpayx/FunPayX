import os
import sys
import logging

def restart_process(chat_id):
    logging.info('Перезапуск бота...')
    if chat_id:
        os.environ['FPX_RESTARTED_BY'] = str(chat_id)
    python = sys.executable
    os.execv(python, [python] + sys.argv)