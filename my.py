# 簡易電影院售票系統核心邏輯實作
# 題目解讀 所需功能涵蓋：資料庫初始化、場次與座位管理、票價計算、購票流程、交易記錄與簡單報表 
#==== MVP 功能清單 ====
#1. 印出歡迎畫面 （main()) (ok)
#2. 歡迎選單 (ok)
#3. 列出場次並購票 (purchase_flow()) (OK)
#4. 顯示簡單報表 (simple_reports())
#5. 計算票價（看年齡分價制）
#6. 交易紀錄（暫存在記憶體）
import datetime


#1. 印出歡迎畫面 （main())
def main():
    while True:
        print("\n====== 電影院售票系統（簡化版） ======")
        print("1. 列出場次並購票")
        print("2. 顯示簡單報表（今日）")
        print("3. 退出")
        choice = input("請選擇：").strip() #.strip()轉去掉字串 兩端 的空白，不會去掉中間的空格
        if choice == "1":
            purchase_flow()
        elif choice == "2":
            print("還在做")
        elif choice == "3":
            print("再見！")
            break
        else:
            print("無效選項，請重新輸入。")


#3. 列出場次並購票 (purchase_flow())
def purchase_flow(): #自訂函式＿購買程序：列出場次並購票
    print("電影場次公告：")
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
    for movie in Movie_time_list: #設變數movie為卡片（Movie_time_list裡，有幾個就執行幾次迴圈）
        print(f"編號: {movie['id']}, 電影: {movie['movie']}, 時間: {movie['time']}, 價格: {movie['price']}, 限制年齡: {movie['age']}") #因為Movie_time_list 串列，電影一的資料是用字典故可以取出用f{“key"}

    return Movie_time_list #函式內的變數不會自動傳回到外面，故需要回傳 #不建議用gobal，因為函式依賴外部狀態，修改全域變數可能影響程式其他地方，容易出錯。

#請使用者輸入電影編號，輸出可以選得座位
def choose_seats(movie):

    print("\n座位狀態：")
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
            for code, (name, discount)  in discount_identity_dict.items(): 
                print(f"編號： {code} 身份： {name}")
            identity_choice = input("請問是否有其他優惠身份(請輸入數字)").strip()
            if identity_choice in discount_identity_dict:
                identity_name, discount_rate = discount_identity_dict[identity_choice]
                price = movie['price'] * discount_rate
                print(f"\n 購票確認：應用 {identity_name} 優惠 ({int(discount_rate*100)}折)，最終票價為 {price} 元。")
        else:
            print("購票已取消。")
        
    # 4. 成功購買 → 修改座位狀態
    movie["seats"][buy_seat] = False
    print("購買成功！")

#主要程式
movies = purchase_flow()
movie_id = int(input("請輸入想看的電影編號："))

#找到選到的電影
selected_movie = None
for m in movies:
    if m["id"] == movie_id:
        selected_movie = m
        break

if selected_movie:
    choose_seats(selected_movie)
else:
    print("❌ 查無此電影編號")
