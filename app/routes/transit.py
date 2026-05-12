from flask import Blueprint, render_template, request, jsonify

# 定義 F-01 一站式平台藍圖
transit_bp = Blueprint('transit', __name__)

# ─────────────────────────────────────────────
# 台中常用站點清單（供前端 autocomplete 使用）
# ─────────────────────────────────────────────
COMMON_STATIONS = [
    "台中火車站", "台中高鐵站", "逢甲商圈", "一中街",
    "中友百貨", "台中市政府", "秀泰廣場", "中科園區",
    "台中科大", "靜宜大學", "朝陽科大", "東海大學",
    "國立自然科學博物館", "國立台中美術館", "台中機場",
    "台中慈濟醫院", "中國醫藥大學", "台中榮總",
    "捷運文心森林公園站", "捷運北屯總站", "捷運高鐵台中站",
    "捷運烏日站", "捷運台中站", "捷運市政府站",
]

# ─────────────────────────────────────────────
# 模擬路線結果資料（F-02 串接 TDX API 後會取代此段）
# ─────────────────────────────────────────────
MOCK_ROUTES = {
    ("台中火車站", "逢甲商圈"): [
        {
            "mode": "捷運 + 公車",
            "icon": "🚇🚌",
            "steps": [
                {"type": "walk",   "desc": "步行至台中火車站捷運站",     "duration": 3,  "fare": 0},
                {"type": "metro",  "desc": "搭乘捷運藍線往高鐵台中站方向", "duration": 12, "fare": 20, "line": "藍線", "from": "台中站", "to": "市政府站"},
                {"type": "bus",    "desc": "搭乘 BRT 快捷公車 88 路",      "duration": 18, "fare": 15, "route": "88", "from": "市政府站", "to": "逢甲商圈"},
                {"type": "walk",   "desc": "步行至目的地",                 "duration": 5,  "fare": 0},
            ],
            "total_time": 38,
            "total_fare": 35,
            "transfers": 1,
            "depart_time": "依班次",
            "arrive_time": "約 38 分鐘後",
            "recommend": True,
        },
        {
            "mode": "公車直達",
            "icon": "🚌",
            "steps": [
                {"type": "walk",   "desc": "步行至台中火車站前站牌",  "duration": 2,  "fare": 0},
                {"type": "bus",    "desc": "搭乘公車 35 路",           "duration": 45, "fare": 30, "route": "35", "from": "台中火車站", "to": "逢甲"},
                {"type": "walk",   "desc": "步行至逢甲商圈",           "duration": 5,  "fare": 0},
            ],
            "total_time": 52,
            "total_fare": 30,
            "transfers": 0,
            "depart_time": "依班次",
            "arrive_time": "約 52 分鐘後",
            "recommend": False,
        },
    ],
    ("台中火車站", "台中高鐵站"): [
        {
            "mode": "捷運直達",
            "icon": "🚇",
            "steps": [
                {"type": "walk",   "desc": "步行至台中捷運站入口",          "duration": 3,  "fare": 0},
                {"type": "metro",  "desc": "搭乘捷運藍線往高鐵台中站",      "duration": 25, "fare": 50, "line": "藍線", "from": "台中站", "to": "高鐵台中站"},
                {"type": "walk",   "desc": "步行至高鐵站大廳",              "duration": 5,  "fare": 0},
            ],
            "total_time": 33,
            "total_fare": 50,
            "transfers": 0,
            "depart_time": "依班次",
            "arrive_time": "約 33 分鐘後",
            "recommend": True,
        },
    ],
}


# ─────────────────────────────────────────────
# F-01 主要路由
# ─────────────────────────────────────────────

@transit_bp.route('/')
def index():
    """F-01 首頁：一站式查詢平台"""
    return render_template('transit_search.html', stations=COMMON_STATIONS)


@transit_bp.route('/search', methods=['GET', 'POST'])
def search():
    """
    路線查詢端點。
    GET  /search?from=台中火車站&to=逢甲商圈  → 回傳 HTML 頁面（含結果）
    POST /search  (JSON body)               → 回傳 JSON 結果（供前端 AJAX 呼叫）
    """
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        origin      = (data.get('from') or '').strip()
        destination = (data.get('to')   or '').strip()
    else:
        origin      = request.args.get('from', '').strip()
        destination = request.args.get('to',   '').strip()

    results = []
    error   = None

    if origin and destination:
        if origin == destination:
            error = '起點與終點不能相同！'
        else:
            # 先從模擬資料查找（key 順序不限）
            key = (origin, destination)
            rev = (destination, origin)
            if key in MOCK_ROUTES:
                results = MOCK_ROUTES[key]
            elif rev in MOCK_ROUTES:
                # 反向路線：把步驟反轉並調整描述
                results = MOCK_ROUTES[rev]
            else:
                # 若無模擬資料，回傳通用佔位結果
                results = _generic_route(origin, destination)

    if request.method == 'POST':
        return jsonify({
            'origin':      origin,
            'destination': destination,
            'results':     results,
            'error':       error,
        })

    return render_template(
        'transit_search.html',
        stations=COMMON_STATIONS,
        origin=origin,
        destination=destination,
        results=results,
        error=error,
        searched=(origin and destination),
    )


@transit_bp.route('/api/stations')
def api_stations():
    """回傳站點清單 JSON（供前端 autocomplete）"""
    q = request.args.get('q', '').strip()
    if q:
        matched = [s for s in COMMON_STATIONS if q in s]
    else:
        matched = COMMON_STATIONS
    return jsonify(matched)


# ─────────────────────────────────────────────
# 內部工具函式
# ─────────────────────────────────────────────

def _generic_route(origin: str, destination: str) -> list:
    """
    當模擬資料庫無對應路線時，產生通用佔位路線。
    F-02（林紫誼）串接 TDX API 後，此函式可替換為真實資料。
    """
    return [
        {
            "mode": "建議路線（預估）",
            "icon": "🚇🚌",
            "steps": [
                {"type": "walk",  "desc": f"從「{origin}」附近站牌出發", "duration": 5,  "fare": 0},
                {"type": "bus",   "desc": "搭乘適合公車路線",            "duration": 30, "fare": 30, "route": "—"},
                {"type": "walk",  "desc": f"步行至「{destination}」",     "duration": 5,  "fare": 0},
            ],
            "total_time": 40,
            "total_fare": 30,
            "transfers": 0,
            "depart_time": "依班次",
            "arrive_time": "約 40 分鐘後",
            "recommend": True,
            "note": "⚠️ 此為估算資料，正確資訊請待 TDX API 串接後顯示。",
        }
    ]
