# FIXME
# - Installing error

import urequests
from system.apps import install

class Apps:
    def install(self, app):
        url = f"https://picoos.dev/download/apps/{app}.py"

        try:
            response = urequests.get(url)

            if response.status_code == 200:
                print(f"Installing {app}")
                data = response.text
                with open(f"/{app}.py", "w") as f:
                    f.write(data)

            elif response.status_code == 404:
                print(f"App {app} not existing")

            response.close()

        except Exception as e:
            print(e)

apps = Apps()

class System:
    def update(self):
        print("Hello")
        
system = System()