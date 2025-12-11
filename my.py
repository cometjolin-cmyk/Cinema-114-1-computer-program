# 簡易電影院售票系統核心邏輯實作
# 題目解讀 所需功能涵蓋：資料庫初始化、場次與座位管理、票價計算、購票流程、交易記錄與簡單報表 
#==== MVP 功能清單 ====
#1. 印出歡迎畫面 （main()) (ok)
#2. 歡迎選單 (ok)
#3. 列出場次並購票 (purchase_flow()) (OK)
#4. 顯示簡單報表 (simple_reports())
#5. 計算票價（看年齡分價制） (ok)
#6. 交易紀錄（暫存在記憶體）
import datetime
TRANSACTIONS = []

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


#3. 列出場次並購票 (purchase_flow())

Movie_time_list =  [
    {   "id" : 1,
        "movie": "Horror Night",
        "time": "19:00",
        "price": 250,
        "age": 15,
        "seats": {
            "A1": True,
            "A2": True,
            "A3": True,
            "A4": True,
            "A5": True,
        }
    },
    {
        "id": 2,
        "movie": "Love in Taipei",
        "time": "21:00",
        "price": 220,
        "age": 18,
        "seats": {
            "A1": True,
            "A2": True,
            "A3": True,
            "A4": True,
            "A5": True,
        }
    }]
    #Movie_time_list = purchase_flow() 是把函式回傳的資料「拿出來」存成變數。(這段會讓程式變成無限迴圈)
    #函式內的變數不會自動傳回到外面，故需要回傳 #不建議用gobal，因為函式依賴外部狀態，修改全域變數可能影響程式其他地方，容易出錯。

#請使用者輸入電影編號，輸出可以選得座位
def choose_seats(movie):

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

    # 3. 年齡判斷
    today = datetime.date.today()
    user_birth = int(input("請輸入出生年份，以確保可以購買此場電影"))
    age = today.year - user_birth

    if age < movie["age"]:
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
                print(f"\n 購票確認：應用 {identity_name} 優惠 ({int(discount_rate*10)}折)，最終票價為 {price} 元。")

                transaction_record = {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "movie": movie["movie"],
                "seat": buy_seat,
                "discount(%)": int(discount_rate*10),
                "final_price": price, # 必須使用計算出來的最終價格
                "identity": identity_name # 儲存使用的折扣身份
                 }
                
                for a, b  in transaction_record.items(): #輸出報表的列表
                    print(f"{a} ： {b}")

                TRANSACTIONS.append(transaction_record) #將交易紀錄存入報表串列


                return identity_name, discount_rate, price
        else:
            print("購票已取消。")
        
    # 4. 成功購買 → 修改座位狀態
    movie["seats"][buy_seat] = False


def all_change():
    print("報表列印及電影現況")
    for index, transaction in enumerate(TRANSACTIONS):  #有做更改
        print(f"\n======== 第 {index + 1} 筆交易 ========")
        for key, value in transaction.items():
            print(f"{key:<15}： {value}") #為什麼要<15:確保 Key 佔據至少 15 個字符寬度，讓輸出報表看起來整齊
    for seat, available in Movie_time_list['seats'].items():
        status = "可購買" if available else "已售出"
        print(f"{seat}: {status}")
    
    

#主要程式
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
            for movie in Movie_time_list : #設變數movie為卡片（Movie_time_list裡，有幾個就執行幾次迴圈）
                print(f"編號: {movie['id']}, 電影: {movie['movie']}, 時間: {movie['time']}, 價格: {movie['price']}, 限制年齡: {movie['age']}")
    
            # 2. 接收電影 ID #try...except ValueError： 這是一個錯誤處理機制。如果使用者不小心輸入了非數字的內容（例如 "ABC"），程式就不會崩潰，而是會執行 except 區塊，列印錯誤訊息並用 continue 回到 main() 迴圈的開頭（重新顯示選單）。
            try:
                movie_id = int(input("請輸入想看的電影編號：").strip())
            except ValueError:
                print("❌ 輸入格式錯誤，請輸入數字編號。")
                continue
                
            # 3. 找到電影（必須使用迴圈遍歷，因為 movies 是串列）
            selected_movie = None #初始化一個變數，用於存放找到的電影資料。如果迴圈結束都沒找到，它仍會是 None。
            for m in list_schedules: # m 不再是串列，它已經是串列裡面的一個字典了，再去字典內找[id]
                if m["id"] == movie_id:
                    selected_movie = m
                    break
            
            if selected_movie:
                choose_seats(selected_movie) # ✅ 傳入選中的電影字典
            else:
                print("❌ 查無此電影編號")


        elif choice == "2":
            all_change()
        elif choice == "3":
            print("再見！")
            break
        else:
            print("無效選項，請重新輸入。")

main()



