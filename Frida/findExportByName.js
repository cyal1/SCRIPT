Interceptor.attach(Module.getExportByName('libsscronet.so', 'SSL_CTX_set_custom_verify'), {
    onEnter: function(args) {
      //this.first = args[0].toInt32(); // int
      //console.log("on enter with: " + this.first)
    },
    onLeave: function(retval) {
      //const dstAddr = Java.vm.getEnv().newIntArray(1117878);
      //console.log("dstAddr is : " + dstAddr.toInt32())
	console.log(retval);
      //retval.replace(dstAddr);
	retval.replace(0);
    }
});

Interceptor.attach(Module.getExportByName('libttboringssl.so', 'SSL_CTX_set_custom_verify'), {
    onEnter: function(args) {
      //this.first = args[0].toInt32(); // int
      //console.log("on enter with: " + this.first)
    },
    onLeave: function(retval) {
      //const dstAddr = Java.vm.getEnv().newIntArray(1117878);
      //console.log("dstAddr is : " + dstAddr.toInt32())
      //retval.replace(dstAddr);
	console.log(retval);
	retval.replace(0);
    }
});
