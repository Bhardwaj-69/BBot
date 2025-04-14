from datetime import datetime, timedelta
import asyncio
import logging
from pyrogram import Client, filters, types

# लॉगिंग कॉन्फ़िगर करें
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_ID = 27392387
API_HASH = "37ee47c18c8be62716a27335a771e7da"
BOT_TOKEN = "7828770858:AAH78_btTyPNvRb6rESFKQT6Br0QT4Esh6w"
LOG_CHANNEL_ID = -1002479013444
GROUP_CHAT_ID = -1002661534796
REQUIRED_TAGS = ["@LarvaLinks"]
CHECK_INTERVAL = 60  # Check every 60 seconds
APPROVE_STICKER = "CAACAgUAAxkBAAKTlmfudEZKYYjP4l6XJZ5QRYWu00c3AAKwDwAC7osxVhzQOn1XTmwNHgQ"  # replace with your sticker id

app = Client("bio_check_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def check_bio(client: Client, message: types.ChatJoinRequest):
    try:
        user = await client.get_chat(message.from_user.id)
        bio = user.bio or ""

        if any(tag.lower() in bio.lower() for tag in REQUIRED_TAGS):
            await client.approve_chat_join_request(message.chat.id, message.from_user.id)

            approve_text = f"""
<b>🎃Ahhoyy! Pirate.🏴‍☠️ Access Granted!🌟</b>

<b>⚡️Welcome, <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>!🤞</b>

🔆You've been approved to join 🏝<b>{message.chat.title}</b>! We're thrilled to have you!🧿

⚠️ 💢❗️<b>Important!</b>❗️💢 ⚠️
❗️Removing the Required TAG❗️ from your Bio❗️ will result in Your ♨️REMOVE from the Channel♨️.

🤞Keep this tag in your bio to stay🌻 a verified member of <b>{message.chat.title}♻️</b>.

✨🏴‍☠️ <i>Supported by</i> <b>@LarvaLinks</b> ‍☠️
"""
            await send_messages(client, message.from_user.id, approve_text)
            await send_messages(client, LOG_CHANNEL_ID, approve_text)
        else:
            decline_text = f" 💢Access Denied❗️🚫 \n\n🤞Sorry, you don't meet the requirements🙄.\n\n 🌻Please Add this Tag in your Bio  : {', '.join(REQUIRED_TAGS)}.\n\n💥🏝after Ading in Bio again Send Join Req.🤞 your JoinReq. will Accept Instant⚡️⚡️\n\n 🏴‍☠️Send Req.💢https://t.me/+Ldp2BQ0BleQzMTA1 🔆"
            await client.decline_chat_join_request(message.chat.id, message.from_user.id)
            await send_messages(client, message.from_user.id, decline_text)

    except Exception as e:
        logging.error(f"❌ Error during bio check: {e}")

async def periodic_bio_check(client: Client):
    while True:
        try:
            async for member in client.get_chat_members(GROUP_CHAT_ID):
                if member.user and not member.user.is_bot:
                    user_id = member.user.id
                    try:
                        user = await client.get_chat(user_id)
                        bio = user.bio or ""
                        user = await client.get_users(user_id)
                        first_name = user.first_name
                        chat_id = user.id
                        if not any(tag.lower() in bio.lower() for tag in REQUIRED_TAGS):
                            kick_reason = f" 💢❗️💀You were REMOVED from ❤️‍🔥𝑴𝒐𝒗𝒊𝒆 𝑴𝒂𝒇𝒊𝒂💀 Group Because you Removed the TAG from your Bio💀."
                            try:
                                await client.ban_chat_member(GROUP_CHAT_ID, user_id, datetime.now() + timedelta(seconds=35))  # Kick ki jagah Ban use kiya
                                log_message = f"Haah!💀 User [{first_name}](tg://openmessage?user_id={chat_id}) kicked💥\n\n because they Removed the TAG⭕. \n\n🎃Reason:💢 {kick_reason}"
                                await send_messages(client, LOG_CHANNEL_ID, log_message)
                                await send_messages(client, user_id, kick_reason)
                            except Exception as kick_error:
                                logging.error(f"❌ Error kicking user {user_id}: {kick_error}")

                    except Exception as e:
                        logging.error(f"❌ Error checking bio for user {user_id}: {e}")

        except Exception as e:
            logging.error(f"❌ Error during periodic bio check: {e}")

        await asyncio.sleep(CHECK_INTERVAL)

async def send_messages(client, chat_id, text):
    try:
        await client.send_message(chat_id, text)
        await client.send_sticker(chat_id, APPROVE_STICKER)
    except Exception as e:
        logging.error(f"❌ Error sending messages to {chat_id}: {e}")

@app.on_chat_join_request()
async def handle_join_request(client: Client, message: types.ChatJoinRequest):
    await check_bio(client, message)

@app.on_message(filters.command("start"))
async def start(client: Client, message: types.Message):
    try:
        await message.reply_text(
            " 💢💀Ahhoyy! Pirate⚓️🏴‍☠️\n\n 🔆Just add @LarvaLinks this Tag in Your Bio and Send Join Req.🌻.\n\n 💢Dont Remove Tag From Bio You Will be Kicked From Grp within 60 Sec.\n\n 🏝Send Join Req.🌻 https://t.me/+Ldp2BQ0BleQzMTA1 ✨"
        )
    except Exception as e:
        logging.error(f"❌ Error sending /start message: {e}")

async def main():
    async with app:
        logging.info("Bot started!")
        await asyncio.gather(periodic_bio_check(app))

if __name__ == "__main__":
    app.run(main())