import os
import time
from pathlib import Path

from aiogram.types import Message
from aiogram.types import FSInputFile
from aiogram.methods.send_audio import SendAudio
from aiogram import Router
from aiogram import F
from aiogram.filters import CommandStart, Command
from logic.prepare_info import get_list_messages_for_today, get_quantity_phrases_repeat_today, get_list_messages_day
from voice.get_voice import convert_text_to_speech
from settings import get_logger

logger = get_logger(__name__)

user1 = int(os.getenv('user1'))
users = {user1}

router = Router()


@router.message(CommandStart(), F.from_user.id.in_(users))
async def get_start(message: Message):
    logger.debug('Получена комманда start')
    await message.answer(f'Привет {message.from_user.first_name}. Начнем!')
    await message.answer(f'Посмотри список команд и запускай нужный режим.')


@router.message(Command("all_days"), F.from_user.id.in_(users))
async def get_start(message: Message, bot):
    logger.debug('Получена комманда all_days')
    await message.answer(f'Привет {message.from_user.first_name}. Начнем!')
    chat_id = message.chat.id
    list_message = get_list_messages_for_today()
    await send_periodic_messages(bot, chat_id, list_message)


@router.message(Command("1_day"), F.from_user.id.in_(users))
async def day1(message: Message, bot):
    logger.debug('Получена команда 1_day')
    await message.answer(f'Привет {message.from_user.first_name}. Начнем повтор вчерашних фраз!')
    chat_id = message.chat.id
    list_message = get_list_messages_day(1)
    await message.answer(f'Кол-во фраз {len(list_message)}')
    await send_messages_per_day(bot, chat_id, list_message)


@router.message(Command("3_day"), F.from_user.id.in_(users))
async def day3(message: Message, bot):
    logger.debug('Получена команда 3_day')
    await message.answer(f'Привет {message.from_user.first_name}. Начнем повтор фраз добавленных 3 дня назад!')
    chat_id = message.chat.id
    list_message = get_list_messages_day(3)
    await message.answer(f'Кол-во фраз {len(list_message)}')
    await send_messages_per_day(bot, chat_id, list_message)


@router.message(Command("7_day"), F.from_user.id.in_(users))
async def day7(message: Message, bot):
    logger.debug('Получена команда 7_day')
    await message.answer(f'Привет {message.from_user.first_name}. Начнем повтор фраз добавленных 7 дней назад!')
    chat_id = message.chat.id
    list_message = get_list_messages_day(7)
    await message.answer(f'Кол-во фраз {len(list_message)}')
    await send_messages_per_day(bot, chat_id, list_message)


@router.message(Command("12_day"), F.from_user.id.in_(users))
async def day12(message: Message, bot):
    logger.debug('Получена команда 12_day')
    await message.answer(f'Привет {message.from_user.first_name}. Начнем повтор фраз добавленных 12 дней назад!')
    chat_id = message.chat.id
    list_message = get_list_messages_day(12)
    await message.answer(f'Кол-во фраз {len(list_message)}')
    await send_messages_per_day(bot, chat_id, list_message)


@router.message(Command("16_day"), F.from_user.id.in_(users))
async def day16(message: Message, bot):
    logger.debug('Получена команда 16_day')
    await message.answer(f'Привет {message.from_user.first_name}. Начнем повтор фраз добавленных 16 дней назад!')
    chat_id = message.chat.id
    list_message = get_list_messages_day(16)
    await message.answer(f'Кол-во фраз {len(list_message)}')
    await send_messages_per_day(bot, chat_id, list_message)


@router.message(Command("35_day"), F.from_user.id.in_(users))
async def day35(message: Message, bot):
    logger.debug('Получена команда 35_day')
    await message.answer(f'Привет {message.from_user.first_name}. Начнем повтор фраз добавленных 35 дней назад!')
    chat_id = message.chat.id
    list_message = get_list_messages_day(35)
    await message.answer(f'Кол-во фраз {len(list_message)}')
    await send_messages_per_day(bot, chat_id, list_message)


@router.message(Command("50_day"), F.from_user.id.in_(users))
async def day50(message: Message, bot):
    logger.debug('Получена команда 50_day')
    await message.answer(f'Привет {message.from_user.first_name}. Начнем повтор фраз добавленных 50 дней назад!')
    chat_id = message.chat.id
    list_message = get_list_messages_day(50)
    await message.answer(f'Кол-во фраз {len(list_message)}')
    await send_messages_per_day(bot, chat_id, list_message)


@router.message(Command("today"), F.from_user.id.in_(users))
async def get_start(message: Message):
    logger.debug('Получена команда today')
    quantity = get_quantity_phrases_repeat_today()
    await message.answer(f'ок. сегодня повторяем фраз: {quantity}')
    logger.debug('Отправленно сообщение с количеством фраз')


@router.message(Command("audio"), F.from_user.id.in_(users))
async def get_start(message: Message, bot):
    logger.debug('Получена команда audio')
    list_message = get_list_messages_for_today()
    chat_id = message.chat.id
    await send_audio(bot, chat_id, list_message)


async def send_periodic_messages(bot, chat_id, list_message):
    logger.debug(f'Длина списка фраз на сегодня: {len(list_message)}')
    for message in list_message:
        ask = await bot.send_message(chat_id, message['ask'])
        logger.debug(f'send ask')
        time.sleep(10)
        answer = await bot.send_message(chat_id, message['answer'])
        logger.debug(f'send answer')
        time.sleep(10)
        await bot.delete_message(chat_id=chat_id, message_id=ask.message_id)
        logger.debug(f'delete ask')
        await bot.delete_message(chat_id=chat_id, message_id=answer.message_id)
        logger.debug(f'delete answer')


async def send_messages_per_day(bot, chat_id, list_message):
    logger.debug(f'Длина выбранного списка фраз: {len(list_message)}')
    for message in list_message:
        ask = await bot.send_message(chat_id, message['ask'])
        logger.debug(f'send ask')
        time.sleep(10)
        answer = await bot.send_message(chat_id, message['answer'])
        logger.debug(f'send answer')
        time.sleep(10)
        await bot.delete_message(chat_id=chat_id, message_id=ask.message_id)
        logger.debug(f'delete ask')
        await bot.delete_message(chat_id=chat_id, message_id=answer.message_id)
        logger.debug(f'delete answer')


async def send_audio(bot, chat_id, list_message):
    logger.debug(f'Длина выбранного списка фраз: {len(list_message)}')
    file_path = Path.cwd() / "voice/output.mp3"
    for message in list_message:
        convert_text_to_speech(message['ask'])
        mp3 = FSInputFile(file_path)
        # Send the image file to the specified chat ID
        await bot.send_audio(chat_id, audio=mp3)
        logger.debug(f'Отправили mp3 файл')
        time.sleep(10)



if __name__ == "__main__":
    pass
