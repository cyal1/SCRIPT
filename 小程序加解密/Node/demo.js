var WXBizDataCrypt = require('./WXBizDataCrypt')

var appId = 'wxcf86b7777ec88caf'
var sessionKey = 'bLPULqbwwWmq2FmYTcTEMg=='
var encryptedData ='Tcoy6tZnGFusGt0gTTZ6LCP/eEZ8TRmX0DaxBNErMGrs+HIZo157zvGUwjzSjKDyXu9ZpBvqtPT282u3KFEoSc7USxSMvKocEiZOr/vXC2GBbHRX5r69f9bQwVjKYyrqiXcWupqBoU+0Pfsaoginc4+k+pgW0BCoyzNHWSTBBE4uoXLK/2n16I1NRENsU8k711uxcH/L1vCFJ00B4zTNeA=='
var iv = 'E6ZUIw3qAhTvkF8L0K8Beg=='

var pc = new WXBizDataCrypt(appId, sessionKey)

var data = pc.decryptData(encryptedData , iv)

console.log('解密后 data: ', data)
