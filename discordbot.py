import discord
from discord.ext import commands
import youtube_dl
import os

# 봇 설정
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
PREFIX = os.environ.get('PREFIX', '!')  # PREFIX 환경 변수를 가져오고, 없으면 기본값 '!'을 사용합니다.

intents = discord.Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# 봇이 준비되었을 때 실행할 코드
@bot.event
async def on_ready():
    print(f'{bot.user}이(가) 성공적으로 로그인했습니다.')

# "안녕하세요" 명령어 처리
@bot.command(name='정애니맨안녕')
async def say_hello(ctx):
    await ctx.send('안녕하세요! 정애니맨님')

# 음성 채널 지원: 음성 채널 입장
@bot.command(name='들어와')
async def join_voice(ctx):
    channel = ctx.author.voice.channel
    if channel:
        await channel.connect()
    else:
        await ctx.send("음성 채널에 먼저 들어가주세요.")

# 음악 재생
@bot.command(name='재생')
async def play(ctx, url):
    # 봇이 음성 채널에 없으면 입장
    if not ctx.voice_client:
        channel = ctx.author.voice.channel
        await channel.connect()

    # YouTube 영상 다운로드 및 재생
    voice_client = ctx.voice_client
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('재생 완료', e))

# 봇 실행
bot.run(TOKEN)
