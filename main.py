#!/usr/bin/env python3
"""Module to test Moleculer Services API endpoints"""

import json
import sys
import requests


class MSTester:
    """Main class to run API endpoints tests"""

    def __init__(self, config_path=""):
        """Tester initializtion
        Params:
          - OPTIONAL: config_path: string An path to a json configuration file.
          If not provided, will look for a "config.json" file on the same folder
        """

        super().__init__()
        # Id of the document used for tests (created by the "test_create" method)
        self.test_document_id = ""
        # Auth token for authenticated requests
        self.auth_token = ""
        try:
            self.config = json.loads(
                open(config_path or "config.json", "r").read())
            for resource, actions in self.config["resources"].items():
                print(f"""[+] TESTING {resource} RESOURCE""")
                request_url = f"""{self.config["api_url"]}/{resource}"""
                headers = self.config["headers"]
                if self.auth_token:
                    headers["Authorization"] = f"""Bearer {self.auth_token}"""

                for action, data in actions.items():
                    data = json.dumps(data)
                    if action == "login":
                        print("     [+] TESTING LOGIN ACTION")
                        self.test_login(request_url, data, headers)
                    if action == "create":
                        print("     [+] TESTING CREATE ACTION")
                        self.test_create(request_url, data, headers)
                    elif action == "update":
                        print("     [+] TESTING UPDATE ACTION")
                        self.test_update(request_url, data, headers)
                    elif action == "get":
                        print("     [+] TESTING GET ACTION")
                        self.test_get_one(request_url, headers)
                    elif action == "list":
                        print("     [+] TESTING LIST ACTION")
                        self.test_list(request_url, headers)
                    elif action == "delete":
                        print("     [+] TESTING DELETE ACTION")
                        self.test_delete(request_url, headers)

        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            self.gracefull_exit(
                f"""Error! Config file not found or invalid ({e}). Please try again"""
            )

    def gracefull_exit(self, message):
        print(message)
        print("Exiting now...")
        sys.exit(0)

    def test_login(self, request_url, auth_data, headers):
        try:
            response = requests.post(
                request_url + "/login", data=auth_data, headers=headers)
            response = response.json()
            self.auth_token = response["services"]["authToken"]
        except Exception as e:
            print(f"""[!] Error on test: {e}""")

    def test_create(self, request_url, data, headers):
        try:
            response = requests.post(request_url, data=data, headers=headers)
            self.test_document_id = response.json()["id"]
        except Exception as e:
            print(f"""[!] Error on test: {e}""")

    def test_update(self, request_url, data, headers):
        try:
            response = requests.put(
                f"""{request_url}/{self.test_document_id}""", data=data, headers=headers).json()
            if not response["id"]:
                print("[-] Warning: Check the response of update action")
        except Exception as e:
            print(f"""[!] Error on test: {e}""")

    def test_get_one(self, request_url, headers):
        try:
            response = requests.get(
                f"""{request_url}/{self.test_document_id}""", headers=headers).json()
            if not response["id"]:
                print("[-] Warning: Check the response of update action")
        except Exception as e:
            print(f"""[!] Error on test: {e}""")

    def test_list(self, request_url, headers):
        try:
            response = requests.get(request_url, headers=headers).json()
            if not isinstance(response, list):
                print("[-] Warning: Check the response of update action")
        except Exception as e:
            print(f"""[!] Error on test: {e}""")

    def test_delete(self, request_url, headers):
        try:
            response = requests.delete(
                f"""{request_url}/{self.test_document_id}""", headers=headers).json()
            if not response["id"]:
                print("[-] Warning: Check the response of update action")
        except Exception as e:
            print(f"""[!] Error on test: {e}""")


if __name__ == "__main__":
    CONFIG_PATH = input(
        "Please enter a path to a JSON config file: "
    )
    TESTER = MSTester(CONFIG_PATH)
