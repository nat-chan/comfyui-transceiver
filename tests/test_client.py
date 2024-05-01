import unittest
import requests

HOST = "localhost"
PORT = 8189

class test_transceiver_endpoint(unittest.TestCase):
    def test_transceiver_send_to_channel(self):
        url = f"http://{HOST}:{PORT}/transceiver_send_to_channel"
        # POSTするデータ
        data = {"buffer": b"dummy_buffer"}
        # POSTリクエストを送信
        response = requests.post(f"{url}?channel=test_channnel", data=data)

        # レスポンスの内容を表示
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)

        self.assertEqual(response.status_code, 200)

    def test_transceiver_recieve_from_channel(self):
        url = f"http://{HOST}:{PORT}/transceiver_recieve_from_channel"
        response = requests.get(f"{url}?channel=test_channnel")

        # レスポンスの内容を表示
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
