import os
import git
import time

cwd = os.getcwd()
control_repo = cwd + '/control-repo'
git_repo = 'git@github.com:lavalamp231/control-repo.git'
repo_dict = {}
repo_list = []
puppet_environment_dir = '/etc/puppetlabs/code/environments/'
log_files = '/var/log/r10k/r10k_runner.txt'


def clone_repo():
  if not os.path.exists(control_repo):
    git.Git(cwd).clone(git_repo)

def repo_change():
    my_repo = git.Repo(control_repo) # intialiazing repo
    puppet_environments = os.listdir(puppet_environment_dir) # variable for list of directories in /etc/puppetlabs/code/environments
    for branch in my_repo.remotes.origin.refs:
      if branch not in repo_list:
        repo_list.append(str(branch))
    for branch in repo_list: # loop to get every branch in my repo (for what ever reason it's not showing all branches - trying to figure shit out)
      remote_branch = branch.split(" ")[0].replace("origin/", "")
      #print(branch)
      if remote_branch != "HEAD":
        my_repo.git.checkout(remote_branch) # checking out each branch
        #my_repo.fetch()
        commit_count = len(list(my_repo.iter_commits(remote_branch))) # length of the amount of commits in each branch
        try:
          my_repo.git.pull()
        except:
          os.system(f"git branch --set-upstream-to=origin/{remote_branch} {remote_branch}") # not too sure if this is what I should be doing or not. 
        if remote_branch not in repo_dict:
          repo_dict[remote_branch] = {'Length': commit_count}
          length = repo_dict[remote_branch]['Length']
          print(f"list length: {commit_count} in {remote_branch}")
          print(f"length in dict: {length} in {remote_branch}")
        else:
          length = repo_dict[remote_branch]['Length']
          if length < commit_count:
            print(f"{remote_branch} has changed")
            os.system(f"/usr/bin/r10k deploy environment {remote_branch} && chmod 775 /etc/puppetlabs/code/environments/{remote_branch}/scripts/config_version.sh && chown -R puppet:puppet /etc/puppetlabs/code/")
            print(f"r10k creating {remote_branch}")
            repo_dict[remote_branch] = {'Length': commit_count}

          if str(remote_branch) not in puppet_environments:
            os.system(f"/usr/bin/r10k deploy environment {remote_branch}")
            print(f"{remote_branch} is not in {puppet_environments}")
            print(f"r10k creating {remote_branch}")
          
          # for remote in repo_list:
          #   i = remote.split(" ")[0].replace("origin/", "")
          #   print(i)

    time.sleep(5)



while True:
    clone_repo()
    repo_change()