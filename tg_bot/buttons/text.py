from bot.models import MagicWord
ortga = "🔙 Ortga"
menuga='🔙 Asosiy menu qaytish'
movies_text="🧾 Kinolar ro'yxati"
chanels="🧾 Kanallar ro'yxati"
message_to_bot="✍️ Botga xabar yuborish"
magic_word="⭐️ Sehirli sozni o'zgartirish"
admin_txt=MagicWord.objects.filter(id=1).first().word
create="📥 Kino qo'shish"
delete="✂️ Kinoni o'chirish"
create_chan="📥 Kanal qo'shish"
delete_chan="✂️ Kanalni o'chirish"


