from dotenv import load_dotenv
import requests
import os
import time

# .envファイルを読み込む
load_dotenv()

def control_light(appliance_id: str, button: str = "on") -> bool:
    """
    照明を制御する関数
    Args:
        appliance_id: 制御する照明のID
        button: 操作ボタン（"on"または"off"または"onoff"）
    Returns:
        bool: 制御が成功したかどうか
    """
    api_token = os.getenv('NATURE_ACCESS_TOKEN')
    
    if not api_token:
        raise ValueError('NATURE_ACCESS_TOKENが設定されていません')
    
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }
    
    try:
        print(f"リクエスト情報: ID={appliance_id}, ボタン={button}")
        response = requests.post(
            f'https://api.nature.global/1/appliances/{appliance_id}/light',
            headers=headers,
            data={'button': button}
        )
        print(f"レスポンスステータス: {response.status_code}")
        print(f"レスポンス内容: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"制御エラー: {str(e)}")
        print(f"エラーの種類: {type(e).__name__}")
        return False

def main():
    # 照明のID
    LIGHT_ID = "af7d5329-99a1-4f40-849e-e7025197906c"
    INTERVAL = 5  # 制御間隔（秒）
    
    try:
        while True:
            print("照明の状態を切り替えます...")
            if control_light(LIGHT_ID, "onoff"):
                print("切り替え完了")
            else:
                print("切り替え失敗")
                
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print("\n終了します")

if __name__ == "__main__":
    main() 