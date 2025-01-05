import requests
import json


class FuncionsValidation:

    def __init__(self, token, databaseId) -> None:
        self.NOTION_TOKEN = token
        self.DATABASE_ID = databaseId
        self.header = {
            'Authorization': 'Bearer ' + self.NOTION_TOKEN,
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28',
        }

    def getPages(self) -> list:
        url = f'https://api.notion.com/v1/databases/{self.DATABASE_ID}/query'

        payload = {'page_size': 100}
        response = requests.post(url, json=payload, headers=self.header)

        data = response.json()

        with open('db.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return data

    def findStatusInData(self, raw_data, user_email) -> str | bool:
        data = raw_data['results']
        for i in data:
            properties = i['properties']
            emailField = properties['E-mail']
            email = emailField['email']
            if user_email == email:
                statusField = properties['Status']
                status = statusField['status']['name']
                return status
        return False

    def UserValidation(self, user_email: str):
        data = self.getPages()
        user_status = self.findStatusInData(data, user_email)
        if user_status == 'Pago':
            return True
        return False


if __name__ == '__main__':

    ...
