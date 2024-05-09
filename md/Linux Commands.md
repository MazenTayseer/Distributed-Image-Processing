# Commands

List of Used Commands

## Downloading python on VM

```bash
sudo apt-get install python3
```

```bash
sudo apt update
```

```bash
sudo apt install python3-pip
```

```bash
sudo apt install python3-mpi4py
```

## Useful Commands

### Copy

- Copy to master001

```bash
scp "C:\Users\Mazii\Desktop\Semester 8\Distributed\Project\code\dist2.py" mazen@13.68.212.242:/home/mazen/mpi4py
```

- Copy to node001

```bash
scp "C:\Users\Mazii\Desktop\Semester 8\Distributed\Project\code\dist2.py" mazen@52.224.125.28:/home/mazen/mpi4py
```

### Run

```bash
mpirun -np 2 -machinefile myfile python3 dist2.py
```
