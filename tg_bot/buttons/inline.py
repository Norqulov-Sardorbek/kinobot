from bot.models import ChannelsToSubscribe, VideoInformation
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.core.paginator import Paginator
def join_channels():
    channels = ChannelsToSubscribe.objects.all()

    buttons = [
        [InlineKeyboardButton(
            text=f"{index+1} - kanal",
            url=f"https://t.me/{channel.link.replace("@", "")}"
        )] for index, channel in enumerate(channels)
    ]

    buttons.append([InlineKeyboardButton(
        text="✅ Check",
        callback_data="check_subscription"
    )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)



def generate_pdf_list_message(page: int = 1, per_page: int = 10):
    pdfs = VideoInformation.objects.all().order_by('-created_at')
    paginator = Paginator(pdfs, per_page)
    page_obj = paginator.get_page(page)

    message_text = f"📄 *Kinolar*             (Page {page}/{paginator.num_pages})      \n\n"
    buttons = []

    for index, file in enumerate(page_obj, start=1 + (page - 1) * per_page):
        message_text += f"{index}. {file.caption}\n"
        buttons.append(InlineKeyboardButton(text=str(index), callback_data=f"pdf_{file.id}"))

    keyboard_buttons = [buttons[i:i+5] for i in range(0, len(buttons), 5)]


    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Prev", callback_data=f"page_{page - 1}"))
    if page < paginator.num_pages:
        navigation_buttons.append(InlineKeyboardButton(text="Next ➡️", callback_data=f"page_{page + 1}"))

    if navigation_buttons:
        keyboard_buttons.append(navigation_buttons)

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    return message_text, keyboard
