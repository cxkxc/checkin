import os
import requests

# 签到函数，更新一下
def glados_checkin():
    cookie = 'koa:sess=eyJ1c2VySWQiOjU2MjA2MSwiX2V4cGlyZSI6MTc1ODYwODU4NzQwMCwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=eKj0s-ySfgfwxtHEtHu6uVznnqM; __stripe_mid=ec8811ed-4989-4bd6-9733-98d6e1335f8117daae; _ga=GA1.1.958598174.1732687648; _ga_CZFVKMNT9J=GS1.1.1733730016.4.1.1733730585.0.0.0'
    if not cookie:
        print('GLADOS cookie not found in environment variables.')
        return ['Checkin Error', 'GLADOS cookie not found in environment variables.', '']

    try:
        headers = {
            'cookie': cookie,
            'referer': 'https://glados.rocks/console/checkin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        # 发起签到请求
        checkin_response = requests.post(
            'https://glados.rocks/api/user/checkin',
            headers={**headers, 'content-type': 'application/json'},
            json={"token": "glados.one"}
        )
        checkin_data = checkin_response.json()

        # 获取用户状态
        status_response = requests.get(
            'https://glados.rocks/api/user/status',
            headers=headers
        )
        status_data = status_response.json()

        # 检查响应是否成功
        if checkin_response.status_code != 200 or status_response.status_code != 200:
            raise Exception(f"Request failed: {checkin_response.status_code}, {status_response.status_code}")

        return [
            'Checkin OK',
            checkin_data.get('message', 'No message from server'),
            f'Left Days {status_data.get("data", {}).get("leftDays", "N/A")}',
        ]

    except Exception as e:
        error_message = f'Checkin Error: {str(e)}'
        print(error_message)
        github_repo_url = f'<{os.getenv("GITHUB_SERVER_URL")}/{os.getenv("GITHUB_REPOSITORY")}' if os.getenv("GITHUB_SERVER_URL") and os.getenv("GITHUB_REPOSITORY") else ''
        return ['Checkin Error', error_message, github_repo_url]

# 发送通知函数
def notify(contents):
    token = os.getenv('NOTIFY')
    if not token or not contents:
        print('Notification token not found or no content to send.')
        return

    try:
        response = requests.post(
            'https://www.pushplus.plus/send',
            headers={'content-type': 'application/json'},
            json={
                'token': token,
                'title': contents[0],
                'content': '<br>'.join(contents),
                'template': 'markdown',
            }
        )

        if response.status_code != 200:
            print(f'Notification failed: {response.status_code}')
            print(response.text)
        else:
            print('Notification sent successfully.')

    except Exception as e:
        print(f'Notification error: {str(e)}')

# 主函数
def main():
    result = glados_checkin()
    print(result)
    notify(result)

if __name__ == '__main__':
    main()
