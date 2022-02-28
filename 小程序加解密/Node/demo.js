var WXBizDataCrypt = require('./WXBizDataCrypt')

var appId = 'wx1225006d58ea6ac4'
var sessionKey = 'XJ35NxgRnPCylazcGIBM+g=='
var encryptedData ='PyUXvlR3uZDTNQ46S6HSU66zlkqhbudVP4Wl5eN7fs8NZJ1s8ZsM7COQTj3+5nDnD9i11IYp7p9HPqQ7vytTUVvwqPNQCEG+y+zzp3d/b2VmZugj0sSbJ9uMauAA+Q5Zw+UdrXnWLavIOEJ0INJVip/PCrvNcpi5szEC6nMeh4c4IsvpgtGnIkkR9+MYgzQmm/C7rswcDyqmIZ+fc61DSw=='
var iv = 'GnSxNEeHYWeKQNCrilqhUg=='

var pc = new WXBizDataCrypt(appId, sessionKey)

var data = pc.decryptData(encryptedData , iv)

console.log('解密后 data: ', data)
