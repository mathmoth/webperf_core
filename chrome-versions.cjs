/* 
 * USED FOR SITESPEED TEST (TO collect software and javascript used)!!!
 */
module.exports = async function (context, commands) {
    cdpClient = commands.cdp.engineDelegate.getCDPClient()
    // https://chromedevtools.github.io/devtools-protocol/tot/Storage/#method-getCookies
    // bodyResult = await cdpClient.send('Runtime.evaluate', {
    //     'expression': 'document.location.href'
    // });
    // await commands.wait.byTime(20000);

    // bodyResult = await cdpClient.send('Runtime.evaluate', {
    //     'allowUnsafeEvalBlockedByCSP': true,
    //     'expression': '"jQuery" in window && "fn" in window.jQuery && "jquery" in window.jQuery.fn ? window.jQuery.fn.jquery : ""'
    // });
    commands.wait.byPageToComplete();

    core_js_versions = [];
    try {
        core_js_count = await commands.js.run('return "__core-js_shared__" in window && "versions" in window["__core-js_shared__"] ? window["__core-js_shared__"]["versions"].length : 0')
        for (let index = 0; index < core_js_count; index++) {
            value = await commands.js.run('return "__core-js_shared__" in window && "versions" in window["__core-js_shared__"] ? window["__core-js_shared__"]["versions"][' + index +']["version"] : -1')
            if (value.indexOf('ERROR') === -1) {
                core_js_versions.push(value);
            }
        }
    } catch (error) {
        console.error(error);
    }

    modernizr_versions = []
    try {
        modernizr_versions = await commands.js.run('return "Modernizr" in window && "_version" in window.Modernizr ? [window.Modernizr._version] : []');
    } catch (error) {
        console.error(error);
    }

    jquery_versions = []
    try {
        jquery_versions = await commands.js.run('return "jQuery" in window && "fn" in window["jQuery"] && "jquery" in window["jQuery"]["fn"] ? [window["jQuery"]["fn"]["jquery"]] : []');
        if (jquery_versions === null || jquery_versions == {}) {
            jquery_versions = []
        }
    } catch (error) {
        console.error(error);
    }

    versions = {
        'jquery': jquery_versions,
        'modernizr': modernizr_versions,
        'core-js': core_js_versions
    }


    // window['__core-js_shared__'].versions

    // bodyResult = await commands.js.run('return { "jquery": "jQuery" in window && "fn" in window.jQuery && "jquery" in window.jQuery.fn ? window.jQuery.fn.jquery : ""}');
    // bodyResult = await cdpClient.send('Runtime.evaluate', {
    //     'expression': 'window.jQuery.fn.jquery'
    // });
    context.log.info('VERSIONS:START:', versions, 'VERSIONS:END');
}