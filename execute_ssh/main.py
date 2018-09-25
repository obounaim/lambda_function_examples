import paramiko
import boto3
import base64
import io


def handler(event, context):
    encrypted_private_key = str(event['rsa_key_encrypted'])
    host_ip               = str(event['ip'])
    host_username         = str(event['username'])
    host_cmd              = str(event['cmd'])

    ssh_client = connect_ssh(host_ip, host_username, encrypted_private_key)

    result = execute_ssh_cmd(ssh_client, host_cmd)
 
    ssh_client.close()

    return result


def connect_ssh(host_ip, host_username, encrypted_private_key):
    aws_kms_client = boto3.client('kms')

    '''
    Decrypting private RSA key using KMS
    '''
    rsa_key_ciphertextblob = base64.b64decode(encrypted_private_key)
    rsa_key_temp           = aws_kms_client.decrypt(CiphertextBlob = rsa_key_ciphertextblob)
    rsa_key_bytes          = rsa_key_temp['Plaintext']
  
    '''
    Converting rsa_key_bytes from 'bytes' type to ASCII 'str'.
    Use StringIO to simulate file behaviour.
    Load RSA Key In Paramiko PKey object.
    '''
    rsa_key_str  = rsa_key_bytes.decode('ascii')
    rsa_key_file = io.StringIO(rsa_key_str)
    rsa_key      = paramiko.RSAKey(file_obj = rsa_key_file)

    '''
    Initialize Paramiko SSH client.
    Automatically acception host key.
    '''
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  
    '''
    Connection to host
    '''
    ssh_client.connect(host_ip, username = host_username, pkey = rsa_key) 
    return ssh_client


def execute_ssh_cmd(ssh_client, cmd):
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    result = ''
    for line in stdout:
        print('... ' + line.strip('\n'))
        result += line

    return result

