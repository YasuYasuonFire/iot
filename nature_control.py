from nature_api import _make_nature_request
import time
import requests
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

def control_appliance(appliance_id: str, button: str = "power") -> bool:
    """
    家電を制御する関数
    Args:
        appliance_id: 制御する家電のID
        button: 押すボタンの種類（デフォルトは"power"）
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
        response = requests.post(
            f'https://api.nature.global/1/appliances/{appliance_id}/signals/{button}/send',
            headers=headers
        )
        return response.status_code == 200
    except Exception as e:
        print(f"制御エラー: {str(e)}")
        return False

def main():
    APPLIANCE_ID = "793ae10f-c404-4167-a9b8-3a804df9e40b"
    INTERVAL = 5  # 制御間隔（秒）
    
    try:
        while True:
            print("ONにします...")
            if control_appliance(APPLIANCE_ID):
                print("ON完了")
            else:
                print("ON失敗")
                
            time.sleep(INTERVAL)
            
            print("OFFにします...")
            if control_appliance(APPLIANCE_ID):
                print("OFF完了")
            else:
                print("OFF失敗")
                
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print("\n終了します")

if __name__ == "__main__":
    main() 