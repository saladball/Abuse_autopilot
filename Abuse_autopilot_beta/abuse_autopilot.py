import csv
import requests
from urllib.parse import urlparse
import re
from socket import getaddrinfo
import geoip2.database
import datetime

i = 1

# 국가 코드를 한국어 국가 이름으로 매핑
country_code_to_korean = {
    'AF': '아프가니스탄',
    'AX': '올란드 제도',
    'AL': '알바니아',
    'DZ': '알제리',
    'AS': '아메리칸 사모아',
    'AD': '안도라',
    'AO': '앙골라',
    'AI': '앵귈라',
    'AQ': '남극',
    'AG': '앤티가 바부다',
    'AR': '아르헨티나',
    'AM': '아르메니아',
    'AW': '아루바',
    'AU': '호주',
    'AT': '오스트리아',
    'AZ': '아제르바이잔',
    'BS': '바하마',
    'BH': '바레인',
    'BD': '방글라데시',
    'BB': '바베이도스',
    'BY': '벨라루스',
    'BE': '벨기에',
    'BZ': '벨리즈',
    'BJ': '베냉',
    'BM': '버뮤다',
    'BT': '부탄',
    'BO': '볼리비아',
    'BQ': '보네르, 신트 유스타티우스 및 사바',
    'BA': '보스니아 헤르체고비나',
    'BW': '보츠와나',
    'BV': '부베 섬',
    'BR': '브라질',
    'IO': '영국령 인도양 지역',
    'BN': '브루나이',
    'BG': '불가리아',
    'BF': '부르키나파소',
    'BI': '부룬디',
    'CV': '카보베르데',
    'KH': '캄보디아',
    'CM': '카메룬',
    'CA': '캐나다',
    'KY': '케이맨 제도',
    'CF': '중앙아프리카 공화국',
    'TD': '차드',
    'CL': '칠레',
    'CN': '중국',
    'CX': '크리스마스 섬',
    'CC': '코코스 제도',
    'CO': '콜롬비아',
    'KM': '코모로',
    'CD': '콩고 민주 공화국',
    'CG': '콩고 공화국',
    'CK': '쿡 제도',
    'CR': '코스타리카',
    'CI': '코트디부아르',
    'HR': '크로아티아',
    'CU': '쿠바',
    'CW': '퀴라소',
    'CY': '키프로스',
    'CZ': '체코',
    'DK': '덴마크',
    'DJ': '지부티',
    'DM': '도미니카',
    'DO': '도미니카 공화국',
    'EC': '에콰도르',
    'EG': '이집트',
    'SV': '엘살바도르',
    'GQ': '적도 기니',
    'ER': '에리트레아',
    'EE': '에스토니아',
    'SZ': '에스와티니',
    'ET': '이디오피아',
    'FK': '포클랜드 제도',
    'FO': '페로 제도',
    'FJ': '피지',
    'FI': '핀란드',
    'FR': '프랑스',
    'GF': '프랑스령 기아나',
    'PF': '프랑스령 폴리네시아',
    'TF': '프랑스령 남부 및 남극 지역',
    'GA': '가봉',
    'GM': '감비아',
    'GE': '조지아',
    'DE': '독일',
    'GH': '가나',
    'GI': '지브롤터',
    'GR': '그리스',
    'GL': '그린란드',
    'GD': '그레나다',
    'GP': '과들루프',
    'GU': '괌',
    'GT': '과테말라',
    'GG': '건지',
    'GN': '기니',
    'GW': '기니비사우',
    'GY': '가이아나',
    'HT': '아이티',
    'HM': '허드 맥도널드 제도',
    'VA': '바티칸',
    'HN': '온두라스',
    'HK': '홍콩',
    'HU': '헝가리',
    'IS': '아이슬란드',
    'IN': '인도',
    'ID': '인도네시아',
    'IR': '이란',
    'IQ': '이라크',
    'IE': '아일랜드',
    'IM': '맨 섬',
    'IL': '이스라엘',
    'IT': '이탈리아',
    'JM': '자메이카',
    'JP': '일본',
    'JE': '저지',
    'JO': '요르단',
    'KZ': '카자흐스탄',
    'KE': '케냐',
    'KI': '키리바시',
    'KP': '북한',
    'KR': '대한민국',
    'KW': '쿠웨이트',
    'KG': '키르기스스탄',
    'LA': '라오스',
    'LV': '라트비아',
    'LB': '레바논',
    'LS': '레소토',
    'LR': '라이베리아',
    'LY': '리비아',
    'LI': '리히텐슈타인',
    'LT': '리투아니아',
    'LU': '룩셈부르크',
    'MO': '마카오',
    'MG': '마다가스카르',
    'MW': '말라위',
    'MY': '말레이시아',
    'MV': '몰디브',
    'ML': '말리',
    'MT': '몰타',
    'MH': '마셜 제도',
    'MQ': '마르티니크',
    'MR': '모리타니',
    'MU': '모리셔스',
    'YT': '마요트',
    'MX': '멕시코',
    'FM': '미크로네시아',
    'MD': '몰도바',
    'MC': '모나코',
    'MN': '몽골',
    'ME': '몬테네그로',
    'MS': '몬트세랫',
    'MA': '모로코',
    'MZ': '모잠비크',
    'MM': '미얀마',
    'NA': '나미비아',
    'NR': '나우루',
    'NP': '네팔',
    'NL': '네덜란드',
    'NC': '뉴칼레도니아',
    'NZ': '뉴질랜드',
    'NI': '니카라과',
    'NE': '니제르',
    'NG': '나이지리아',
    'NU': '니우에',
    'NF': '노퍽섬',
    'MK': '북마케도니아',
    'MP': '북마리아나 제도',
    'NO': '노르웨이',
    'OM': '오만',
    'PK': '파키스탄',
    'PW': '팔라우',
    'PS': '팔레스타인',
    'PA': '파나마',
    'PG': '파푸아뉴기니',
    'PY': '파라과이',
    'PE': '페루',
    'PH': '필리핀',
    'PN': '핏케언 제도',
    'PL': '폴란드',
    'PT': '포르투갈',
    'PR': '푸에르토리코',
    'QA': '카타르',
    'RE': '레위니옹',
    'RO': '루마니아',
    'RU': '러시아',
    'RW': '르완다',
    'BL': '생바르텔레미',
    'SH': '세인트헬레나',
    'KN': '세인트키츠 네비스',
    'LC': '세인트루시아',
    'MF': '생마르탱',
    'PM': '생피에르 미클롱',
    'VC': '세인트빈센트 그레나딘',
    'WS': '사모아',
    'SM': '산마리노',
    'ST': '상투메 프린시페',
    'SA': '사우디아라비아',
    'SN': '세네갈',
    'RS': '세르비아',
    'SC': '세이셸',
    'SL': '시에라리온',
    'SG': '싱가포르',
    'SX': '신트마르턴',
    'SK': '슬로바키아',
    'SI': '슬로베니아',
    'SB': '솔로몬 제도',
    'SO': '소말리아',
    'ZA': '남아프리카',
    'GS': '사우스조지아 사우스샌드위치 제도',
    'SS': '남수단',
    'ES': '스페인',
    'LK': '스리랑카',
    'SD': '수단',
    'SR': '수리남',
    'SJ': '스발바르드 얀마옌 제도',
    'SE': '스웨덴',
    'CH': '스위스',
    'SY': '시리아',
    'TW': '대만',
    'TJ': '타지키스탄',
    'TZ': '탄자니아',
    'TH': '태국',
    'TL': '동티모르',
    'TG': '토고',
    'TK': '토켈라우',
    'TO': '통가',
    'TT': '트리니다드 토바고',
    'TN': '튀니지',
    'TR': '터키',
    'TM': '투르크메니스탄',
    'TC': '터크스 케이커스 제도',
    'TV': '투발루',
    'UG': '우간다',
    'UA': '우크라이나',
    'AE': '아랍 에미리트',
    'GB': '영국',
    'US': '미국',
    'UM': '미국령 군소 제도',
    'UY': '우루과이',
    'UZ': '우즈베키스탄',
    'VU': '바누아투',
    'VE': '베네수엘라',
    'VN': '베트남',
    'YE': '예멘',
    'ZM': '잠비아',
    'ZW': '짐바브웨'
}

# 국가 코드를 한국어 국가 이름으로 변환하는 함수
def get_korean_country_name(country_code):
    return country_code_to_korean.get(country_code, 'None')

def get_country(reader, ip_address):
    try:
        response = reader.country(ip_address)
        return response.country.iso_code
    except:
        return 'None'

# 다운로드 URL 지정
url = "https://urlhaus.abuse.ch/downloads/csv_recent/"

# 파일 다운로드
response = requests.get(url)
text_data = response.text.splitlines()

# 텍스트 데이터를 CSV 형식으로 변환
reader = csv.reader(text_data)

# 3열에서 URL 추출 (3열이 없거나 빈 행을 무시)
urls = [row[2] for row in reader if len(row) > 2 and row[2]]

# URL에서 "http://" 또는 "https://"부터 첫 번째 "/"까지의 값을 추출
domains = [urlparse(url).netloc.split(':')[0] for url in urls]

# 중복 값 제거
unique_domains = list(set(domains))

# IP 주소와 도메인 이름 구분
ip_regex = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
domain_name_regex = re.compile(r'(?:(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,6})')
ips = [domain for domain in unique_domains if ip_regex.fullmatch(domain)]
domains = [domain for domain in unique_domains if domain_name_regex.fullmatch(domain)]

# 요청된 개수만큼 IP 주소와 도메인 이름 선택
selected_ips = ips[:198]
selected_domains = domains[:2] if len(domains) >= 2 else domains

# 선택된 IP 주소와 도메인 이름을 하나의 리스트로 결합
final_data = selected_ips + selected_domains

# GeoLite2 데이터베이스 읽기
reader = geoip2.database.Reader('GeoLite2-Country.mmdb')

today = datetime.datetime.today().strftime('%y%m%d')

filename = f"{today}_재정정보원.csv"

# 최종 데이터를 CSV 파일로 저장
with open(f"{filename}", 'w', newline='', encoding = 'utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['URL', '공격 IP', '공격국가'])
    for domain in final_data:
        if ip_regex.fullmatch(domain):
            country_code = get_country(reader, domain)
        else:
            ip_address = getaddrinfo(domain, None)[0][4][0]
            country_code = get_country(reader, ip_address)
        country_name = get_korean_country_name(country_code)
        if i <= 198:
            writer.writerow(['', domain, country_name])
        else:
            writer.writerow([domain, '', country_name])
        i = i+1

# GeoLite2 데이터베이스 닫기
reader.close()
