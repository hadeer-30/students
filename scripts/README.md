Quick copy-paste in order: (assuming your `python` is 3.6+)

```bash
python -m scripts.netid-github-link
python -m scripts.student-names-from-bios
python -m scripts.assign-docker-ports
python -m scripts.make-ports-md > Ports.md
python -m scripts.get-ssh-keys
# on da2: (remember to commit/push/pull this repo with new changes)
sudo python3 -m scripts.da2.create-user-home-dirs
python3 -m scripts.da2.create-docker-containers
```

# Ordering for populating students.yml

- `scripts/netid-github-link.py` makes calls to github api, sets 'github' and creates netids in students.yml
- `scripts/student-names-from-bios.py` reads bio markdown files to get 'firstname' 'lastname'
- `scripts/assign-docker-ports.py` assigns ports to students for their docker containers

# Ports.md

Updating the markdown file with data from the yml:

```bash
python -m scripts.make-ports-md > Ports.md
```

# SSH keys

Pulls SSH keys from the github api for each student and puts the keys in the students.yml:

```bash
python -m scripts.get-ssh-keys
```

# da2 admin actions

Create user dirs and import ssh keys from the yml:

```bash
# REQUIRES ROOT, ONLY RUN ON DA2:
# Ensure you are in the repository directory!
sudo python3 -m scripts.da2.create-user-home-dirs
```

Starting the docker containers should NOT be run with root privs:

```bash
python3 -m scripts.da2.create-docker-containers
```

