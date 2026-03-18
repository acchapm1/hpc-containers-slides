# Docker Multi-Arch Build

## Updated Step 2 — Build Multi-Architecture Images (Apple Silicon Mac)

The standard `docker build` only builds for your local architecture. On an M-series Mac you need `docker buildx` to create a multi-platform manifest that covers both `arm64` (other Apple Silicon users) and `amd64` (most HPC clusters, which run x86 Intel/AMD).

---

### One-time setup — create a multi-arch builder

```bash
# Create a new buildx builder that supports multi-platform builds
docker buildx create --name multiarch-builder --driver docker-container --use

# Boot it up and verify it supports both platforms
docker buildx inspect --bootstrap
# Look for: linux/amd64, linux/arm64 in the platforms list
```

You only need to do this once. After that `multiarch-builder` persists across terminal sessions.

---

### Build and push both platforms in one command

```bash
# Builds linux/amd64 + linux/arm64 and pushes a combined manifest to Docker Hub
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag yourusername/myanalysis:1.0 \
    --tag yourusername/myanalysis:latest \
    --push \
    .
```

The `--push` flag is required here — `buildx` multi-platform builds cannot be loaded into your local Docker daemon directly (it wouldn't know which arch to use). The image goes straight to Docker Hub as a manifest list that covers both architectures.

---

### Verify the manifest on Docker Hub

```bash
# Confirm both platforms are present in the manifest
docker buildx imagetools inspect yourusername/myanalysis:1.0
```

You should see output like:

```
Name:      docker.io/yourusername/myanalysis:1.0
MediaType: application/vnd.oci.image.index.v1+json
Digest:    sha256:abc123...

Manifests:
  Name:      docker.io/yourusername/myanalysis:1.0@sha256:aaa...
  MediaType: application/vnd.oci.image.manifest.v1+json
  Platform:  linux/amd64          ← HPC cluster uses this one

  Name:      docker.io/yourusername/myanalysis:1.0@sha256:bbb...
  MediaType: application/vnd.oci.image.manifest.v1+json
  Platform:  linux/arm64          ← your Mac and Apple Silicon use this one
```

---

### Test locally before pushing (arm64 only)

If you want to quickly test the image on your Mac before doing a full multi-arch push:

```bash
# Build just for your local arm64 Mac and load into Docker daemon
docker buildx build \
    --platform linux/arm64 \
    --tag yourusername/myanalysis:test \
    --load \
    .

# Test it runs correctly
docker run --rm yourusername/myanalysis:test

# Once happy, do the full multi-arch push
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag yourusername/myanalysis:1.0 \
    --push \
    .
```

---

### On the HPC cluster — nothing changes

```bash
# Apptainer automatically selects linux/amd64 from the manifest
apptainer pull myanalysis.sif docker://yourusername/myanalysis:1.0
```

Docker Hub serves the correct architecture automatically. Apptainer on an `x86_64` HPC node pulls the `amd64` layer; an Apple Silicon Mac running Apptainer would get the `arm64` layer. You never have to think about it.

---

### Updated full workflow summary

```
M-SERIES MACBOOK                              DOCKER HUB                    HPC CLUSTER (x86)
----------------                              ----------                    -----------------
docker buildx build \                         user/img:1.0                  apptainer pull img.sif \
  --platform linux/amd64,linux/arm64 \  →    ├── linux/amd64  →  →  →       docker://user/img:1.0
  --tag user/img:1.0 \                        └── linux/arm64              apptainer exec img.sif \
  --push .                                    (manifest list)                 python3 script.py
```

---

### Troubleshooting common buildx issues

```bash
# If the builder goes stale or throws errors, reset it
docker buildx rm multiarch-builder
docker buildx create --name multiarch-builder --driver docker-container --use
docker buildx inspect --bootstrap

# If amd64 builds are very slow on your M-series Mac
# that's QEMU emulation — it's normal, amd64 runs under emulation locally.
# The resulting image runs at full native speed on the actual amd64 HPC nodes.

# Check which builder is currently active
docker buildx ls
```
