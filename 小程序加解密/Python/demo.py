from WXBizDataCrypt import WXBizDataCrypt
import json

def main():

    decryptedData = '{"phoneNumber": "17863975270", "countryCode": "86", "purePhoneNumber": "17863975270", "watermark": {"timestamp": 1621403946, "appid": "wx2ffe954c1d2e5369"}}'

    encryptedData = 'WpoX+4guVg9UQHR62AEBntkqKPeUhLcre1GJgTIfHXoL3yCrj462WY0TJ7BuZhdOwA72f+JHPx/TOQvM24XhIErjHQSgCu3A5mGenHIXK+nVYz3O/bDvLzbNSPCtQ3bJBnsCO4Wdrx65kEphKX1HM0tTCDAuhme95zy9DSMbgTVAY78v/RSlVZ1W3UY65trWTITHoZ/cs4soLYdaEbSHtw=='
    
    iv = 'KOrX3nPV9thfiteRFEp0qg=='
    
    appId = 'wx2ffe954c1d2e5369'
    
    sessionKey = 'P/DYg6bBt+A8PlxV45CH2Q=='

    pc = WXBizDataCrypt(appId, sessionKey)

    # print pc.encrypt(decryptedData, iv)

    print json.dumps(pc.decrypt(pc.encrypt(decryptedData, iv), iv))

if __name__ == '__main__':
    main()
