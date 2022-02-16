import docker

HOST_DOCKER = 'unix://var/run/docker.sock'
client = docker.DockerClient(base_url=HOST_DOCKER)

def list():
    """
    Funcao para listar os containers
    """
    texto = ''
    container_list = client.containers.list() # Listando containers
    for container in container_list:
        container_short_id = container.short_id
        container_name = container.name
        container_attrs = container.attrs 
        container_status = container_attrs['State']['Status']
        texto += f'[{container_short_id}] - {container_name} - {container_status}\n'
    return texto


def info():
    container_info = client.info()
    return container_info

