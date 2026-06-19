from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from client.keyboards.settings_menu import settings_menu, _paginate_blacklist, set_meeting
from core.logic.settings import Settings
from utils.config_manager import config_manager
from client.keyboards.main_menu import back_to_main_menu


router = Router()

class BlacklistAdding(StatesGroup):
    user_name = State()

class ChangeWelcomeCooldownProcessing(StatesGroup):
    waiting_hours = State()

class ChangeWelcomeMessageProcessing(StatesGroup):
    waiting_text = State()

@router.callback_query(F.data == 'settings_menu')
async def open_settings(callback: types.CallbackQuery):
    return await callback.message.edit_text('Выбери опцию:', reply_markup=settings_menu())

@router.callback_query(F.data.startswith('notify:'))
async def toggle_notify(callback: types.CallbackQuery):
    option = callback.data.split(':')[-1]
    settings = Settings()
    await settings.toggle_notifications(option)
    return await callback.message.edit_text('Выбери опцию', reply_markup=settings_menu())

@router.callback_query(F.data.startswith('blacklist:page:'))
async def blacklist_open(callback: types.CallbackQuery):
    page = callback.data.split(':')[-1]
    return await callback.message.edit_text('Выбери опцию', reply_markup=_paginate_blacklist(config_manager.blacklist_buyers, page))

@router.callback_query(F.data.startswith('blacklist:rm:'))
async def blacklist_remove(callback: types.CallbackQuery):
    user_name = callback.data.split(':')[-2]
    page = callback.data.split(':')[-1]
    settings = Settings()
    await settings.toggle_user_msg_filter(user_name)
    return await callback.message.edit_text('Выбери опцию', reply_markup=_paginate_blacklist(config_manager.blacklist_buyers, page))

@router.callback_query(F.data.startswith('blacklist:add_prompt:'))
async def blacklist_adding_first(callback: types.CallbackGame, state: FSMContext):
    page = callback.data.split(':')[-1]
    await callback.message.edit_text('Введите имя пользователя, сообщения которого хотите игноировать.', reply_markup=back_to_main_menu())
    await state.set_state(BlacklistAdding.user_name)
    await state.update_data(page=page)

@router.message(BlacklistAdding.user_name)
async def blacklist_adding_second(message: types.Message, state: FSMContext):
    data = await state.get_data()
    page = data.get('page')
    settings = Settings()
    await settings.toggle_user_msg_filter(message.text)
    await message.answer('Успешно установлено!', reply_markup=_paginate_blacklist(config_manager.blacklist_buyers, page))

@router.callback_query(F.data == 'meeting:set')
async def meeting_settings(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f'Выберите опцию\nТекущее сообщение: `{config_manager.welcome_msg['message']}`', 
        parse_mode='markdown',
        reply_markup=set_meeting()
    )

@router.callback_query(F.data.startswith('meeting:toggle:'))
async def meeting_toggle(callback: types.CallbackQuery):
    action = callback.data.split(':')[-1]
    await callback.answer('Загрузка...')
    settings = Settings()
    await settings.toggle_meeting(action)
    await callback.message.edit_text(
        f'Выберите опцию\nТекущее сообщение: `{config_manager.welcome_msg['message']}`', 
        parse_mode='markdown',
        reply_markup=set_meeting()
    )
    
@router.callback_query(F.data.startswith('meeting:change:'))
async def meeting_change(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split(':')[-1]
    if action == 'cooldown':
        await state.set_state(ChangeWelcomeCooldownProcessing.waiting_hours)
        return await callback.message.edit_text('Введите новый кулдаун в часах\n(1д = 24ч)')
    elif action == 'message':
        await state.set_state(ChangeWelcomeMessageProcessing.waiting_text)
        return await callback.message.edit_text(
            text=(
                'Введите новый текст сообщения.'
                'Вы можете использовать форматирование:\n`{sender}` - **Имя отправителя сообщения**\n'
                '`{chat_id}` - **ID чата, из которого было отправлено сообщение**\n'
                '`{text}` - **Текст сообщения, на которое вы отвечаете**'
            ),
            parse_mode='markdown'
        )

@router.message(ChangeWelcomeCooldownProcessing.waiting_hours)
async def meeting_change_cd(message: types.Message, state: FSMContext, db):
    cooldown = message.text
    if not cooldown.isdigit():
        return await message.answer('Вы должны ввести целое число')
    cd = int(cooldown)
    settings = Settings()
    await settings.meeting_cooldown(cd)
    await state.clear()
    await message.answer(
        f'Выберите опцию\nТекущее сообщение: `{config_manager.welcome_msg['message']}`', 
        parse_mode='markdown',
        reply_markup=set_meeting()
    )

@router.message(ChangeWelcomeMessageProcessing.waiting_text)
async def meeting_change_msg(message: types.Message, state: FSMContext, db):
    text = message.text
    settings = Settings()
    await settings.meeting_text(text)
    await state.clear()
    await message.answer(
        f'Выберите опцию\nТекущее сообщение: `{config_manager.welcome_msg['message']}`', 
        parse_mode='markdown',
        reply_markup=set_meeting()
    )