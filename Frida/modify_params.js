// .js
console.log("Script loaded successfully ");
Java.perform(function () {
    console.log("Inside java perform function");
    var my_class = Java.use("com.yuanrenxue.match2022.security.Sign");
    //Hook "fun" with parameters (int, int)

    my_class.sign.implementation = function (bArr) { //hooking the old function
        console.log("original params: " + bArr.toString());
        send(bArr); // send data to python code
        var string_to_recv = ""
        recv(function (received_json_object) {
            string_to_recv = received_json_object.python_data;
        }).wait(); //block execution till the message is received
        console.log("Final string_to_recv: "+ string_to_recv.toString())
        return this.sign(string_to_recv);
    };
});