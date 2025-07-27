# CareView Docker Setup

## Quick Start

1. **Install Docker Desktop**
   - Download from https://docker.com/products/docker-desktop
   - Start Docker Desktop

2. **Clone and Run**
   ```bash
   git clone <your-repo>
   cd careview
   docker-compose up --build
   ```

3. **Initialize Database**
   ```bash
   # In another terminal, run:
   docker-compose exec api python reset.py
   ```

4. **Access the Application**
   - **API**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **Database Admin**: http://localhost:8080

## Demo Accounts
- **Manager**: `manager@demo.com` / `password123`
- **Carer**: `carer@demo.com` / `password123`
- **Family**: `family@demo.com` / `password123`

## Services

### CareView API (Port 8000)
- Main application server
- Health check: http://localhost:8000/health
- Interactive docs: http://localhost:8000/docs

### PostgreSQL Database (Port 5432)
- Production-grade database
- Persistent data storage
- Automatic health checks

### Adminer (Port 8080)
- Web-based database management
- Login: Server=db, Username=admin, Password=MySecurePass123, Database=careview

## Docker Commands

### Start Services
```bash
docker-compose up -d          # Start in background
docker-compose up --build     # Rebuild and start
```

### View Logs
```bash
docker-compose logs api       # API logs
docker-compose logs db        # Database logs
docker-compose logs -f        # Follow all logs
```

### Initialize Database
```bash
docker-compose exec api python reset.py
```

### Run Tests
```bash
docker-compose exec api pytest tests/ -v
```

### Stop Services
```bash
docker-compose down           # Stop services
docker-compose down -v        # Stop and remove volumes (delete data)
```

### Database Backup
```bash
docker-compose exec db pg_dump -U admin careview > backup.sql
```

### Database Restore
```bash
docker-compose exec -T db psql -U admin careview < backup.sql
```

## Production Deployment

1. **Update Environment Variables**
   ```bash
   # Set secure values in docker-compose.yml
   SECRET_KEY: "your-production-secret-key"
   POSTGRES_PASSWORD: "secure-production-password"
   ```

2. **Use Production Database**
   ```yaml
   # Replace db service with external database
   environment:
     DB_HOST: your-production-db-host
     DB_PORT: 5432
   ```

3. **Enable HTTPS**
   ```bash
   # Add reverse proxy (nginx) for SSL termination
   ```

## Troubleshooting

### Port Already in Use
```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Use different port
```

### Database Connection Failed
```bash
# Check database is healthy
docker-compose ps
docker-compose logs db

# Restart services
docker-compose restart
```

### API Won't Start
```bash
# Check API logs
docker-compose logs api

# Rebuild image
docker-compose build --no-cache api
```

### Reset Everything
```bash
# Nuclear option - removes all data
docker-compose down -v
docker system prune -a
docker-compose up --build
```