console.log("Script loaded successfully ");
var instances_array = [];
function callEncryptfunction(msg) {
    var ret = null
    Java.perform(function () { 
        if (instances_array.length == 0) { // if array is empty
            Java.choose("com.yuanrenxue.match2022.security.Sign", { // instance method
                onMatch: function (instance) {
                    console.log("Found instance: " + instance);
                    instances_array.push(instance);
                    var string_class = Java.use("java.lang.String");
                    // var my_string = string_class.$new(msg).getBytes();
                    // console.log(typeof msg)
                    ret = instance.sign(string_class.$new(msg).getBytes());
                    console.log(ret);
                    // send(ret)
                    return
                },
                onComplete: function () {
                    if (instances_array.length == 0) {
                        console.log("Not found encrypt instance. " );
                    }
                }

            });
        }
        else {//else if the array has some values
            console.log("An instance already exists." );
            var string_class = Java.use("java.lang.String");
            // var my_string = string_class.$new(msg.message).getBytes();
            ret = instances_array[0].sign(string_class.$new(msg).getBytes());
            console.log(ret);
            // send(ret)
        }

    });

    return ret
}

// function hookEncrypt() { 
//     Java.perform(function () {
//         var my_class = Java.use("com.yuanrenxue.match2022.security.Sign");
//         var string_class = Java.use("java.lang.String");
//         my_class.encrypt.overload().implementation = function(){ // static method
//             var my_string = string_class.$new("TE ENGANNNNEEE");
//             return my_string;
//         }
//     });
// }

rpc.exports = {
    callencryptfunction: callEncryptfunction,
    // hookencryptfunction: hookEncrypt
};
