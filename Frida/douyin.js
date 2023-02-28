function hookso_ssl() {
	// body...
	var android_dlopen_ext = Module.getExportByName(null, "android_dlopen_ext");
	console.log("android_dlopen_ext --> ", android_dlopen_ext);

	if(android_dlopen_ext){
		Interceptor.attach(android_dlopen_ext, {
		    onEnter: function(args) {

		      var soName = args[0].readCString();
		      if(soName.indexOf("libsscronet.so") != -1){
		      	this.hook = true;
		      }
		    },
		    onLeave: function(retval) {

				if(this.hook){
					dlopentodo();
				}
		    }
		});
	}
}

function dlopentodo() {
	// body...
	var cronet = Module.findBaseAddress("libsscronet.so");
	var ver = Module.findExportByName("libttboringssl.so", "SSL_CTX_set_custom_verify");

	var custom_verify = new NativeFunction(ver, 'pointer', ['pointer', 'int', 'pointer']);

	var self = new NativeCallback(function(arg1, arg2, arg3){
		console.log("custom_verify is calling", arg2, arg3);
		return custom_verify(arg1, 0, arg3);
	}, 'pointer', ['pointer', 'int', 'pointer']);

	Interceptor.replace(ver, self)
}

hookso_ssl();
