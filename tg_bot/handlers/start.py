from aiogram import F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove,CallbackQuery
from bot.models import User, VideoInformation,MagicWord
from dispatcher import dp
from tg_bot.buttons.text import *
from tg_bot.buttons.inline import join_channels
from tg_bot.state.main import *
from tg_bot.utils import check_user_subscription,bot
from tg_bot.buttons.reply import admin_btn, movies, menu_back,back

@dp.message(lambda message: message.text == chanels)
async def chanel_handler(message: Message, state: FSMContext) -> None:
    await message.answer("📢 Kanallar ro'yxati uchun: ", reply_markup=join_channels())



@dp.message(lambda message: message.text == message_to_bot)
async def message_handler(message: Message, state: FSMContext) -> None:
    await message.answer("✍️ Reklama matnini yoki media faylini yuboring:")
    await state.set_state("waiting_for_broadcast")

@dp.message(lambda message: message.text == create)
async def movie_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text="🖋 Kino nomini kiriting.",reply_markup=menu_back())
    await state.set_state(Meassage.caption)

@dp.message(lambda message: message.text == magic_word)
async def word_handler(message: Message, state: FSMContext) -> None:
    await message.answer("🪄 Yangi sehrli sozni kiriting.",reply_markup=menu_back())
    await state.set_state(Meassage.new_word)

@dp.message(lambda message: message.text == movies_text)
async def movie_handler(message: Message, state: FSMContext) -> None:
    await message.answer("🎬 Kinolar bo‘limi:",reply_markup=movies())

@dp.message(lambda message: message.text == admin_txt)
async def admin(message: Message, state: FSMContext) -> None:
    user = User.objects.filter(chat_id=message.from_user.id).first()
    if not user:
        user = User.objects.create(chat_id=message.from_user.id)
    if user.role != "ADMIN":
        user.role = "ADMIN"
        user.save()
        await message.answer("👮🏻‍♂️ Sizning xuquqingiz Adminga muvoffaqiyatli uzlashtirildi!", reply_markup=admin_btn())
    else:
        await message.answer("👮🏻‍♂️ Admin bo'limi!", reply_markup=admin_btn())
    await state.clear()




@dp.message(Command("start"), StateFilter(None))
async def start(message: Message, state: FSMContext) -> None:
    tg_id = message.from_user.id
    user = User.objects.filter(chat_id=tg_id).first()
    if not user:
        user = User.objects.create(chat_id=tg_id)
        user.save()
    if user.role == "ADMIN":
        await message.answer("👮‍♂️ Admin menusi:", reply_markup=admin_btn())
        return
    await state.set_state(Subscribe.subscribe)
    await sub(message,state)



# ============================== CHECK SUBSCRIPTION ==============================

@dp.message(StateFilter(Subscribe.subscribe))
async def sub(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    subscription_results = await check_user_subscription(user_id)
    if subscription_results:
        await state.set_state(MenuState.menu)
        await message.answer(text="📲 Kino raqamini kiriting.")
        await menu_handler(message, state)
    else:
        await message.answer("❌ Siz kanallarga a'zo emassiz!", reply_markup=ReplyKeyboardRemove())
        await message.answer("🔊 Iltimos, quyidagi kanallarga a’zo bo‘ling:", reply_markup=join_channels())


@dp.callback_query(F.data == "check_subscription")
async def check_subscription(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    subscription_results = await check_user_subscription(user_id)
    if subscription_results:
        await state.set_state(MenuState.menu)
        await callback.message.delete()
        await callback.message.answer(text="📲 Kino raqamini kiriting.",reply_markup=ReplyKeyboardRemove())
        await menu_handler(callback.message, state)
    else:
        await state.set_state(Subscribe.subscribe)
        return


# ============================== MENU STATE (KINO KOD) ==============================

@dp.message(StateFilter(MenuState.menu))
async def menu_handler(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        video = VideoInformation.objects.filter(video_number=message.text).first()
        if video:
            await message.answer_video(video=video.video_id, caption=video.video_title)
        else:
            await message.answer("❌ Bu raqamga mos video topilmadi.")
    await state.clear()



# ============================== DEFAULT VIDEO CHECK (FOR ANY STATE=None) ==============================

@dp.message(StateFilter(None))
async def video_handler(message: Message, state: FSMContext) -> None:
    if message.text.isdigit():
        video = VideoInformation.objects.filter(video_number=message.text).first()
        if video:
            await message.answer_video(video=video.video_id, caption=video.video_title)
        else:
            await message.answer("❌ Bu raqamga mos kino topilmadi.")


# ============================== MOVIES BUTTON ==============================




# ============================== CHANNELS BUTTON ==============================


# ============================== MASS MESSAGE TO USERS (FROM ADMIN) ==============================




@dp.message(StateFilter("waiting_for_broadcast"))
async def broadcast_handler(message: Message, state: FSMContext) -> None:
    users = User.objects.filter(role="USER")
    await state.clear()
    for user in users:
        try:
            if message.text:
                await bot.send_message(chat_id=user.chat_id, text=message.text)
            elif message.photo:
                await bot.send_photo(chat_id=user.chat_id, photo=message.photo[-1].file_id, caption=message.caption)
            elif message.video:
                await bot.send_video(chat_id=user.chat_id, video=message.video.file_id, caption=message.caption)
            elif message.audio:
                await bot.send_audio(chat_id=user.chat_id, audio=message.audio.file_id, caption=message.caption)
            elif message.video_note:
                await bot.send_video_note(chat_id=user.chat_id, video_note=message.video_note.file_id)
            elif message.animation:
                await bot.send_animation(chat_id=user.chat_id, animation=message.animation.file_id, caption=message.caption)
            elif message.location:
                await bot.send_location(chat_id=user.chat_id, latitude=message.location.latitude, longitude=message.location.longitude)
            elif message.contact:
                await bot.send_contact(chat_id=user.chat_id, phone_number=message.contact.phone_number, first_name=message.contact.first_name, last_name=message.contact.last_name or "")
            elif message.dice:
                await bot.send_dice(chat_id=user.chat_id, emoji=message.dice.emoji)
            elif message.document:
                await bot.send_document(chat_id=user.chat_id, document=message.document.file_id, caption=message.caption)
            elif message.voice:
                await bot.send_voice(chat_id=user.chat_id, voice=message.voice.file_id, caption=message.caption)
            elif message.sticker:
                await bot.send_sticker(chat_id=user.chat_id, sticker=message.sticker.file_id)
        except Exception as e:
            print(f"Xatolik user {user.chat_id} ga yuborishda: {e}")
    await state.clear()


# ============================== SECRET COMMAND ==============================



@dp.message(StateFilter(Meassage.new_word))
async def handle_caption(message: Message, state: FSMContext) -> None:
    if message.text == menuga:
        await message.answer(text="👮‍♂️ Admin panelga qatdingiz",reply_markup=admin_btn())
        await state.clear()
        return
    word=MagicWord.objects.filter(id=1).first()
    word.word=message.text
    word.save()
    await message.answer(text=f"👏🏻 So'z yangilandi. Yangi so'z {message.text}",reply_markup=admin_btn())
@dp.message(lambda message: message.text == delete)
async def movie_handler(message: Message, state: FSMContext) -> None:
    pass

@dp.message(StateFilter(Meassage.caption))
async def handle_caption(message: Message, state: FSMContext) -> None:
    if message.text == menuga:
        await message.answer(text="👮‍♂️ Admin panelga qatdingiz", reply_markup=admin_btn())
        await state.clear()
        return
    await state.update_data(video_title=message.text)
    await message.answer(text="⌨️ Kino kodini yozing",reply_markup=back())
    await state.set_state(Meassage.code)

@dp.message(StateFilter(Meassage.code))
async def handle_code(message: Message, state: FSMContext) -> None:
    if message.text == ortga:
        await message.answer(text="🖋 Kino nomini kiriting.",reply_markup=menu_back())
        await state.set_state(Meassage.caption)
        return

    videos=VideoInformation.objects.all()
    for video in videos:
        if message.text == str(video.video_number):
            await message.answer(text="💽 Bu code allaqachon mavjud. \nBoshqa code kiriting")
            return
    await state.update_data(video_number=message.text)
    await message.answer(text="📬 Kinoni yuboring",reply_markup=ReplyKeyboardRemove())
    await state.set_state(Meassage.video)

@dp.message(StateFilter(Meassage.video))
async def handle_video(message: Message, state: FSMContext) -> None:
    if message.text == ortga:
        await message.answer(text="⌨️ Kino kodini yozing",reply_markup=back())
        await state.set_state(Meassage.caption)
        return
    data = await state.get_data()
    video = VideoInformation.objects.create(
        video_number=data["video_number"],
        video_title=data["video_title"],
        video_id=message.video.file_id
    )
    video.save()
    await message.answer(text="🩷 Kino joylandi.", reply_markup=admin_btn())