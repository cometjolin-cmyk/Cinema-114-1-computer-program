# 簡易電影院售票系統核心邏輯實作
# 題目解讀 所需功能涵蓋：資料庫初始化、場次與座位管理、票價計算、購票流程、交易記錄與簡單報表 
#==== MVP 功能清單 ====
#1. 印出歡迎畫面 （main()) (ok)
#2. 歡迎選單 (ok)
#3. 列出場次並購票 (purchase_flow()) (OK)
#4. 顯示簡單報表 (simple_reports())
#5. 計算票價（看年齡分價制） (ok)
#6. 交易紀錄（暫存在記憶體） (ok)
import datetime
TRANSACTIONS = []
RATING_MAP = {"G": 0, "P": 6, "PG-12": 12, "PG-15": 15, "R": 18}

#1. 印出歡迎畫面 （main())
def main():
    print("\n====== 電影院售票系統（簡化版） ======")
    print("1. 列出場次並購票")
    print("2. 顯示簡單報表（今日）")
    print("3. 退出")
    choice = input("請選擇：").strip() #.strip()轉去掉字串 兩端 的空白，不會去掉中間的空格
    if choice == "1":
        movies
    elif choice == "2":
        all_change()
    elif choice == "3":
        print("再見！")
        return
    else:
        print("無效選項，請重新輸入。")


#設全域變數 Movie_time_list
Movie_time_list =  [
    {   "id" : 0,
        "movie": "Horror Night",
        "time": "19:00",
        "price": 250,
        "age": 18,            # <-- 舊有年齡欄位 (建議保留，但實際流程應以 rating 為主)
        "rating": "R",        # <-- 新增：限制級 (18 歲以上)
        "seating_type": "assigned" ,# <-- 新增：對號入座
        "seats": {
            "A1": True,
            "A2": True
            }
    },
    {
        "id": 1,
        "movie": "Love in Taipei",
        "time": "21:00",
        "price": 220,
        "age": 18,
        "rating": "PG-12",     # <-- 新增：輔導十二級 (12 歲以上)
        "seating_type": "free",     # <-- 新增：自由座
        "seat capacity": 2,
        
    }]
    #Movie_time_list = purchase_flow() 是把函式回傳的資料「拿出來」存成變數。(這段會讓程式變成無限迴圈)
    #函式內的變數不會自動傳回到外面，故需要回傳 #不建議用gobal，因為函式依賴外部狀態，修改全域變數可能影響程式其他地方，容易出錯。

#請使用者輸入電影編號，輸出可以選得座位
def choose_seats(movie):
    # 確保買座位的變數在整個函式中都可被存取？？
    buy_seat = "N/A"
    num_tickets = 1 # 預設為 1 (如果非自由座或單張購買)


    if movie['seating_type'] == "assigned":
    #對號入座的購票判斷
        print("\n座位狀態： ")
        for seat, available in movie['seats'].items():
            status = "可購買" if available else "已售出"
            print(f"{seat}: {status}")

        buy_seat = input("請輸入要購買的座位：").strip()

        # 1. 判斷座位是否存在
        if buy_seat not in movie['seats']:
            print("❌ 無此座位")
            return

        # 2. 判斷是否已售出
        elif movie['seats'][buy_seat] == False: #指哪一個變數？
            print("❌ 此座位已售出")
            return

        else :
            print("座位可購買，請輸入年齡確認")

    elif movie['seating_type'] == "free":
    #自由座的購票判斷
        seats_remaining = movie.get('seat capacity', 0)        
        print("\n座位狀態： ")
        #使用 if / elif / else 時，程式認為這些條件是互斥的（mutually exclusive），即：只有一個條件會被執行。
        #使用if 是因為：如果發生錯誤，就立即退出；否則，繼續執行下一條檢查」。這些檢查不是互斥的，它們是連續的、必須按順序通過的關卡。
        
        # 自由座的 try 區塊後，邏輯沒有連貫，導致輸入張數後，程式會直接退出，無法執行年齡判斷。這是因為 try/except 區塊並沒有告訴程式下一步該怎麼做 ＿L3 修正：將所有輸入和檢查放在一個 try/except 區塊內，並使用 if-return 模式
        try: 
            num_tickets = int(input(f"該場為自由座，目前尚餘 {seats_remaining} 個座位。請輸入購買張數：").strip())
            
            # 檢查購買張數是否有效
            if num_tickets <= 0:
                print("❌ 購買張數必須大於零。")
                return
            
            if num_tickets > seats_remaining:
                print(f"❌ 剩餘票數不足，最多只能購買 {seats_remaining} 張。")
                return
                
            # L2 修正：成功獲取張數後，為 buy_seat 賦予描述性字串
            buy_seat = f"自由座 ({num_tickets} 張)" 
            print(f"✅ 確認購買 {num_tickets} 張，進入年齡確認。")

        except ValueError:
            print("❌ 輸入格式錯誤，請輸入數字。")
            return
    else:
        # 如果電影數據設定了無效的 seating_type
        print("❌ 系統錯誤：無效的入座方式設定。")
        return
    
        


    # 3. 年齡判斷
    today = datetime.date.today()
    
    try:
        user_birth = int(input("請輸入出生年份，以確保可以購買此場電影：").strip())
    except ValueError:
        print("❌ 輸入出生年份格式錯誤。")
        return
    
    age = today.year - user_birth

    if age < RATING_MAP[movie["rating"]]: #由檢查年齡更改為提取分級年齡去比較
        print("年齡不符，不能購買此電影")
        return
    else:
        print(f"您目前{age}歲可以購買此場電影")
        confirm = input("是否確認購票？(請輸入 'y' 確認)：").strip().lower() 
        # .lower() 確保使用者輸入 Y 或 y 都能被接受
        if confirm == 'y':
        # 執行折扣選擇和購票流程 ＃為了讓使用者能輸入編號故在字典內增加tuple
            
            discount_identity_dict = {
                '1': ("學生", 0.8),  
                '2': ("早鳥", 0.7), 
                '3': ("會員", 0.5),
                '4': ("無折扣", 1.0) 
            }
            for code, (name, discount)  in discount_identity_dict.items(): #輸出優惠身份的列表
                print(f"編號： {code} __ 身份： {name}")

            identity_choice = input("請問是否有其他優惠身份(請輸入數字)").strip()
            if identity_choice in discount_identity_dict:
                identity_name, discount_rate = discount_identity_dict[identity_choice] #指定變數優惠身份和優惠率=所輸入的key的valure
                price = movie['price'] * discount_rate

                #確定購買 → 修改座位狀態
                if movie['seating_type'] == "assigned":
                    movie["seats"][buy_seat] = False 
                elif movie['seating_type'] == "free":
                    movie['seat capacity'] -= num_tickets #購票不一定只有買一張，需設變數

                print(f"\n===購票確認：應用 {identity_name} 優惠 ({int(discount_rate*10)}折)，最終票價為 {price} 元。===")

                transaction_record = {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), #strftime("%Y-%m-%d %H:%M:%S")確保了每筆交易記錄的時間格式都是一致且易於排序的
                "movie": movie["movie"],
                "seating_type": movie["seating_type"],
                "seat": buy_seat,
                "discount": f"{int(discount_rate*10)}折",
                "final_price": price, # 必須使用計算出來的最終價格
                "identity": identity_name # 儲存使用的折扣身份
                 }
                
                for a, b  in transaction_record.items(): #輸出報表的列表
                    print(f"{a} ： {b}")

                TRANSACTIONS.append(transaction_record) #將交易紀錄存入報表串列


                return identity_name, discount_rate
            else:
                print("無效的優惠身份編號，購票已取消")
                print("\n回到主選單")
        else:
            print("購票已取消。")
            print("\n回到主選單")
    return 
        



def all_change():
    sum_price = 0
    print("\n報表列印: \n")
    if not TRANSACTIONS:
        print("今日尚無交易")
    else:
        
        for index, transaction in enumerate(TRANSACTIONS):  #有做更改 #解釋emumerate():這個函式的作用是讓迴圈在遍歷 TRANSACTIONS 時，同時產生兩個值：index(索引), transaction（內部字典）
            print(f"\n======== 第 {index + 1} 筆交易 ========")
            for key, value in transaction.items():
                print(f"{key:<15}： {value}") #為什麼要<15:確保 Key 佔據至少 15 個字符寬度，讓輸出報表看起來整齊
            sum_price += int(transaction['final_price'])

    print(f"\n總交易金額： {sum_price} 元\n")   
    print("*"*15)
    print("\n電影座位現況: \n")
    for m in Movie_time_list: 
        print(f"🎬 電影： {m['movie']}")

        if m['seating_type'] == "assigned":
            # --- 對號入座邏輯 ---
            print("  [入座方式]: 對號入座")
            seats_display = [] #串列是作為 報表輸出 和 核心數據結構 之間的一個緩衝區或轉譯器 .它確保了您核心的 Movie_time_list 數據保持乾淨（只存 True/False），而輸出則可以根據您的需求，隨時調整為最清晰的格式。
        
            for seat, available in m['seats'].items():
                status = "🟢 " if available else "❌ "
                
                # 關鍵修正點：將『完整的輸出字串』存入緩衝區
                formatted_line = f"    - {seat}: {status}" 
                seats_display.append(formatted_line)

            print("  座位狀態:")
            
            # 最終輸出：遍歷緩衝區，逐行輸出已格式化的字串
            for line in seats_display:
                print(line)

            

            
        elif m['seating_type'] == "free":
            # --- 自由座邏輯 ---
            # 這裡假設您在 Movie_time_list 中新增了 'seat capacity' 欄位
            capacity = m.get('seat capacity', 0) 
            # 為了正確顯示，我們需要一個 'tickets_sold' 變數，但您的字典中沒有
            # 暫時假設 'seat capacity' 儲存的是剩餘數量 (如您在 choose_seats 中的用法)
            
            # **注意**：自由座數據結構不完善，這裡使用 seats_remaining 欄位
            seats_remaining = m.get('seat capacity', 0)

            
            print("  [入座方式]: 自由座")
            if capacity > 0:
                print(f"  剩餘票數: {seats_remaining} 張 ")
            else:
                 # 這裡可以根據總座位數減去剩餘座位數來計算已售出張數，但為了最小修改，我們直接顯示剩餘張數
                print(f"  剩餘票數: {seats_remaining} 張 ")
            
    
    

#設主要程式函式
movies = Movie_time_list #變為全區變數

def main():
    while True:
        print("\n====== 電影院售票系統（簡化版） ======")
        print("1. 列出場次並購票")
        print("2. 顯示簡單報表（今日）")
        print("3. 退出")
        choice = input("請選擇：").strip() #.strip()轉去掉字串 兩端 的空白，不會去掉中間的空格
        if choice == "1":
            # 1. 顯示場次列表，不太懂啊啊啊啊啊 
            # purchase_flow() 內部會列印場次
            list_schedules = Movie_time_list # 雖然 movies 在全域，但這裡用 list_schedules 接收回傳確保可用性
            print("電影場次公告：")
            for movie in list_schedules : #設變數movie為卡片（Movie_time_list裡，有幾個就執行幾次迴圈）
                print(f"編號: {movie['id']}, 電影: {movie['movie']}, 時間: {movie['time']}, 價格: {movie['price']}, 限制年齡: {movie['age']}, 限制級: {movie['rating']}, 入座方式: {movie['seating_type']}")
    
            # 2. 接收電影 ID #try...except ValueError： 這是一個錯誤處理機制。如果使用者不小心輸入了非數字的內容（例如 "ABC"），程式就不會崩潰，而是會執行 except 區塊，列印錯誤訊息並用 continue 回到 main() 迴圈的開頭（重新顯示選單）。
            try: 
                movie_id = int(input("請輸入想看的電影編號：").strip())
            except ValueError:
                print("❌ 輸入格式錯誤，請輸入數字編號。")
                continue #跳過當前 while True 迴圈中 main() 函式剩餘的程式碼，直接回到迴圈的頂部，重新顯示主選單
                
            # 3. 找到電影（必須使用迴圈遍歷，因為 movies 是串列）
            selected_movie = None #初始化一個變數，用於存放找到的電影資料。如果迴圈結束都沒找到，它仍會是 None。
            for m in list_schedules: # m 不再是串列，它已經是串列裡面的一個字典了，再去字典內找[id]
                if m["id"] == movie_id:
                    selected_movie = m
                    break
            
            if selected_movie:
                choose_seats(selected_movie)  #???
            else:
                print("❌ 查無此電影編號")            


        elif choice == "2":
            all_change()
        elif choice == "3":
            print("再見！")
            break
        else:
            print("無效選項，請重新輸入。")
#執行程式
main()



