var page = require('webpage').create(),
system = require('system'),
address;

if (system.args.length === 1) {
    phantom.exit(1);
} else {
    address = system.args[1];
    page.open(address, function(status) {
        if (status !== 'success') {
            phantom.exit();
        } else {
            var sc = page.evaluate(function() {
                return document.getElementsByClassName("daisy-link spec-download-burp-suite-project-file")[0].href;
            });
            window.setTimeout(function() {
                console.log(sc);
                phantom.exit();
            }, 1000);
        }
    });
};
