from WXBizDataCrypt import WXBizDataCrypt
import json

def main():

    decryptedData = '{"phoneNumber": "13333333333", "countryCode": "86", "purePhoneNumber": "13333333333", "watermark": {"timestamp": 1657609970, "appid": "wx203b37ad2ad5d2a6"}}'

    encryptedData = '2kA//qWOlCmeMKtEzJU/Vh39yATOSra5VSGouZL0YkAv2XKnK+KZ4GXjnwH54iutOLigL0iKVIM4+iCiulkKVMw40dcfNAH6Ngz8jTTSDz0hcgbplEHxi1CbNWr1P7Hx3neCwekY6F3B6Q+4ckVvC09CqVWxrn76N1ZHN60MCdpDavFeRhyl4JfK45z9rmAGu/SI8LjJAFPpgta37Qc8kg=='
    
    iv = '2QpkqMB8TKeYaGs1MEVM6A=='
    
    appId = 'wx203b37ad2ad5d2a6'
    
    sessionKey = 'JDQ3o3hFG4K0TAi4Qy/YFg=='

    pc = WXBizDataCrypt(appId, sessionKey)

    print pc.encrypt(decryptedData, iv)
    # print(pc.decrypt(encryptedData, iv))
    # print json.dumps(pc.decrypt(pc.encrypt(decryptedData, iv), iv))

if __name__ == '__main__':
    main()
    