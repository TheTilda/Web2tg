import subprocess
import uuid

# Function to create a new Docker container
def create_container():
    # Generate a unique container name
    container_name = str(uuid.uuid4())
    # Create the container
    subprocess.run(['docker', 'run', '-it', '--name', container_name, '-d', 'ubuntu'])
    # Get the container's IP address
    ip = subprocess.run(['docker', 'inspect', '-f', '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}', container_name], capture_output=True).stdout.strip()
    # Get the container's SSH port
    ssh_port = subprocess.run(['docker', 'inspect', '-f', '{{(index (index .NetworkSettings.Ports "22/tcp") 0).HostPort}}', container_name], capture_output=True).stdout.strip()
    # Print the container's SSH access information
    print(f"Container name: {container_name}")
    print(f"IP address: {ip}")
    print(f"SSH port: {ssh_port}")

# Create 5 containers
for i in range(5):
    create_container()

    app.run()
