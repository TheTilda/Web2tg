import requests
import time

while True:
    
    print((requests.get('https://api.telegram.org/bot5748514452:AAH0PsLIEZttWE1mtcidjVpcX6nGL2tNvQs/getUpdates')).text)
