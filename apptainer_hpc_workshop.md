---
title: "Containers for HPC"
sub_title: "Getting Started with Apptainer"
author: "HPC Research Computing Workshop  ·  60 min  ·  20 min slides + 40 min hands-on"
theme:
  name: tokyonight-night
---

<!-- 
speaker_note: |
    Welcome everyone. Today's session is structured as two parts: about 20 minutes of slides to cover the "why and what," followed by 40 minutes of live hands-on demos where we'll actually build and run containers together.

    The core promise: by the end of this session, you'll be able to take any piece of software — any Python environment, any bioinformatics pipeline, any ML framework — freeze it in time, and run it identically on any HPC cluster, now or in five years.

    If you've ever said "it worked on my machine" or spent a day debugging a dependency conflict before you could even start your real work, this session is for you.

    Quick show of hands: Who has Docker experience? Who has used containers on HPC before? Good — we'll make sure we cover the fundamentals without assuming prior knowledge.
-->

<!-- end_slide -->

What Problem Are We Solving?
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

> **"It works on my laptop"**
> The classic research tragedy — your analysis runs fine locally but crashes on the cluster or a collaborator's machine.
<!--
speaker_note: |
    The Problem (2 min)
    Let's set the scene with problems everyone in this room has probably experienced.

    "It works on my laptop" — I want you to think about the last time you tried to run someone else's code, or reran your own code six months later. How long did it take to get it to run? If you're honest, the answer is probably "too long."
-->

<!-- pause -->

> **Dependency Hell**
> Conflicting Python, R, or CUDA versions across projects. Installing one package breaks another. Shared clusters can't satisfy everyone.

<!--
speaker_note: |
    Dependency hell is especially brutal on HPC clusters. You have one shared system, and the sysadmin can't install every version of every package for every user. So you end up in a maze of module load commands, conda environments that break each other, and Python version mismatches.
-->

<!-- column: 1 -->

<!-- pause -->

> **Irreproducibility**
> You can't re-run your own analysis 6 months later because the environment has changed. Reviewers can't reproduce your results.

<!--
speaker_note: |
    Irreproducibility isn't just an inconvenience — it's becoming a scientific crisis. Nature and Science have both published editorials about computational irreproducibility. When you submit a paper, reviewers are increasingly asking to re-run your code.
-->

<!-- pause -->

> **Collaboration Barriers**
> Sending setup instructions that span 3 pages of README is fragile. One missed step and it falls apart.

<!--
speaker_note: |
    And collaboration: sending someone a setup guide that says "install Python 3.9.2, then pip install these 15 packages in this exact order" is a recipe for frustration.
-->

<!-- reset_layout -->

<!-- new_line -->

<!-- pause -->

<span style="color: #00b4d8">**✓ Containers solve ALL of these — one file, everything inside it, runs everywhere.**</span>

<!--
speaker_note: |
    The good news — all four of these are solved by containers. One file, everything inside it, runs everywhere. Let's look at how.
-->

<!-- end_slide -->

What Is a Container?
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

## 📦 The Shipping Container Analogy

- A **standardized box** that works on any ship, truck, or dock
- Your container works on your **laptop, the cluster, and your collaborator's machine**
- Bundles your app + **ALL** its dependencies into **ONE portable file**
- Isolated from the host — no more *"which Python am I using?"*
- **Lightweight** — NOT a full VM, shares the host OS kernel

<!--
speaker_note: |
    Slide 3: What Is a Container? (2 min)

    Think about the standardized shipping container — before containers, every ship had to be loaded and unloaded differently, every dock had different equipment. The shipping container was revolutionary because it made the "box" standardized — the same box that goes on a ship goes on a truck goes in a warehouse.

    Software containers do the same thing. Your code and ALL its dependencies — Python, R, libraries, binaries, config files — go into one standardized box. That box runs identically on your laptop, on the HPC cluster, on AWS, on your collaborator's workstation.
-->

<!-- pause -->

<!-- column: 1 -->

### Container vs. Virtual Machine

| Feature   | Container     | VM          |
|-----------|---------------|-------------|
| Boot time | **< 1 sec**   | Minutes     |
| Size      | **MBs**       | GBs         |
| Overhead  | **Near zero** | Significant |
| Kernel    | **Shared**    | Own copy    |
| HPC ready | **✅ Yes**    | ❌ No      |

<!--
speaker_note: | 
The key thing to understand about how this differs from a Virtual Machine: containers are NOT running a full copy of an operating system. They share the host's kernel. This means they start in under a second (not minutes), they're small (megabytes, not gigabytes), and they have almost zero performance overhead — which is critical for scientific computing.
-->

<!-- pause -->

<!-- new_line -->

> **On HPC:** Container overhead is < 1-2% for most compute-bound workloads. You pay no meaningful performance tax.

<!-- reset_layout -->

<!--
speaker_note: |
    On HPC specifically, we've measured container overhead at less than 1-2% for most compute-bound workloads. You're not paying a meaningful performance tax.
-->

<!-- end_slide -->

Docker vs. Apptainer: Why Not Just Use Docker?
===

<!-- column_layout: [2, 1, 1] -->

<!-- column: 0 -->

| Feature                      | Docker                 | Apptainer            |
|------------------------------|------------------------|----------------------|
| Requires root/sudo           | ✅ Yes                 | ❌ No               |
| Runs as your user            | ❌ No                  | ✅ Yes              |
| Security model               | Daemon = **root risk** | **Rootless** by design |
| HPC scheduler (SLURM/PBS)    | ❌ Problematic         | ✅ Native support   |
| Shared filesystems (Lustre)  | ⚠️ Issues             | ✅ Seamless         |
| Import Docker images         | N/A                    | ✅ `docker://`      |
| Portable single file         | ❌ No                  | ✅ `.sif` file      |

<!-- reset_layout -->

<!-- new_line -->

> 🔑 **The core problem with Docker on HPC:** The Docker daemon runs as **root**. On a shared cluster with thousands of users and petabytes of data, anyone who can run Docker can trivially escalate to root on the host. HPC sysadmins universally ban it.

<!-- new_line -->

<span style="color: #00b4d8">**Apptainer was built from the ground up in 2015 specifically for shared HPC systems. A user inside a container is always the same user outside.**</span>

<!--
speaker_note: |
    SPEAKER NOTES — Slide 4: Docker vs. Apptainer (3 min)

    This is the most important slide in the talk, so let's spend a moment on it.

    Docker is fantastic — it's the dominant container technology in industry, it has a huge ecosystem, and we can actually reuse Docker images directly in Apptainer. So why not just use Docker on HPC?

    The answer comes down to one word: root.

    Docker works by running a daemon — a background service — as the root user. When you run a Docker container, you're effectively getting root access on that machine. On your personal laptop, that's fine. On a shared HPC cluster with thousands of users and petabytes of research data, that's a catastrophic security risk. Anyone who can run Docker can trivially escalate to root on the host system.

    This is why HPC sysadmins universally say no to Docker. I've never seen a production HPC cluster that allows Docker for general users.

    Apptainer — previously called Singularity — was built from the ground up in 2015 specifically because of this problem. Its core design principle is: a user inside a container is the same user outside. You can never get more privileges than you started with.

    It also produces a single .sif file — a Singularity Image Format file — that you can just copy around like any other file. No daemon, no background process, no root. Just a file.

    And critically — it can import and run Docker images directly. So the entire Docker Hub ecosystem is available to you.
-->

<!-- end_slide -->

How Apptainer Works on HPC
===

<!-- column_layout: [1, 1, 1, 1] -->

<!-- column: 0 -->
**1 · Definition File**

📄 Plain text recipe  
`.def` file in Git  
Version controlled  

<!-- column: 1 -->
**2 · Build Once**

🔨 `apptainer build`  
Creates `.sif` file  
Run as user/fakeroot  

<!-- column: 2 -->
**3 · One File**

📦 Copy, share, store  
`rsync` it anywhere  
Archive with data  

<!-- column: 3 -->
**4 · Run Everywhere**

🚀 Cluster, cloud, laptop  
SLURM native  
Same command always  

<!-- reset_layout -->

<!-- new_line -->

### Key Behaviours

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

- 🔐 Runs under **your UID** — no privilege escalation ever
- 📂 Auto-mounts `$HOME`, current dir, and `/tmp`
- 💾 Use `--bind` to mount Scratch/Lustre storage

<!-- column: 1 -->

- 🐳 Imports Docker Hub images via `docker://` prefix
- 🖥️ Works natively with SLURM — prefix with `apptainer exec`
- 🔒 Container filesystem is **read-only** at runtime

<!-- reset_layout -->

<!--
speaker_note: |
    SPEAKER NOTES — Slide 5: How Apptainer Works (2 min)

    Let me walk you through the workflow — four steps.

    First, you write a definition file. It's just a plain text file that describes what goes in your container — what base image to start from, what packages to install, what environment variables to set. We'll look at these in detail shortly, and you can check them into Git just like your code.

    Second, you run apptainer build. This creates a .sif file — your container. This is the only step that might require elevated privileges, and we'll talk about ways around that in a moment.

    Third — and this is beautiful — you have one file. You can cp it, rsync it to another cluster, share it with a collaborator, archive it with your data. Five years from now, that file still runs exactly the same way.

    Fourth, you run it. Anywhere. On your workstation, on the cluster, in a SLURM job script — it's the same command.

    A few key behaviours to know: Apptainer automatically makes your home directory available inside the container. Your $HOME mounts through transparently. So your scripts, your data files in home — they're all accessible. If your data is on scratch or a Lustre filesystem, you add --bind /scratch:/scratch and it's mounted inside the container too.
-->

<!-- end_slide -->

Key Apptainer Commands
===

*90% of your day-to-day usage fits in four commands*

<!-- new_line -->

<!-- pause -->

**`apptainer pull`** — Download a pre-built image from Docker Hub. Millions available. No build required.

```bash
apptainer pull python311.sif docker://python:3.11-slim
```

<!-- pause -->

**`apptainer shell`** — Drop into an interactive shell inside the container. Great for exploring and debugging.

```bash
apptainer shell myenv.sif
```

<!-- pause -->

**`apptainer exec`** — Run a single command inside the container. Used in SLURM job scripts.

```bash
apptainer exec myenv.sif python3 analysis.py
```

<!-- pause -->

**`apptainer build`** — Build your own image from a definition file. Your reproducibility recipe.

```bash
apptainer build myenv.sif myenv.def
```

<!--
speaker_note: |
    SPEAKER NOTES — Slide 6: Key Commands (2 min)

    You really only need four commands to be productive with Apptainer, and we'll use all of them in the demo.

    apptainer pull is your entry point into the ecosystem. Docker Hub has millions of images — Python, R, Ubuntu, CUDA, Bioconductor, all the major bioinformatics tools. You can pull any of them and have a running environment in minutes without writing a single line of a definition file.

    apptainer shell is your interactive exploration mode. Think of it like SSH-ing into a lightweight environment. You get a command prompt inside the container, you can run commands, check which packages are installed, test your workflow interactively. When you're done, just type exit.

    apptainer exec is what you'll use in production. It runs one command inside the container and exits. This is what goes in your SLURM job scripts. It's non-interactive and scriptable — perfect for batch computing.

    apptainer build is where you define your own environment from scratch using a definition file. We'll spend a chunk of the demo building definition files, because this is where the real reproducibility magic lives.

    In the demo we'll go through each of these in order, starting with pull and building up to running jobs in SLURM.
-->

<!-- end_slide -->

Definition Files: Your Reproducibility Recipe
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

### Why use `.def` files?

- 📄 **Version control** — check into Git alongside your code
- 🔄 **Rebuild anytime** — anyone can recreate the exact environment
- 📖 **Self-documenting** — the `.def` file IS the documentation
- 🤝 **Share the recipe** — send the `.def`, not the gigabyte `.sif`
- 🔬 **Peer review** — reviewers can verify and re-run your exact setup

<!-- column: 1 -->

```bash
# myenv.def

Bootstrap: docker        # start from Docker Hub
From: ubuntu:22.04       # base image

%post                    # runs during BUILD (as root)
    apt-get install -y python3
    pip install numpy scipy

%environment             # set at RUNTIME
    export PATH=/opt/app:$PATH
    export LC_ALL=C

%runscript               # default command
    python3 analysis.py
```

<!-- reset_layout -->

<!-- new_line -->

> 💡 **Key insight:** `Bootstrap` + `From` tap the entire Docker Hub ecosystem. Start from Python, R, Ubuntu, CUDA, Bioconductor — whatever fits your project.

<!--
speaker_note: |
    SPEAKER NOTES — Slide 7: Definition Files (3 min)

    The definition file — the .def file — is the heart of reproducibility with Apptainer. Think of it as a Dockerfile, but for HPC.

    It's a plain text file. You can open it in any text editor. And I want to emphasize that you should absolutely version-control this file in Git alongside your analysis code. When your .def file is in Git, you have a complete, reproducible record of your entire computational environment at every point in time.

    Let me walk through the sections:

    Bootstrap and From tell Apptainer where to start. We almost always start from an existing Docker Hub image — Ubuntu, Python, a Bioconductor image, whatever makes sense for your project. This is where the Docker ecosystem integration really pays off.

    %post is the installation section. It runs once when you're building the container, and it runs as root. So you can install anything — apt packages, pip packages, conda packages, compile from source. Whatever you need. And because it runs during build and is baked in, your users never need to install anything.

    %environment sets environment variables that will be active every time the container runs. PATH modifications, library paths, locale settings — this all goes here.

    %runscript is optional — it defines a default command that runs when someone calls apptainer run. Think of it like the ENTRYPOINT in Docker.

    The key insight: this file IS your documentation. When a collaborator or reviewer gets your container, they can look at this file and see exactly what was installed and how. That's the gold standard for computational reproducibility.
-->

<!-- end_slide -->

Real Research Use Cases
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

### 🧬 Bioinformatics

- Pin exact GATK, BWA, Samtools versions
- Share complete pipeline with your paper
- Run legacy tools on modern clusters
- Increasingly required by journals (Nature Methods)

<!-- pause -->

### 🧠 ML / Deep Learning

- Freeze CUDA + PyTorch + driver versions
- Guarantee GPU code reproduces exactly
- Move between GPU cluster generations seamlessly

<!-- column: 1 -->

<!-- pause -->

### 🐍 Python / R Science

- No more conda environment conflicts
- Isolate per-project dependencies
- Collaborate across lab members safely

<!-- pause -->

### 🗄️ Legacy Code & Archive

- Run 2015 workflows on 2025 clusters
- Archive containers alongside published data
- Meet journal reproducibility requirements

<!-- reset_layout -->

<!-- new_line -->

> 💡 **Pattern:** Build once → archive the `.sif` with your data → anyone re-runs your analysis years later with zero setup friction.

<!--
speaker_note: |
    SPEAKER NOTES — Slide 8: Use Cases (2 min)

    Let me make this concrete with examples from actual research workflows.

    Bioinformatics is probably the most mature use case. Genomics pipelines — GATK, BWA, Samtools — have very specific version dependencies. A GATK 3.x pipeline is completely different from GATK 4.x. Containerizing your pipeline means that five years later, when someone wants to reanalyze your data, they run the exact same software you used. This is increasingly a requirement for journals like Nature Methods.

    Machine Learning and GPU computing is the other big one. Getting CUDA, cuDNN, PyTorch, and your specific driver version all working together is a nightmare. You do it once, you containerize it, and now that exact stack is frozen. When the cluster upgrades their drivers or when you move from one GPU generation to another, your container handles the compatibility layer.

    For Python and R — instead of maintaining one giant conda environment that everyone shares and no one dares update, each project gets its own container. Your RNA-seq project has one environment, your proteomics project has another, and they never conflict.

    And legacy code — this is underappreciated. If you're an HPC admin, you know the pain of users who have code that only runs on CentOS 7 that you decommissioned two years ago. Containers solve this permanently. The 2015 workflow runs inside a 2015-era container on your 2025 cluster.
-->

<!-- end_slide -->

Typical HPC Workflow
===

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   1. BUILD      │───▶│   2. STORE      │───▶│   3. TEST       │───▶│   4. RUN        │
│                 │    │                 │    │                 │    │                 │
│ apptainer build │    │ $HOME/containers│    │ apptainer shell │    │ sbatch job.sh   │
│ myenv.sif       │    │ /myenv.sif      │    │ myenv.sif       │    │ (apptainer exec │
│ myenv.def       │    │                 │    │                 │    │  inside)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

<!-- new_line -->

### Typical SLURM job script

```bash
#!/bin/bash
#SBATCH --job-name=myanalysis
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --output=logs/%j.out

module load apptainer

apptainer exec \
    --bind $SCRATCH:/scratch \
    $HOME/containers/myenv.sif \
    python3 /scratch/my_analysis.py
```

> 💡 **The scheduler sees a normal job.** `apptainer exec` is completely transparent to SLURM — no special configuration needed.

<!--
speaker_note: |
    SPEAKER NOTES — Slide 9: HPC Workflow (2 min)

    Here's what your day-to-day workflow looks like in practice.

    Step 1 is building your container. You do this once — or whenever your software requirements change. Now, building requires root or --fakeroot access, which varies by cluster. Most clusters either have --fakeroot configured, or they provide access to Sylabs Cloud — a free web service where you submit your .def file and they build the .sif for you. We'll talk about your specific cluster's setup.

    Step 2 is storing it. Usually in your home directory under a containers/ folder, or in shared lab storage if your whole group uses the same environment. The .sif file is just a file — treat it like your data.

    Step 3 is testing interactively. Before you submit a big job, do apptainer shell and poke around. Make sure your packages are installed, your scripts can see the data you expect.

    Step 4 is production. This SLURM script is what most of you will end up with. Notice how it's just a normal SLURM script — the container is completely transparent to the scheduler. You just prefix your command with apptainer exec and tell it where the .sif file is.

    The --bind $SCRATCH:/scratch flag makes your cluster's scratch filesystem available at /scratch inside the container. Your analysis script writes to /scratch/results, and those files are actually being written to your cluster's scratch storage. Perfect.
-->

<!-- end_slide -->

Tips & Gotchas
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

### 🔧 Building — needs root or a workaround

```bash
# Option 1: fakeroot (most clusters)
apptainer build --fakeroot myenv.sif myenv.def

# Option 2: build remotely (free, no root)
# Upload .def to cloud.sylabs.io
# Download finished .sif
```

<!-- pause -->

### 🔒 Container filesystem is READ-ONLY

```bash
# WRONG — can't write inside the container
apptainer exec myenv.sif touch /opt/newfile

# RIGHT — write to bound host paths
apptainer exec --bind $SCRATCH:/scratch \
    myenv.sif python3 script.py
#   (script writes to /scratch/results)
```

<!-- column: 1 -->

<!-- pause -->

### 🖥️ GPU Jobs — the `--nv` flag

```bash
# Pass through NVIDIA GPU from host
apptainer exec --nv pytorch.sif python3 train.py

# In SLURM: request GPU first
#SBATCH --gres=gpu:1
apptainer exec --nv pytorch.sif python3 train.py
```

<!-- pause -->

### 💾 Large Image Cache

```bash
# Default cache can fill your home quota
# Redirect to scratch:
export APPTAINER_CACHEDIR=$SCRATCH/.appcache

# Inspect any image
apptainer inspect --deffile image.sif
apptainer inspect --labels  image.sif
```

<!-- reset_layout -->

<!-- speaker_note: |
    SPEAKER NOTES — Slide 10: Tips & Gotchas (2 min)

    Before we jump into the demo, let me flag the common stumbling blocks so you're prepared.

    Building — this trips people up most. apptainer build needs either root or --fakeroot. On most modern clusters, --fakeroot is configured. If not, Sylabs Cloud at cloud.sylabs.io lets you upload your .def file and they build the .sif for free. You can also build on your own laptop if you have root there and then copy the .sif to the cluster.

    Read-only filesystem — once a container is built, its internal filesystem is locked. You cannot write files inside it. This is actually a feature for reproducibility, but it means all your outputs have to go to bound paths — your home directory, scratch, etc. We'll demonstrate this.

    MPI jobs — for parallel jobs across multiple nodes, the recommended approach is to let the host's MPI handle the process spawning, and have Apptainer just wrap the actual application code. Your sysadmin will have guidance on the right flags for your specific MPI setup.

    GPU support is almost magical — you just add --nv to your apptainer exec command and NVIDIA GPU access passes through from the host. Your container can use the GPU without any special driver installation inside the container.

    Cache management — big images like PyTorch with CUDA can be several gigabytes. By default they cache in your home directory. If your home has a quota, redirect the cache to scratch with the environment variable shown.
-->

<!-- end_slide -->

<!-- jump_to_middle -->

HANDS-ON DEMOS
===

<span style="color: #00b4d8">*40 minutes · 5 exercises · stay in your terminal*</span>

<!-- end_slide -->

Demo 1 — Pull & Explore a Pre-built Image
===

<span style="color: #f59e0b">⏱ 8 min  ·  "Zero to running in 2 minutes"</span>

<!-- new_line -->

**Step 1 — Pull Python 3.11 from Docker Hub**

```bash +exec
# Pull Python from Docker Hub (~200MB, takes 1-2 min)
apptainer pull python311.sif docker://python:3.11-slim
echo "Pull complete. File size:"
ls -lh python311.sif 2>/dev/null || echo "(run on your cluster)"
```

<!-- pause -->

**Step 2 — Compare host vs container Python**

```bash
# Your host Python
python3 --version

# Container Python (different version, isolated)
apptainer exec python311.sif python3 --version
```

<!-- pause -->

**Step 3 — Drop into an interactive shell**

```bash
apptainer shell python311.sif
# Apptainer> whoami          ← same username as host!
# Apptainer> echo $HOME      ← your home dir is mounted
# Apptainer> pip list        ← see installed packages
# Apptainer> exit
```

<!-- new_line -->

> 👁 **Notice:** Same username inside and outside. `$HOME` already mounted. No `sudo` anywhere.

<!--
speaker_note: |
    SPEAKER NOTES — Demo 1: Pull & Explore (8 min)

    [BEFORE starting: make sure participants have Apptainer loaded — 'module load apptainer' or 'module load singularity' depending on your cluster. Have everyone open a terminal.]

    Let's start with the simplest possible thing — pulling a pre-built image from Docker Hub. No definition file, no building, just downloading and running.

    [Type the pull command]
    "Watch the progress bar — it's downloading layers from Docker Hub and assembling them into a single .sif file. Depending on network speed this takes 1-2 minutes. While it downloads, notice the command — docker://python:3.11-slim. That docker:// prefix is telling Apptainer to go to Docker Hub and pull the 'python' image, version '3.11-slim'. The slim variant is a minimal image — just what we need."

    [While it downloads, talk through what a .sif file is — immutable squashfs archive]

    [After pull completes]
    "Now let's do something revealing. Check your host Python version, then check the container's Python version."
    [run both commands]
    "Different versions, right? And crucially — neither affected the other. They're completely isolated."

    [Shell into the container]
    "Now let's get interactive. Notice when you're inside — your prompt changes to 'Apptainer>'. You're in a different environment, but look:"
    [run 'whoami' and 'ls $HOME']
    "Same username. Same home directory mounted. The container is transparent for things that should be transparent."

    [Type exit]
    "And we're back. That's it — zero to running in under 5 minutes. Questions on this part?"

    [Pause for questions — 1 min]
-->

<!-- end_slide -->

Demo 2 — Build a Simple Science Image
===

<span style="color: #f59e0b">⏱ 10 min  ·  "Your first definition file"</span>

<!-- new_line -->

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

**scipy-demo.def**

```bash
Bootstrap: docker
From: python:3.11-slim

%post
    pip install --no-cache-dir \
        numpy scipy matplotlib

%runscript
    python3 -c "
import numpy as np
from scipy import stats
data = np.random.normal(5, 2, 1000)
print(f'Mean:  {data.mean():.3f}')
print(f'Stdev: {data.std():.3f}')
t, p = stats.ttest_1samp(data, 5)
print(f't={t:.3f}  p={p:.4f}')
"
```

<!-- column: 1 -->

**Build & run**

```bash
# Write the def file
nano scipy-demo.def

# Build the container
apptainer build \
    scipy-demo.sif \
    scipy-demo.def

# Check file size
ls -lh scipy-demo.sif

# Run the %runscript
apptainer run scipy-demo.sif

# Confirm container Python version
apptainer exec scipy-demo.sif \
    python3 --version
```

<!-- reset_layout -->

<!-- new_line -->

> 🎯 **Reproducibility magic:** Send the 300MB `.sif` to anyone → identical output, same numpy/scipy versions, guaranteed.

<!--
speaker_note: |
    SPEAKER NOTES — Demo 2: Build a Science Image (10 min)

    [Have participants open a text editor to follow along]

    Now we're going to build our first container from scratch using a definition file. This is the core skill.

    [Walk through writing the .def file]
    "Let's create scipy-demo.def. The Bootstrap and From lines say 'start from the official Python 3.11 slim image on Docker Hub.'"

    "The %post section has one job: install our scientific Python stack. The --no-cache-dir flag keeps the image smaller by not storing the pip download cache."

    "The %runscript is a little self-contained statistics demo — generate 1000 samples from a normal distribution and run a t-test. This is a toy example but it shows the pattern: your actual analysis script would go here."

    [Run the build command — takes 2-3 min]
    "apptainer build scipy-demo.sif scipy-demo.def — watch the output. You'll see it pulling the base layer, then running your %post commands. Every apt install, every pip install — it's baking it all in."

    [While building]
    "Notice we didn't need sudo anywhere — if your cluster has --fakeroot configured this runs entirely as you. If you're getting a permission error, add '--fakeroot' to the build command."

    [After build completes]
    "ls -lh — how big is your .sif? Typically 150-300MB for this one. Now run it."

    [apptainer run scipy-demo.sif]
    "There's your t-test output. Now here's the reproducibility magic — I can send you this 300MB .sif file and you will get identical output. Same numpy random seed behavior, same scipy version, same everything."

    "Try apptainer exec scipy-demo.sif python3 --version — confirm it's using the containerized Python, not your host Python."

    [Pause for questions — 1 min]
-->

<!-- end_slide -->

Demo 3 — Bioinformatics Pipeline Container
===

<span style="color: #f59e0b">⏱ 10 min  ·  "Real-world research example — FastQC + MultiQC"</span>

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

**bioinfo.def**

```bash
Bootstrap: docker
From: ubuntu:22.04

%post
    apt-get update -y
    apt-get install -y \
        python3 python3-pip \
        wget curl fastqc
    pip3 install multiqc

%environment
    export LC_ALL=C   # required!
    export LANG=C

%runscript
    echo "=== Bioinformatics Tools ==="
    fastqc --version
    multiqc --version
```

<!-- column: 1 -->

**Build & run on data**

```bash
# Build (~3-4 min — more packages)
apptainer build \
    bioinfo.sif bioinfo.def

# Verify tools installed
apptainer run bioinfo.sif

# Run FastQC on your data
# (--bind makes ./data visible as /data)
apptainer exec \
    --bind ./data:/data \
    bioinfo.sif \
    fastqc /data/sample.fastq.gz \
    -o /data/results/

# Aggregate with MultiQC
apptainer exec \
    --bind ./data:/data \
    bioinfo.sif \
    multiqc /data/results/
```

<!-- reset_layout -->

<!-- new_line -->

> 🔑 **The bind mount pattern:** Container is read-only. All I/O happens through `--bind` paths. Your data never enters the container image.

<!--
speaker_note: |
    SPEAKER NOTES — Demo 3: Bioinformatics Pipeline (10 min)

    [For non-bioinformatics audiences, frame this as "a real production pipeline" — the specific tools aren't the point, the pattern is]

    This demo is for anyone who works with sequencing data, but even if you don't, pay attention to the pattern — it applies to any domain-specific toolchain.

    We're building a container with FastQC for quality control of raw sequencing reads, and MultiQC for aggregating the reports. These are tools that have very specific system dependencies — FastQC needs a particular Java version, specific Perl modules. On a shared cluster you often can't guarantee those are available. In a container, it doesn't matter.

    [Walk through the .def file]
    "Notice the %environment section — LC_ALL and LANG. These aren't optional for bioinformatics tools on Ubuntu. FastQC will produce cryptic errors without the locale set correctly. This is exactly the kind of tribal knowledge that lives in a well-maintained .def file."

    [Build the container — 3-4 minutes]
    "This one takes a bit longer because apt-get is downloading more packages."

    [After build]
    "apptainer run bioinfo.sif — it runs the %runscript and tells you what versions are installed. That's your container's manifest."

    [Bind mount demo]
    "Now the critical piece — the --bind flag. Our data is in ./data on the host. We tell Apptainer to make that available at /data inside the container. The FastQC command then reads from /data and writes results to /data/results — which is actually writing to ./data/results on the host. The data never goes inside the container."

    [If you have sample FASTQ data, run FastQC on it. Otherwise show the command.]

    "This bind mount pattern is how all your HPC workflows should be structured — container is read-only, all I/O happens through bound host paths."

    [Questions — 1 min]
-->

<!-- end_slide -->

Demo 4 — SLURM Job Script Integration
===

<span style="color: #f59e0b">⏱ 7 min  ·  "Submitting container jobs to the scheduler"</span>

<!-- new_line -->

**run_analysis.sh**

```bash +line_numbers
#!/bin/bash
#SBATCH --job-name=apptainer-demo
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4          # 4 CPU cores
#SBATCH --mem=8G                   # 8 GB RAM
#SBATCH --time=01:00:00            # 1 hour walltime
#SBATCH --output=logs/%j.out      # log per job ID

# Load apptainer module (cluster-specific)
module load apptainer

# Run analysis inside container
apptainer exec \
    --bind $SCRATCH:/scratch \          # mount Lustre scratch
    $HOME/containers/scipy-demo.sif \   # your .sif file
    python3 /scratch/analysis/my_analysis.py
```

<!-- new_line -->

<!-- column_layout: [1, 1, 1] -->

<!-- column: 0 -->
**Submit**

```bash
mkdir -p logs
sbatch run_analysis.sh
```

<!-- column: 1 -->
**Monitor**

```bash
squeue -u $USER
```

<!-- column: 2 -->
**Cancel**

```bash
scancel <jobid>
```

<!-- reset_layout -->

<!-- new_line -->

> 💡 **SLURM sees a normal job.** No special configuration. Just prefix your command with `apptainer exec` — the rest is identical to any other batch script.

<!--
speaker_note: |
    SPEAKER NOTES — Demo 4: SLURM Integration (7 min)

    [This is the most practical demo for HPC users — everyone submits SLURM jobs]

    This is where everything comes together. The beautiful thing about Apptainer on SLURM is how transparent it is — the scheduler doesn't know or care that you're using a container. From SLURM's perspective, it's just another job.

    [Walk through the script line by line]

    "Standard SLURM headers — job name, cores, memory, time. Nothing container-specific here."

    "module load apptainer — depending on your cluster this might be 'module load singularity' or it might already be in your PATH. Check your cluster docs."

    "Then the key line: apptainer exec, followed by your flags, the path to your .sif, then the command to run inside it. That's it. The SLURM scheduler allocates your resources, starts your job on a compute node, and apptainer exec launches your analysis inside the container."

    "The --bind $SCRATCH:/scratch is critical for most HPC workflows. Your data lives on Scratch — a high-performance parallel filesystem. You bind it into the container so your analysis script can read from it and write results to it."

    [Write the script together and submit it]
    "Let's actually submit this. sbatch run_analysis.sh."

    [Show squeue output]
    "See your job in the queue? SLURM is treating it like any other job — it'll schedule it, run it, and the output goes to your log file."

"One tip: always create a logs/ directory before submitting if you're using %j in the output path. SLURM won't create it for you."

    [Discuss job arrays for parameter sweeps — great use case for containers]
    "Bonus tip: container + SLURM job arrays is an incredibly powerful pattern for parameter sweeps. Same container, 100 different input files, all running in parallel. Ask me about this if you want to explore it."

    [Questions — 1 min]
-->

<!-- end_slide -->

Demo 5 — GPU Container: PyTorch + CUDA
===

<span style="color: #f59e0b">⏱ 5 min  ·  "NVIDIA GPU passthrough — the --nv flag"</span>

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

**pytorch-gpu.def**

```bash
Bootstrap: docker
From: pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

%post
    pip install --no-cache-dir \
        torchvision torchaudio

%runscript
    python3 -c "
import torch
print('PyTorch:', torch.__version__)
print('CUDA available:', torch.cuda.is_available())
if torch.cuda.is_available():
    gpu = torch.cuda.get_device_name(0)
    print('GPU:', gpu)
"
```

<!-- column: 1 -->

**Run with GPU passthrough**

```bash
# Build (5+ min — large base image)
apptainer build \
    pytorch.sif pytorch-gpu.def

# Without --nv: no GPU access
apptainer run pytorch.sif
# → CUDA available: False

# With --nv: GPU passes through!
apptainer run --nv pytorch.sif
# → CUDA available: True
# → GPU: NVIDIA A100 80GB

# In a SLURM script:
# #SBATCH --gres=gpu:1
apptainer exec --nv \
    pytorch.sif python3 train.py
```

<!-- reset_layout -->

<!-- new_line -->

> 🎮 **`--nv` magic:** The flag binds NVIDIA drivers from the host into the container. No CUDA installation needed inside the image — it inherits the host's GPU driver automatically.

<!--
speaker_note: |
    SPEAKER NOTES — Demo 5: GPU Container (5 min)

    [Only run this demo if GPU nodes are accessible. Otherwise walk through the code and explain conceptually]

    GPU computing is one of the areas where Apptainer really shines, because getting the CUDA stack right is historically painful. The wrong driver version, the wrong cuDNN, the wrong PyTorch — and your code either won't run at all or runs 10x slower than expected.

    [Walk through the .def file]
    "Notice the base image: pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime. This is an official PyTorch image from Docker Hub with a specific CUDA version baked in. This is the recommended approach — start from a pre-built CUDA image rather than trying to install CUDA yourself. NVIDIA maintains these images and they Just Work."

    "We add torchvision and torchaudio on top. The whole stack — CUDA runtime, cuDNN, PyTorch — is frozen at these exact versions."

    [Run without --nv first]
    "First, run it without the --nv flag. CUDA shows as False — the container can't see the GPU because we haven't passed it through."

[Run with --nv]
"Now add --nv. Magic. The container can now see the GPU. No driver installation, no CUDA install in the container — the --nv flag handles all the driver binding from the host into the container."

"This works because the CUDA runtime in the container talks to the host's GPU driver through a well-defined interface. As long as the host driver is recent enough to support your CUDA version, it works."

    [SLURM note]
    "In a SLURM script, you first request the GPU with --gres=gpu:1, and then use --nv in your apptainer exec. SLURM allocates the GPU, and Apptainer passes it through to your container."

    "The practical upside: one .sif file works on any NVIDIA cluster, regardless of which generation of GPU they have."

    [Final Q&A wrap-up]
-->

<!-- end_slide -->

<!-- jump_to_middle -->

Key Takeaways & Resources
===

<!-- end_slide -->

Key Takeaways
===

<!-- incremental_lists: true -->

- 📦 **One `.sif` file = your entire software environment, frozen in time**
  *Not a requirements.txt — the `.sif` IS the environment, ready to run*

- 👤 **Runs as YOU — same UID inside and outside. No root, no risk.**
  *This is why sysadmins allow it — it can't escalate privileges*

- 🐳 **The entire Docker Hub ecosystem works via `docker://` prefix**
  *Millions of images: Python, R, CUDA, Bioconductor, GATK, and more*

- 📄 **`.def` files in Git = reproducible, peer-reviewable science**
  *Your environment is code — version control it like code*

- 🖥️ **Transparent to SLURM — just prefix with `apptainer exec`**
  *No special scheduler config, no sysadmin intervention needed*

<!--
speaker_note: |
    SPEAKER NOTES — Slide 16: Wrap-up & Q&A (5 min)

    [Summarize each point briefly, then open to questions]

    Let's land on the five things I want you to walk away with.

    One: One .sif file is your entire environment. Not a requirements.txt — that still requires someone to reconstruct the environment. The .sif IS the environment. Ready to run, no assembly required.

    Two: The security model. You always run as yourself. If you're user jsmith on the cluster, you're jsmith inside the container. You cannot escalate privileges. This is why sysadmins actually like Apptainer — it's the container technology that doesn't terrify security teams.

    Three: Docker Hub is your friend. Hundreds of thousands of scientific software images — Bioconductor, CUDA, GATK, all the common databases — available right now. You don't have to build from scratch. Start with pull, add your customizations in %post.

    Four: .def files in Git. Please, please do this. When your paper is under review and someone asks to replicate your results, you want to point them to a git commit and a .sif file. That's the gold standard.

    Five: SLURM transparency. You don't need any special SLURM configuration. Your sysadmin doesn't need to do anything special. It just works.

    [Open for questions]

    Before I open for questions — what specific workflows do you want to containerize? Let's troubleshoot together. Maybe you have a C++ simulation with tricky dependencies, or an old R package that doesn't install on the current system. These are exactly the problems containers were built to solve.

    [Take questions — remaining time]

    Thank you all. The .def files from today's demos are all available at [your URL/email]. Reach out if you run into issues building on our specific cluster — happy to help debug.
-->

<!-- end_slide -->

Resources
===

<!-- new_line -->

| Resource              | URL                              | Notes                                  |
|-----------------------|----------------------------------|----------------------------------------|
| 📖 Apptainer docs     | `apptainer.org/docs`             | Official — installation, CLI reference |
| ☁️ Sylabs Cloud       | `cloud.sylabs.io`                | Free remote builds — no root needed    |
| 🐳 Docker Hub         | `hub.docker.com`                 | Use with `docker://` prefix            |
| 🔑 Def file examples  | `github.com/apptainer/apptainer` | Community definition files             |

<!-- new_line -->

### Quick reference card

```bash
apptainer pull  myenv.sif  docker://image:tag   # download image
apptainer shell myenv.sif                        # interactive shell
apptainer exec  myenv.sif  <command>             # run one command
apptainer build myenv.sif  myenv.def             # build from recipe
apptainer exec  --bind /scratch:/scratch  ...    # mount filesystem
apptainer exec  --nv  ...                        # enable NVIDIA GPU
apptainer inspect --deffile myenv.sif            # inspect image
```

<!-- new_line -->

<span style="color: #00b4d8">*Questions? Reach out with your specific workflow — every container problem has a solution.*</span>

<!-- end_slide -->
