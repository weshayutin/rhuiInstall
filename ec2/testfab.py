from fabric.api import env, run, put, settings
print "Hello"

env.host_string = 'ec2-23-20-133-37.compute-1.amazonaws.com'
env.user = "root"
env.key_filename = '/home/whayutin/.ec2/WESHAYUTIN/cloude-key.pem'

def deploy():
	env.host_string = 'ec2-23-20-133-37.compute-1.amazonaws.com'
	env.user = "root"
	env.key_filename = '/home/whayutin/.ec2/WESHAYUTIN/cloude-key.pem'
        #put('/home/whayutin/hostname.sh', '/root')
        run('xxhostname')

if __name__ == '__main__':
    deploy()
