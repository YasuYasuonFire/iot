from dotenv import load_dotenv
import requests
import os
import json

# .envファイルを読み込む
load_dotenv()

def _make_nature_request(endpoint):
    """共通のNature API リクエスト処理"""
    api_token = os.getenv('NATURE_ACCESS_TOKEN')
    
    if not api_token:
        raise ValueError('NATURE_ACCESS_TOKENが設定されていません')
    
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }
    
    try:
        response = requests.get(
            f'https://api.nature.global/1/{endpoint}',
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"APIエラー: {response.status_code}")
            return None
            
        return response.json()
    except Exception as e:
        print(f"リクエストエラー: {str(e)}")
        return None

def get_nature_user():
    user_data = _make_nature_request('users/me')
    return user_data['nickname'] if user_data else 'ユーザー情報の取得に失敗しました'

def get_nature_devices():
    devices = _make_nature_request('devices')
    if not devices:
        return []
        
    return [{
        'name': device.get('name'),
        'id': device.get('id'),
        'temperature': device.get('newest_events', {}).get('te', {}).get('val'),
        'humidity': device.get('newest_events', {}).get('hu', {}).get('val'),
        'illumination': device.get('newest_events', {}).get('il', {}).get('val')
    } for device in devices]

def get_nature_appliances():
    appliances = _make_nature_request('appliances')
    if not appliances:
        return []
    
    # デバッグ出力を追加
    print("\n=== APIレスポンス（生データ） ===")
    print(json.dumps(appliances, indent=2, ensure_ascii=False))
    print("===============================\n")
        
    return [{
        'id': appliance.get('id'),
        'name': appliance.get('nickname'),
        'type': appliance.get('type'),
        'device_id': appliance.get('device', {}).get('id'),
        'device_name': appliance.get('device', {}).get('name'),
        'signals': [
            {
                'name': signal.get('name'),
                'id': signal.get('id')
            } for signal in appliance.get('signals', [])
        ]
    } for appliance in appliances]

if __name__ == "__main__":
    result = get_nature_user()
    print(f"結果: {result}")
    
    devices = get_nature_devices()
    print("デバイス一覧:")
    for device in devices:
        print(f"デバイス名: {device['name']}")
        print(f"ID: {device['id']}")
        print(f"温度: {device['temperature']}℃")
        print(f"湿度: {device['humidity']}%")
        print(f"照度: {device['illumination']}")
        print("-------------------")
    
    print("\n登録済み家電一覧:")
    appliances = get_nature_appliances()
    for appliance in appliances:
        print(f"家電名: {appliance['name']}")
        print(f"タイプ: {appliance['type']}")
        print(f"ID: {appliance['id']}")
        print(f"接続デバイス: {appliance['device_name']}")
        print("登録済みシグナル:")
        for signal in appliance['signals']:
            print(f"  - {signal['name']} (ID: {signal['id']})")
        print("-------------------")