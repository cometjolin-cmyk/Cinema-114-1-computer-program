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
        choice = input("請選擇：").strip() #轉成字串型態
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
    p

