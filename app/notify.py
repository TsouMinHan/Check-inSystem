import requests
class LineNotify:
    def __init__(self,):
        pass

    @classmethod
    def sendMsg(cls, msg, token):
    # 修改為你要傳送的訊息內容
        headers = {
            "Authorization": "Bearer " + token, 
            "Content-Type" : "application/x-www-form-urlencoded"
        }        
        payload = {'message': msg}

        r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
        return r.status_code