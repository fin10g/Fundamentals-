import paramiko

instance_ip="176.34.85.48" # CHANGE THIS
securityKeyFile="~/.ssh/UbuntuCT169.pem" # CHANGE THIS

searchTerm="Paul Thomas Anderson" # CHANGE THIS
cmd = "python3 ~/Desktop/1SDC1/Semester 2/Fundamentals of Cloud/Assignment Project/wiki.py" # CHANGE THIS

try:
    # Connect/ssh to an instance    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file(securityKeyFile)
    client.connect(hostname=instance_ip, username="ubuntu", pkey=key)
    
    # Execute a command(cmd) after connecting/ssh to an instance
    stdin, stdout, stderr = client.exec_command(cmd+" "+searchTerm)
    stdin.close()
    outerr = stderr.readlines()
    print("ERRORS: ", outerr)
    output = stdout.readlines()
    
    # Get/Use the result
    print("output:", output)
    for items in output:
        print(items, end="")
    
    # Close the client connection once the job is done
    client.close()
except Exception as e:
    print(e)