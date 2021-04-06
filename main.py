import logging
import paramiko

serverList = {'nginx': '192.168.0.119',
              'app': '192.168.0.118',
              'db': '192.168.0.117'}
credentials = {'login': 'ubuntu',
               'password': 'ubuntu'}
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class SSH:
    def __init__(self):
        pass

    def get_ssh_connection(self, ssh_machine, ssh_username, ssh_password):
        """Establishes a ssh connection to execute command.
          :param ssh_machine: IP of the machine to which SSH connection to be established.
          :param ssh_username: User Name of the machine to which SSH connection to be established..
          :param ssh_password: Password of the machine to which SSH connection to be established..
          returns connection Object
          """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ssh_machine, username=ssh_username, password=ssh_password, timeout=10)
        return client

    def run_sudo_command(self, ssh_username="root", ssh_password="abc123", ssh_machine="localhost", command="ls",
                         jobid="None"):
        """Executes a command over a established SSH connectio.
        :param ssh_machine: IP of the machine to which SSH connection to be established.
        :param ssh_username: User Name of the machine to which SSH connection to be established..
        :param ssh_password: Password of the machine to which SSH connection to be established..
        returns status of the command executed and Output of the command.
        """
        conn = self.get_ssh_connection(ssh_machine=ssh_machine, ssh_username=ssh_username, ssh_password=ssh_password)
        command = "sudo -S -p '' %s" % command
        logging.info("Job[%s]: Executing: %s" % (jobid, command))
        stdin, stdout, stderr = conn.exec_command(command=command)
        stdin.write(ssh_password + "\n")
        stdin.flush()
        stdoutput = [line for line in stdout]
        stderroutput = [line for line in stderr]
        for output in stdoutput:
            logging.info("Job[%s]: %s" % (jobid, output.strip()))
        # Check exit code.
        logging.debug("Job[%s]:stdout: %s" % (jobid, stdoutput))
        logging.debug("Job[%s]:stderror: %s" % (jobid, stderroutput))
        logging.info("Job[%s]:Command status: %s" % (jobid, stdout.channel.recv_exit_status()))
        if not stdout.channel.recv_exit_status():
            logging.info("Job[%s]: Command executed." % jobid)
            conn.close()
            if not stdoutput:
                stdoutput = True
            return True, stdoutput
        else:
            logging.error("Job[%s]: Command failed." % jobid)
            for output in stderroutput:
                logging.error("Job[%s]: %s" % (jobid, output))
            conn.close()
            return False, stderroutput


# excluded these 3 defs from class, just to separate tasks
def db_creation():
    connection = SSH()
    connection.run_sudo_command(
        ssh_username=credentials['login'],
        ssh_machine=serverList['db'],
        ssh_password=credentials['password'],
        command='sudo wget https://raw.githubusercontent.com/poolfire/pythontestproj/master/db_script.sh &&'
                'sudo bash db_script.sh')



def app_creation():
    connection = SSH()
    connection.run_sudo_command(
        ssh_username=credentials['login'],
        ssh_machine=serverList['app'],
        ssh_password=credentials['password'],
        command='sudo wget https://raw.githubusercontent.com/poolfire/pythontestproj/master/app_script.sh &&'
                'bash app_script.sh')


# please comment line
# f"sudo sed -i 's/127.0.0.1:5000/{serverList['app']}:5000/g' /etc/nginx/sites-available/default && "
# in case you need to use app server on the same host as nginx host
def nginx_creation():
    connection = SSH()
    connection.run_sudo_command(
        ssh_username=credentials['login'],
        ssh_machine=serverList['app'],
        ssh_password=credentials['password'],
        command="sudo wget https://raw.githubusercontent.com/poolfire/pythontestproj/master/nginx_script.sh && "
                "sudo bash nginx_script.sh && "
                f"sudo sed -i 's/127.0.0.1:5000/{serverList['app']}:5000/g' /etc/nginx/sites-available/default && "
                "sudo systemctl restart nginx")


if __name__ == '__main__':
    db_creation()
    app_creation()
    nginx_creation()
