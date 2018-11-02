
var arraySize = 1000000;
var numIters = 10000;

var start = new Date().getTime();
for (i = 0; i < numIters; ++i) {
  var a = new Array(arraySize);
  for (j = 0; j < arraySize; ++j) {
    a[j] = 1;
  }
  //console.log("finished array of size " + a.length);
}
var end = new Date().getTime();
console.log("pre-allocated took " + (end-start));

var start = new Date().getTime();
for (i = 0; i < numIters; ++i) {
  var a = new Array();
  for (j = 0; j < arraySize; ++j) {
    a.push(1);
  }
  //console.log("finished array of size " + a.length);
}
var end = new Date().getTime();
console.log("dynamically resized took " + (end-start));

