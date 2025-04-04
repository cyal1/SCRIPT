function printCurrentStack(){
    console.log(Java.use('android.util.Log').getStackTraceString(Java.use('java.lang.Exception').$new()));
}

function printExceptionStack(){
    var Throwable = Java.use("java.lang.Throwable");
    var StringWriter = Java.use("java.io.StringWriter");
    var PrintWriter = Java.use("java.io.PrintWriter");
    // 找到Exception类的getMessage方法
    var getMessage = Throwable.getMessage;
    // hook getMessage() 方法
    getMessage.implementation = function() {
        // 调用原始的getMessage()方法
        var message = getMessage.call(this);
        var sw = StringWriter.$new();
        var pw = PrintWriter.$new(sw);
        this.printStackTrace(pw);
        var stackTrace = sw.toString();
        // 打印异常消息和堆栈跟踪
        // console.log("[*] Exception Message: ", message);
        console.log("[*] Stack Trace: \n", stackTrace);
        return message;
    };
}

function hookParseUri(){
    var Intent = Java.use('android.content.Intent');
    // 找到parseUri方法
    var parseUri = Intent.parseUri.overload('java.lang.String', 'int');
    // hook parseUri方法
    parseUri.implementation = function(intent_uri, flags) {
        // 打印拦截的URI和标志
        console.log('Intercepted Intent Uri:', intent_uri, 'Flags:', flags);
        // 调用原始parseUri方法
        return this.parseUri(intent_uri, flags);
    };
}

function hookGetStringExtra(){
    var Intent = Java.use('android.content.Intent');
    // 找到getStringExtra方法
    var getStringExtra = Intent.getStringExtra.overload('java.lang.String');
    // hook getStringExtra方法
    getStringExtra.implementation = function(str) {
        var result = this.getStringExtra(str);
        console.log(`getStringExtra("${str}") => ${result}`);
        return result;
    };
}

function hookGetAction(){
    var Intent = Java.use('android.content.Intent');
    Intent["getAction"].implementation = function() {
        var result = this.getAction();
        console.log(`getAction = ${result}`);
        return result;
    };
}

function hookSetPacakge(){
    var Intent = Java.use('android.content.Intent');
    var setPackage = Intent.setPackage.overload('java.lang.String');
    setPackage.implementation = function(pkgName) {
        console.log(`intent.setPackage('${pkgName}')`);
        // printCurrentStack();
        return this.setPackage(pkgName);
    };
}

function hookStartActivity(){
    var Activity = Java.use('android.app.Activity');
    var Intent = Java.use('android.content.Intent');
    Activity.startActivity.overload('android.content.Intent').implementation = function(intent) {
        console.log('startActivity was called with intent:', intent);
        // 在这里添加你想要执行的代码，例如修改 Intent 或者记录日志
        // 如果你希望继续执行原始的 startActivity() 方法，可以调用它：
        this.startActivity(intent);
    };
}
function hookPackageManager(){
      var ApplicationPackageManager = Java.use("android.app.ApplicationPackageManager");

    // Hook ApplicationPackageManager.queryIntentActivities() 方法
    ApplicationPackageManager.queryIntentActivities.overload('android.content.Intent', 'int').implementation = function(intent, flags) {
        console.log(`queryIntentActivities(intent=${intent}, flags=${flags})`);
        var result = this.queryIntentActivities(intent, flags);
        console.log(`ResolveInfo = ${result}, size = ${result.size()}`);
        // 调用原始方法
        return this.queryIntentActivities(intent, flags);
    };

    // Hook ApplicationPackageManager.queryBroadcastReceivers() 方法
    ApplicationPackageManager.queryBroadcastReceivers.overload('android.content.Intent', 'int').implementation = function(intent, flags)
    {
        console.log(`queryBroadcastReceivers(intent=${intent}, flags=${flags})`);
        var result = this.queryBroadcastReceivers(intent, flags);
        console.log(`ResolveInfo = ${result}, size = ${result.size()}`);
        // 调用原始方法
        return result;
    };
}

function hookBroadcastReceiver(){
    var Application = Java.use("android.app.Application");

    // Hook registerReceiver 方法
    Application.registerReceiver.overload('android.content.BroadcastReceiver', 'android.content.IntentFilter').implementation = function(receiver, filter) {
        console.log("Dynamic BroadcastReceiver registered:", receiver, filter);
        // 调用原始的 registerReceiver 方法
        return this.registerReceiver(receiver, filter);
    };

    // Hook unregisterReceiver 方法
    Application.unregisterReceiver.implementation = function(receiver) {
        console.log("Dynamic BroadcastReceiver unregistered:", receiver);
        // 调用原始的 unregisterReceiver 方法
        return this.unregisterReceiver(receiver);
    };
}

function watchClass(classname, filter=['filterMethodName']){
    var targetClass1 = Java.use(classname); // 替换为你要监视的目标类的完整类名
    // 获取目标类的所有方法
    var methods = targetClass1.class.getDeclaredMethods();
    methods.forEach(function(method) {
        // 为每个方法创建 Hook
        var methodName = method.getName();
        if(filter.includes(methodName)){
            return
        }

        var overloadCount = targetClass1[methodName].overloads.length;
        console.log("[*] Hooking " + methodName + " with " + overloadCount + " overloads");
        // 遍历每个重载
        for (var i = 0; i < overloadCount; i++) {
            targetClass1[methodName].overloads[i].implementation = function() {
                // 调用原始方法
                var result = this[methodName].apply(this, arguments);
                console.log(`[*] ${targetClass1} ${methodName}(` + JSON.stringify(arguments) + `) => ${result}`);
                return result;
            };
        }
    });
}

function hookWebview(){
    const WebView = Java.use('android.webkit.WebView');
    // Hook the loadUrl method of WebView
    WebView.loadUrl.overload('java.lang.String').implementation = function(url) {
        console.log('[WebView.loadUrl] URL:', url.toString());
        return this.loadUrl(url);
    };
}

function convertJavaList(list){
    const ArrayList = Java.use('java.util.ArrayList');
    // Convert Java list to JavaScript array for logging
    let arrayList = Java.cast(list, ArrayList);
    let array = arrayList.toArray();

    // Log the contents of the list
    let r = "[";
    for (let i = 0; i < array.length; i++) {
        r += `${array[i]},`;
    }
    return r + ']';
}

function hookPenddingIntent(){
    var pendingIntent = Java.use('android.app.PendingIntent');

    var getActivity_1 = pendingIntent.getActivity.overload("android.content.Context", "int", "android.content.Intent", "int");

    getActivity_1.implementation = function(context, requestCode, intent, flags){
        console.log("[*] Calling PendingIntent.getActivity("+intent.getAction()+")");
        console.log("\t[-] Base Intent toString: " + intent.toString());
        console.log("\t[-] Base Intent getExtras: " + intent.getExtras());
        console.log("\t[-] Base Intent getFlags: " + intent.getFlags());
        return this.getActivity(context, requestCode, intent, flags);
    }
}


function hookDeepLink(){
    var Intent = Java.use("android.content.Intent");
    Intent.getData.implementation = function() {
        var action = this.getAction() !== null ? this.getAction().toString() : false;
        if (action) {
            console.log("[*] Intent.getData() was called");
            console.log("[*] Activity: " + this.getComponent().getClassName());
            console.log("[*] Action: " + action);
            var uri = this.getData();
            if (uri !== null) {
                console.log("\n[*] Data");
                uri.getScheme() && console.log("- Scheme:\t" + uri.getScheme() + "://");
                uri.getHost() && console.log("- Host:\t\t/" + uri.getHost());
                uri.getQuery() && console.log("- Params:\t" + uri.getQuery());
                uri.getFragment() && console.log("- Fragment:\t" + uri.getFragment());
                console.log("\n\n");
            } else {
                console.log("[-] No data supplied.");
            }
        }
        return this.getData();
    }
}


// startActivityForResult
// shouldOverrideUrlLoading
// shouldInterceptRequest

Java.perform(function(){
    hookBroadcastReceiver();
});

