#pip install ccxt

while True:
  ## Login 
  import ccxt
  # เปลี่ยน API เปลียน ข้อมูลกันด้วยนะครับ
  apiKey    = "vXUp81ynMW_mnjSd4CtloeNmDjOTAYZrfDtpYDzU" 
  secret    = "u9kub1BziW9-OIfZGgsfFOv3tD5WMpUN3wLdf7il" 
  password  = ""  #FTX ไม่มี Pass API ไม่ต้องใส่อะไร
  Account_name  = "Rebalancing" 

  exchange = ccxt.ftx  ({'apiKey' : apiKey ,'secret' : secret ,'password' : password ,'enableRateLimit': True})
  # Sub Account Check
  if Account_name == "" :
    print("\n""Account Name - This is Main Account",': Broker - ',exchange)     
  else:
    print( "\n"'Account Name - ',Account_name,': Broker - ',exchange)
    exchange.headers = {'ftx-SUBACCOUNT': Account_name,}

  # ดูในพอร์ท ว่ามีเงินเท่าไร
  Get_balance = exchange.fetch_balance()
  print(Get_balance)  

  # ดูในพอร์ท ว่ามีเงินเท่าไร
  Asset_01 = Get_balance ['USDT'] ['total']
  #Asset_01 = 10
  print("Asset 01 = " , Asset_01,"USDT")



  import requests
  import time
  import hmac
  import urllib.parse
  from typing import Optional, Dict, Any, List
  from requests import Request, Session, Response

  class FtxClient:
      _ENDPOINT = 'https://ftx.com/api/'

      def __init__(self, api_key=None, api_secret=None, subaccount_name=None) -> None:
          self._session = Session()
          self._api_key = api_key
          self._api_secret = api_secret
          self._subaccount_name = subaccount_name

      def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
          return self._request('GET', path, params=params)

      def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
          return self._request('POST', path, json=params)

      def _request(self, method: str, path: str, **kwargs) -> Any:
          request = Request(method, self._ENDPOINT + path, **kwargs)
          self._sign_request(request)
          response = self._session.send(request.prepare())
          return self._process_response(response)

      def _sign_request(self, request: Request) -> None:
          ts = int(time.time() * 1000)
          prepared = request.prepare()
          signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
          if prepared.body:
              signature_payload += prepared.body
          signature = hmac.new(self._api_secret.encode(), signature_payload, 'sha256').hexdigest()
          request.headers['FTX-KEY'] = self._api_key
          request.headers['FTX-SIGN'] = signature
          request.headers['FTX-TS'] = str(ts)
          if self._subaccount_name:
              request.headers['FTX-SUBACCOUNT'] = urllib.parse.quote(self._subaccount_name)

      def _process_response(self, response: Response) -> Any:
          try:
              data = response.json()
          except ValueError:
              response.raise_for_status()
              raise
          else:
              if not data['success']:
                  raise Exception(data['error'])
              return data

  # ส่งคำสัง Lending
  ftx_client = FtxClient(api_key= apiKey , api_secret=secret, subaccount_name=Account_name)
  Auto_Lending = ftx_client._post('spot_margin/offers', {
    "coin": 'USDT' ,
    "size": Asset_01,
    "rate": 1e-6
  })    
  print (Auto_Lending) # แสดง สถานะ


  # เรียกดู สถานะ การ Lending ทั้งหมด
  lending_info = ftx_client._get('spot_margin/lending_info')['result']
  print (lending_info)# แสดง สถานะ

  # พักการทำงาน 
  import time
  sleep = 600 
  print("Sleep",sleep,"sec.")
  time.sleep(sleep) # Delay for 1 minute (60 seconds).  