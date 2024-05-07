from aiogram import executor,types,Dispatcher,Bot 
from aiogram.dispatcher.filters import CommandStart
from datetime import datetime
from admin_keybord import admin_panel
from aiogram.utils.markdown import code
from datebase import DataBase

bot = Bot(token="")  # <-- Botin tokeni
dp = Dispatcher(bot)
db =  DataBase()

async def check_one_channel(channel, user):
    try:
        is_member = await bot.get_chat_member(
            chat_id=channel,
            user_id=user,
        )
        if is_member["status"] != "left":
            return "true"
        return "false"
    except:
        return "error"
    
async def check_all_channels(user):
    for channel in db.get_channels():
        checker = await check_one_channel(channel=channel[0], user=user)
        if checker == "true":
            print("passd")
            continue
        else:
            return False
    return True



@dp.message_handler(CommandStart())
async def start_command_handler(message: types.Message):

    now = datetime.now()
    if not db.get_user(message.from_user.id):
        db.add_user(message.from_user.id, False, now.strftime("%d/%m/%Y"))
    if await check_all_channels(user=message.from_user.id):
        db.update_user(message.from_user.id)
        await message.answer(f"👋Sálem, {message.from_user.first_name} botqa xosh kelip siz!")
    else:
        await message.answer(f"👋Sálem, {message.from_user.first_name} botqa xosh kelip siz!")


@dp.message_handler(commands=['admin'])
async def admin_panel_handler(message: types.Message):
    is_admin = db.get_admin(message.from_user.id)
    if is_admin:
        await message.answer(f"Sálem {message. from_user. first_name}! Admin panelge xosh kelipsiz.", reply_markup=admin_panel)
    else:
        await message.answer("Keshiresiz sizge tiyisli bolmaǵan buyrıqtan paydalanayabsiz!")


@dp.callback_query_handler(text="add_admin") # <- Taza admin qosiw!
async def add_admin(call: types.CallbackQuery):
    await call.message.answer("Botga tómendegi buyrıqtı jiberiń ```text @add_admin admining_telegram_id_qosiladi```", parse_mode="markdown")


@dp.callback_query_handler(text="delete_admin") # <- Admindi alip taslaw!
async def delete_admin(call: types.CallbackQuery):
    await call.message.answer("Botga tómendegi buyrıqtı jiberiń ```text @del_admin alip_taslaw_kerek_bolgan_admining_telegram_id_qosiladi```", parse_mode="markdown")

@dp.callback_query_handler(text="add_channel") # <- Kanal qosiw!
async def add_admin(call: types.CallbackQuery):
    await call.message.answer("Botga tómendegi buyrıqtı jiberiń ```text @add_channel @kanaldin_ati_kiritiledi```", parse_mode="markdown")


@dp.callback_query_handler(text="delete_channel") # <- Kanaldi alip taslaw!
async def delete_admin(call: types.CallbackQuery):
    await call.message.answer("Botga tómendegi buyrıqtı jiberiń ```text @del_channel @alip_taslaw_kerek_bolgan_kanal_ati_qosiladi!```", parse_mode="markdown")

@dp.callback_query_handler(text="send_message") # <- Habar jiberiw yaki paydalaniwshilarga reklama jiberiw!
async def add_admin(call: types.CallbackQuery):
    await call.message.answer("Xabarni kiriting:", parse_mode="markdown")

@dp.callback_query_handler(text="check")
async def check_(call: types.CallbackQuery):
    if await check_all_channels(call.message.chat.id):
        await call.message.edit_text("🎉")
    else:
        channels_inline_button = types.InlineKeyboardMarkup(row_width=1)
        for channel in db.get_channels():
            channels_inline_button.add(types.InlineKeyboardButton(text=f"{channel[0]}", url=f"t.me/{channel[0][1::]}"))
        channels_inline_button.add(types.InlineKeyboardButton(text="Tekseriw", callback_data="check"))
        await call.message.edit_text("⚠️Botdan paydalanıw ushın, tómendegi kanallarǵa jazılıw bolıń:")
        await call.message.edit_reply_markup(channels_inline_button)

@dp.callback_query_handler(text="list_admins") # <- Adminler dizimi!
async def list_admins(call: types.CallbackQuery):
    text = ""
    for i in db.get_admins():
        text += f"{code(str(i[0]))}\n"
    await call.message.answer(text)

@dp.callback_query_handler(text="list_channels") # <- Kanalar dizimi!
async def list_admins(call: types.CallbackQuery):
    text = ""
    for i in db.get_channels():
        text += f"{i[0]}\n"
    await call.message.answer(text)

@dp.callback_query_handler(text="statistics") # <- Adminge bot paydalaniwshilar qansha ekenin ko'rsetedi h.t.b!
async def delete_admin(call: types.CallbackQuery):
    await call.message.answer(f"""
Paydalanıwshılar sanı : {len(db.get_all_users())}
Aktiv paydalanıwshılar: {len(list(db.get_users()))}
Kúnlik paydalanıwshılar: {len(db.get_now_users())}
Kanallar: {len(list(db.get_channels()))}
Adminler: {len(list(db.get_admins()))}
""", parse_mode="markdown")



@dp.message_handler(commands=["statistika"]) # <- Paydalaniwshilarga botin statistikasin ko'rsetedi!
async def menu_panel(message: types.Message):
    await message.answer(f"""
🗣<b>Botdagi paydalanıwshılar sanı:</b> {len(db.get_all_users())}
<b>Aktiv paydalanıwshılar:</b> {len(list(db.get_users()))}
<b>Botning jumısqa túsken sánesi:</b>?.?.2023
\n@Bawz_01\tstatistikasi""",parse_mode="HTML")


@dp.message_handler(content_types=types.ContentType.ANY)
async def text_handler(message: types.Message):
    if message.chat.type == "private":
        if await check_all_channels(user=message.from_user.id):
            db.update_user(message.from_user.id)
            try:
                is_admin = db.get_admin(message.from_user.id)
                if is_admin:
                    if message.text:
                        if message.text.split()[0] == "@add_admin":
                            r = db.add_admin(message.text.split()[1])
                            if r:
                                await message.answer("Admin qosıldı!")
                            else:
                                await message.answer("Bul admin ámeldegi")
                        elif message.text.split()[0] == "@del_admin":
                            r = db.delete_admin(message.text.split()[1])
                            if r:
                                await message.answer("Admin óshirildi!")
                            else:
                                await message.answer("Bunday admin joq!")
                        elif message.text.split()[0] == "@add_channel":
                            try:
                                channel = message.text.split()[1] if "@" in message.text.split()[1] else "@" + message.text.split()[1]
                                await bot.get_chat_administrators(channel)
                                r = db.add_channel(channel)
                                if r:
                                    await message.answer("Kanal qosıldı!")
                                else:
                                    await message.answer("Bul kanal ámeldegi!")
                            except Exception as e:
                                print(e)
                                await message.answer("Bul kanal joq yamasa bot bul kanal admini emes!")
                        elif message.text.split()[0] == "@del_channel":
                            r = db.delete_channel(message.text.split()[1])
                            if r:
                                await message.answer("Kanal óshirildi!")
                            else:
                                await message.answer("Bunday kanal joq!")
                        else:
                            for user in db.get_users():
                                try:
                                    await bot.copy_message(
                                        chat_id=user[0],
                                        from_chat_id=message.from_user.id,
                                        message_id=message.message_id,
                                    )
                                except:
                                    pass
                    else:
                        for user in db.get_users():
                            await bot.copy_message(
                                chat_id=user[0],
                                from_chat_id=message.from_user.id,
                                message_id=message.message_id,
                            )

            except Exception as e:
                print(e)
        else:
            channels_inline_button = types.InlineKeyboardMarkup(row_width=1)
            for channel in db.get_channels():
                channels_inline_button.add(types.InlineKeyboardButton(text=f"{channel[0]}", url=f"t.me/{channel[0][1::]}"))
            channels_inline_button.add(types.InlineKeyboardButton(text="Tekseriw", callback_data="check"))
            await message.answer("⚠️Botdan paydalanıw ushın, tómendegi kanallarǵa jazılıw bolıń:", reply_markup=channels_inline_button)









if  __name__ == '__main__':
    executor.start_polling(dispatcher=dp,skip_updates=True)



