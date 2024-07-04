import discord
from discord.ext import commands
from discord.ui import Button, View
import json
import random
from typing import Dict, List, Set, Union, Optional
import math

# 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
DDRAGON_VERSION = "14.13.1"  # 최신 버전으로 업데이트하세요
DDRAGON_BASE_URL = f"http://ddragon.leagueoflegends.com/cdn/{DDRAGON_VERSION}"

# 챔피언 이름 한글 번역 딕셔너리
champion_translations: Dict[str, str] = {

    "Aatrox": "아트록스", "Ahri": "아리", "Akali": "아칼리", "Akshan": "아크샨", "Alistar": "알리스타",
    "Amumu": "아무무", "Anivia": "애니비아", "Annie": "애니", "Aphelios": "아펠리오스", "Ashe": "애쉬",
    "AurelionSol": "아우렐리온 솔", "Azir": "아지르", "Bard": "바드", "Belveth": "벨베스", "Blitzcrank": "블리츠크랭크",
    "Brand": "브랜드", "Braum": "브라움", "Briar": "브라이어", "Caitlyn": "케이틀린", "Camille": "카밀",
    "Cassiopeia": "카시오페아", "Chogath": "초가스", "Corki": "코르키", "Darius": "다리우스", "Diana": "다이애나",
    "Draven": "드레이븐", "DrMundo": "문도 박사", "Ekko": "에코", "Elise": "엘리스", "Evelynn": "이블린",
    "Ezreal": "이즈리얼", "Fiddlesticks": "피들스틱", "Fiora": "피오라", "Fizz": "피즈", "Galio": "갈리오",
    "Gangplank": "갱플랭크", "Garen": "가렌", "Gnar": "나르", "Gragas": "그라가스", "Graves": "그레이브즈",
    "Gwen": "그웬", "Hecarim": "헤카림", "Heimerdinger": "하이머딩거", "Hwei": "흐웨이", "Illaoi": "일라오이",
    "Irelia": "이렐리아", "Ivern": "아이번", "Janna": "잔나", "JarvanIV": "자르반 4세", "Jax": "잭스",
    "Jayce": "제이스", "Jhin": "진", "Jinx": "징크스", "Kaisa": "카이사", "Kalista": "칼리스타",
    "Karma": "카르마", "Karthus": "카서스", "Kassadin": "카사딘", "Katarina": "카타리나", "Kayle": "케일",
    "Kayn": "케인", "Kennen": "케넨", "Khazix": "카직스", "Kindred": "킨드레드", "Kled": "클레드",
    "KogMaw": "코그모", "KSante": "크산테", "Leblanc": "르블랑", "LeeSin": "리 신", "Leona": "레오나",
    "Lillia": "릴리아", "Lissandra": "리산드라", "Lucian": "루시안", "Lulu": "룰루", "Lux": "럭스",
    "Malphite": "말파이트", "Malzahar": "말자하", "Maokai": "마오카이", "MasterYi": "마스터 이", "Milio": "밀리오",
    "MissFortune": "미스 포츈", "MonkeyKing": "오공", "Mordekaiser": "모데카이저", "Morgana": "모르가나",
    "Naafiri": "나피리", "Nami": "나미", "Nasus": "나서스", "Nautilus": "노틸러스", "Neeko": "니코",
    "Nidalee": "니달리", "Nilah": "닐라", "Nocturne": "녹턴", "Nunu": "누누와 윌럼프", "Olaf": "올라프",
    "Orianna": "오리아나", "Ornn": "오른", "Pantheon": "판테온", "Poppy": "뽀삐", "Pyke": "파이크",
    "Qiyana": "키아나", "Quinn": "퀸", "Rakan": "라칸", "Rammus": "람머스", "RekSai": "렉사이",
    "Rell": "렐", "Renata": "레나타 글라스크", "Renekton": "레넥톤", "Rengar": "렝가", "Riven": "리븐",
    "Rumble": "럼블", "Ryze": "라이즈", "Samira": "사미라", "Sejuani": "세주아니", "Senna": "세나",
    "Seraphine": "세라핀", "Sett": "세트", "Shaco": "샤코", "Shen": "쉔", "Shyvana": "쉬바나",
    "Singed": "신지드", "Sion": "사이온", "Sivir": "시비르", "Skarner": "스카너", "Smolder": "스몰더",
    "Sona": "소나", "Soraka": "소라카", "Swain": "스웨인", "Sylas": "사일러스", "Syndra": "신드라",
    "TahmKench": "탐 켄치", "Taliyah": "탈리야", "Talon": "탈론", "Taric": "타릭", "Teemo": "티모",
    "Thresh": "쓰레쉬", "Tristana": "트리스타나", "Trundle": "트런들", "Tryndamere": "트린다미어",
    "TwistedFate": "트위스티드 페이트", "Twitch": "트위치", "Udyr": "우디르", "Urgot": "우르곳", "Varus": "바루스",
    "Vayne": "베인", "Veigar": "베이가", "Velkoz": "벨코즈", "Vex": "벡스", "Vi": "바이",
    "Viego": "비에고", "Viktor": "빅토르", "Vladimir": "블라디미르", "Volibear": "볼리베어", "Warwick": "워윅",
    "Xayah": "자야", "Xerath": "제라스", "XinZhao": "신 짜오", "Yasuo": "야스오", "Yone": "요네",
    "Yorick": "요릭", "Yuumi": "유미", "Zac": "자크", "Zed": "제드", "Zeri": "제리",
    "Ziggs": "직스", "Zilean": "질리언", "Zoe": "조이", "Zyra": "자이라"
}

# 챔피언 목록 로드
def load_champions() -> Dict[str, str]:
    file_path = 'champion.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lol_data = json.load(file)
        champions = {champ_id: champion_translations.get(champ_id, champ_id) for champ_id in lol_data['data'].keys()}
        print(f"Loaded {len(champions)} champions")
        return champions
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error loading champions: {e}")
        return champion_translations

champions = load_champions()


# 새로운 함수: 챔피언 목록을 표 형식으로 변환
def champions_to_table(champions_list: List[str], columns: int = 5) -> str:
    # 열 너비 계산 (가장 긴 챔피언 이름 + 2 for padding)
    col_width = max(len(name) for name in champions_list) + 2

    # 행 수 계산
    rows = math.ceil(len(champions_list) / columns)

    table = "```\n"
    for i in range(rows):
        for j in range(columns):
            index = i + j * rows
            if index < len(champions_list):
                table += f"{champions_list[index]:{col_width}}"
            else:
                table += " " * col_width
        table += "\n"
    table += "```"
    return table


class TeamDraft:
    def __init__(self, all_champions: Dict[str, str]):
        self.all_champions: List[str] = list(all_champions.values())
        self.blue_team: List[str] = []
        self.red_team: List[str] = []
        self.selected_champions: Set[str] = set()
        self.blue_redraw_used: bool = False
        self.red_redraw_used: bool = False

    def initial_draft(self) -> None:
        available_champions = list(set(self.all_champions) - self.selected_champions)
        selected = random.sample(available_champions, min(30, len(available_champions)))
        self.blue_team = selected[:15]
        self.red_team = selected[15:]
        self.selected_champions.update(selected)

    def redraw_champion(self, team: str) -> Union[str, discord.Embed]:
        if (team == "blue" and self.blue_redraw_used) or (team == "red" and self.red_redraw_used):
            return "이미 리드로우를 사용했습니다."

        available_champions = list(set(self.all_champions) - self.selected_champions)
        if not available_champions:
            return "더 이상 선택할 수 있는 챔피언이 없습니다."

        new_champion = random.choice(available_champions)
        if team == "blue":
            self.blue_team.append(new_champion)
            self.blue_redraw_used = True
        else:
            self.red_team.append(new_champion)
            self.red_redraw_used = True

        self.selected_champions.add(new_champion)

        embed = self.get_team_embed()
        champ_id = next((k for k, v in champion_translations.items() if v == new_champion), None)
        if champ_id:
            icon_url = f"{DDRAGON_BASE_URL}/img/champion/{champ_id}.png"
            embed.set_thumbnail(url=icon_url)
            footer_text = f"{team.capitalize()} 팀에 새로 추가된 챔피언: {new_champion} [<:champion:{icon_url}>]()"
        else:
            footer_text = f"{team.capitalize()} 팀에 새로 추가된 챔피언: {new_champion}"

        embed.set_footer(text=footer_text)

        return embed

    def get_team_embed(self) -> discord.Embed:
        embed = discord.Embed(title="팀 드래프트 결과 :tada:", color=discord.Color.blue())

        for team, team_name, emoji in [(self.blue_team, "블루 팀", "🔵"), (self.red_team, "레드 팀", "🔴")]:
            team_out = ""
            for i, champ in enumerate(team, 1):
                champ_id = next((k for k, v in champion_translations.items() if v == champ), None)
                if champ_id:
                    icon_url = f"{DDRAGON_BASE_URL}/img/champion/{champ_id}.png"
                    team_out += f"{i}. {champ} [<:champion:{icon_url}>]()\n"
                else:
                    team_out += f"{i}. {champ}\n"
            embed.add_field(name=f"{emoji} {team_name}", value=team_out, inline=True)

        return embed


# 각 서버별로 TeamDraft 인스턴스를 저장할 딕셔너리
server_drafts: Dict[int, TeamDraft] = {}

class TeamDraftView(View):
    def __init__(self, draft: TeamDraft):
        super().__init__()
        self.draft = draft

    @discord.ui.button(label="레드팀 리드로우", style=discord.ButtonStyle.red)
    async def red_redraw(self, interaction: discord.Interaction, button: Button):
        result = self.draft.redraw_champion("red")
        if isinstance(result, str):
            await interaction.response.send_message(result, ephemeral=True)
        else:
            embed = self.draft.get_team_embed()
            embed.set_footer(text=f"레드팀에 새로 추가된 챔피언: {result}")
            await interaction.response.send_message(embed=embed)
        self.check_and_disable_buttons()

    @discord.ui.button(label="블루팀 리드로우", style=discord.ButtonStyle.blurple)
    async def blue_redraw(self, interaction: discord.Interaction, button: Button):
        result = self.draft.redraw_champion("blue")
        if isinstance(result, str):
            await interaction.response.send_message(result, ephemeral=True)
        else:
            embed = self.draft.get_team_embed()
            embed.set_footer(text=f"블루팀에 새로 추가된 챔피언: {result}")
            await interaction.response.send_message(embed=embed)
        self.check_and_disable_buttons()

    def check_and_disable_buttons(self):
        if self.draft.red_redraw_used:
            self.red_redraw.disabled = True
        if self.draft.blue_redraw_used:
            self.blue_redraw.disabled = True

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='champions')
async def list_champions(ctx):
    """챔피언 목록을 표시합니다."""
    champion_list = ', '.join(champions.values())
    await ctx.send(f"챔피언 목록:\n{champion_list}")

@bot.command(name='random')
async def random_champion(ctx):
    """랜덤 챔피언을 선택합니다."""
    champion = random.choice(list(champions.values()))
    await ctx.send(f"랜덤 챔피언: {champion}")

@bot.command(name='teamdraft')
async def team_draft_command(ctx):
    """30개의 챔피언을 뽑아 레드팀과 블루팀에 15개씩 랜덤 분배합니다."""
    if len(champions) < 30:
        await ctx.send("Error: 챔피언 풀이 30개 미만입니다.")
        return

    draft = TeamDraft(champions)
    draft.initial_draft()
    server_drafts[ctx.guild.id] = draft

    embed = draft.get_team_embed()
    view = TeamDraftView(draft)
    await ctx.send(embed=embed, view=view)

@bot.command(name='translate')
async def translate_champion(ctx, *, champion_name):
    """챔피언의 영문 이름을 입력하면 한글 이름을 알려줍니다."""
    champion_name = champion_name.capitalize()
    if champion_name in champions:
        await ctx.send(f"{champion_name}의 한글 이름은 {champions[champion_name]}입니다.")
    else:
        await ctx.send(f"'{champion_name}'은(는) 챔피언 목록에 없습니다.")

# 여기에 봇 토큰을 입력하세요
bot.run('DISCORD_API_KEY')