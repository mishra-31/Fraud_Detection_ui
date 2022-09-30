import time

import streamlit as st
import requests
from requests.structures import CaseInsensitiveDict
from requests.auth import HTTPBasicAuth
from PIL import Image

image1 = Image.open('Capgemini.PNG')
image2 = Image.open('GCP.PNG')
image3 = Image.open('waylay.PNG')
image4 = Image.open('width.PNG')
image = [image1,image4,image2,image4,image3]
st.image(image)

st.title("Transaction Fraud Detection")
merchant_no=st.text_input('Enter Merchant Id')
terminal_category=st.text_input('Enter Terminal Category')
amount=st.text_input('Enter Amount')



if(st.button('Submit')):
    result1 = merchant_no
    result2 = terminal_category
    result3 = amount
    str1 = f'"MD_MERCHANT_NUMBER":"{result1}"'
    str2 = f'"TERMINAL_CATEGORY":"{result2}"'
    str3 = f'"TT_TRANSACTION_AMOUNT":"{result3}"'
    my_command = str1 + ',' + str2 + ',' + str3

    split_command = my_command.split()
    split_command.insert(0, '{')
    split_command.insert(len(my_command) + 1, '}')
    final_command = ' '.join(split_command)
    data = final_command


    url = "https://webscripts-io.waylay.io/api/v1/1e3ff493-1c0a-42d1-904b-a46f7fcfda5f/paymentCheck"

    headers = CaseInsensitiveDict()
    headers["Authorization"]= "hmac-sha256 uZKTrit2n90OUc2BMrKcO1qDw5B1SaXy34iyW9F05ws="
    headers["Content-Type"] = "application/json"
    resp = requests.post(url, headers=headers, data=data)
    st.write(resp.json())
    
    time.sleep(5)
    ID=resp.json()['ID']
    alarm_url = "https://api-io.waylay.io/alarms/v1/alarms?source=" + ID
    time.sleep(5)
    resp2 = requests.get(alarm_url, auth=HTTPBasicAuth('e10a0f641bccdafbd954a29a', 'tiUG/cuntOmZN8Qyb/sTckuImIstdM5K'))

    
    #print(resp2.json())
    detection = resp2.json()['alarms'][0]['type']
    if detection:
        print(resp2.json()['alarms'][0]['type'])
        st.write('Fraud Detection Notification : ' + resp2.json()['alarms'][0]['type'])
        st.write('Severity : '+resp2.json()['alarms'][0]['severity'])
    else:
        st.write('Transaction successful')



