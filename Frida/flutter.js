// https://mp.weixin.qq.com/s/e8eBfk3nFhmD_bonakEv-A
function hook_ssl_verify_result(address) {
Interceptor.attach(address, {
        onEnter: function(args) {
            console.log("Disabling SSL validation")
        },
        onLeave: function(retval) {
            console.log("Retval: " + retval);
            retval.replace(0x1);
        }
    }); 
}
function hookFlutter() {
    var m = Process.findModuleByName("libflutter.so");
    var pattern = "FF C3 01 D1 FD 7B 01 A9 FC 6F 02 A9FA 67 03 A9 F8 5F 04 A9 F6 57 05 A9 F4 4F 06 A9 08 0A 80 52 48 00 00 39";
    var res = Memory.scan(m.base, m.size, pattern, {
        onMatch: function(address, size){
            console.log('[+] ssl_verify_result found at: ' + address.toString());
        // Add 0x01 because it's a THUMB function
        // Otherwise, we would get 'Error: unable to intercept function at 0x9906f8ac; please file a bug'
            // hook_ssl_verify_result(address.add(0x01)); 
            hook_ssl_verify_result(address)
        },
        onError: function(reason){
            console.log('[!] There was an error scanning memory');
        },
        onComplete: function() {
            console.log("All done")
        }
    });
}
