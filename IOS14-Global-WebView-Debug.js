// frida -U webinspectord -l IOS14-Global-WebView-Debug.js
// ios 14
Interceptor.attach(ObjC.classes.RWIRelayDelegateIOS['- relay:allowIncomingApplicationConnection:bundleIdentifier:'].implementation, {
  onEnter: function(args) {
    this.bundleId = new ObjC.Object(args[3]);
  },
  onLeave: function(retVal) {
    const allow = !retVal.equals(NULL)
    console.log(this.bundleId + (allow ? ' allows' : ' does not allow') + ' WebInspect')
    if (!allow) {
      console.log('now patch it');
      retVal.replace(ptr(1));
    }
  }
});


/*
 * Auto-generated by Frida. Please modify to match the signature of -[RWIRelayDelegateIOS relayClientConnectionDidChange:].
 * This stub is currently auto-generated from manpages when available.
 *
 * For full API reference, see: https://frida.re/docs/javascript-api/
 */

