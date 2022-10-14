
from aiogram.types import ReplyKeyboardMarkup , KeyboardButton , InlineKeyboardMarkup , InlineKeyboardButton
import telebot 
from telebot import types
#srart menu
Pars = KeyboardButton('🖇 Парсить')
Settings_users = KeyboardButton('🔗 Настройки профиля')
report_error = KeyboardButton('⚠️ Сообщить о ошибке')
menu_users = ReplyKeyboardMarkup(resize_keyboard=True)
menu_users.add(Pars).add(Settings_users).add(report_error)

#start menu adm
Pars_ad = KeyboardButton('🖇 Парсить')
Settings_users_ad = KeyboardButton('🔗 Настройки профиля')
report_error_ad = KeyboardButton('⚠️ Сообщить о ошибке')
adm_panel_ad = KeyboardButton('🔱 Админ панель')
menu_users_adm = ReplyKeyboardMarkup(resize_keyboard=True)
menu_users_adm.add(Pars).add(Settings_users).add(report_error).add(adm_panel_ad)

#stop menu

stop_pars_but = KeyboardButton('❌ Остановить парсинг обьявлений')
stop_pars = ReplyKeyboardMarkup(resize_keyboard=True)
stop_pars.add(stop_pars_but)

# Settings 
Ad_sett = InlineKeyboardButton("💿 Кол-во обьявлений", callback_data="Obv")
view_sett = InlineKeyboardButton("👁 Кол-во просмотров", callback_data="Pros")
text_wots = InlineKeyboardButton("💼 Текст WhatsApp'a", callback_data="Text")
text_wots2 = InlineKeyboardButton("💼 Текст WhatsApp'a #2", callback_data="Text2")
data_reg_user = InlineKeyboardButton("📫 Дата регистрации пользователя", callback_data="data_reg_pl")
Butt_pars = InlineKeyboardMarkup(row_widht = 1).add(Ad_sett).add(view_sett).add(data_reg_user).row(text_wots,text_wots2)


#Parser
sbazar_butt = InlineKeyboardButton("🇨🇿 sbazar.cz", callback_data="sbazar")
wallpop_butt = InlineKeyboardButton("🇪🇸 es.wallapop.com", callback_data="wallpop_es")
vinted_it = InlineKeyboardButton("🇮🇹 vinted.it", callback_data="vinted_it")
vinted_pl = InlineKeyboardButton("🇵🇱 vinted.pl", callback_data="vinted_pl")
vinted_nl = InlineKeyboardButton("🇳🇱 vinted.nl", callback_data="vinted_nl")
md999 = InlineKeyboardButton("🇲🇩 999.md", callback_data="md999")
olxkz = InlineKeyboardButton("Olx.kz", callback_data="Olxtoken")
#
pars_choise_but = InlineKeyboardMarkup(row_widht = 1).add(wallpop_butt).add(sbazar_butt).row(vinted_it,vinted_pl).add(md999).add(olxkz)

#ADM PANEL ADD OR DELETE USER
add_user_to_pars = InlineKeyboardButton("✅ Добавить пользователя в парсер", callback_data="add_user")
delete_user_to_pars = InlineKeyboardButton("❌ Удалить пользователя с парсера", callback_data="delete_user")
send_message_all_users = InlineKeyboardButton("🔅 Сделать рассылку", callback_data="send_message_all_users")
adm_user = InlineKeyboardMarkup(row_widht = 1).add(add_user_to_pars).add(delete_user_to_pars).add(send_message_all_users)



add_user_to_pars_l = InlineKeyboardButton("✅ Добавить пользователя в парсер", callback_data="add_user")
delete_user_to_pars_l = InlineKeyboardButton("❌ Удалить пользователя с парсера", callback_data="delete_user")
send_message_all_users_l = InlineKeyboardButton("🔅 Сделать рассылку", callback_data="send_message_all_users")
add_to_adm_l = InlineKeyboardButton("✅ Добавить админа в парсер", callback_data="add_adm_l")
adm_user_l = InlineKeyboardMarkup(row_widht = 1).row(add_user_to_pars,add_to_adm_l).add(delete_user_to_pars).add(send_message_all_users)

def but_for_phone(phone,text,link_ad,text2,title):
    button_wots_phone = telebot.types.InlineKeyboardMarkup()
    if text == "Не установленно" or text == "0":
        url=str("https://wa.me/"+str(phone)).replace(" ","+")
        button_wots_phone.add(telebot.types.InlineKeyboardButton(text='📍 WhatsApp', url=url))
    elif "-ссылка-" in text or "-товар-" in text:
            url=str("https://wa.me/"+str(phone)+"?text="+text.replace("-ссылка-",link_ad).replace("-товар-",title).replace(" ","+")).replace(" ","+")
            button_wots_phone.add(telebot.types.InlineKeyboardButton(text='📍 WhatsApp', url=url )) 
    else:
        url = str("https://wa.me/"+str(phone)+"?text="+str(text)).replace(" ","+")
        button_wots_phone.add(telebot.types.InlineKeyboardButton(text='📍 WhatsApp', url=url))

    if text2 == "Не установленно" or text2 == "0":
        url=str("https://wa.me/"+str(phone)).replace(" ","+")
        button_wots_phone.add(telebot.types.InlineKeyboardButton(text='📍 WhatsApp', url=url))
    elif "-ссылка-" in text2 or "-товар-" in text2:
            url=str("https://wa.me/"+str(phone)+"?text="+text2.replace("-ссылка-",link_ad).replace(" ","+")).replace(" ","+")
            button_wots_phone.add(telebot.types.InlineKeyboardButton(text='📍 WhatsApp', url=url ))   
    else:
        url = str("https://wa.me/"+str(phone)+"?text="+str(text2)).replace(" ","+")
        button_wots_phone.add(telebot.types.InlineKeyboardButton(text='📍 WhatsApp',url=url))
    return button_wots_phone


def but_for_phone_as(phone,text,link_ad,text2,title_ad):
    wots_phone = InlineKeyboardMarkup()
    if text == "Не установленно" or text == "0":
        url=str("https://wa.me/"+str(phone)).replace(" ","+")
        button_wots_phone = InlineKeyboardButton("📍 WhatsApp",url=url)
        wots_phone.add(button_wots_phone)
    elif "-ссылка-" in text or "-товар-" in text:
            url=str("https://wa.me/"+str(phone)+"?text="+text.replace("-ссылка-",link_ad).replace("-товар-",title_ad).replace(" ","+"))
            button_wots_phone = InlineKeyboardButton("📍 WhatsApp", url=url )
            wots_phone.add(button_wots_phone)   
    else:
        url = str("https://wa.me/"+str(phone)+"?text="+str(text)).replace(" ","+")
        button_wots_phone = InlineKeyboardButton("📍 WhatsApp",url=url)
        wots_phone = InlineKeyboardMarkup(row_widht = 1).add(button_wots_phone)

    if text2 == "Не установленно" or text2 == "0":
        url=str("https://wa.me/"+str(phone)).replace(" ","+")
        button_wots_phone2 = InlineKeyboardButton("📍 WhatsApp",url=url)
        wots_phone.add(button_wots_phone2)
    elif "-ссылка-" in text2 or "-товар-" in text2:
            url=str("https://wa.me/"+str(phone)+"?text="+text2.replace("-ссылка-",link_ad).replace(" ","+")).replace(" ","+")
            button_wots_phone2 = InlineKeyboardButton("📍 WhatsApp", url=url )
            wots_phone.add(button_wots_phone2)   
    else:
        url = str("https://wa.me/"+str(phone)+"?text="+str(text2)).replace(" ","+")
        button_wots_phone2 = InlineKeyboardButton("📍 WhatsApp",url=url)
        wots_phone.add(button_wots_phone2)        
    return wots_phone    
#Telebot
menu_users_telebot=types.ReplyKeyboardMarkup(resize_keyboard=True)
Pars_telebot = types.KeyboardButton('🖇 Парсить')
Settings_users_telebot = types.KeyboardButton('🔗 Настройки профиля')
report_error_telebot = types.KeyboardButton('⚠️ Сообщить о ошибке')
menu_users_telebot.add(Pars_telebot).add(Settings_users_telebot).add(report_error_telebot)

menu_users_telebot_ad=types.ReplyKeyboardMarkup(resize_keyboard=True)
Pars_telebot_ad = types.KeyboardButton('🖇 Парсить')
Settings_users_telebot_ad = types.KeyboardButton('🔗 Настройки профиля')
report_error_telebot_ad = types.KeyboardButton('⚠️ Сообщить о ошибке')
adm_panel_ad = types.KeyboardButton('🔱 Админ панель')
menu_users_telebot_ad.add(Pars_telebot_ad).add(Settings_users_telebot_ad).add(report_error_telebot_ad).add(adm_panel_ad)