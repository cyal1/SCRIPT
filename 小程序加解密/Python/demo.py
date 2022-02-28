from WXBizDataCrypt import WXBizDataCrypt
import json

def main():

    decryptedData = '{"phoneNumber": "17863975270", "countryCode": "86", "purePhoneNumber": "17863975270", "watermark": {"timestamp": 1621403946, "appid": "wx2ffe954c1d2e5369"}}'

    encryptedData = 'B8V/YTxGYCxbJodMqpPD/dZWWQUdtew+yubNlMpKBZJixHgHjOteIHYZ6YEwPjCOwTzEKEzK51ebk/hhRoSbRk7yDBnIPwjljqb7rmfFDJniLtI/q1qXK9nsxc4pLg4O2NhiLmEWjihRXVp4kIXXWj+fAyCZ4/9bsFjItsDlu/9eHt+LZtE9n2TKBOBspPb/NkHuAxZNKodljMaVqtp4ZA=='
    
    iv = 'psvhTxAEcXytuvfmJ+l36A=='
    
    appId = 'wx4706a9fcbbca10f2'
    
    sessionKey = 'hqzzdCxapmh9j55e5HB4cQ=='

    pc = WXBizDataCrypt(appId, sessionKey)

    # print pc.encrypt(decryptedData, iv)
    print(pc.decrypt(encryptedData, iv))
    # print json.dumps(pc.decrypt(pc.encrypt(decryptedData, iv), iv))

if __name__ == '__main__':
    main()
