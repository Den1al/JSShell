''' Pre flight scripts that will run on every client when they register '''

pf_scripts = [
    "window",
    "window.document",
    "var l = {\"availHeight\" : window.screen.availHeight,\"availLeft\" : window.screen.availLeft,\"availTop\" : window.screen.availTop, \"availWidth\" : window.screen.availWidth, \"colorDepth\": window.screen.colorDepth, \"height\" : window.screen.height, \"orientation\" : window.screen.orientation, \"ScreenOrientation\" : window.screen.ScreenOrientation, \"pixelDepth\" : window.screen.pixelDepth, \"width\" : window.screen.width};l",
    "var l = [];for(var i=0;i<navigator.plugins.length;i++){ l.push(navigator.plugins[i].name) };l"
]