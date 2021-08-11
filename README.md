# Eventer
Eventer is a simple Discord Bot for creating and moderating event's in your server.

### 📄 Bot features
- Creating any **types of Event**
- Creating **Events** of a specific type that you created earlier
- Auto-creating **roles** for event on enabling Event types and Events
- **Notification** event members on enabling Event types and Events
- Disabling, deleting and viewing created Event types and Events

### 📥 Install ans setup bot
- Download archive and copy files to `/opt/Eventer/`
- Install Python (3.9+)
- Install PostgreSQL
+ Setup database
  - Create database
  - Run `scripts/scheme.sql` in psql console to setup tables
+ Setup bot
  - Install and activate virualenv
  - Install requirements from `requiremets.txt`
  - Edit `setting.py` for your database, bot settings
  - Run setup.py

### 🧰 Creating Linux service for bot
- Copy `eventerbot.service` to `/etc/systemd/system`
- Run `sudo systemctl daemon-reload`
- Run `sudo systemctl start eventerbot.service`
- Make sure that service is works by `sudo systemctl status eventerbot.service`
