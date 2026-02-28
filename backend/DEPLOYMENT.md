# Deployment Checklist

## Pre-Deployment

### Environment Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Set strong `JWT_SECRET` (use: `openssl rand -hex 32`)
- [ ] Add valid `GEMINI_API_KEY`
- [ ] Add valid `YOUTUBE_API_KEY`
- [ ] Set `DATABASE_TYPE=mongodb` for production
- [ ] Configure production `MONGO_URL`

### Database Setup
- [ ] MongoDB installed and running
- [ ] Database user created with proper permissions
- [ ] Connection string tested
- [ ] Backup strategy in place

### Security
- [ ] Change default JWT secret
- [ ] Set appropriate token expiration
- [ ] Configure CORS for specific origins
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Implement request logging

### Code Review
- [ ] Remove debug statements
- [ ] Check for hardcoded credentials
- [ ] Verify error handling
- [ ] Test all endpoints
- [ ] Run security scan

---

## Deployment Steps

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.8+
sudo apt install python3 python3-pip -y

# Install MongoDB
# Follow: https://docs.mongodb.com/manual/installation/
```

### 2. Application Setup

```bash
# Clone/upload code
cd /var/www/
git clone <your-repo>
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with production values
```

### 3. Process Manager (Systemd)

Create `/etc/systemd/system/learning-api.service`:

```ini
[Unit]
Description=Learning Platform API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/backend
Environment="PATH=/var/www/backend/venv/bin"
ExecStart=/var/www/backend/venv/bin/python run.py

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable learning-api
sudo systemctl start learning-api
sudo systemctl status learning-api
```

### 4. Reverse Proxy (Nginx)

Create `/etc/nginx/sites-available/learning-api`:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/learning-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.yourdomain.com
```

---

## Post-Deployment

### Verification
- [ ] API accessible via domain
- [ ] HTTPS working
- [ ] All endpoints responding
- [ ] Database connections working
- [ ] File uploads working
- [ ] AI services responding

### Monitoring
- [ ] Set up logging
- [ ] Configure error tracking (Sentry)
- [ ] Set up uptime monitoring
- [ ] Configure alerts
- [ ] Monitor database performance

### Backup
- [ ] Database backup scheduled
- [ ] Uploaded files backup
- [ ] Configuration backup
- [ ] Test restore procedure

---

## Production Environment Variables

```env
# Database
DATABASE_TYPE=mongodb
MONGO_URL=mongodb://username:password@host:27017/dbname?authSource=admin

# Security
JWT_SECRET=<generate-with-openssl-rand-hex-32>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
GEMINI_API_KEY=<your-production-key>
YOUTUBE_API_KEY=<your-production-key>
```

---

## Docker Deployment (Alternative)

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "run.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_TYPE=mongodb
      - MONGO_URL=mongodb://mongo:27017
    depends_on:
      - mongo
    volumes:
      - ./app/storage:/app/app/storage

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

### Deploy

```bash
docker-compose up -d
```

---

## Cloud Deployment Options

### AWS
- **Compute**: EC2 or ECS
- **Database**: DocumentDB (MongoDB compatible)
- **Storage**: S3 for files
- **Load Balancer**: ALB

### Google Cloud
- **Compute**: Cloud Run or GKE
- **Database**: MongoDB Atlas
- **Storage**: Cloud Storage
- **Load Balancer**: Cloud Load Balancing

### Heroku (Quick Deploy)

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Add MongoDB addon
heroku addons:create mongolab

# Set environment variables
heroku config:set JWT_SECRET=your_secret
heroku config:set GEMINI_API_KEY=your_key
heroku config:set YOUTUBE_API_KEY=your_key
heroku config:set DATABASE_TYPE=mongodb

# Deploy
git push heroku main
```

---

## Performance Optimization

### Database
- [ ] Add indexes on frequently queried fields
- [ ] Enable connection pooling
- [ ] Configure query timeout
- [ ] Monitor slow queries

### Application
- [ ] Enable response compression
- [ ] Add caching layer (Redis)
- [ ] Optimize file upload size
- [ ] Implement pagination

### Infrastructure
- [ ] Use CDN for static files
- [ ] Enable HTTP/2
- [ ] Configure load balancing
- [ ] Set up auto-scaling

---

## Monitoring & Logging

### Application Logs

```python
# Add to main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Error Tracking (Sentry)

```bash
pip install sentry-sdk
```

```python
# Add to main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

---

## Maintenance

### Regular Tasks
- [ ] Update dependencies monthly
- [ ] Review logs weekly
- [ ] Check disk space
- [ ] Monitor API usage
- [ ] Review security alerts

### Backup Schedule
- [ ] Daily database backup
- [ ] Weekly full backup
- [ ] Monthly backup verification
- [ ] Offsite backup storage

---

## Rollback Plan

### If Deployment Fails

1. **Stop new service**
```bash
sudo systemctl stop learning-api
```

2. **Restore previous version**
```bash
git checkout <previous-commit>
sudo systemctl start learning-api
```

3. **Restore database** (if needed)
```bash
mongorestore --db learning_platform backup/
```

---

## Health Checks

### Endpoint
```
GET /health
```

### Monitoring Script

```bash
#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ $response != "200" ]; then
    echo "API is down!"
    # Send alert
fi
```

---

## Security Hardening

### Firewall
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### Fail2Ban
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
```

### Regular Updates
```bash
sudo apt update && sudo apt upgrade -y
```

---

## Cost Optimization

### Free Tier Options
- **MongoDB Atlas**: 512MB free
- **Heroku**: 1 dyno free
- **Vercel**: Serverless functions
- **Railway**: $5 credit/month

### Paid Recommendations
- **DigitalOcean**: $5/month droplet
- **AWS EC2**: t2.micro ($10/month)
- **MongoDB Atlas**: M10 ($57/month)

---

## Final Checklist

- [ ] All environment variables set
- [ ] Database connected and tested
- [ ] SSL certificate installed
- [ ] Monitoring configured
- [ ] Backups scheduled
- [ ] Documentation updated
- [ ] Team notified
- [ ] Rollback plan ready

**Ready to deploy!** 🚀
