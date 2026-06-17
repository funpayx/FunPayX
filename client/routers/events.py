from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from core.logic.events import EventLogic


router = Router()

class MsgAnsweringProcessing(StatesGroup):
    waiting_text = State()

@router.callback_query(F.data.startswith('message:answer:'))
async def answering_message_start(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.data.split(':')[-1]
    await callback.message.answer('Введите текст сообщения')
    await state.set_state(MsgAnsweringProcessing.waiting_text)
    await state.update_data(chat_id=chat_id)

@router.message(MsgAnsweringProcessing.waiting_text)
async def answering_message_end(message: types.Message, state: FSMContext):
    data = await state.get_data()
    chat_id = data.get('chat_id')
    event = EventLogic()
    await event.send_message(chat_id, message.text)
    return await message.answer('Успешно отправлено')