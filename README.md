# JSShell

An interactive multi-user web based shell written in Python with Flask (for server side) and of course Javascript and HTML (client side). It was initally created in order to debug remote isoteric browsers during tests and research. I am well aware of other purposes this tool might serve, use it at your own responabilty and risk.

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
If you running localy, then navigate to `http://localhost:5000` (port can be changed)

### Open the interactive shell
```python
python shell.py
```
### Profit :)

### Usage
The shell interface contains various commands (can be reavealed using the `help` command).
```python
  ╦╔═╗╔═╗┬ ┬┌─┐┬  ┬
  ║╚═╗╚═╗├─┤├┤ │  │
 ╚╝╚═╝╚═╝┴ ┴└─┘┴─┘┴─┘
  By @Daniel_Abeles

>> help

list        | Lists all the clients registered                              
help        | self.help()                                                   
select <id> | Selected a specific client from the list                      
<command>   | Executes a command to the current selected client             
back        | Detaches from the current client                              
exit        | Exists this interactive shell                                 
coms        | Displays the commands and output for the current client       
com <id>    | Displays a specific command and output for the current client 
comk        | Kills a command ("*" for all)                                 
clik        | Kills a client ("*" for all)                                  

```
Utilizing the command queue, you can fire mutliple commands and the client will execute them one by one.
All the commands are executed using a single context, so you issue mutiple related commands.

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

## Database Handling
I have included a script that i've been using during tests, which is the `db_handler.py` file. It includes varius function to handle and test your database.


## Credits
[Canop](https://github.com/Canop) for [JSON.prune](https://github.com/Canop/JSON.prune/)
