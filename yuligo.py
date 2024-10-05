import logging
import aiohttp
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Inisialisasi bot token dan log level
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'

# Logging untuk melihat informasi bot saat berjalan
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Fungsi untuk melakukan permintaan ke API Yuliverse secara asinkron
async def fetch_api(session, url, token=None):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0 Mobile Safari/537.36"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    async with session.get(url, headers=headers) as response:
        if response.status in (200, 201):
            return await response.json()
        else:
            return {"error": f"API request failed with status: {response.status}"}

# Command untuk menampilkan misi
async def missions(update: Update, context):
    async with aiohttp.ClientSession() as session:
        url = "https://yuligo.yuliverse.io/api/g/v1/missions?query_id=0"
        data = await fetch_api(session, url)

        if "error" in data:
            await update.message.reply_text(f"Error: {data['error']}")
        else:
            missions = data.get("missions", [])
            if missions:
                message = "Missions Available:\n" + "\n".join([mission.get('title', 'Unknown') for mission in missions])
            else:
                message = "No missions available."
            await update.message.reply_text(message)

# Command untuk menampilkan role
async def roles(update: Update, context):
    async with aiohttp.ClientSession() as session:
        url = "https://yuligo.yuliverse.io/api/g/v1/roles"
        data = await fetch_api(session, url)

        if "error" in data:
            await update.message.reply_text(f"Error: {data['error']}")
        else:
            roles = data.get("roles", [])
            if roles:
                message = "Roles Available:\n" + "\n".join([role.get('name', 'Unknown') for role in roles])
            else:
                message = "No roles available."
            await update.message.reply_text(message)

# Command untuk melihat profile
async def profile(update: Update, context):
    async with aiohttp.ClientSession() as session:
        url = "https://yuligo.yuliverse.io/api/g/v1/profile"
        data = await fetch_api(session, url)

        if "error" in data:
            await update.message.reply_text(f"Error: {data['error']}")
        else:
            user_profile = data.get('profile', {})
            if user_profile:
                message = f"Profile:\nUsername: {user_profile.get('username', 'Unknown')}\nLevel: {user_profile.get('level', 'Unknown')}\nXP: {user_profile.get('xp', 0)}"
            else:
                message = "Profile not found."
            await update.message.reply_text(message)

# Command untuk mengundang user
async def invite(update: Update, context):
    async with aiohttp.ClientSession() as session:
        url = "https://yuligo.yuliverse.io/api/g/v1/invite"
        invite_data = {
            "inviteCode": "INVITE_CODE_HERE",  # Ganti dengan kode undangan
            "email": "email@example.com"       # Ganti dengan email yang valid
        }
        async with session.post(url, json=invite_data) as response:
            if response.status in (200, 201):
                data = await response.json()
                message = f"Invitation sent successfully! Status: {data.get('status', 'Unknown')}"
            else:
                message = f"Failed to send invitation. Status: {response.status}"
            await update.message.reply_text(message)

# Command handler untuk /start
async def start(update: Update, context):
    await update.message.reply_text('Hello! I am @YuliGoBot. Here are the commands you can use:\n/missions - List available missions\n/roles - List available roles\n/profile - View user profile\n/invite - Invite a user')

# Fungsi utama untuk menjalankan bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Daftar command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("missions", missions))
    application.add_handler(CommandHandler("roles", roles))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("invite", invite))

    # Jalankan bot
    application.run_polling()

if __name__ == "__main__":
    main()
