import telebot
import re
import requests
from urllib.parse import urlparse, urlunparse
from telebot import types
from keep_alive import keep_alive

# Telegram bot API key
API_KEY = '7925683283:AAG2QUVayxeCE_gS70OdOm79dOFwWDqPvlU'
bot = telebot.TeleBot(API_KEY)

# Your AliExpress affiliate tracking
TRACKING_ID = 'default'

def extract_links(text):
    return re.findall(r"(?i)\bhttps?://[^\s]+", text)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = '''
👋 <b>مرحبًا بك في بوت @Coins_Aliexpress_bot</b>

🔹 مهمة هذا البوت زيادة نسبة التخفيض بالنقاط من 1% حتى 70%

✅ تعمل الروابط فقط مع المنتوجات التي يتوفر فيها تخفيض النقاط

🔹 <b>كيف تستعمل البوت ؟</b>
💡 انسخ الرابط فقط 🔗 
💬 ارسل كرسالة هنا للبوت 
⏳ إنتظر لحظات
📌 إضغط على الرابط الذي يأتيك

⭐️ <b>لمزيد من العروض، انضم إلى قناتنا عبر الرابط التالي:</b>
<a href="https://t.me/Aliexpress_coupons_chine">@Aliexpress_coupons_chine</a>

🔄 ثبّت البوت واستفد من عروض حصرية ونقاط إضافية!

🎉 <b>شكراً على استخدامك AliCoinsBot</b>
    '''
    bot.reply_to(message, msg, parse_mode='HTML')

@bot.message_handler(func=lambda message: True)
def modify_link(message):
    urls = extract_links(message.text)
    if not urls:
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("قناتنا🔥", url="https://t.me/Aliexpress_coupons_chine")
        markup.add(button)
        bot.reply_to(message, "⚠️ لم يتم ايجاد اي روابط في رسالتك!", reply_markup=markup)
        return

    original_link = urls[0]
    if 'item' not in original_link:
        bot.reply_to(message, "يجب نسخ الرابط من التطبيق ثم إرساله إلى البوت✅")
        return

    try:
        bot.reply_to(message, "🔄 جاري معالجة الرابط...")
        # Clean up the URL
        parsed = urlparse(original_link)
        cleaned_url = urlunparse(parsed._replace(query=''))

        # Add affiliate tracking manually
        affiliate_link = f"{cleaned_url}?aff_fcid={TRACKING_ID}&aff_fsk=&aff_platform=portals-tool&sk=&aff_trace_key=&terminal_id="

        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("رابط التخفيض 🥰", url=affiliate_link)
        button2 = types.InlineKeyboardButton("قناتنا🔥", url="https://t.me/Aliexpress_coupons_chine")
        markup.add(button1)
        markup.add(button2)

        bot.send_message(message.chat.id, f"✅ <b>تم توليد رابط التخفيض الخاص بك!</b>\n\n{affiliate_link}", parse_mode='HTML', reply_markup=markup)

    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "❌ حدث خطأ أثناء معالجة الرابط. حاول مرة أخرى.")

if __name__ == "__main__":
    while True:
        try:
            keep_alive()
            bot.polling()
        except Exception as e:
            print(f"Polling error: {e}")
