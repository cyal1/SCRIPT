Module.enumerateExports("libttboringssl.so", {
    onMatch: function(e) {
        if (e.type == 'function') {
            console.log("name of function = " + e.name);

            if (e.name == "Java_example_decrypt") {
                console.log("Function Decrypt recognized by name");
                Interceptor.attach(e.address, {
                    onEnter: function(args) {
                        console.log("Interceptor attached onEnter...");
                    },
                    onLeave: function(retval) {
                        console.log("Interceptor attached onLeave...");
                    }
                });
            }
        }
    },
    onComplete: function() {}
});
