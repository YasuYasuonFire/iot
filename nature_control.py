from nature_api import _make_nature_request
import time
import requests
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

def control_appliance(appliance_id: str, signal_id: str) -> bool:
    """
    家電を制御する関数
    Args:
        appliance_id: 制御する家電のID（この引数は現在は使用しません）
        signal_id: 送信するシグナルのID
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
            f'https://api.nature.global/1/signals/{signal_id}/send',
            headers=headers
        )
        return response.status_code == 200
    except Exception as e:
        print(f"制御エラー: {str(e)}")
        return False

def main():
    # 寝室の扇風機のID
    APPLIANCE_ID = "61924a2e-4b4c-4916-937f-98f2a9069167"
    ON_SIGNAL = "5a3c20d1-4eeb-422b-b716-c3848467d6e3"
    OFF_SIGNAL = "81318538-2c3a-4009-923a-734ba0fcfe4a"
    INTERVAL = 5  # 制御間隔（秒）
    
    try:
        while True:
            print("扇風機をONにします...")
            if control_appliance(APPLIANCE_ID, ON_SIGNAL):
                print("ON完了")
            else:
                print("ON失敗")
                
            time.sleep(INTERVAL)
            
            print("扇風機をOFFにします...")
            if control_appliance(APPLIANCE_ID, OFF_SIGNAL):
                print("OFF完了")
            else:
                print("OFF失敗")
                
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print("\n終了します")

if __name__ == "__main__":
    main() 