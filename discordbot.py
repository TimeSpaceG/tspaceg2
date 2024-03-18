import os

import discord
from discord.ext import commands

# 봇 설정
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
PREFIX = os.environ.get('PREFIX', '!')

# 모든 Intents를 활성화하여 봇을 초기화합니다.
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# 이하 봇의 코드를 계속 작성합니다.

warnings = {}  # 사용자에 대한 경고를 저장하기 위한 딕셔너리, {사용자 아이디: 경고 횟수}
kick_reasons = {}  # 사용자에 대한 추방 이유를 저장하기 위한 딕셔너리, {사용자 아이디: 이유}


# 봇이 준비되었을 때 실행할 코드
@bot.event
async def on_ready():
    print(f'{bot.user}이(가) 성공적으로 로그인했습니다.')


# 사용자의 상태가 변할 때 실행할 코드
@bot.event
async def on_member_update(before, after):
    # 사용자가 오프라인에서 온라인으로 변경되었을 때
    if before.status == discord.Status.offline and after.status == discord.Status.online:
        user_id = after.id
        if user_id in warnings:
            warnings[user_id] += 1
        else:
            warnings[user_id] = 1
        await check_warnings(after)


# 사용자를 추방하는 함수
async def kick_user(user, reason):
    await user.kick(reason=reason)


# 사용자에게 경고를 보내는 함수
async def warn_user(user):
    await user.send("경고를 받았습니다.")


# 경고 횟수를 확인하고 3회 이상이면 사용자를 추방하는 함수
async def check_warnings(user):
    user_id = user.id
    if user_id in warnings and warnings[user_id] >= 3:
        kick_reason = kick_reasons.get(user_id, "경고 3회 누적")
        await kick_user(user, kick_reason)
    else:
        await warn_user(user)


# 추방 이유를 저장하는 함수
def record_kick_reason(user_id, reason):
    kick_reasons[user_id] = reason


# 관리자에게 메시지를 보내는 예시 명령어
@bot.command(name='send_message_to_admin')
async def send_message_to_admin(ctx, *, message):
    # 관리자의 ID
    admin_id = 610708164572086284  # 여기에 관리자의 ID를 입력합니다.

    # 관리자에게 메시지를 보냅니다.
    admin = bot.get_user(admin_id)
    if not admin:
        await ctx.send("관리자를 찾을 수 없습니다.")
    else:
        await admin.send(message)
        await ctx.send("메시지를 관리자에게 전송했습니다.")


# 봇 실행
bot.run(TOKEN)
