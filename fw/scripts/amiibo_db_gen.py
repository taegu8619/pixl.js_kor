# download latest amiibo data and merge to amiibo_data.csv


from urllib.request import urlopen
import json
import os
import csv

# --- 전체 한글 번역 데이터 시작 ---
amiibo_translation = {
    # Animal Crossing
    "Sandy": "샌디", "Isabelle - Winter": "여울 (겨울옷)", "Ava": "에바", "Blanca": "블랑카", "Mac": "맥", "Lucha": "루차", "Punchy": "빙티",
    "Violet": "비올라", "Tom": "톰", "Mint": "민트", "Caroline": "캐롤라인", "Mabel": "고순이", "Frett": "챔프", "Kidd": "염두리",
    "Purrl": "타마", "Mitzi": "마르", "Reneigh": "리아나", "Rasher": "글레이", "Chrissy": "크리스틴", "Harriet": "카트리나", "Daisy": "데이지",
    "Bam": "록키", "Anabelle": "아롱이", "Labelle": "라벨", "Rover": "낯선고양이", "Wendell": "세이", "Renée": "르네", "Agnes": "아그네스",
    "Resetti - Without Hat": "도루묵씨 (모자 없음)", "Daisy Mae": "무파니", "Merry": "유네찌", "Big Top": "1호", "Leif": "늘봉", "Rocco": "아폴로",
    "Gladys": "글라라", "Twiggy": "핀틱", "Camofrog": "충성", "Lottie": "솜이", "Deirdre": "나디아", "Flick": "레온", "Naomi": "화자",

    "Raddle": "개군", "Tortimer": "고북", "Digby": "켄트", "Puddles": "가위", "Pashmina": "바바라", "Paolo": "파올로", "June": "쭈니",
    "Rudy": "루돌", "Flurry": "뽀야미", "Tammy": "아네사", "Teddy": "곰도로스", "Frank": "헐크", "Stu": "모리스", "Roscoe": "로데오",
    "Rodney": "지미", "Bruce": "브루스", "Bree": "사라", "Bangle": "루주", "Stitches": "패치", "Aurora": "오로라", "Iggly": "펭수",
    "Vic": "빅터", "Amelia": "안데스", "Miranda": "미랑", "Katrina": "마추릴라", "Audie": "모니카", "Bill": "코코아", "Anchovy": "앤쵸비",
    "Harvey": "파니엘", "Tommy - Uniform": "밤돌이 (유니폼)", "Maggie": "마가렛", "Orville": "로드리", "Chai": "차이", "Dom": "차둘",
    "Kapp'n": "갑돌", "Limberg": "단무지", "Weber": "아잠만", "Bunnie": "릴리안", "Pelly": "펠리", "Frobert": "구리구리", "Tasha": "나타샤",
    "Robin": "로빈", "Alfonso": "알베르트", "Peck": "쪼끼", "Cyrus": "리포", "Frita": "웬디", "Sprinkle": "크리미", "Bella": "이자벨",
    "Drago": "용남이", "Grams": "갑순", "OHare": "오골", "Hamphrey": "햄둥", "Pave": "베르리나", "Alli": "크로크", "Bones": "토미",
    "Gaston": "대길", "Quillson": "덕", "Gwen": "폴라", "Kevin": "멧지", "Blaire": "실루엣", "Wolfgang": "시베리아", "Peggy": "꽃지",
    "Boyd": "덤벨", "Gabi": "패티카", "T-Bone": "티본", "Portia": "블랜더", "Benedict": "페니실린", "Pudge": "우띠", "Jay": "참돌이",
    "Tabby": "호랭이", "Kody": "아이루", "Apollo": "아폴로", "Maple": "메이첼", "Sly": "하이드", "Goose": "건태", "Cookie": "베리",

    "Pietro": "피에로", "Henry": "헨리", "Blathers": "부엉", "Timbra": "잔디", "Ed": "꺼벙", "Sable": "고옥이", "Keaton": "프랭크",
    "Hugh": "먹고파", "Wart Jr.": "샘", "Kicks": "패트릭", "Shrunk": "스승", "Eugene": "코알", "Pecan": "리키", "Sparro": "춘섭",
    "Isabelle - Dress": "여울 (원피스)", "Kabuki": "가북희", "Eloise": "엘레핀", "Gala": "꽃돼지", "Tex": "펭기", "Reese": "리사",
    "Bianca": "백희", "Cephalobot": "기계로", "Fuchsia": "제시카", "Tucker": "맘모", "Annalisa": "설백", "Yuka": "유카리", "Pate": "나키",
    "Carmen": "초코", "Lily": "레이니", "Bob": "히죽", "Ankha": "클레오", "Zucker": "쭈니", "Jack": "펌킹", "Sylvia": "실비아",
    "Whitney": "비앙카", "Redd - Shirt": "여욱 (셔츠)", "Chevre": "윤이", "Shep": "존", "Fang": "시베리아", "Snake": "닌토",
    "Pekoe": "재스민", "Norma": "젖소", "Butch": "존", "Marshal": "쭈니", "Cleo": "클레오", "Hornsby": "뿌람", "Dobie": "켄",
    "Tiansheng": "손오공", "Ace": "에이스", "Zoe": "팽기", "Chabwick": "펭구", "Ione": "스피카", "Marlo": "돈후앙", "Petri": "리카",
    "Quinn": "샹펜", "Rio": "리카", "Sasha": "미첼", "Shino": "요비", "Azalea": "鹃", "Faith": "믿음", "Frett": "챔프",
    "Reneigh": "리아나", "Cephalobot": "기계로", "Ione": "스피카", "Marlo": "돈후앙", "Petri": "리카", "Quinn": "샹펜", "Rio": "리카",
    "Sasha": "미첼", "Shino": "요비", "Tiansheng": "손오공", "Zoe": "팽기", "Ace": "에이스", "Azalea": "鹃", "Faith": "믿음",
    "Frett": "챔프", "Reneigh": "리아나", "Cephalobot": "기계로", "Ione": "스피카", "Marlo": "돈후앙", "Petri": "리카", "Quinn": "샹펜",
    "Rio": "리카", "Sasha": "미첼", "Shino": "요비", "Tiansheng": "손오공", "Zoe": "팽기", "Ace": "에이스", "Azalea": "鹃",
    "Faith": "믿음", "Frett": "챔프", "Reneigh": "리아나", "Cephalobot": "기계로", "Ione": "스피카", "Marlo": "돈후앙",
    "Petri": "리카", "Quinn": "샹펜", "Rio": "리카", "Sasha": "미첼", "Shino": "요비", "Tiansheng": "손오공", "Zoe": "팽기",
    "Ace": "에이스", "Azalea": "鹃", "Faith": "믿음", "Frett": "챔프", "Reneigh": "리아나", "Cephalobot": "기계로",
    "Ione": "스피카", "Marlo": "돈후앙", "Petri": "리카", "Quinn": "샹펜", "Rio": "리카", "Sasha": "미첼", "Shino": "요비",

    # Super Mario
    "Mario - Cat": "고양이마리오", "Peach - Cat": "고양이피치", "Mario - Gold Edition": "골드 마리오", "Mario - Silver Edition": "실버 마리오",
    "Goomba": "굼바", "Koopa Troopa": "엉금엉금", "Boo": "부끄부끄", "Waluigi": "와루이지", "Diddy Kong": "디디콩",
    "Rosalina": "로젤리나", "Bowser - Wedding": "웨딩 쿠파", "Peach - Wedding": "웨딩 피치", "Mario - Wedding": "웨딩 마리오",

    # The Legend of Zelda
    "Zelda & Loftwing": "젤다 & 로프트버드", "Link - Archer": "링크 (활)", "Link - Rider": "링크 (라이더)", "Guardian": "가디언",
    "Bokoblin": "보코블린", "Daruk": "다르케르", "Mipha": "미파", "Revali": "리발", "Urbosa": "우르보사",
    "Toon Link - The Wind Waker": "툰링크 (바람의 지휘봉)", "Toon Zelda - The Wind Waker": "툰젤다 (바람의 지휘봉)",
    "8-Bit Link": "8비트 링크", "Link - Ocarina of Time": "링크 (시간의 오카리나)", "Link - Majora's Mask": "링크 (무쥬라의 가면)",
    "Link - Twilight Princess": "링크 (황혼의 공주)", "Wolf Link": "울프 링크", "Link - Skyward Sword": "링크 (스카이워드 소드)",
    "Link - Link's Awakening": "링크 (꿈꾸는 섬)", "Link - Tears of the Kingdom": "링크 (티어스 오브 더 킹덤)",
    "Zelda - Tears of the Kingdom": "젤다 (티어스 오브 더 킹덤)", "Ganondorf - Tears of the Kingdom": "가논돌프 (티어스 오브 더 킹덤)",

    # Super Smash Bros.
    "Mii Brawler": "Mii 격투가", "Mii Swordfighter": "Mii 검술가", "Mii Gunner": "Mii 사격수", "Rosalina & Luma": "로젤리나 & 치코",
    "King K. Rool": "킹크루루", "Lucina": "루키나", "Ike": "아이크", "Robin": "러플레", "Roy": "로이", "Corrin": "카무이",
    "Corrin - Player 2": "카무이 (2P)", "Dark Pit": "블랙피트", "Zero Suit Samus": "제로 슈트 사무스", "Piranha Plant": "뻐끔플라워",
    "Ice Climbers": "아이스 클라이머", "Incineroar": "어흥염", "Isabelle": "여울", "Joker": "조커", "Hero": "용사",
    "Banjo & Kazooie": "반조 & 카주이", "Terry": "테리", "Byleth": "벨레트", "Min Min": "미엔미엔", "Steve": "스티브",
    "Alex": "알렉스", "Sephiroth": "세피로스", "Pyra": "호무라", "Mythra": "히카리", "Kazuya": "카즈야", "Sora": "소라",

    # Splatoon
    "Inkling - Yellow": "잉클링 (노랑)", "Shiver": "후우카", "Frye": "우츠호", "Big Man": "만타로", "Smallfry": "꼬마연어",
    "Inkling Girl - Lime Green": "잉클링 걸 (라임 그린)", "Inkling Boy - Purple": "잉클링 보이 (보라)", "Inkling Squid - Orange": "잉클링 스퀴드 (주황)",
    "Octoling - Blue": "옥토링 (파랑)",

    # 기타
    "Qbby": "큐비", "Detective Pikachu": "명탐정 피카츄", "Solaire of Astora": "태양의 전사 솔라", "Loot Goblin": "보물 고블린",
    "Shovel Knight - Gold Edition": "골드 삽질 기사", "Plague Knight": "역병 기사", "Specter Knight": "스펙터 기사",
    "King Knight": "킹 기사", "Mega Man - Gold Edition": "록맨 (골드 에디션)", "Super Mario Cereal": "슈퍼 마리오 시리얼"
}

gameseries_translation = {
    "Animal Crossing": "동물의 숲", "Sonic": "소닉", "Mii": "Mii", "Mario Sports Superstars": "마리오 스포츠 슈퍼스타즈",
    "The Legend of Zelda": "젤다의 전설", "Splatoon": "스플래툰", "BoxBoy!": "BOXBOY!", "Yu-Gi-Oh!": "유희왕",
    "Donkey Kong": "동키콩", "Final Fantasy": "파이널 판타지", "Kellogs": "켈로그", "Punch Out": "펀치 아웃!!",
    "Megaman": "록맨", "Power Pros": "파워풀 프로야구", "Kirby": "별의 커비", "Fire Emblem": "파이어 엠블렘",
    "Star Fox": "스타폭스", "Pokemon": "포켓몬", "Metroid": "메트로이드", "Kid Icarus": "키드 이카루스",
    "Pikmin": "피크민", "Wii Fit": "Wii Fit", "Xenoblade Chronicles": "제노블레이드 크로니클스", "Pac-man": "팩맨",
    "Street Fighter": "스트리트 파이터", "Bayonetta": "베요네타", "Chibi Robo": "작은 로보!", "Shovel Knight": "삽질 기사",
    "Dark Souls": "다크 소울", "Diablo": "디아블로", "Skylanders": "스카이랜더스", "Monster Hunter": "몬스터 헌터",
    "Castlevania": "캐슬바니아", "Metal Gear Solid": "메탈 기어 솔리드", "Dragon Quest": "드래곤 퀘스트",
    "Banjo-Kazooie": "반조-카주이", "Fatal Fury": "아랑전설", "ARMS": "ARMS", "Minecraft": "마인크래프트",
    "Kingdom Hearts": "킹덤 하츠", "Monster Hunter Rise": "몬스터 헌터 라이즈", "Monster Hunter Stories": "몬스터 헌터 스토리즈",
    "Tekken": "철권", "Classic Nintendo": "클래식 닌텐도", "Earthbound": "마더", "F-Zero": "F-ZERO", "Persona": "페르소나",
    "Super Mario": "슈퍼 마리오", "Yoshi's Woolly World": "요시 울리 월드", "Super Smash Bros.": "슈퍼 스매시브라더스"
}
# --- 전체 한글 번역 데이터 끝 ---

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
