# cinema_ticketing.py
# 簡易電影院售票系統核心邏輯實作
# 功能涵蓋：資料庫初始化、場次與座位管理、票價計算、購票流程、交易記錄與簡單報表  

import sqlite3         # SQLite 輕量資料庫
import os              # 檔案存在檢查
import datetime        # 處理日期時間
import json            # 若需儲存複雜欄位（選擇座位清單等）
import uuid            # 生成交易或票券唯一 id

DB_FILE = "cinema.db"  # SQLite 檔名

# ---------------------------
# 1. Database 初始化與範例資料
# ---------------------------

def init_db(db_file = DB_FILE):
    """建立資料庫與基本表格（如果尚未存在），並加入範例資料。"""
    first_time = not os.path.exists(db_file)  # 檢查檔案是否存在
    conn = sqlite3.connect(db_file)           # 連線
    c = conn.cursor()                         # 取得 cursor

    # 建表：movies（電影）、halls（廳院）、showtimes（場次）、seats（座位）、items（加購品）、transactions（交易）、tickets（票券）
    c.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        rating TEXT NOT NULL  -- e.g., "G", "PG-12", "R"
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS halls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        seat_type TEXT NOT NULL  -- 'reserved' or 'general'
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS showtimes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER NOT NULL,
        hall_id INTEGER NOT NULL,
        start_time TEXT NOT NULL,  -- ISO datetime
        base_price REAL NOT NULL,
        is_first_run INTEGER NOT NULL,  -- 1 = 首輪 (reserved)，0 = 次輪 (可能 general)
        FOREIGN KEY(movie_id) REFERENCES movies(id),
        FOREIGN KEY(hall_id) REFERENCES halls(id)
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS seats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        showtime_id INTEGER NOT NULL,
        seat_label TEXT NOT NULL,  -- e.g., "A1"
        status TEXT NOT NULL,      -- 'available', 'sold'
        FOREIGN KEY(showtime_id) REFERENCES showtimes(id)
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id TEXT PRIMARY KEY,       -- using uuid
        showtime_id INTEGER,
        datetime TEXT,
        buyer_name TEXT,
        buyer_age INTEGER,
        buyer_identity TEXT,      -- e.g., 'regular','student','military','companion'
        seats TEXT,               -- JSON list of seat labels (or empty for general)
        tickets_count INTEGER,
        base_amount REAL,
        items_amount REAL,
        total_amount REAL,
        ticket_type TEXT,         -- 'electronic' or 'physical'
        FOREIGN KEY(showtime_id) REFERENCES showtimes(id)
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS ticket_lines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id TEXT,
        ticket_label TEXT,   -- single ticket id
        price REAL,
        FOREIGN KEY(transaction_id) REFERENCES transactions(id)
    )
    """)
    conn.commit()

    # 若第一次建立 DB，塞入範例資料（4 廳院、數部電影、場次、座位、加購品）
    if first_time:
        # 範例電影
        movies = [
            ("The Family Adventure", "G"),
            ("Love in Taipei", "PG-12"),
            ("Horror Night", "R"),        # 限制級
            ("Sci-Fi Epic", "PG-12")
        ]
        c.executemany("INSERT INTO movies (title, rating) VALUES (?, ?)", movies)

        # 四個廳院：可設定其中一些為 reserved / general
        halls = [
            ("Hall 1", "reserved"),
            ("Hall 2", "reserved"),
            ("Hall 3", "general"),   # 自由座
            ("Hall 4", "reserved")
        ]
        c.executemany("INSERT INTO halls (name, seat_type) VALUES (?, ?)", halls)

        # 建立幾個場次（今天與隔日）
        now = datetime.datetime.now()
        base_hours = [10, 13, 16, 19]  # 4 個時段
        # 將前三部電影分配到 4 個廳不同時段（示範）
        c.execute("SELECT id FROM movies")
        movie_ids = [r[0] for r in c.fetchall()]

        c.execute("SELECT id FROM halls")
        hall_ids = [r[0] for r in c.fetchall()]

        showtimes = []
        for i, mh in enumerate([(movie_ids[0], hall_ids[0]), (movie_ids[1], hall_ids[1]),
                                (movie_ids[2], hall_ids[2]), (movie_ids[3], hall_ids[3])]):
            movie_id, hall_id = mh
            # 建兩天的同時段（首輪與次輪示範）
            for day_offset in [0, 1]:
                for h in base_hours:
                    start = (now + datetime.timedelta(days=day_offset)).replace(hour=h, minute=0, second=0, microsecond=0)
                    is_first = 1 if day_offset == 0 and h in (10,13) else 0  # 模擬首輪 / 次輪
                    base_price = 250.0  # 基本票價
                    showtimes.append((movie_id, hall_id, start.isoformat(), base_price, is_first))
        c.executemany("INSERT INTO showtimes (movie_id, hall_id, start_time, base_price, is_first_run) VALUES (?, ?, ?, ?, ?)", showtimes)

        # 加購品
        items = [("Small Popcorn", 80.0), ("Large Popcorn", 120.0), ("Soda", 60.0), ("Combo (Large Popcorn + Soda)", 170.0)]
        c.executemany("INSERT INTO items (name, price) VALUES (?, ?)", items)

        conn.commit()

        # 建立座位資料（只對「對號入座」場次建立座位表）
        # 我們為每個 reserved hall 的每個 showtime 建立 5 排 × 8 座 = 40 個座位
        c.execute("""
        SELECT s.id, h.seat_type FROM showtimes s
        JOIN halls h ON s.hall_id = h.id
        """)
        show_rows = c.fetchall()
        for show_id, seat_type in show_rows:
            if seat_type == "reserved":
                # 建立座位標籤 A1..A8, B1..B8 ...
                for r in range(5):  # 5 rows A..E
                    row_letter = chr(ord('A') + r)
                    for num in range(1, 9):  # 8 seats per row
                        label = f"{row_letter}{num}"
                        c.execute("INSERT INTO seats (showtime_id, seat_label, status) VALUES (?, ?, ?)", (show_id, label, "available"))
        conn.commit()

    conn.close()

# ---------------------------
# 2. 輔助函式（資料取得、顯示）
# ---------------------------

def list_showtimes(conn):
    """列出所有未來的場次（簡單 CLI 顯示）"""
    c = conn.cursor()
    now_iso = datetime.datetime.now().isoformat()
    c.execute("""
    SELECT st.id, m.title, h.name, h.seat_type, st.start_time, st.base_price, st.is_first_run, m.rating
    FROM showtimes st
    JOIN movies m ON st.movie_id = m.id
    JOIN halls h ON st.hall_id = h.id
    WHERE st.start_time >= ?
    ORDER BY st.start_time
    """, (now_iso,))
    rows = c.fetchall()
    # 顯示
    print("\n可售場次：")
    for row in rows:
        sid, title, hall, seat_type, start_time, price, is_first, rating = row
        start_fmt = datetime.datetime.fromisoformat(start_time).strftime("%Y-%m-%d %H:%M")
        mode = "首輪(對號入座)" if is_first == 1 else ("自由座" if seat_type == "general" else "次輪(對號/視設定)")
        print(f"[{sid}] {start_fmt} | {title} | {hall} | {mode} | 評級:{rating} | 基本票價:{price}")

def get_showtime(conn, show_id):
    """回傳指定場次資訊（包含 movie rating 與 hall seat_type）"""
    c = conn.cursor()
    c.execute("""
    SELECT st.id, st.movie_id, m.title, m.rating, st.hall_id, h.name, h.seat_type, st.start_time, st.base_price, st.is_first_run
    FROM showtimes st
    JOIN movies m ON st.movie_id = m.id
    JOIN halls h ON st.hall_id = h.id
    WHERE st.id = ?
    """, (show_id,))
    return c.fetchone()

def available_seats(conn, show_id):
    """回傳可用座位清單（對號入座場次使用）"""
    c = conn.cursor()
    c.execute("SELECT seat_label FROM seats WHERE showtime_id = ? AND status = 'available' ORDER BY seat_label", (show_id,))
    return [r[0] for r in c.fetchall()]

def sell_seat(conn, show_id, seat_label):
    """將指定座位標記為 sold，回傳是否成功"""
    c = conn.cursor()
    # 以 UPDATE + rowcount 確保原本是 available 才改成 sold（避免 race condition）
    c.execute("UPDATE seats SET status = 'sold' WHERE showtime_id = ? AND seat_label = ? AND status = 'available'", (show_id, seat_label))
    conn.commit()
    return c.rowcount == 1  # 若有更新則成功

def count_available_general(conn, show_id):
    """對於自由座，計算剩餘可售座位（若不在 DB 建表，可用容量減去已售張數）"""
    # 在此簡化處理：預設 general 廳容量為 100（可根據 hall 調整）
    c = conn.cursor()
    # 取得HallType並決定容量（這裡固定容量 100）
    c.execute("SELECT h.seat_type FROM showtimes s JOIN halls h ON s.hall_id = h.id WHERE s.id = ?", (show_id,))
    seat_type_row = c.fetchone()
    if seat_type_row is None:
        return 0
    capacity = 100
    # 計算已售張數（transaction 中 tickets_count）
    c.execute("SELECT SUM(tickets_count) FROM transactions WHERE showtime_id = ?", (show_id,))
    sold = c.fetchone()[0] or 0
    return max(0, capacity - sold)

def list_items(conn):
    """列出可加購品項"""
    c = conn.cursor()
    c.execute("SELECT id, name, price FROM items")
    return c.fetchall()

# ---------------------------
# 3. 價格計算策略（可擴充）
# ---------------------------

def calculate_ticket_price(base_price, age, identity, showtime_row):
    """
    計算單張票價（可依年齡、身份與場次規則做調整）
    - base_price: 場次基本票價
    - age: 購票者年齡（int）
    - identity: 'regular', 'student', 'military', 'companion'
    - showtime_row: 取自 get_showtime 的整行資訊（可依 rating 或時間做加價/折扣）
    """
    # 解構 showtime_row
    # showtime_row indices: 0=id,1=movie_id,2=title,3=rating,4=hall_id,5=hall_name,6=seat_type,7=start_time,8=base_price,9=is_first_run
    rating = showtime_row[3]
    start_time_iso = showtime_row[7]
    is_first = showtime_row[9]

    price = base_price  # 從基本票價開始

    # 年齡折扣/加價範例
    if age < 3:
        price = 0.0  # 幼兒免費（示例）
    elif age < 12:
        price *= 0.5  # 兒童半價
    elif age >= 65:
        price *= 0.8  # 長者 8 折

    # 身份優惠
    if identity == "student":
        price *= 0.85  # 學生 85 折
    elif identity == "military":
        price *= 0.8   # 軍警 8 折
    elif identity == "companion":
        price *= 0.9   # 陪伴者 9 折（示例）

    # 首輪或熱門場次可以加價（示意）
    if is_first == 1:
        price += 20.0

    # 輔導/限制級場次不打折（示例）：若 rating == "R" 則不適用某些折扣（此處簡化處理）
    if rating == "R" and age < 18:
        # 未成年不得觀賞，這裡應由上層檢查；若到達這裡仍計算則視情況
        pass

    # 最少價位可設一個下限
    price = max(price, 0.0)
    # 四捨五入到整數
    return round(price, 2)

# ---------------------------
# 4. 主售票流程（核心）
# ---------------------------

def purchase_flow():
    """主售票 CLI 流程：選場次 → 輸入購買人資訊 → 選座/計算價錢 → 加購 → 確認 → 寫入 DB"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # 使 fetch 結果可用 key 存取
    list_showtimes(conn)
    show_id = int(input("\n請輸入欲購買之場次 ID（數字）：").strip())
    st = get_showtime(conn, show_id)
    if not st:
        print("找不到該場次。")
        conn.close()
        return

    # 顯示場次詳細
    st_id, movie_id, title, rating, hall_id, hall_name, seat_type, start_time_iso, base_price, is_first = st
    start_fmt = datetime.datetime.fromisoformat(start_time_iso).strftime("%Y-%m-%d %H:%M")
    print(f"你選擇：{title} | {hall_name} | {start_fmt} | 評級:{rating} | 座位型態:{seat_type}")

    # 若評級需要年齡查驗（例如 R）、且購票者無法辨識年齡，提示出示證件
    print("\n請輸入購買人資訊：")
    buyer_name = input("購買人姓名：").strip()
    # 轉成數字時要處理錯誤輸入
    while True:
        try:
            buyer_age = int(input("購買人年齡（數字）：").strip())
            break
        except ValueError:
            print("請輸入有效年齡（數字）。")
    # 身份選項
    print("身份選項：1. regular 2. student 3. military 4. companion")
    id_map = {"1":"regular","2":"student","3":"military","4":"companion"}
    identity = id_map.get(input("請選擇身份代碼（預設 1）：").strip() or "1")

    # 若為限制級 (R)，檢查年齡
    if rating == "R" and buyer_age < 18:
        # 依規定未成年不宜進場；此處示警並終止交易
        print("此場次為限制級 (R)，購票者年齡不足 18 歲，請勿購票。若為陪同者請使用陪伴者身分。")
        conn.close()
        return
    elif rating in ("PG-12", "R"):
        # 若人員無法辨識年齡，系統會提示出示證件；這裡模擬確認
        need_id_check = True
        print("系統提示：本場次為分級電影，若無法辨識年齡請於入場前出示證件。")
    else:
        need_id_check = False

    # 決定購票張數
    while True:
        try:
            qty = int(input("欲購買票張數：").strip())
            if qty <= 0:
                raise ValueError
            break
        except ValueError:
            print("請輸入有效張數（整數，大於 0）。")

    # 座位處理
    chosen_seats = []
    if seat_type == "reserved" or is_first == 1:
        # 對號入座：顯示可選座位並讓使用者挑選
        avail = available_seats(conn, show_id)
        if len(avail) == 0:
            print("抱歉，本場次所有座位已售完。")
            conn.close()
            return
        print(f"可選座位（共 {len(avail)} 個）：")
        print(", ".join(avail))
        # 讓使用者挑選 qty 個座位
        while len(chosen_seats) < qty:
            s = input(f"請輸入第 {len(chosen_seats)+1} 張票欲選座位（例如 A1）：").strip().upper()
            if s not in avail:
                print("該座位不可選（可能不存在或已被售出），請重新選擇。")
                continue
            # 嘗試寫入座位（原子性更新）
            success = sell_seat(conn, show_id, s)
            if not success:
                print("座位在你選取前被其他交易售出，請改選其他座位。")
                avail = available_seats(conn, show_id)  # 重新取得可用座位
                continue
            chosen_seats.append(s)
            # 更新可選清單
            avail.remove(s)
        print("已選座位：", chosen_seats)
        tickets_count = qty
    else:
        # 自由座：只檢查是否有足夠剩餘座位
        remaining = count_available_general(conn, show_id)
        if remaining < qty:
            print(f"剩餘座位不足，僅剩 {remaining} 席。")
            conn.close()
            return
        # 註：自由座通常不選座，系統只記錄數量
        print(f"自由座訂購成功（系統僅保留 {qty} 張座位），剩餘可售：{remaining - qty}")
        tickets_count = qty

    # 計算票價：每張依年齡/身份計價，然後總和
    per_ticket_price = calculate_ticket_price(base_price, buyer_age, identity, st)
    base_amount = round(per_ticket_price * tickets_count, 2)
    print(f"單張票價：{per_ticket_price} 元，票款小計：{base_amount} 元")

    # 加購處理
    items = list_items(conn)
    print("\n可加購項目：")
    for it in items:
        print(f"{it[0]}. {it[1]} - {it[2]} 元")
    chosen_items = []
    items_amount = 0.0
    while True:
        choose = input("輸入加購品 id（或 Enter 結束）：").strip()
        if choose == "":
            break
        try:
            iid = int(choose)
        except ValueError:
            print("請輸入數字 id。")
            continue
        # 找到該 item
        found = None
        for it in items:
            if it[0] == iid:
                found = it
                break
        if not found:
            print("找不到該加購品 id，請重新輸入。")
            continue
        # 數量
        while True:
            try:
                q = int(input(f"請輸入 {found[1]} 數量：").strip())
                if q <= 0:
                    raise ValueError
                break
            except ValueError:
                print("請輸入大於 0 的整數。")
        chosen_items.append((found[1], found[2], q))
        items_amount += found[2] * q
        print(f"已加入 {found[1]} x {q}")

    total_amount = round(base_amount + items_amount, 2)
    print("\n--- 購票摘要 ---")
    print(f"購買人：{buyer_name} ({buyer_age}) 身份：{identity}")
    print(f"票張數：{tickets_count} | 座位：{chosen_seats if chosen_seats else '自由座/不指定'}")
    print(f"票款小計：{base_amount} 元")
    print(f"加購小計：{items_amount} 元")
    print(f"總計：{total_amount} 元")

    # 選擇票券型態：電子 or 實體；單張或批次列印（模擬）
    ticket_type = input("票券類型（輸入 'e' 為電子票，否則實體票）：").strip().lower()
    ticket_type = "electronic" if ticket_type == "e" else "physical"

    # 確認是否完成交易
    confirm = input("確認付款並完成交易？(y/n)：").strip().lower()
    if confirm != "y":
        # 若使用者取消，釋放先前已鎖定的座位（若是對號入座）
        if chosen_seats:
            c = conn.cursor()
            for s in chosen_seats:
                c.execute("UPDATE seats SET status = 'available' WHERE showtime_id = ? AND seat_label = ?", (show_id, s))
            conn.commit()
        print("交易取消。")
        conn.close()
        return

    # 交易寫入資料庫
    txn_id = str(uuid.uuid4())
    now = datetime.datetime.now().isoformat()
    seats_json = json.dumps(chosen_seats)
    c = conn.cursor()
    c.execute("""
    INSERT INTO transactions (id, showtime_id, datetime, buyer_name, buyer_age, buyer_identity, seats, tickets_count, base_amount, items_amount, total_amount, ticket_type)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (txn_id, show_id, now, buyer_name, buyer_age, identity, seats_json, tickets_count, base_amount, items_amount, total_amount, ticket_type))
    # 建立 ticket_lines（每張票一行，方便報表）
    for i in range(tickets_count):
        ticket_label = f"T-{txn_id[:8]}-{i+1}"
        c.execute("INSERT INTO ticket_lines (transaction_id, ticket_label, price) VALUES (?, ?, ?)", (txn_id, ticket_label, per_ticket_price))
    conn.commit()

    # 列印票券（模擬）：單張或批次（此處顯示於終端）
    print("\n--- 票券列印 ---")
    for i in range(tickets_count):
        ticket_label = f"T-{txn_id[:8]}-{i+1}"
        print("##########################")
        print(f"電影：{title}")
        print(f"場次：{start_fmt}  廳院：{hall_name}")
        if chosen_seats:
            print(f"座位：{chosen_seats[i]}")
        else:
            print("座位：自由座（入場憑票）")
        print(f"票券編號：{ticket_label}")
        print(f"票價：{per_ticket_price} 元")
        print(f"票種：{ticket_type}")
        print("##########################")

    # 列印發票/收據（模擬）
    print("\n--- 收據 ---")
    print(f"交易編號：{txn_id}")
    print(f"購買人：{buyer_name}  身分：{identity}")
    print(f"票款：{base_amount}  加購：{items_amount}  合計：{total_amount}")
    print("----------------------------")
    print("交易完成，已記錄於系統。")

    conn.close()

# ---------------------------
# 5. 報表與對帳功能
# ---------------------------

def simple_reports():
    """顯示簡單報表：總營收、各場次營收、加購品統計"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # 今日總營收
    today = datetime.date.today().isoformat()
    start_today = today + "T00:00:00"
    end_today = today + "T23:59:59"
    c.execute("SELECT SUM(total_amount) FROM transactions WHERE datetime BETWEEN ? AND ?", (start_today, end_today))
    total = c.fetchone()[0] or 0.0
    print(f"\n=== 今日總營收 ({today})：{total} 元 ===")

    # 各場次營收（取前 10 筆）
    c.execute("""
    SELECT st.id, m.title, st.start_time, SUM(t.total_amount) as revenue
    FROM showtimes st
    LEFT JOIN transactions t ON st.id = t.showtime_id
    LEFT JOIN movies m ON st.movie_id = m.id
    WHERE st.start_time BETWEEN ? AND ?
    GROUP BY st.id
    ORDER BY st.start_time
    LIMIT 10
    """, (start_today, end_today))
    rows = c.fetchall()
    print("\n場次營收（今日）:")
    for r in rows:
        sid, title, stime, rev = r
        stfmt = datetime.datetime.fromisoformat(stime).strftime("%Y-%m-%d %H:%M")
        rev = rev or 0.0
        print(f"[{sid}] {stfmt} | {title} | 營收：{rev} 元")

    # 加購品統計
    # 注意：本範例 items 於 transactions 中僅以總額儲存，若要詳細分析需另建 transaction_items 關聯表
    # 這裡只顯示總加購收入
    c.execute("SELECT SUM(items_amount) FROM transactions WHERE datetime BETWEEN ? AND ?", (start_today, end_today))
    items_total = c.fetchone()[0] or 0.0
    print(f"\n今日加購品收入：{items_total} 元")

    conn.close()

# ---------------------------
# 6. 主程式入口（簡易 CLI）
# ---------------------------

def main():
    """簡單 CLI 介面入口"""
    init_db()
    while True:
        print("\n====== 電影院售票系統（簡化版） ======")
        print("1. 列出場次並購票")
        print("2. 顯示簡單報表（今日）")
        print("3. 退出")
        choice = input("請選擇：").strip()
        if choice == "1":
            purchase_flow()
        elif choice == "2":
            simple_reports()
        elif choice == "3":
            print("再見！")
            break
        else:
            print("無效選項，請重新輸入。")

if __name__ == "__main__":
    main()

