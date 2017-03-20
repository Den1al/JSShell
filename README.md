# JSShell

An interactive multi-user web based JS shell written in Python with Flask (for server side) and of course Javascript and HTML (client side). It was initially created to debug remote esoteric browsers during tests and research. I'm aware of other purposes this tool might serve, use it at your own responsibility and risk.

## Author
[Daniel Abeles](https://twitter.com/Daniel_Abeles).

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

### For both
```python
pip install -r requirements.txt
```

## Features
* Multi client support
* Cyclic DOM objects support
* Pre flight scripts
* Command queue
* Command Context

## Running
### Create the database
```python
python db_handler.py create
```
### Start the server (at the background):
```python
python run.py
```
### Navigate with a browser to the server address
If you running localy, then navigate to `http://localhost:5000` (port and host can of course be changed)

### Open the interactive shell
```python
python shell.py
```

### Optional : Pre flight scripts
Those are scripts that will execute on every registration of a new client. Use them wisely :)

##### Profit :)

### Usage
The shell interface contains various commands (can be revealed using the `help` command).
```bash
  ╦╔═╗╔═╗┬ ┬┌─┐┬  ┬
  ║╚═╗╚═╗├─┤├┤ │  │
 ╚╝╚═╝╚═╝┴ ┴└─┘┴─┘┴─┘
  By @Daniel_Abeles

>> help
+-------------+---------------------------------------------------------------+
| command     | description                                                   |
+-------------+---------------------------------------------------------------+
| list        | Lists all the clients registered                              |
| help        | self.help()                                                   |
| select <id> | Selected a specific client from the list                      |
| <command>   | Executes a command to the current selected client             |
| back        | Detaches from the current client                              |
| exit        | Exists this interactive shell                                 |
| coms        | Displays the commands and output for the current client       |
| com <id>    | Displays a specific command and output for the current client |
| comk        | Kills a command ("*" for all)                                 |
| clik        | Kills a client ("*" for all)                                  |
+-------------+---------------------------------------------------------------+                               

```
Utilizing the command queue, you can fire mutliple commands and the client will execute them one by one.
All the commands are executed using a single context, so all of the commands are aware of each other (same scope).

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

## Workflow
After all the installations and configuration is done, the workflow of the application is the following:

1. Client visits the home page `http://localhost:5000/` (or the host you chose)

2. The client makes an asynchronous `register` request to the server

3. Then he waits for commands

4. In the meanwhile, on the server, you execute commands using the `shell.py` script

5. The client probes the server for commands, when he sees a new one appeared, he pulls it and executes it

6. Once he's done executing, he will post back the result to the server

7. Now, using the `coms` command, you can see the output for that command


## Database Handling
I have included a script that I've been using during tests, which is the `db_handler.py` file. It includes varius function to handle and test your database.


## Credits
[Canop](https://github.com/Canop) for [JSON.prune](https://github.com/Canop/JSON.prune/)
