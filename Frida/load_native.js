Interceptor.attach(Module.getExportByName('libsscronet.so', 'SSL_CTX_set_custom_verify'), {
    onEnter: function(args) {
	console.log(args[0]);
	//console.log(arg2);
	//console.log(arg3);
    },
    onLeave: function(retval) {
      // simply replace the value to be returned with 0
      retval.replace(0);
    }
});
