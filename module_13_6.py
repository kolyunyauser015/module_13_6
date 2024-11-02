from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = InlineKeyboardMarkup(resize_keyboard=True)
button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_2 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
kb.add(button_1)
kb.insert(button_2)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.")


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию", reply_markup=kb)



@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10*вес(кг) + 6.25 * рост(см) + 5 * возраст(г) + 5")
    await call.message.answer("Выберите опцию", reply_markup=kb)
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_colories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    calc_colories = 10 * int(data['first']) + 6.25 * int(data['second']) + 5 * int(data['third']) + 5
    await message.answer(f"Ваша норма калорий: {calc_colories}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
