# Ambiente virtual
1. sudo apt install python3.9-venv
2. python3 -m venv .env
3. source .env/bin/activate
4. deactivate

# Compartilhamento do ambiente
1. pip freeze > requirements.txt
2. pip install -r requirements.txt

# Removendo o ambiente
1. deactivate
2. rm -r .env

# Containers para teste
1. docker container run --name web01 -d nginx
2. docker container run --name web02 -d htpd
3. docker container run --name -P web03-externo -d nginx
4. docker container run --name -P web04-externo -d nginx

# Em andamento...