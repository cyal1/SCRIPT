<?php
echo "请输入SessionKey: ";
$sessionKey = fgets(STDIN);
echo "请输入本次解密IV: ";
$iv = fgets(STDIN);
echo "请输入待加密内容: ";
$decryptedData = fgets(STDIN);

function encryptData( $decryptedData, $iv, $sessionKey )
    {
        $aesIV = base64_decode($iv);
        $aesCipher = $decryptedData;
        $aesKey = base64_decode($sessionKey);
        $result = openssl_encrypt($aesCipher, "AES-128-CBC", $aesKey, 0, $aesIV);
        $dataObj = json_decode($result);
        return $result;
    }

$result = encryptData($decryptedData, $iv, $sessionKey);
echo sprintf("最终的加密结果为: %s\n", $result);

?>
