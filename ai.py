import requests
import json
from bs4 import BeautifulSoup

bale_token = "765534315:7oJiKNejp2Sa3hUZKBU8oUwloV4UOLUYVTjWj65p"
base_url = f'https://tapi.bale.ai/bot{bale_token}/'
admin_chat_id = "465605867"
user_data = {}

def get_aqi():
    url = "https://airnow.tehran.ir/"
    page = requests.get(url)
    page_soup = BeautifulSoup(page.content, 'html.parser')
    AQI = page_soup.find("span", {"id": "ContentPlaceHolder1_lblAqi3h"}).text
    desc = page_soup.find("span", {"id": "ContentPlaceHolder1_lblAqi3hDesc"}).text.split()
    status = desc[0]
    pollutant = desc[-1]
    return AQI, status, pollutant

def get_weather_forecast():
    forecast = '''دماي فعلي : 34 درجه سانتي گراد\nوضعيت هوا : تا حدودي آفتابي\nاحتمال بارش: 0٪'''
    return forecast

def send_message(chat_id, text, keyboard=None):
    url = base_url + "sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
    }
    if keyboard:
        payload['reply_markup'] = json.dumps(keyboard)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.text}")
    else:
        print(f"Message sent to {chat_id}: {text}")

def send_notification_to_all_users(message):
    for chat_id in user_data.keys():
        send_message(chat_id, message)

def send_start_reminder_to_all_users():
    reminder_message = '''سلام🥹☘️ استارتم نکردی ها🤍🥹 [/start](send:/start)'''
    send_notification_to_all_users(reminder_message)

def get_updates(offset=None):
    url = base_url + "getUpdates"
    if offset:
        url += f"?offset={offset}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f"Failed to get updates: {response.text}")
        return []

def send_apology_message(chat_id):
    apology_message = '''پوزش میخوام! یه چند ساعتی قطع بودم. ولی الان درست شدم. می‌تونی استارتم کنی /start'''
    send_message(chat_id, apology_message)

def handle_message(chat_id, text):
    if chat_id not in user_data:
        user_data[chat_id] = {'score': 0, 'current_game': None}
    if text == '/start':
        user_data[chat_id] = {'score': 0, 'current_game': None}
        keyboard = {
            'keyboard': [
                [{'text': 'شاخص کیفیت هوا'}, {'text': 'جزئیات وضعیت هوای تهران'}],
                [{'text': 'پیش‌بینی کیفیت هوا'}, {'text': 'گزارش کیفیت هوا'}],
                [{'text': 'اطلاعات جذاب کیفیت هوا'}],
            ],
            'one_time_keyboard': True
        }
        send_message(chat_id, " سلام! به اولين بازو *کيفيت هوا* خوش آمديد لطفا گزينه مورد نظر خود را انتخاب کنيد", keyboard)
    else:
        if text == 'شاخص کیفیت هوا':
            AQI, status, pollutant = get_aqi()
            air_quality_message = f"شاخص کیفیت هوا: {AQI}\nوضعیت: {status}\nآلاینده: {pollutant}"
            send_message(chat_id, air_quality_message)
        elif text == 'جزئیات وضعیت هوای تهران':
            details_message = '''هم اکنون شاخص آلودگي در وضعيت قابل قبول هست
احتمال ميرود که تا شب در همين محدوده شاخص بماند!'''
            send_message(chat_id, details_message)
        elif text == 'پیش‌بینی کیفیت هوا':
            forecast = get_weather_forecast()
            send_message(chat_id, forecast)
        elif text == 'گزارش کیفیت هوا':
            report_message = '''کیفیت هوای تهران طی هفته گذشته به طور کلی نوساناتی داشته است. هرچند در ساعات ابتدایی صبح روزهای اخیر، شاخص کیفیت هوا در وضعیت سالم بوده، اما در برخی ساعات بعدازظهر و شبانگاه، وضعیت به محدوده ناسالم برای گروه‌های حساس رسید. پیشنهاد می‌شود که افراد حساس از تردد غیرضروری در ساعات با شاخص بالا خودداری کنند.'''
            send_message(chat_id, report_message)
        elif text == 'هوش مصنوعی':
            ai_message = '''سلام! من هوش مصنوعی بات هستم. چطور می‌توانم کمکتون کنم؟'''
            send_message(chat_id, ai_message)
        elif text == 'اطلاعات جذاب کیفیت هوا':
            interesting_info = '''کیفیت هوای تهران به دلیل ترافیک سنگین و تعداد زیادی خودروهای دودزا یکی از مسائل مهم است. با این حال، دولت و سازمان‌های مختلف در حال تلاش برای بهبود وضعیت هستند. چند نکته جالب:
            - مناطق شمالی تهران به طور کلی کیفیت هوای بهتری نسبت به مناطق مرکزی و جنوبی دارند.
            - در فصول پاییز و زمستان، کیفیت هوا به دلیل استفاده بیشتر از سوخت‌های فسیلی و شرایط جوی بدتر می‌شود.
            - پارک‌ها و فضاهای سبز نقش مهمی در کاهش آلودگی هوا دارند.
            اقدامات پیشنهادی:
            1. استفاده از وسایل نقلیه عمومی: این کمک می‌کند تا ترافیک و آلودگی کاهش یابد.
            2. استفاده از دوچرخه و پیاده‌روی: این نه تنها برای محیط زیست مفید است بلکه برای سلامتی شما نیز عالی است.
            3. حمایت از طرح‌های محیط زیستی و کاهش مصرف سوخت‌های فسیلی.
            یادآوری می‌کنم که روزهای آلوده، بهتر است از فعالیت‌های بیرون و به خصوص ورزش‌های سنگین خودداری کنید.
            در نهایت، باید بگوییم که کیفیت هوای تهران بهبود یافته ولی هنوز نیاز به تلاش‌های بیشتری داریم. به کمک هم می‌توانیم شهرمان را پاکتر کنیم!'''
            send_message(chat_id, interesting_info)
        else:
            send_message(chat_id, "دستور نامعتبر.")

def main():
    last_update_id = None
    
    # Sending initial notification to all users when the bot starts
    notification_message = '''مدارس تهران تعطیل شد'''
    send_notification_to_all_users(notification_message)
    
    while True:
        updates = get_updates(last_update_id)
        for update in updates:
            update_id = update['update_id']
            if update_id != last_update_id:
                message = update.get('message')
                if message:
                    chat_id = message['chat']['id']
                    text = message.get('text')
                    if text:
                        handle_message(chat_id, text)
                last_update_id = update_id

if __name__ == "__main__":
    main()

