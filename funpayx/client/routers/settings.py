from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from client.keyboards.settings_menu import settings_menu, _paginate_blacklist, set_meeting, command_settings_kb, paginate_commands
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

class NewCommand(StatesGroup):
    waiting_name = State()
    waiting_text = State()

class EditCommandName(StatesGroup):
    waiting_command = State()

class EditCommandMessage(StatesGroup):
    waiting_message = State()

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

@router.callback_query(F.data.startswith('command:page:'))
async def command_settings(callback: types.CallbackQuery):
    page = callback.data.split(':')[-1]
    await callback.message.edit_text('Меню создания простых команд автоответа\n✅ - команда запущена', reply_markup=paginate_commands(config_manager.auto_answer, page))

@router.callback_query(F.data.startswith('command:new:'))
async def new_command(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите название команды, префикс не важен. (хоть !start хоть /help)')
    await state.set_state(NewCommand.waiting_name)

@router.message(NewCommand.waiting_name)
async def new_command_nick(message: types.Message, state: FSMContext):
    command = message.text
    await state.update_data(command=command)
    await message.answer(
            text=(
                'Введите текст, которым будет отвечать команда.'
                'Вы можете использовать форматирование:\n`{sender}` - **Имя отправителя сообщения**\n'
                '`{chat_id}` - **ID чата, из которого было отправлено сообщение**\n'
                '`{text}` - **Текст сообщения, на которое вы отвечаете**'
            ),
            parse_mode='markdown'
        )
    await state.set_state(NewCommand.waiting_text)

@router.message(NewCommand.waiting_text)
async def new_command_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    command, msg = data.get('command'), message.text
    settings = Settings()
    await settings.create_command(command, msg)
    await message.answer(
        text=f'Настройки команды {command}\nСообщение: `{msg}`',
        parse_mode='markdown',
        reply_markup=command_settings_kb(config_manager.find_command(command)))

@router.callback_query(F.data.startswith('command:edit:'))
async def edit_command(callback: types.CallbackQuery):
    command_name = callback.data.split(':')[-1]
    command = config_manager.find_command(command_name)
    await callback.message.edit_text(
        text=f'Настройки команды {command['command']}\nСообщение: `{command['message']}`',
        parse_mode='markdown',
        reply_markup=command_settings_kb(command)
    )

@router.callback_query(F.data.startswith('command:set:'))
async def command_set(callback: types.CallbackQuery, state: FSMContext):
    command = callback.data.split(':')[-1]
    action = callback.data.split(':')[-2]
    await state.update_data(command=command)
    if action == 'msg':
        await callback.message.answer('Введите новое сообщение')
        await state.set_state(EditCommandMessage.waiting_message)
    elif action == 'cmd':
        await callback.message.answer('Введите новое название команды')
        await state.set_state(EditCommandName.waiting_command)
    await callback.answer()

@router.message(EditCommandMessage.waiting_message)
async def edit_command_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    command = data.get('command')
    new_cmd_message = message.text
    settings = Settings()
    await settings.change_cmd_message(command, new_cmd_message)
    await message.answer(
        text=f'Настройки команды {command}\nСообщение: `{new_cmd_message}`',
        parse_mode='markdown',
        reply_markup=command_settings_kb(config_manager.find_command(command)))

@router.message(EditCommandName.waiting_command)
async def edit_command_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    command = data.get('command')
    new_command = message.text
    settings = Settings()
    await settings.change_cmd_name(command, new_command)
    config_manager.find_command(new_command)
    await message.answer(
        text=f'Настройки команды {new_command}\nСообщение: `{config_manager.find_command(new_command)['message']}`',
        parse_mode='markdown',
        reply_markup=command_settings_kb(config_manager.find_command(new_command)))

@router.callback_query(F.data.startswith('command:toggle:'))
async def toggle_command_options(callback: types.CallbackQuery):
    command = callback.data.split(':')[-1]
    option = callback.data.split(':')[-2]
    settings = Settings()
    await settings.toggle_command(command, option)
    await callback.message.edit_text(
        text=f'Настройки команды {command}\nСообщение: `{config_manager.find_command(command)['message']}`',
        parse_mode='markdown',
        reply_markup=command_settings_kb(config_manager.find_command(command)))
    
@router.callback_query(F.data.startswith('command:delete:'))
async def delete_command(callback: types.CallbackQuery):
    command = callback.data.split(':')[-1]
    settings = Settings()
    await settings.delete_command(command)
    await callback.message.edit_text('Меню создания простых команд автоответа\n✅ - команда запущена', reply_markup=paginate_commands(config_manager.auto_answer, 0))