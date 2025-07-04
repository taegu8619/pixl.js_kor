# 먼저 필요한 라이브러리를 설치해야 합니다.
# 터미널이나 명령 프롬프트에서 아래 명령어를 실행하세요:
# pip install thefuzz python-levenshtein

from urllib.request import urlopen
import json
import os
import csv
# --- FUZZY ---: 퍼지 문자열 매칭을 위한 라이브러리 임포트
from thefuzz import process

# --- 한글 번역 데이터 (전체) 시작 ---
# (이전 대화의 번역 데이터는 여기에 그대로 포함됩니다)
amiibo_translation = {
    # Animal Crossing
    "Isabelle": "여울", "Tom Nook": "너굴", "K.K.": "T.K.", "Mabel": "고순이", "Reese": "리사",
    "Cyrus": "리포", "Lottie": "솜이", "Celeste": "부옥", "Blathers": "부엉", "Kicks": "패트릭",
    "Rover": "낯선고양이", "Timmy & Tommy": "콩돌이 & 밤돌이", "Kapp'n": "갑돌", "Resetti": "도루묵씨",
    "Digby": "켄트", "Flick": "레온", "C.J.": "저스틴",
    "Daisy Mae": "무파니", "Orville": "로드리", "Wilbur": "윌버", "Harvey": "파니엘", "Wardell": "너티",
    "Niko": "니코", "Wisp": "깨빈", "Saharah": "사하라", "Label": "라벨", "Sable": "고옥이",
    "Goldie": "카라멜", "Stitches": "패치", "Rosie": "부케", "Marshal": "쭈니", "Fauna": "솔미",
    "Bob": "히죽", "Merengue": "스트로베리", "Julian": "줄리안", "Ankha": "클레오", "Zucker": "먹고파",
    "Lucky": "럭키", "Tangy": "백프로", "Punchy": "빙티", "Lolly": "사이다", "Poppy": "다람",
    "Beau": "피터", "Coco": "이요", "Ruby": "루나", "Whitney": "비앙카", "Chief": "대장",
    "Maple": "메이첼", "Diana": "나탈리", "Skye": "신옥", "Static": "스파크", "Fang": "시베리아",
    "Bluebear": "글루민", "Pekoe": "재스민", "Chrissy": "크리스틴", "Francine": "프랑소와",
    "Merry": "유네찌", "Lily": "레이니", "Marina": "문리나", "Octavian": "문복", "Muffy": "프릴",
    "Pietro": "피에로", "Genji": "토시", "Kabuki": "가북희", "Kid Cat": "1호", "Agent S": "2호",
    "Big Top": "3호", "Rocket": "4호", "Hamlet": "햄스틴", "Apple": "애플", "Flurry": "뽀야미",
    "Judy": "미애", "Raymond": "잭슨", "Sherb": "뽀얌", "Dom": "차둘", "Audie": "모니카",
    "Cyd": "펑크스", "Megan": "캔디", "Reneigh": "리아나", "Shino": "기루", "Ione": "스피카",
    "Sasha": "미첼", "Tiansheng": "샹펜", "Quinn": "풍성", "Marlo": "돈부리", "Petri": "리카",
    "Cephalobot": "기계로", "Azalea": "鹃", "Rio": "리오", "Ace": "에이스", "Frett": "샹펜",
    "Zoe": "조이", "Chabwick": "펭구",
    "Isabelle - Winter": "여울 (겨울옷)", "Isabelle - Summer Outfit": "여울 (여름옷)",
    "Isabelle - Kimono": "여울 (기모노)", "Isabelle - Dress": "여울 (드레스)",
    "Isabelle - Sweater": "여울 (스웨터)", "Isabelle - Character Parfait": "여울 (캐릭터 파르페)",
    "Tom Nook - Jacket": "너굴 (자켓)", "Tom Nook - Coat": "너굴 (코트)",
    "K. K. Slider - Pikopuri": "T.K. (피코프리)", "DJ KK": "DJ K.K.",
    "Goldie - Amiibo Festival": "카라멜 (아미보 페스티벌)",
    "Stitches - Amiibo Festival": "패치 (아미보 페스티벌)",
    "Rosie - Amiibo Festival": "부케 (아미보 페스티벌)",
    "Lottie - Black Skirt And Bow": "솜이 (검은 치마와 리본)", "Lottie - Island": "솜이 (섬)",
    "Digby - Raincoat": "켄트 (우비)",
    "Resetti - Without Hat": "도루묵씨 (모자 없음)", "Don Resetti": "오루묵씨",
    "Don Resetti - Without Hat": "오루묵씨 (모자 없음)",
    "Timmy - Uniform": "콩돌이 (유니폼)", "Tommy - Uniform": "밤돌이 (유니폼)",
    "Timmy - Full Apron": "콩돌이 (앞치마)", "Tommy - Suit": "밤돌이 (정장)",
    "Redd - Shirt": "여욱 (셔츠)",

    # The Legend of Zelda
    "Link": "링크", "Zelda": "젤다", "Ganondorf": "가논돌프", "Sheik": "시크", "Toon Link": "툰링크",
    "Wolf Link": "울프 링크", "Guardian": "가디언", "Bokoblin": "보코블린", "Daruk": "다르케르",
    "Mipha": "미파", "Revali": "리발", "Urbosa": "우르보사", "Midna & Wolf Link": "미드나 & 울프 링크",
    "Link - Archer": "링크 (활)", "Link - Rider": "링크 (라이더)", "Zelda (BotW)": "젤다 (브레스 오브 더 와일드)",
    "8-Bit Link": "8비트 링크", "Link - Ocarina of Time": "링크 (시간의 오카리나)",
    "Toon Link - The Wind Waker": "툰링크 (바람의 지휘봉)", "Toon Zelda - The Wind Waker": "툰젤다 (바람의 지휘봉)",
    "Link - Majora's Mask": "링크 (무쥬라의 가면)", "Link - Skyward Sword": "링크 (스카이워드 소드)",
    "Link - Twilight Princess": "링크 (황혼의 공주)", "Zelda & Loftwing": "젤다 & 로프트버드",
    "Link - Link's Awakening": "링크 (꿈꾸는 섬)",
    "Link - Tears of the Kingdom": "링크 (티어스 오브 더 킹덤)",
    "Zelda - Tears of the Kingdom": "젤다 (티어스 오브 더 킹덤)",
    "Ganondorf - Tears of the Kingdom": "가논돌프 (티어스 오브 더 킹덤)",

    # Super Mario & Others
    "Mario": "마리오", "Luigi": "루이지", "Peach": "피치공주", "Bowser": "쿠파", "Dr. Mario": "닥터 마리오",
    "Rosalina": "로젤리나", "Bowser Jr.": "쿠파주니어", "Wario": "와리오", "Yoshi": "요시", "Donkey Kong": "동키콩",
    "Diddy Kong": "디디콩", "Goomba": "굼바", "Koopa Troopa": "엉금엉금", "Boo": "부끄부끄",
    "Daisy": "데이지", "Waluigi": "와루이지", "Piranha Plant": "뻐끔플라워",
    "Mario - Gold Edition": "골드 마리오", "Mario - Silver Edition": "실버 마리오",
    "8-Bit Mario Modern Color": "8비트 마리오 (모던 컬러)", "8-Bit Mario Classic Color": "8비트 마리오 (클래식 컬러)",
    "Wedding Mario": "웨딩 마리오", "Wedding Peach": "웨딩 피치", "Wedding Bowser": "웨딩 쿠파",
    "Cat Mario": "고양이마리오", "Cat Peach": "고양이피치",
    "Green Yarn Yoshi": "초록 털실 요시", "Light Blue Yarn Yoshi": "하늘색 털실 요시", "Pink Yarn Yoshi": "핑크 털실 요시",
    "Mega Yarn Yoshi": "거대 털실 요시", "Poochy": "포치",
    "Hammer Slam Bowser": "해머 슬램 쿠파", "Turbo Charge Donkey Kong": "터보 차지 동키콩",

    # Splatoon
    "Inkling Girl": "잉클링 걸", "Inkling Boy": "잉클링 보이", "Inkling Squid": "잉클링 스퀴드",
    "Callie": "아오리", "Marie": "호타루", "Pearl": "히메", "Marina": "이이다",
    "Octoling Girl": "옥토링 걸", "Octoling Boy": "옥토링 보이", "Octoling Octopus": "옥토링 옥토퍼스",
    "Smallfry": "꼬마연어", "Shiver": "후우카", "Frye": "우츠호", "Big Man": "만타로",

    # Kirby
    "Kirby": "커비", "King Dedede": "디디디 대왕", "Meta Knight": "메타 나이트", "Waddle Dee": "웨이들 디",

    # Pokemon
    "Pikachu": "피카츄", "Charizard": "리자몽", "Lucario": "루카리오", "Jigglypuff": "푸린",
    "Greninja": "개굴닌자", "Mewtwo": "뮤츠", "Pokemon Trainer": "포켓몬 트레이너", "Squirtle": "꼬부기",
    "Ivysaur": "이상해풀", "Pichu": "피츄", "Incineroar": "어흥염", "Detective Pikachu": "명탐정 피카츄",
    "Shadow Mewtwo": "다크 뮤츠",

    # Fire Emblem
    "Marth": "마르스", "Ike": "아이크", "Robin": "러플레", "Lucina": "루키나", "Roy": "로이",
    "Corrin": "카무이", "Corrin - Player 2": "카무이 (2P)", "Chrom": "크롬", "Tiki": "치키",
    "Alm": "아름", "Celica": "세리카", "Byleth": "벨레트",

    # 기타
    "Samus": "사무스", "Zero Suit Samus": "제로 슈트 사무스", "Metroid": "메트로이드", "Samus Aran": "사무스 아란",
    "E.M.M.I.": "E.M.M.I.", "Samus (Metroid Dread)": "사무스 (메트로이드 드레드)", "Dark Samus": "다크 사무스",
    "Ridley": "리들리", "Pit": "피트", "Palutena": "파르테나", "Dark Pit": "블랙피트", "Fox": "폭스",
    "Falco": "팔코", "Wolf": "울프", "Ness": "네스", "Lucas": "류카", "Captain Falcon": "캡틴 팔콘",
    "Olimar": "올리마", "Pikmin": "피크민", "Wii Fit Trainer": "Wii Fit 트레이너", "Shulk": "슈르크",
    "Mr. Game & Watch": "Mr. 게임&워치", "Duck Hunt": "덕헌트", "R.O.B.": "R.O.B.",
    "R.O.B. - Famicom": "R.O.B. (패미컴)", "R.O.B. - NES": "R.O.B. (NES)",
    "Pac-Man": "팩맨", "Mega Man": "록맨", "Sonic": "소닉", "Ryu": "류", "Ken": "켄",
    "Cloud": "클라우드", "Cloud - Player 2": "클라우드 (2P)", "Bayonetta": "베요네타", "Bayonetta - Player 2": "베요네타 (2P)",
    "Snake": "스네이크", "Simon": "시몬", "Richter": "릭터", "King K. Rool": "킹크루루", "Ice Climbers": "아이스 클라이머",
    "Joker": "조커", "Hero": "용사", "Banjo & Kazooie": "반조 & 카주이", "Terry": "테리", "Min Min": "미엔미엔",
    "Steve": "스티브", "Alex": "알렉스", "Sephiroth": "세피로스", "Pyra": "호무라", "Mythra": "히카리",
    "Kazuya": "카즈야", "Sora": "소라", "Shovel Knight": "삽질 기사", "Plague Knight": "역병 기사",
    "Specter Knight": "스펙터 기사", "King Knight": "킹 기사", "Gold Shovel Knight": "골드 삽질 기사",
    "Solaire of Astora": "태양의 전사 솔라", "Loot Goblin": "보물 고블린", "Qbby": "큐비",
    "Magnamalo": "마가이마가도", "Palamute": "동반자 가루크", "Palico": "동반자 아이루", "Tsukino": "츠키노",
    "Ena": "에나", "Razewing Ratha": "파멸의 날개 레우스"
}

gameseries_translation = {
    "Animal Crossing": "동물의 숲", "The Legend of Zelda": "젤다의 전설", "Super Mario": "슈퍼 마리오",
    "Super Smash Bros.": "슈퍼 스매시브라더스", "Yoshi's Woolly World": "요시 울리 월드",
    "Splatoon": "스플래툰", "Kirby": "별의 커비", "Fire Emblem": "파이어 엠블렘", "Star Fox": "스타폭스",
    "Pokemon": "포켓몬", "Metroid": "메트로이드", "Kid Icarus": "키드 이카루스", "Pikmin": "피크민",
    "Wii Fit": "Wii Fit", "Xenoblade Chronicles": "제노블레이드 크로니클스", "Pac-Man": "팩맨",
    "Mega Man": "록맨", "Sonic the Hedgehog": "소닉 더 헤지혹", "Street Fighter": "스트리트 파이터",
    "Final Fantasy": "파이널 판타지", "Bayonetta": "베요네타", "Chibi-Robo!": "작은 로보!",
    "Shovel Knight": "삽질 기사", "Dark Souls": "다크 소울", "Diablo": "디아블로",
    "Skylanders": "스카이랜더스", "Monster Hunter": "몬스터 헌터", "BoxBoy!": "BOXBOY!",
    "Castlevania": "캐슬바니아", "Metal Gear Solid": "메탈 기어 솔리드", "Dragon Quest": "드래곤 퀘스트",
    "Banjo-Kazooie": "반조-카주이", "Fatal Fury": "아랑전설", "ARMS": "ARMS",
    "Minecraft": "마인크래프트", "Kingdom Hearts": "킹덤 하츠",
    "Monster Hunter Rise": "몬스터 헌터 라이즈", "Monster Hunter Stories": "몬스터 헌터 스토리즈",
    "Power Pros": "파워풀 프로야구", "Yu-Gi-Oh!": "유희왕"
}
# --- 한글 번역 데이터 끝 ---

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

# --- FUZZY ---: 퍼지 매칭을 위한 헬퍼 함수 추가
def find_best_match(name_to_match, choices_dict, threshold=90):
    """
    주어진 이름과 가장 유사한 항목을 번역 딕셔너리에서 찾습니다.
    :param name_to_match: 매칭할 이름 (e.g., API에서 받은 이름)
    :param choices_dict: 번역 데이터 딕셔너리 (e.g., amiibo_translation)
    :param threshold: 일치 판정을 위한 최소 유사도 점수 (0-100)
    :return: 매칭된 번역 이름 또는 None
    """
    # 딕셔너리의 키(영문명) 중에서 가장 유사한 것을 찾음
    best_match = process.extractOne(name_to_match, choices_dict.keys())
    
    if best_match and best_match[1] >= threshold:
        # 유사도 점수가 임계값 이상이면, 해당 키의 값(한글명)을 반환
        return choices_dict[best_match[0]]
    else:
        # 적절한 매치를 찾지 못한 경우
        if best_match:
             print(f"Warning: Low similarity for '{name_to_match}'. Best guess: '{best_match[0]}' ({best_match[1]}%). Using original name.")
        return None

def get_project_directory():
    # '__file__'이 정의되지 않은 환경(예: Jupyter Notebook)을 위한 예외 처리
    try:
        # 스크립트 파일의 상위 디렉토리를 반환
        return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    except NameError:
        # 스크립트로 실행되지 않을 경우 현재 작업 디렉토리를 반환
        return os.path.abspath("./")


def fetch_amiibo_from_api():
    """Amiibo API에서 데이터를 가져옵니다."""
    conn = urlopen("https://www.amiiboapi.com/api/amiibo/")
    body = json.loads(conn.read())
    amiibos = []
    for ami in body["amiibo"]: 
        amiibo = Amiibo()
        amiibo.id = ami["head"] + ami["tail"]
        amiibo.name_en = ami["name"]
        amiibos.append(amiibo)
    return amiibos


def read_amiibo_from_csv(proj_dir):
    """로컬 CSV 파일에서 Amiibo 데이터를 읽습니다."""
    csv_file = os.path.join(proj_dir, "data", "amiidb_amiibo.csv")
    if not os.path.exists(csv_file):
        return []
    amiibos = []
    with open(csv_file, "r", encoding="utf8") as f:
        for r in csv.reader(f):
            amiibo = Amiibo()
            amiibo.id = r[0]
            amiibo.name_en = r[1]
            amiibo.name_cn = r[2] if len(r) > 2 else "" # 빈 중국어 이름 처리
            amiibos.append(amiibo)
    return amiibos


def write_amiibo_to_csv(amiibos, proj_dir):
    """Amiibo 데이터를 CSV 파일에 씁니다."""
    data_dir = os.path.join(proj_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    csv_file = os.path.join(data_dir, "amiidb_amiibo.csv")
    with open(csv_file, "w", encoding="utf8", newline="") as f:
        w = csv.writer(f)
        for amiibo in amiibos:
            r = [amiibo.id, amiibo.name_en, amiibo.name_cn]
            w.writerow(r)


def merge_amiibo(amiibos_csv, amiibos_api):
    """API 데이터와 로컬 CSV 데이터를 병합합니다."""
    amiibos_merged = {amiibo.id: amiibo for amiibo in amiibos_csv}

    for amiibo in amiibos_api:
        if amiibo.id not in amiibos_merged:
            amiibo.name_cn = "" # 새 amiibo의 name_cn을 빈 문자열로 초기화
            amiibos_merged[amiibo.id] = amiibo
            print(f"Found new amiibo: [{amiibo.id}] {amiibo.name_en}")
            
    # ID 순으로 정렬하여 일관성 유지
    return [amiibos_merged[key] for key in sorted(amiibos_merged.keys())]


def gen_amiibo_data_c_file(amiibos, proj_dir):
    """Amiibo 데이터를 위한 C 소스 파일을 생성합니다."""
    c_dir = os.path.join(proj_dir, "application", "src", "amiidb")
    if not os.path.exists(c_dir):
        os.makedirs(c_dir)
    c_file = os.path.join(c_dir, "db_amiibo.c")

    with open(c_file, "w", newline="\n", encoding="utf8") as f:
        f.write('/* This file is auto-generated by script. Do not edit directly. */\n')  
        f.write('#include "db_header.h"\n\n')
        f.write('const db_amiibo_t amiibo_list[] = {\n')
        for amiibo in amiibos:
            # --- FUZZY ---: 퍼지 매칭 함수를 사용하여 한국어 이름 찾기
            korean_name = find_best_match(amiibo.name_en, amiibo_translation)
            if not korean_name:
                # 매칭 실패 시 영어 이름을 그대로 사용
                korean_name = amiibo.name_en
            
            # C 코드에서 문자열 내의 " 문자를 이스케이프 처리
            korean_name_escaped = korean_name.replace('"', '\\"')
            name_cn_escaped = amiibo.name_cn.replace('"', '\\"') if amiibo.name_cn else ""

            f.write(f'    {{0x{amiibo.id[0:8]}, 0x{amiibo.id[8:16]}, "{korean_name_escaped}", "{name_cn_escaped}"}}, \n')
        f.write("    {0, 0, 0, 0}\n")
        f.write("};\n")

def read_games_from_csv(proj_dir):
    """게임 목록을 CSV에서 읽습니다."""
    csv_file = os.path.join(proj_dir, "data", "amiidb_game.csv")
    if not os.path.exists(csv_file):
        return []
    games = []
    with open(csv_file, "r", encoding="utf8") as f:
        for r in csv.reader(f):
            game = Game()
            game.id, game.parent_id, game.name_en, game.name_cn, game.order = r
            games.append(game)
    return games

def read_link_from_csv(proj_dir):
    """게임-Amiibo 연결 정보를 CSV에서 읽습니다."""
    csv_file = os.path.join(proj_dir, "data", "amiidb_link.csv")
    if not os.path.exists(csv_file):
        return []
    links = []
    with open(csv_file, "r", encoding="utf8") as f:
        for r in csv.reader(f):
            link = Link()
            link.game_id, link.amiibo_id, link.note_en, link.note_cn, link.note_it = r
            links.append(link)
    return links

def count_game_links(games, links, game_id):
    """특정 게임 및 그 하위 게임에 연결된 Amiibo 수를 계산합니다."""
    count = sum(1 for link in links if link.game_id == game_id)
    count += sum(count_game_links(games, links, game.id) for game in games if game.parent_id == game_id)
    return count

def gen_amiibo_link_c_file(links, proj_dir):
    """게임-Amiibo 연결 정보를 위한 C 소스 파일을 생성합니다."""
    c_dir = os.path.join(proj_dir, "application", "src", "amiidb")
    c_file = os.path.join(c_dir, "db_link.c")

    with open(c_file, "w", newline="\n", encoding="utf8") as f:
        f.write('/* This file is auto-generated by script. Do not edit directly. */\n')  
        f.write('#include "db_header.h"\n\n')
        f.write('const db_link_t link_list[] = {\n')
        for link in links:
            note_en_escaped = link.note_en.replace('"', '\\"')
            note_cn_escaped = link.note_cn.replace('"', '\\"')
            note_it_escaped = link.note_it.replace('"', '\\"')
            f.write(f'    {{{link.game_id}, 0x{link.amiibo_id[0:8]}, 0x{link.amiibo_id[8:16]}, "{note_en_escaped}", "{note_cn_escaped}", "{note_it_escaped}"}}, \n')
        f.write("    {0, 0, 0, 0, 0, 0}\n")
        f.write("};\n")

def gen_amiibo_game_c_file(games, links, proj_dir):
    """게임 정보를 위한 C 소스 파일을 생성합니다."""
    c_dir = os.path.join(proj_dir, "application", "src", "amiidb")
    c_file = os.path.join(c_dir, "db_game.c")

    with open(c_file, "w", newline="\n", encoding="utf8") as f:
        f.write('/* This file is auto-generated by script. Do not edit directly. */\n')  
        f.write('#include "db_header.h"\n\n')
        f.write('const db_game_t game_list[] = {\n')
        for game in games:
            # --- FUZZY ---: 게임 시리즈 이름에도 퍼지 매칭 적용
            korean_name = find_best_match(game.name_en, gameseries_translation)
            if not korean_name:
                korean_name = game.name_en
            
            korean_name_escaped = korean_name.replace('"', '\\"')
            name_cn_escaped = game.name_cn.replace('"', '\\"')

            link_count = count_game_links(games, links, game.id)
            f.write(f'    {{{game.id}, {game.parent_id}, "{korean_name_escaped}", "{name_cn_escaped}", {game.order}, {link_count}}}, \n')
        f.write("    {0, 0, 0, 0, 0, 0}\n")
        f.write("};\n")

def gen_other_link(amiibos, links):
    """어디에도 분류되지 않은 Amiibo를 '기타' 카테고리에 추가합니다."""
    linked_amiibo_ids = {link.amiibo_id for link in links}
    new_links = []
    
    for amiibo in amiibos:
        if amiibo.id not in linked_amiibo_ids:
            link = Link()
            link.game_id = "255" # '기타' 카테고리 ID
            link.amiibo_id = amiibo.id
            link.note_en, link.note_cn, link.note_it = "", "", ""
            new_links.append(link)
            print(f"Uncategorized amiibo: ({amiibo.id}, {amiibo.name_en})")
            
    if new_links:
        print(f"Adding {len(new_links)} uncategorized amiibo(s) to 'Other'.")
        links.extend(new_links)
    return links

# --- Main Execution ---
if __name__ == "__main__":
    proj_dir = get_project_directory()
    print(f"Project directory set to: {proj_dir}")

    print("\nFetching latest amiibo data from API...")
    amiibos_api = fetch_amiibo_from_api()

    print("Reading existing amiibo data from CSV...")
    amiibos_csv = read_amiibo_from_csv(proj_dir)

    print("Merging API data with local data...")
    amiibos_merged = merge_amiibo(amiibos_csv, amiibos_api)

    print("Writing merged data back to CSV...")
    write_amiibo_to_csv(amiibos_merged, proj_dir)
    print(f"Found {len(amiibos_merged)} total amiibo records.")
    
    print("\nGenerating C source file for amiibos (db_amiibo.c)...")
    gen_amiibo_data_c_file(amiibos_merged, proj_dir)

    print("Reading game and link data...")
    games = read_games_from_csv(proj_dir)
    links = read_link_from_csv(proj_dir)
    links = gen_other_link(amiibos_merged, links)
    
    print("\nGenerating C source file for games (db_game.c)...")
    gen_amiibo_game_c_file(games, links, proj_dir)

    print("Generating C source file for links (db_link.c)...")
    gen_amiibo_link_c_file(links, proj_dir)
    
    print("\n✅ All tasks completed successfully!")
