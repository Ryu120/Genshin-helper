from pyrogram import filters
from pyrogram.types import InputMediaPhoto
import genshinstats as gs
import requests
from timi import bot as app

# Database to store user login information
user_accounts = {}

# Start command handler
@app.on_message(filters.command("help"))
def start_command(_, message):
    reply_text = "Welcome to Genshin helper Bot!\n\nYou can use the following commands:\n\n/login <account_id> <cookie_token> - Log in to your Genshin Impact account.\n/genshindaily - Get daily resin, commissions, and events.\n/character <character_name> - Get information about a character.\n/profile <your game id> <cooki token>"
    message.reply_text(reply_text)

# Login command handler
@app.on_message(filters.command("login"))
def login_command(_, message):
    # Get account ID and cookie token from the command
    account_id = message.command[1]
    cookie_token = message.command[2]

    # Save the login information
    user_accounts[message.from_user.id] = {"account_id": account_id, "cookie_token": cookie_token}

    message.reply_text("Successfully logged in to your Genshin Impact account.")

# Genshin daily command handler
@app.on_message(filters.command("genshindaily"))
def genshin_daily_command(client, message):
    # Get the user's login information
    user_id = message.from_user.id
    if user_id not in user_accounts:
        message.reply_text("You need to log in using /login command.")
        return

    account_id = user_accounts[user_id]["account_id"]
    cookie_token = user_accounts[user_id]["cookie_token"]

    # Set the account ID and cookie token
    gs.set_cookie(account_id=account_id, cookie_token=cookie_token)

    # Get daily resin, commissions, and events
    resin = gs.get_daily_resin()
    commissions = gs.get_daily_commissions()
    events = gs.get_current_events()

    # Generate the response message
    reply_text = f"Daily Resin: {resin}\n\nCommissions: {commissions}\n\nEvents: {events}"

    # Get the event image URL
    event_image_url = gs.get_event_image()

    # Send the response message and event image
    message.reply_text(reply_text)
    message.reply_photo(event_image_url)

# Character command handler
@app.on_message(filters.command("character"))
def character_command(client, message):
    # Get the user's login information
    user_id = message.from_user.id
    if user_id not in user_accounts:
        message.reply_text("You need to log in using /login command.")
        return

    account_id = user_accounts[user_id]["account_id"]
    cookie_token = user_accounts[user_id]["cookie_token"]

    # Set the account ID and cookie token
    gs.set_cookie(account_id=account_id, cookie_token=cookie_token)

    # Get the character name from the command
    character_name = " ".join(message.command[1:])

    # Get character information
    character_info = gs.get_character_info(character_name)

    if character_info:
        # Generate the response message
        reply_text = f"Character: {character_info['name']}\n\nElement: {character_info['element']}\n\nWeapon Type: {character_info['weapon']}\n\nRarity: {character_info['rarity']}"

        # Get the character image URL
        image_url = character_info["image"]

        
        message.reply_text(reply_text)
        message.reply_photo(image_url)
    else:
        reply_text = f"Character '{character_name}' not found."
        message.reply_text(reply_text)

app.run()
