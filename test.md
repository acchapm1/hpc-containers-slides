---
title: "Containers for HPC"
sub_title: "Getting Started with Apptainer"
author: "HPC Research Computing Workshop  ·  60 min  ·  20 min slides + 40 min hands-on"
theme:
  name: tokyonight-night
---

![image:width:75%](img/all.jpeg)

<!-- 
speaker_note: |
    Welcome everyone. Today's session is structured as two parts: about 20 minutes of slides to cover the "why and what," followed by 40 minutes of live hands-on demos where we'll actually build and run containers together.

    The core promise: by the end of this session, you'll be able to take any piece of software — any Python environment, any bioinformatics pipeline, any ML framework — freeze it in time, and run it identically on any HPC cluster, now or in five years.

    If you've ever said "it worked on my machine" or spent a day debugging a dependency conflict before you could even start your real work, this session is for you.

    Quick show of hands: Who has Docker experience? Who has used containers on HPC before? Good — we'll make sure we cover the fundamentals without assuming prior knowledge.
-->

<!-- end_slide -->

Running a container
===

```bash +exec
apptainer exec python311.sif python3 --version
```

<!-- end_slide -->
