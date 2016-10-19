#def check_ssh(self, ip, user, key_file, initial_wait=0, interval=0, retries=1):
#    ssh = paramiko.SSHClient()
#    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
#    sleep(initial_wait)
#
#    for x in range(retries):
#        try:
#            ssh.connect(ip, username=user, key_filename=key_file)
#            return True
#        except Exception, e:
#            print e
#            sleep(interval)
#    return False
#
#
#!/usr/bin/python3
import paramiko
import cmd
import scp

class RunCommand(cmd.Cmd):
    '''Simple shell to run a command on the host'''

    prompt = 'ssh>'

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.hosts = []
        self.connections = []

    def do_add_host(self, args):
        '''add host to the host list'''
        if args:
            self.hosts.append(args.split(','))
        else:
            print('usage: host')

    def do_probe(self, args):
       '''probe ONE host if can be touched.'''
       ret = True
       client = paramiko.SSHClient()
       if args:
            try:
                host = args.split(',')
                #client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host[0], username=host[1], password=host[2])
                ret = True
            except Exception as e:
                print('Error Occured. host = %s %s' % (host, e))
                ret = False
            finally:
                client.close()
                return ret


    def do_connect(self, args=''):
        '''connect to all hosts in the hosts list'''
        for host in self.hosts:
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host[0], username=host[1], password=host[2])
                self.connections.append(client)
            except Exception as e:
                print('Error Occured. host = %s %s', host, e)
                continue

    def do_run(self, command):
        '''execute this command on all hosts in the list'''
        if command:
            for host, conn in zip(self.hosts, self.connections):
                stdin, stdout, stderr = conn.exec_command(command)
                stdin.close()
                for line in stdout.read().splitlines():
                    print('host: %s: %s' % (host[0], line.decode('utf-8')))
        else:
            print('usage: run')

    def do_sftp_get(self, remotefile, localfile):
        '''
        download the file ''remotefile'' from the remote system and write
        it to to the local file, ''localfile
        '''
        if remotefile and localfile:
            for host, conn in zip(self.hosts, self.connections):
                sftp = conn.open_sftp()
                sftp.get(remotefile, localfile + '_' + host[0])
                sftp.close()

    def do_sftp_put(self, localfile, remotefile):
        '''
        put the file ''localfile'' from local to remote remotefile
        '''
        if remotefile and localfile:
            for host, conn in zip(self.hosts, self.connections):
                sftp = conn.open_sftp()
                sftp.put(localfile, remotefile)
                sftp.close()

    def do_scp_get(self, remotefile, localfile):
        if remotefile and localfile:
            for host, conn in zip(self.hosts, self.connections):
                with scp.SCPClient(conn.get_transport()) as scp:
                    scp.get(remotefile, localfile + '_' + host[0])

    def do_scp_put(self, localfile, remotefile):
        if remotefile and localfile:
            for host, conn in zip(self.hosts, self.connections):
                with scp.SCPClient(conn.get_transport()) as s:
                    s.put(localfile, remotefile)

    def do_close(self, args):
        for conn in self.connections:
            conn.close()

    def do_test(self, args):
        print('XXXXXXXXXXXXXX')

import http.client
class HttpUtil():
    def httpget(ip, data, port=80):
        conn = http.client.HTTPConnection(ip, port)
        conn.request("GET", data)
        print(data)
        result = conn.getresponse()
        print(result.status, result.reason)

        data = result.read().decode('utf-8')
        print(data)
        conn.close()
        return data

    def httpcfg(ip, cmd):
        conn = http.client.HTTPConnection(ip, 80)
        req = "/vb.htm?" + cmd
        conn.request("GET", req)
        result = conn.getresponse()
        print(result.status, result.reason)

        data = result.read().decode('utf-8')
        print(data)
        conn.close()
        return data

if __name__ == '__main__':
    RunCommand().cmdloop()

##ssh = paramiko.SSHClient()
##
### automatically add untrusted host key.
##ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
##ssh.connect('192.168.1.153', username='durd', password='durd')
##stdin, stdout, stderr = ssh.exec_command('uptime')
##print(stdout.readlines())
