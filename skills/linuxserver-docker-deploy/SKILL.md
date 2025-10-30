---
name: linuxserver-docker-deploy
description: Deploy and configure LinuxServer.io Docker containers with docker-compose. Use when users want to install, configure, or run apps from linuxserver.io images (Plex, Sonarr, Radarr, Jellyfin, etc.). Handles environment detection, best practices, and docker-compose file management.
allowed-tools: Bash, Read, Write, Edit, WebFetch, Grep, Glob, mcp__context7__resolve-library-id, mcp__context7__get-library-docs, AskUserQuestion
---

# LinuxServer.io Docker Deployment Skill

This skill helps deploy and configure applications from LinuxServer.io's Docker image catalog using docker-compose. It follows best practices and handles the complete workflow from image selection to deployment.

## Workflow

### 1. Environment Detection

First, detect or confirm the environment:

```bash
# Check if running in WSL
uname -a | grep -i microsoft
# Check for WSL-specific environment variable
echo $WSL_DISTRO_NAME
```

If unclear, use AskUserQuestion to ask the user about their environment (WSL vs native Ubuntu/Linux).

**Why this matters:** WSL may have different networking, volume mount paths (e.g., `/mnt/c/`), and systemd availability that affect configuration.

### 2. Image Discovery and Recommendation

When the user requests an app:

1. **Use WebFetch** to access LinuxServer.io's image catalog:
   - Fetch: `https://fleet.linuxserver.io/`
   - Or: `https://docs.linuxserver.io/images/` for specific image docs

2. **Search and recommend** based on user needs:
   - If user provides a specific app name: verify it exists and fetch its documentation
   - If user describes functionality: recommend appropriate images

3. **Present key information:**
   - Image name (e.g., `linuxserver/plex`)
   - Purpose and features
   - Common use cases
   - Dependencies or prerequisites

### 3. Gather Best Practices from Context7

Before creating configuration, obtain current best practices:

```
1. Use mcp__context7__resolve-library-id for "docker-compose"
2. Use mcp__context7__get-library-docs with the library ID
3. Use mcp__context7__resolve-library-id for "docker" if needed
4. Query for relevant topics like "volumes", "networking", "environment variables"
```

**Key areas to check:**
- Volume mount best practices
- Network configuration patterns
- Environment variable security
- Container restart policies
- User/group ID mapping (PUID/PGID)
- Time zone configuration

### 4. Prepare Docker Directory Structure

Ensure the `~/docker` directory exists and has proper structure:

```bash
ls -la ~/docker
```

Create if needed:
```bash
mkdir -p ~/docker
```

For the specific app, consider creating:
```
~/docker/
├── docker-compose.yml (main compose file)
└── [app-name]/
    ├── config/
    └── data/
```

### 5. Configuration Planning

Before modifying files, gather information from the user:

**Required information:**
- PUID and PGID (use `id` command to get user's values)
- Timezone (check `timedatectl` or `/etc/timezone`)
- Port mappings (check for conflicts)
- Volume locations for data and config
- Any app-specific requirements

Use AskUserQuestion for any missing critical information.

### 6. Docker Compose File Management

Check if `~/docker/docker-compose.yml` exists:

- **If exists:** Use Edit tool to add the new service
- **If not exists:** Use Write tool to create it

**Compose file structure:**
```yaml
version: "3.8"

services:
  [app-name]:
    image: lscr.io/linuxserver/[app-name]:latest
    container_name: [app-name]
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/New_York
      # App-specific environment variables
    volumes:
      - ~/docker/[app-name]/config:/config
      - ~/docker/[app-name]/data:/data
      # App-specific volumes
    ports:
      - "8080:8080"
    restart: unless-stopped
    # Optional: networks, depends_on, etc.
```

**Best practices to apply:**
- Use `lscr.io/linuxserver/` registry (LinuxServer.io's registry)
- Set explicit container_name for easy management
- Use `unless-stopped` restart policy
- Map PUID/PGID to user's IDs
- Create host directories before first run
- Use specific port mappings (avoid conflicts)
- Add comments for clarity

### 7. Pre-Deployment Validation

Before deploying:

1. **Create required directories:**
   ```bash
   mkdir -p ~/docker/[app-name]/{config,data}
   ```

2. **Check for port conflicts:**
   ```bash
   sudo netstat -tulpn | grep :[port]
   # or
   sudo ss -tulpn | grep :[port]
   ```

3. **Validate compose file syntax:**
   ```bash
   cd ~/docker && docker-compose config
   ```

### 8. Deployment

Deploy the application:

```bash
cd ~/docker
docker-compose up -d [app-name]
```

**Monitor deployment:**
```bash
docker-compose logs -f [app-name]
```

### 9. Post-Deployment Information

Provide the user with:
- Access URL (e.g., `http://localhost:8080`)
- Initial setup steps (if any)
- Log viewing command: `docker-compose -f ~/docker/docker-compose.yml logs -f [app-name]`
- Container management commands:
  - Stop: `docker-compose -f ~/docker/docker-compose.yml stop [app-name]`
  - Restart: `docker-compose -f ~/docker/docker-compose.yml restart [app-name]`
  - Remove: `docker-compose -f ~/docker/docker-compose.yml down [app-name]`
- Configuration location: `~/docker/[app-name]/config`
- Data location: `~/docker/[app-name]/data`

## Environment-Specific Considerations

### WSL Specifics
- Docker Desktop integration: containers may need `host.docker.internal` for host access
- Volume performance: prefer Linux filesystem (`~/docker`) over Windows mounts (`/mnt/c/`)
- Networking: may need to access via `localhost` or WSL IP
- Systemd: check if systemd is enabled in WSL2

### Native Ubuntu/Linux
- Ensure Docker daemon is running: `sudo systemctl status docker`
- User may need to be in docker group: `groups $USER`
- Firewall rules may need adjustment for port access

## Common LinuxServer.io Images

Popular images to recommend:
- **Media Servers:** plex, jellyfin, emby
- **Media Management:** sonarr, radarr, lidarr, readarr, prowlarr
- **Download Clients:** qbittorrent, transmission, deluge, sabnzbd
- **Home Automation:** homeassistant
- **Network Tools:** wireguard, openvpn-as
- **Web Services:** nginx, swag (nginx with certbot)
- **File Management:** nextcloud, syncthing
- **Monitoring:** grafana, prometheus
- **Utilities:** code-server, duplicati, photoprism

## Error Handling

Common issues to check:
1. **Port already in use:** Suggest alternative port or identify conflicting service
2. **Permission denied:** Check PUID/PGID or volume permissions
3. **Image pull fails:** Check internet connection and registry availability
4. **Container won't start:** Check logs for specific error messages
5. **Can't access service:** Verify firewall, port mapping, and container status

## Example Interaction Flow

```
User: "Install Plex"

1. Detect environment (WSL/Ubuntu)
2. Fetch Plex image details from linuxserver.io
3. Get docker-compose best practices from context7
4. Check ~/docker exists and current compose file
5. Get user's PUID/PGID (run `id` command)
6. Get timezone
7. Ask about port preferences and media library locations
8. Add plex service to docker-compose.yml
9. Create ~/docker/plex/config directory
10. Run `docker-compose up -d plex`
11. Provide access URL and next steps
```

## Important Notes

- Always use the `lscr.io/linuxserver/` registry prefix for images
- LinuxServer.io images use PUID/PGID for permission mapping - this is critical
- Most services need time to initialize on first run - advise patience
- Configuration often happens through the web UI after first launch
- Always create volume directories before starting containers
- Check LinuxServer.io docs for app-specific environment variables and volumes
