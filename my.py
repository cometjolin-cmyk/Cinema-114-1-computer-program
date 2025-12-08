# 簡易電影院售票系統核心邏輯實作
# 題目解讀 所需功能涵蓋：資料庫初始化、場次與座位管理、票價計算、購票流程、交易記錄與簡單報表 
#==== MVP 功能清單 ====
#1. 印出歡迎畫面 （main())
#2. 歡迎選單
#3. 列出場次並購票 (purchase_flow())
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
            simple_reports()
        elif choice == "3":
            print("再見！")
            break
        else:
            print("無效選項，請重新輸入。")
if __name__ == "__main__" : #當這個檔案被「直接執行」時才會跑 main()，避免被其他檔案 import 時自動執行。
    main()

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
    return Movie_time_list #函式內的變數不會自動傳回到外面，故需要回傳 #不建議用gobal，因為函式依賴外部狀態，修改全域變數可能影響程式其他地方，容易出錯。
Movie_time_list = purchase_flow() #是把函式回傳的資料「拿出來」存成變數。
for movie in Movie_time_list: #設變數movie為卡片（Movie_time_list裡，有幾個就執行幾次迴圈）
    print(f"編號: {movie['id']}, 電影: {movie['movie']}, 時間: {movie['time']}, 價格: {movie['price']}, 限制年齡: {movie[]}") #因為Movie_time_list 串列，電影一的資料是用字典故可以取出用f{“key"}

#請使用者輸入電影編號，輸出可以選得座位
def choose_seats():
    movie_number = int(input("購票系統＿請輸入想購買的電影編號"))

    for seat, available in movie['seats'].items(): #為什麼我可以movie['seats']這樣去指定
        status = "可選"if available == True else "已售出"
        print(f"  {seat}: {status}")

    buy_seat = input("請輸入要購買的位子").strip()
    if buy_seat not in movie['seats']:
        print("無此座位喔")
    elif available == False :
        print("此座位已售出")
    else :
        print("座位可購買，請填寫資料")

    today = datetime.date.today()
    thisYear = today.year
    ageYear = int(input("請輸入出生年齡，以確保可以購買此場電影"))
    age = thisYear - ageYear #記得轉格式 字串不可運算
   
    if age >= :
        print(f"您目前{age}歲可以購買18+限制級票\n")
        buy = bool(input("是否購票(請輸入true或false) ")
        if buy = true:
            identity = bool(input("是否有其他優惠身份(請輸入true或false) ")
            

        



