// // 遍历window对象下的属性
// var objectNames = [];
// for (var propertyName in window) {
// 	try {
// 		// 检查属性是否为对象，并且不是null
// 		if (window.hasOwnProperty(propertyName) && typeof window[propertyName] === 'object' && window[propertyName] !== null) {
// 			objectNames.push(propertyName);
// 		}
// 	} catch (error) {
// 		console.error("An error occurred:", error.message);
// 	}
// }
// console.log(objectNames);

// build-in object
var  buildInObjs= ["parent", "top", "frames", "location", "self", "window", "document", "customElements", "history", "locationbar", "menubar", "personalbar", "scrollbars", "statusbar", "toolbar", "navigator", "external", "screen", "visualViewport", "clientInformation", "styleMedia", "performance", "crypto", "indexedDB", "webkitStorageInfo", "trustedTypes", "certificateErrorPageController", "sessionStorage", "localStorage", "jsBridgeList", "buildInObjs", "objectNames", "navigation"]

var jsBridgeList = [];
for (var propertyName in window) {
	try {
		// 检查属性是否为对象，并且不是null
		if (window.hasOwnProperty(propertyName) && typeof window[propertyName] === 'object' && window[propertyName] !== null && !buildInObjs.includes(propertyName)) {
			jsBridgeList.push(propertyName);
		}
	} catch (error) {
		console.error("An error occurred:", error.message);
	}
}
console.log(jsBridgeList);
