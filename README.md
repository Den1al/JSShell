# JSShell

An interactive multi-user web based shell written in Python with Flask (for server side) and of course Javascript and HTML (client side). It was initially created in order to debug remote esoteric browsers during tests and research. I am well aware of other purposes this tool might serve, use it at your own responsibility and risk.

###### Version: 0.4

## Author
[Daniel Abeles](https://twitter.com/Daniel_Abeles).

### Shell Video
[![asciicast](https://asciinema.org/a/152288.png)](https://asciinema.org/a/152288)

## Installation
It is recommended to use a virtual environment (I used python 3.6, but eariler work just fine):
### Pyenv
```python
pyenv virtualenv -p python3.6 venv
pyenv activate venv
```

### virtualenv
```python 
virtualenv -p python3.6 venv
```
```bash
source venv/bin/activate
```

### Then for both
```python
pip install -r requirements.txt
```

## Features
* Multi client support
* Cyclic DOM objects support
* Pre flight scripts
* Command Queue
* Command Context
* Injectable via `<script>` tags
* Dumping output to file
* Shell pagination

## Running
### Create the configuration file
```python
cd app
cp config.py.template config.py
```
Now you can change the settings you need


### Create the database
```python
python db_handler.py create
```
### Start the server (at the background):
```python
python run.py
```
### Navigate with a browser to the server address
If you running locally, then navigate to `http://localhost:5000` (port/host can be changed)

### Open the interactive shell
```python
python shell.py
```
### Optional : Pre flight scripts
Those are scripts that will execute on every registration of a new client.
By default I included pre-flight scripts which grab the following:

1. Window object
2. Document object
3. The browsers screen data
4. The browser plugins

They are mainly useful when you are automating this process and you know apriori what you want to collect.

### Usage
The shell interface contains various commands (can be revealed using the `help` command).
```bash
  ╦╔═╗╔═╗┬ ┬┌─┐┬  ┬
  ║╚═╗╚═╗├─┤├┤ │  │
 ╚╝╚═╝╚═╝┴ ┴└─┘┴─┘┴─┘
  By @Daniel_Abeles

>> help
+-------------+----------------------------------------------------------+
| command     | description                                              |
+-------------+----------------------------------------------------------+
| list        | Lists all the clients registered                         |
| help        | self.help()                                              |
| select <id> | Selected a specific client from the list                 |
| info <id>   | Prints information on a specific client                  |
| <command>   | Executes a command to the current selected client        |
| back        | Detaches from the current client                         |
| exit        | Exists this interactive shell                            |
| coms        | Displays the commands and output for the current client  |
| com <id>    | Displays a specific command and output                   |
| more <id>   | Displays a specific command and output (with pagination) |
| comk        | Kills a command ("*" for all)                            |
| clik        | Kills a client ("*" for all)                             |
| dump <id>   | Dumps the command output to disk - "dump.txt"            |
+-------------+----------------------------------------------------------+                              

```
Utilizing the command queue, you can fire multiple commands and the client will execute them one by one.
All the commands are executed using a single context, so you issue multiple related commands.


To view the commands issued to a client, first select a client:
```python
>> select 1
```

Then, issue the `coms` command to view all the commands for the client:
``` python
(Client 1) >> coms
```
To view the full command and it's full output (on the `coms` command the output is truncated to fit the screen):
```python
(Client 1) >> com 1
```
If the command output is too large for your shell, you can utilize the `more` command:
```python
(Client 1) >> more 1
```

## Workflow
After all the installations and configuration is done, the workflow of the application is the following:

1. Client visits the home page `http://localhost:5000/`
2. He makes a `register` request to the server
3. The client waits for commands
4. In the meanwhile, on the server, you execute commands using the `shell.py` script
5. The client probes the server for commands, see a new one appeared, pulls it and executes it
6. Once he's done executing, he will post back the result to the server
7. Now, using the `coms` command (in the shell), we can see the output for that command


## Database Handling
I have included a script that i've been using during tests, which is the `db_handler.py` file.
It includes various function to handle and test your database. In Example:
* List all records
* List a specific client
* Create the table
* Insert a record
* Insert a dummy record
* Drop the table
* Drop + Create + List the table (useful for debugging)
* Truncate the table
* Create a command


## New: Injectable via `<script>` tags
Now, by visiting the page `http://<yourwebsite>:<port>/js`, the server will automatically generate a new injection payload that contains all the dependencies, specific URL and PORT (from the config file).

In order to comply with this feature, change the following values in the `config.py` file:
* *URL* - the url of your website/server that contains the shell, i.e. `http://yourwebsite.com`
* *PORT* - the port that the website/server listens to.

This method can be useful as a light-weight alternative to the [Beef](http://beefproject.com/) project.


## Credits
[Canop](https://github.com/Canop) for [JSON.prune](https://github.com/Canop/JSON.prune/)
