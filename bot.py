import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import os

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# ================= DATA =================

first_names = [
    "Leon","Aiden","Kai","Noah","Ethan","Luna","Aria","Mika",
    "Sora","Elena","Rin","Akira","Yuki","Alya","Rei","Haru"
]

last_names = [
    "Sullivan","Hart","Raven","Mori","Kuroda",
    "Hayes","Aldrich","Valkyr","Winter","Blackwood"
]

countries = [
    "Jepang","Korea Selatan","Kanada","Inggris",
    "Prancis","Jerman","Italia","Australia"
]

mbti = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

jobs = [
    "Programmer","CEO","Streamer","Racer",
    "Model","Dokter","Mahasiswa",
    "Musisi","Hacker","Influencer"
]

races = [
    "Human","Elf","Dark Elf",
    "Dragonborn","Demon",
    "Angel","Vampire","Werewolf"
]

classes = [
    "Knight","Mage","Assassin",
    "Paladin","Necromancer",
    "Ranger","Berserker","Alchemist"
]

hobbies = [
    "Balapan malam",
    "Fotografi",
    "Bermain gitar",
    "Membaca novel",
    "Traveling",
    "Gaming",
    "Ngopi",
    "Menulis jurnal"
]

habits = [
    "Sering begadang",
    "Minum kopi setiap pagi",
    "Mendengarkan musik saat hujan",
    "Mengoleksi jam tangan",
    "Berolahraga setiap hari",
    "Menyendiri saat stres"
]

relationship = [
    "Single",
    "In Relationship",
    "Situationship",
    "Complicated"
]

zodiacs = [
    "Aries","Taurus","Gemini","Cancer",
    "Leo","Virgo","Libra","Scorpio",
    "Sagittarius","Capricorn","Aquarius","Pisces"
]

# Simpan karakter terakhir user
user_data = {}

# ================= FUNCTION =================

def avatar_url():
    gender = random.choice(["boy", "girl"])
    return f"https://avatar.iran.liara.run/public/{gender}"

def generate_character():

    name = f"{random.choice(first_names)} {random.choice(last_names)}"

    age = random.randint(18, 35)
    height = random.randint(155, 195)

    stats = {
        "STR": random.randint(1,100),
        "AGI": random.randint(1,100),
        "INT": random.randint(1,100),
        "VIT": random.randint(1,100),
        "DEX": random.randint(1,100),
        "LUK": random.randint(1,100)
    }

    lore = f"""
{name} berasal dari {random.choice(countries)} dan dikenal sebagai sosok yang penuh ambisi.

Sejak kecil ia memiliki ketertarikan besar terhadap petualangan dan tantangan yang membuatnya terus berkembang.

Dalam kehidupannya, ia memilih jalan sebagai {random.choice(jobs)} sekaligus memiliki kemampuan unik sebagai {random.choice(classes)}.

Meski terlihat tenang, banyak orang tidak mengetahui perjuangan panjang yang pernah ia lalui.

Kini ia terus mengejar mimpinya sambil menulis kisah hidup yang suatu hari akan dikenang banyak orang.
"""

    data = {
        "name": name,
        "age": age,
        "height": height,
        "mbti": random.choice(mbti),
        "zodiac": random.choice(zodiacs),
        "country": random.choice(countries),
        "relationship": random.choice(relationship),
        "job": random.choice(jobs),
        "race": random.choice(races),
        "class": random.choice(classes),
        "hobby": random.choice(hobbies),
        "habit": random.choice(habits),
        "stats": stats,
        "lore": lore
    }

    return data

def format_character(data):

    return f"""
🎭 KARAKTER BARU

👤 Nama: {data['name']}
🎂 Umur: {data['age']} Tahun
📏 Tinggi: {data['height']} cm

❤️ MBTI: {data['mbti']}
♈ Zodiac: {data['zodiac']}

🌍 Negara: {data['country']}
💍 Status: {data['relationship']}

💼 Pekerjaan: {data['job']}

🧬 Ras: {data['race']}
⚔ Class: {data['class']}

🎮 Hobi: {data['hobby']}
🚬 Kebiasaan: {data['habit']}

📊 RPG STATS

STR: {data['stats']['STR']}
AGI: {data['stats']['AGI']}
INT: {data['stats']['INT']}
VIT: {data['stats']['VIT']}
DEX: {data['stats']['DEX']}
LUK: {data['stats']['LUK']}

📖 LORE

{data['lore']}
"""

def keyboard():
    kb = InlineKeyboardMarkup()

    kb.row(
        InlineKeyboardButton("🎲 Generate Lagi", callback_data="generate")
    )

    kb.row(
        InlineKeyboardButton("📄 TXT", callback_data="txt"),
        InlineKeyboardButton("📕 PDF", callback_data="pdf")
    )

    return kb

# ================= COMMAND =================

@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        """
🎭 KarakterBot

Perintah:

/karakter - Buat karakter baru
/help - Bantuan
"""
    )

@bot.message_handler(commands=['help'])
def help_cmd(message):

    bot.reply_to(
        message,
        "Gunakan /karakter untuk membuat karakter RP."
    )

@bot.message_handler(commands=['karakter'])
def karakter(message):

    data = generate_character()

    user_data[message.from_user.id] = data

    text = format_character(data)

    try:
        bot.send_photo(
            message.chat.id,
            avatar_url(),
            caption=text[:1024],
            reply_markup=keyboard()
        )
    except:
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=keyboard()
        )

# ================= CALLBACK =================

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    uid = call.from_user.id

    if call.data == "generate":

        data = generate_character()
        user_data[uid] = data

        bot.send_message(
            call.message.chat.id,
            format_character(data),
            reply_markup=keyboard()
        )

    elif call.data == "txt":

        if uid not in user_data:
            return

        filename = f"{uid}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(format_character(user_data[uid]))

        with open(filename, "rb") as f:
            bot.send_document(
                call.message.chat.id,
                f
            )

        os.remove(filename)

    elif call.data == "pdf":

        if uid not in user_data:
            return

        filename = f"{uid}.pdf"

        doc = SimpleDocTemplate(filename)

        styles = getSampleStyleSheet()

        story = [
            Paragraph(
                format_character(user_data[uid]).replace("\n","<br/>"),
                styles["BodyText"]
            )
        ]

        doc.build(story)

        with open(filename, "rb") as f:
            bot.send_document(
                call.message.chat.id,
                f
            )

        os.remove(filename)

print("Bot aktif...")

bot.infinity_polling(skip_pending=True)
