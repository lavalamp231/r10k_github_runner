import os
import git
import time

cwd = os.getcwd()
control_repo = cwd + '/control-repo'
repo_dict = {}
puppet_environment_dir = '/etc/puppetlabs/code/environments/'
log_files = '/var/log/r10k/r10k_runner.txt'

def repo_change():
    my_repo = git.Repo(control_repo) # intialiazing repo
    puppet_environments = os.listdir(puppet_environment_dir) # variable for list of directories in /etc/puppetlabs/code/environments
    for branch in my_repo.branches: # loop to get every branch in my repo (for what ever reason it's not showing all branches - trying to figure shit out)
      #print(branch)
      my_repo.git.checkout(branch) # checking out each branch
      #my_repo.fetch()
      commit_count = len(list(my_repo.iter_commits(branch)))
      try:
        my_repo.git.pull()
      except:
        os.system(f"git branch --set-upstream-to=origin/{branch} {branch}")
      if branch not in repo_dict:
        repo_dict[branch] = {'Length': commit_count}
        length = repo_dict[branch]['Length']
        print(f"list length: {commit_count} in {branch}")
        print(f"length in dict: {length} in {branch}")
      else:
        length = repo_dict[branch]['Length']
        if length < commit_count:
          print(f"{branch} has changed")
          os.system(f"/usr/bin/r10k deploy environment {branch} && chmod 775 /etc/puppetlabs/code/environments/production/scripts/config_version.sh && chown -R puppet:puppet /etc/puppetlabs/code/")
          print(f"r10k creating {branch}")
          repo_dict[branch] = {'Length': commit_count}

        if str(branch) not in puppet_environments:
          os.system(f"/usr/bin/r10k deploy environment {branch}")
          print(f"{branch} is not in {puppet_environments}")
          print(f"r10k creating {branch}")

    time.sleep(5)

while True:
    repo_change()