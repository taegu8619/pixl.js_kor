# download latest amiibo data and merge to amiibo_data.csv


from urllib.request import urlopen
import json
import os
import csv

# --- 한글 번역 데이터 추가 시작 ---
amiibo_translation = {
    "Mario": "마리오", "Luigi": "루이지", "Peach": "피치공주", "Bowser": "쿠파", "Dr. Mario": "닥터 마리오",
    "Rosalina": "로젤리나", "Bowser Jr.": "쿠파주니어", "Wario": "와리오", "Yoshi": "요시", "Donkey Kong": "동키콩",
    "Diddy Kong": "디디콩", "Link": "링크", "Zelda": "젤다", "Sheik": "시크", "Ganondorf": "가논돌프",
    "Toon Link": "툰링크", "Samus": "사무스", "Zero Suit Samus": "제로 슈트 사무스", "Pit": "피트", "Palutena": "파르테나",
    "Dark Pit": "블랙피트", "Marth": "마르스", "Ike": "아이크", "Robin": "러플레", "Lucina": "루키나",
    "Roy": "로이", "Kirby": "커비", "King Dedede": "디디디 대왕", "Meta Knight": "메타 나이트", "Fox": "폭스",
    "Falco": "팔코", "Pikachu": "피카츄", "Charizard": "리자몽", "Lucario": "루카리오", "Jigglypuff": "푸린",
    "Greninja": "개굴닌자", "Duck Hunt": "덕헌트", "R.O.B.": "R.O.B.", "Mr. Game & Watch": "Mr. 게임&워치",
    "Ness": "네스", "Captain Falcon": "캡틴 팔콘", "Villager": "마을 주민", "Olimar": "올리마",
    "Wii Fit Trainer": "Wii Fit 트레이너", "Shulk": "슈르크", "Pac-Man": "팩맨", "Mega Man": "록맨", "Sonic": "소닉",
    "Mewtwo": "뮤츠", "Ryu": "류", "Cloud": "클라우드", "Corrin": "카무이", "Bayonetta": "베요네타",
    "Inkling Girl": "잉클링 걸", "Inkling Boy": "잉클링 보이", "Inkling Squid": "잉클링 스퀴드", "Isabelle": "여울",
    "Tom Nook": "너굴", "K.K.": "K.K.", "Mabel": "고순이", "Reese": "리사", "Cyrus": "리포", "Lottie": "솜이",

    # 추가된 아미보들
    "Wolf Link": "울프 링크", "Guardian": "가디언", "Bokoblin": "보코블린", "Zelda (BotW)": "젤다 (브레스 오브 더 와일드)",
    "Link (Archer)": "링크 (활)", "Link (Rider)": "링크 (라이더)", "Daruk": "다르케르", "Mipha": "미파", "Revali": "리발",
    "Urbosa": "우르보사", "Squid Sisters": "시오카라즈", "Callie": "아오리", "Marie": "호타루", "Pearl": "히메",
    "Marina": "이이다", "Octoling Girl": "옥토링 걸", "Octoling Boy": "옥토링 보이", "Octoling Octopus": "옥토링 옥토퍼스",
    "Celeste": "부옥", "Blathers": "부엉", "Kicks": "패트릭", "Rover": "낯선고양이", "Timmy & Tommy": "콩돌이 & 밤돌이",
    "Celica": "세리카", "Alm": "아름", "Tiki": "치키", "Chrom": "크롬", "Goomba": "굼바", "Koopa Troopa": "엉금엉금",
    "Boo": "부끄부끄", "Daisy": "데이지", "Waluigi": "와루이지", "Poochy": "포치", "Wedding Mario": "웨딩 마리오",
    "Wedding Peach": "웨딩 피치", "Wedding Bowser": "웨딩 쿠파", "Metroid": "메트로이드", "Samus Aran": "사무스 아란",
    "Pikmin": "피크민", "Detective Pikachu": "명탐정 피카츄", "Solaire of Astora": "태양의 전사 솔라",
    "Loot Goblin": "보물 고블린", "Shovel Knight": "삽질 기사", "Plague Knight": "역병 기사", "Specter Knight": "스펙터 기사",
    "King Knight": "킹 기사", "Gold Shovel Knight": "골드 삽질 기사", "Ken": "켄", "Young Link": "소년 링크",
    "Snake": "스네이크", "Pokemon Trainer": "포켓몬 트레이너", "Squirtle": "꼬부기", "Ivysaur": "이상해풀",
    "Simon": "시몬", "Richter": "릭터", "King K. Rool": "킹크루루", "Piranha Plant": "뻐끔플라워", "Joker": "조커",
    "Hero": "용사", "Banjo & Kazooie": "반조 & 카주이", "Terry": "테리", "Byleth": "벨레트",
    "Min Min": "미엔미엔", "Steve": "스티브", "Alex": "알렉스", "Sephiroth": "세피로스", "Pyra": "호무라",
    "Mythra": "히카리", "Kazuya": "카즈야", "Sora": "소라", "Magnamalo": "마가이마가도", "Palamute": "동반자 가루크",
    "Palico": "동반자 아이루", "Tsukino": "츠키노", "Ena": "에나", "Razewing Ratha": "파멸의 날개 레우스",
    "Link (Majora's Mask)": "링크 (무쥬라의 가면)", "Link (Skyward Sword)": "링크 (스카이워드 소드)",
    "Link (Twilight Princess)": "링크 (황혼의 공주)", "8-Bit Link": "8비트 링크", "Link (Ocarina of Time)": "링크 (시간의 오카리나)",
    "Cat Mario": "고양이마리오", "Cat Peach": "고양이피치", "Loftwing & Zelda": "로프트버드 & 젤다",
    "E.M.M.I.": "E.M.M.I.", "Samus (Metroid Dread)": "사무스 (메트로이드 드레드)", "Isabelle (Winter Outfit)": "여울 (겨울옷)",
    "Digby": "켄트"
}

gameseries_translation = {
    "Super Mario": "슈퍼 마리오", "The Legend of Zelda": "젤다의 전설", "Super Smash Bros.": "슈퍼 스매시브라더스",
    "Yoshi's Woolly World": "요시 울리 월드", "Animal Crossing": "동물의 숲", "Splatoon": "스플래툰",
    "Kirby": "별의 커비", "Fire Emblem": "파이어 엠블렘", "Star Fox": "스타폭스", "Pokemon": "포켓몬",
    "Metroid": "메트로이드", "Kid Icarus": "키드 이카루스", "Pikmin": "피크민", "Wii Fit": "Wii Fit",
    "Xenoblade Chronicles": "제노블레이드 크로니클스", "Pac-Man": "팩맨", "Mega Man": "록맨", "Sonic the Hedgehog": "소닉 더 헤지혹",
    "Street Fighter": "스트리트 파이터", "Final Fantasy": "파이널 판타지", "Bayonetta": "베요네타",
    "Chibi-Robo!": "작은 로보!", "Shovel Knight": "삽질 기사", "Dark Souls": "다크 소울", "Diablo": "디아블로",
    "Skylanders": "스카이랜더스", "Monster Hunter": "몬스터 헌터", "BoxBoy!": "BOXBOY!", "Castlevania": "캐슬바니아",
    "Metal Gear Solid": "메탈 기어 솔리드", "Dragon Quest": "드래곤 퀘스트", "Banjo-Kazooie": "반조-카주이",
    "Fatal Fury": "아랑전설", "ARMS": "ARMS", "Minecraft": "마인크래프트", "Kingdom Hearts": "킹덤 하츠",
    "Monster Hunter Rise": "몬스터 헌터 라이즈", "Monster Hunter Stories": "몬스터 헌터 스토리즈"
}
# --- 한글 번역 데이터 추가 끝 ---

class Amiibo:
    def __init__(self):
        self.id = None
        self.name_en = None
        self.name_cn = None

class Game:
    def __init__(self):
        self.id = None
        self.parent_id = None
        self.name_en = None
        self.name_cn = None
        self.order = None

class Link:
    def __init__(self):
        self.game_id = None
        self.amiibo_id = None
        self.note_en = None
        self.note_cn = None
        self.note_it = None



def get_prorject_directory():
    return os.path.abspath(os.path.dirname(__file__)+"/../")


def fetch_amiibo_from_api():
    conn = urlopen("https://www.amiiboapi.com/api/amiibo/")
    body = json.loads(conn.read())
    amiibos = list()
    for ami in body["amiibo"]: 
        amiibo = Amiibo()
        amiibo.id = ami["head"] + ami["tail"]
        amiibo.name_en = ami["name"]
        amiibos.append(amiibo)
    return amiibos


def read_amiibo_from_csv():
    csv_file = get_prorject_directory() + "/data/amiidb_amiibo.csv"
    if not os.path.exists(csv_file):
        return list()
    amiibos = list()
    with open(csv_file, "r", encoding="utf8") as f:
        for r in csv.reader(f):
            amiibo = Amiibo()
            amiibo.id = r[0]
            amiibo.name_en = r[1]
            amiibo.name_cn = r[2]
            amiibos.append(amiibo)
    
    return amiibos


def write_amiibo_to_csv(amiibos):
    csv_file = get_prorject_directory() + "/data/amiidb_amiibo.csv"
    with open(csv_file, "w", encoding="utf8", newline="") as f:
        w = csv.writer(f)
        for amiibo in amiibos:
            r = list()
            r.append(amiibo.id)
            r.append(amiibo.name_en)
            r.append(amiibo.name_cn)
            w.writerow(r)


def merge_amiibo(amiibos_csv, amiibos_api):
    amiibos_merged = dict()
    for amiibo in amiibos_csv:
        amiibos_merged[amiibo.id] = amiibo

    for amiibo in amiibos_api:
        if amiibos_merged.get(amiibo.id) == None:
            amiibos_merged[amiibo.id] = amiibo
            print("Found new amiibo: [%s] %s " % (amiibo.id, amiibo.name_en))
    amiibos = list()
    for k in amiibos_merged:
        amiibos.append(amiibos_merged[k])
    return amiibos

def gen_amiibo_data_c_file(amiibos):
    c_file = get_prorject_directory() + "/application/src/amiidb/db_amiibo.c"
    with open(c_file, "w+", newline="\n", encoding="utf8") as f:
        f.write('/* This file is auto-generated by amiibo_db_gen.py. Do not edit directly. */\n')  
        f.write('#include "db_header.h"\n')
        f.write('const db_amiibo_t amiibo_list[] = {\n')
        for amiibo in amiibos:
            # --- 번역 코드 추가 ---
            korean_name = amiibo_translation.get(amiibo.name_en, amiibo.name_en)
            # --- 번역 코드 추가 끝 ---
            f.write('{0x%s, 0x%s, "%s", "%s"}, \n' % 
                    (amiibo.id[0:8], amiibo.id[8:16], korean_name, 
                    amiibo.name_cn)) 
        f.write("{0, 0, 0, 0}\n")
        f.write("};\n")


def read_games_from_csv():
    csv_file = get_prorject_directory() + "/data/amiidb_game.csv"
    if not os.path.exists(csv_file):
        return list()
    games = list()
    with open(csv_file, "r", encoding="utf8") as f:
        for r in csv.reader(f):
            game = Game()
            game.id = r[0]
            game.parent_id = r[1]
            game.name_en = r[2]
            game.name_cn = r[3] 
            game.order = r[4]
            games.append(game)
    return games


def read_link_from_csv():
    csv_file = get_prorject_directory() + "/data/amiidb_link.csv"
    if not os.path.exists(csv_file):
        return list()
    links = list()
    with open(csv_file, "r", encoding="utf8") as f:
        for r in csv.reader(f):
                link = Link()
                link.game_id = r[0]
                link.amiibo_id = r[1]
                link.note_en = r[2]
                link.note_cn = r[3]
                link.note_it = r[4]
                links.append(link)
    return links


def count_game_links(games, links, game_id):

    count = 0
    for link in links:
        if link.game_id == game_id:
            count = count + 1
    for game in games:
        if game.parent_id == game_id:
            count = count + count_game_links(games, links, game.id)

    return count


def gen_amiibo_link_c_file(links):
    c_file = get_prorject_directory() + "/application/src/amiidb/db_link.c"
    with open(c_file, "w+", newline="\n", encoding="utf8") as f:
        f.write('/* This file is auto-generated by amiibo_db_gen.py. Do not edit directly. */\n')  
        f.write('#include "db_header.h"\n')
        f.write('const db_link_t link_list[] = {\n')
        for link in links:
            f.write('{%s, 0x%s, 0x%s, "%s", "%s", "%s"}, \n' % 
                    (link.game_id, link.amiibo_id[0:8], link.amiibo_id[8:16], link.note_en, 
                    link.note_cn, link.note_it))  
        f.write("{0, 0, 0, 0, 0, 0}\n")
        f.write("};\n")

def gen_amiibo_game_c_file(games, links):
    c_file = get_prorject_directory() + "/application/src/amiidb/db_game.c"
    with open(c_file, "w+", newline="\n", encoding="utf8") as f:
        f.write('/* This file is auto-generated by amiibo_db_gen.py. Do not edit directly. */\n')  
        f.write('#include "db_header.h"\n')
        f.write('const db_game_t game_list[] = {\n')
        for game in games:
            # --- 번역 코드 추가 ---
            korean_name = gameseries_translation.get(game.name_en, game.name_en)
            # --- 번역 코드 추가 끝 ---
            f.write('{%s, %s, "%s", "%s", %s, %s}, \n' % 
                    (game.id, game.parent_id, korean_name, 
                    game.name_cn, game.order, count_game_links( games, links, game.id)))
        f.write("{0, 0, 0, 0, 0}\n")
        f.write("};\n")      
    
def gen_other_link(amiibos, links):
    linked_amiibo_ids = set()
    new_link = list()
    for link in links:
        linked_amiibo_ids.add(link.amiibo_id)
    for amiibo in amiibos:
        if amiibo.id not in linked_amiibo_ids:
            link = Link()
            link.game_id = "255" # other
            link.amiibo_id = amiibo.id
            link.note_en = ""
            link.note_cn = ""
            link.note_it = ""
            new_link.append(link)
            print("uncategorized amiibo (%s, %s)" % (link.amiibo_id, amiibo.name_en))
    if len(new_link) > 0:
        print("add %d uncategoried amiibo to other." %(len(new_link)))
    for link in new_link:
        links.append(link)
    return links


amiibos_api = fetch_amiibo_from_api()
amiibos_csv = read_amiibo_from_csv()
amiibos_merged = merge_amiibo(amiibos_csv, amiibos_api)
write_amiibo_to_csv(amiibos_merged)
print("Found %d amiibo records." % len(amiibos_merged))
gen_amiibo_data_c_file(amiibos_merged)
games = read_games_from_csv()
links = read_link_from_csv()
links = gen_other_link(amiibos_merged, links)
gen_amiibo_game_c_file(games, links)
gen_amiibo_link_c_file(links)
