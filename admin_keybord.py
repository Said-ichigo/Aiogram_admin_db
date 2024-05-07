from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

admin_panel = InlineKeyboardMarkup(row_width=2)
admin_panel.add(InlineKeyboardButton(text="➕Admin qosıw", callback_data="add_admin"), InlineKeyboardButton(text="🗑Admin óshiriw", callback_data="delete_admin"))
admin_panel.add(InlineKeyboardButton(text="➕Kanal qosıw", callback_data="add_channel"), InlineKeyboardButton(text="🗑Kanal óshiriw", callback_data="delete_channel"))
admin_panel.add(InlineKeyboardButton(text="👨‍👨‍👦‍👦Adminlar dizimi", callback_data="list_admins"), InlineKeyboardButton(text="📎Kanalar dizimi", callback_data="list_channels"))
admin_panel.add(InlineKeyboardButton(text="✍️Jańa xabar jiberiw", callback_data="send_message"), InlineKeyboardButton(text="📊Bot statistikası", callback_data="statistics"))
