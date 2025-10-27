
# 8. CREATE CONFIGURATION FILES

# package.json
package_json = """{
  "name": "xcx-wallet-bot",
  "version": "2.0.0",
  "description": "Enhanced Telegram Wallet Bot with Gamification and Rewards",
  "main": "backend/server.js",
  "scripts": {
    "start": "node backend/server.js",
    "dev": "nodemon backend/server.js",
    "seed": "node scripts/seed-database.js",
    "test": "echo \\"No tests specified\\" && exit 0"
  },
  "keywords": [
    "telegram",
    "bot",
    "wallet",
    "gamification",
    "rewards",
    "cryptocurrency"
  ],
  "author": "Your Name",
  "license": "MIT",
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.6.3",
    "node-telegram-bot-api": "^0.64.0",
    "dotenv": "^16.3.1",
    "bcryptjs": "^2.4.3",
    "jsonwebtoken": "^9.0.2",
    "cors": "^2.8.5",
    "helmet": "^7.1.0",
    "express-rate-limit": "^7.1.5",
    "express-validator": "^7.0.1",
    "node-cron": "^3.0.3",
    "axios": "^1.6.2",
    "qrcode": "^1.5.3",
    "crypto": "^1.0.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  },
  "engines": {
    "node": ">=16.0.0"
  }
}
"""

# .env.example
env_example = """# Server Configuration
PORT=3000
NODE_ENV=development

# Database
MONGODB_URI=mongodb://localhost:27017/xcx_wallet_bot

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_WEBHOOK_URL=https://yourdomain.com/webhook

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_change_this
JWT_EXPIRE=7d

# Application URLs
BASE_URL=https://yourdomain.com
FRONTEND_URL=https://yourdomain.com

# Admin Configuration
ADMIN_CHAT_ID=your_telegram_user_id

# Reward Configuration
DAILY_LOGIN_REWARD=10
REFERRAL_REWARD_DIRECT=100
REFERRAL_REWARD_INDIRECT=50
TASK_COMPLETION_BASE_REWARD=25

# Withdrawal Configuration
MIN_WITHDRAWAL_AMOUNT=100
WITHDRAWAL_FEE_PERCENT=2

# Feature Flags
ENABLE_SPIN_WHEEL=true
ENABLE_ACHIEVEMENTS=true
ENABLE_LEADERBOARDS=true
"""

# .gitignore
gitignore = """# Dependencies
node_modules/
package-lock.json
yarn.lock

# Environment variables
.env
.env.local
.env.production

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Build
dist/
build/
.next/
out/

# Database
*.db
*.sqlite
*.sqlite3

# Uploads
uploads/
temp/

# Testing
coverage/
.nyc_output/

# Misc
*.pem
*.key
"""

# Save configuration files
with open('package.json', 'w') as f:
    f.write(package_json)
    
with open('env.example', 'w') as f:
    f.write(env_example)
    
with open('gitignore.txt', 'w') as f:
    f.write(gitignore)

print("✅ Created configuration files:")
print("  - package.json")
print("  - env.example (rename to .env and configure)")
print("  - gitignore.txt (rename to .gitignore)")
