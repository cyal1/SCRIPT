<?php

include_once "wxBizDataCrypt.php";


$appid = 'wx1225006d58ea6ac4';
$sessionKey = 'hqzzdCxapmh9j55e5HB4cQ==';

$encryptedData="B8V/YTxGYCxbJodMqpPD/dZWWQUdtew+yubNlMpKBZJixHgHjOteIHYZ6YEwPjCOwTzEKEzK51ebk/hhRoSbRk7yDBnIPwjljqb7rmfFDJniLtI/q1qXK9nsxc4pLg4O2NhiLmEWjihRXVp4kIXXWj+fAyCZ4/9bsFjItsDlu/9eHt+LZtE9n2TKBOBspPb/NkHuAxZNKodljMaVqtp4ZA==";

$iv = 'psvhTxAEcXytuvfmJ+l36A==';

$pc = new WXBizDataCrypt($appid, $sessionKey);
$errCode = $pc->decryptData($encryptedData, $iv, $data );

if ($errCode == 0) {
    print($data . "\n");
} else {
    print($errCode . "\n");
}
