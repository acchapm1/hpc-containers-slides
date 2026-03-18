# Build on Laptop → Push to Docker Hub → Pull with Apptainer

---

### Step 1 — Write your Dockerfile (on your laptop)

```dockerfile
# Dockerfile
FROM python:3.11-slim

RUN pip install --no-cache-dir numpy scipy matplotlib pandas

WORKDIR /app

CMD ["python3", "-c", "import scipy; print('scipy', scipy.__version__)"]
```

---

### Step 2 — Build the Docker image (on your laptop)

```bash
# Build and tag with your Docker Hub username
docker build -t acchapm1/myanalysis:1.0 .

# Verify it built and runs
docker run --rm acchapm1/myanalysis:1.0

# Tag a 'latest' alias too (optional but common)
docker tag acchapm1/myanalysis:1.0 acchapm1/myanalysis:latest
```

---

### Step 3 — Push to Docker Hub (on your laptop)

```bash
# Log in (one-time, or when credentials expire)
docker login

# Push both tags
docker push acchapm1/myanalysis:1.0
docker push acchapm1/myanalysis:latest
```

Your image is now publicly available at `hub.docker.com/r/acchapm1/myanalysis`.

---

### Step 4 — Pull with Apptainer (on the HPC cluster)

```bash
# SSH into your cluster first
ssh acchapm1@sol.asu.edu

# Pull from Docker Hub — converts to .sif automatically
apptainer pull myanalysis.sif docker://acchapm1/myanalysis:1.0

# Always pin a version tag, not :latest
# :latest can change — :1.0 is frozen forever
```

The `docker://` prefix tells Apptainer to fetch from Docker Hub and convert the image layers into a `.sif` file in one step. No intermediate steps needed.

---

### Step 5 — Run it on the cluster

```bash
# Quick test — run the default CMD
apptainer run myanalysis.sif

# Run a specific command
apptainer exec myanalysis.sif python3 --version

# Interactive shell to explore
apptainer shell myanalysis.sif

# With scratch filesystem bound
apptainer exec \
    --bind $SCRATCH:/scratch \
    myanalysis.sif \
    python3 /scratch/my_script.py
```

---

### Step 6 — SLURM job script

```bash
#!/bin/bash
#SBATCH --job-name=myanalysis
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=logs/%j.out

module load apptainer

apptainer exec \
    --bind $SCRATCH:/scratch \
    $HOME/containers/myanalysis.sif \
    python3 /scratch/analysis/run.py

```

```bash
# Submit
mkdir -p logs
sbatch run.sh
```

---

### Updating the image later

When your code or dependencies change, the cycle is just:

```bash
# On your laptop — bump the version tag
docker build -t acchapm1/myanalysis:1.1 .
docker push acchapm1/myanalysis:1.1

# On the cluster — pull the new version
apptainer pull myanalysis_v1.1.sif docker://acchapm1/myanalysis:1.1
```

Old `.sif` files stay on disk untouched — you can keep multiple versions and switch between them by changing the filename in your SLURM script.

---

### Private Docker Hub repositories

If your image contains proprietary code or data you don't want public:

```bash
# On your laptop — push to a private repo (same commands, repo set to private on hub.docker.com)
docker push acchapm1/myanalysis-private:1.0

# On the cluster — authenticate first, then pull
apptainer registry login --username acchapm1 docker://docker.io
# enter your Docker Hub password or access token when prompted

apptainer pull private.sif docker://acchapm1/myanalysis-private:1.0
```

For tokens (recommended over passwords): Docker Hub → Account Settings → Security → New Access Token.

---

### Full workflow summary

```
YOUR LAPTOP                          DOCKER HUB              HPC CLUSTER
-----------                          ----------              -----------
docker build -t user/img:1.0 .  →   user/img:1.0   →   apptainer pull img.sif docker://user/img:1.0
docker push user/img:1.0             (stored)            apptainer exec img.sif python3 script.py
                                                         sbatch job.sh
```

The key advantage over building directly on the cluster: you have root on your laptop, so `docker build` runs without any `--fakeroot` workarounds, and you can test the container locally before it ever touches shared infrastructure.
