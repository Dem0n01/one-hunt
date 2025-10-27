
# Create comprehensive documentation
readme_content = '''# XCX Wallet Bot - Enhanced Version with Backend

🚀 **Complete Telegram Wallet Bot with Gamification, Tasks, and Reward System**

## 🌟 Features

### Core Features
- ✅ **Telegram Bot Integration** - Seamless Telegram Web App
- ✅ **Wallet Management** - Track balance, earnings, withdrawals
- ✅ **User Authentication** - Secure JWT-based authentication
- ✅ **Multi-tier Referral System** - Direct & indirect referrals

### 🎮 Gamification System
- **Level & XP System** - Progress through levels by earning XP
- **Daily Login Rewards** - Claim rewards daily with streak bonuses
- **Achievement Badges** - Unlock achievements for milestones
- **Leaderboards** - Compete with other users (by balance, level, referrals)
- **Spin the Wheel** - Lucky wheel feature for random rewards
- **Streak Bonuses** - Consecutive day rewards multiply

### 📋 Advanced Task System
- **Task Categories:**
  - Daily Tasks (reset every 24 hours)
  - Weekly Challenges
  - Social Media Tasks (Telegram, Twitter, YouTube)
  - Quiz & Survey Tasks
  - Referral Tasks
  - Special/Partner Tasks

- **Task Features:**
  - Auto & manual verification
  - Difficulty levels (Easy, Medium, Hard)
  - Recurring tasks
  - Limited availability tasks
  - Scheduled tasks (start/end dates)
  - Priority sorting

### 💰 Reward System
- Daily login rewards with increasing streak bonuses
- Task completion rewards (Coins + XP)
- Referral rewards (multi-level)
- Achievement unlocking rewards
- Bonus rewards and special events
- Level-up bonuses

### 📊 Analytics & Tracking
- Real-time leaderboards
- User rankings
- Transaction history
- Reward history
- Task completion tracking
- Performance statistics

## 🛠️ Technology Stack

### Backend
- **Runtime:** Node.js
- **Framework:** Express.js
- **Database:** MongoDB with Mongoose ODM
- **Authentication:** JWT (JSON Web Tokens)
- **Bot Framework:** node-telegram-bot-api
- **Scheduling:** node-cron
- **Security:** Helmet, CORS, Rate Limiting

### Frontend
- **Framework:** HTML5, CSS3, JavaScript
- **UI Library:** Telegram Web App API
- **Icons:** Font Awesome
- **Alerts:** SweetAlert2
- **Styling:** Custom CSS with dark/light mode

## 📁 Project Structure

```
xcx-wallet-bot/
├── backend/
│   ├── models/
│   │   ├── User.model.js
│   │   ├── Task.model.js
│   │   ├── TaskCompletion.model.js
│   │   ├── Reward.model.js
│   │   ├── Achievement.model.js
│   │   ├── Referral.model.js
│   │   └── Transaction.model.js
│   │
│   ├── controllers/
│   │   ├── auth.controller.js
│   │   ├── user.controller.js
│   │   ├── task.controller.js
│   │   ├── reward.controller.js
│   │   ├── referral.controller.js
│   │   ├── transaction.controller.js
│   │   └── leaderboard.controller.js
│   │
│   ├── routes/
│   │   ├── auth.routes.js
│   │   ├── user.routes.js
│   │   ├── task.routes.js
│   │   ├── reward.routes.js
│   │   ├── referral.routes.js
│   │   ├── transaction.routes.js
│   │   └── leaderboard.routes.js
│   │
│   ├── middleware/
│   │   ├── auth.middleware.js
│   │   ├── validation.middleware.js
│   │   └── error.middleware.js
│   │
│   ├── utils/
│   │   ├── telegram.js
│   │   ├── crypto.js
│   │   └── scheduler.js
│   │
│   ├── server.js
│   ├── config.js
│   └── package.json
│
├── public/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── .env
├── .gitignore
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites
- Node.js (v16 or higher)
- MongoDB (v5 or higher)
- Telegram Bot Token (from @BotFather)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd xcx-wallet-bot
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Configure Environment
Create a `.env` file in the root directory:

```env
# Server
PORT=3000
NODE_ENV=development

# Database
MONGODB_URI=mongodb://localhost:27017/xcx_wallet_bot

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_WEBHOOK_URL=https://yourdomain.com/webhook

# JWT
JWT_SECRET=your_super_secret_jwt_key
JWT_EXPIRE=7d

# App
BASE_URL=https://yourdomain.com
ADMIN_CHAT_ID=your_admin_telegram_id

# Rewards
DAILY_LOGIN_REWARD=10
REFERRAL_REWARD_DIRECT=100
REFERRAL_REWARD_INDIRECT=50
TASK_COMPLETION_BASE_REWARD=25

# Withdrawal
MIN_WITHDRAWAL_AMOUNT=100
WITHDRAWAL_FEE_PERCENT=2
```

### Step 4: Setup MongoDB
```bash
# Start MongoDB service
sudo systemctl start mongod

# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Step 5: Create Telegram Bot
1. Open Telegram and search for @BotFather
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the bot token to `.env` file
5. Set webhook (optional):
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_WEBHOOK_URL>"
   ```

### Step 6: Run the Application
```bash
# Development mode
npm run dev

# Production mode
npm start
```

The server will start on `http://localhost:3000`

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Tasks
- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/type/:type` - Get tasks by type
- `GET /api/tasks/user/available` - Get available tasks
- `GET /api/tasks/user/completed` - Get completed tasks
- `POST /api/tasks/:id/complete` - Complete a task

### Rewards
- `POST /api/rewards/daily` - Claim daily reward
- `POST /api/rewards/spin` - Spin the wheel
- `GET /api/rewards/history` - Get reward history

### Referrals
- `GET /api/referrals/code` - Get referral code
- `POST /api/referrals/apply` - Apply referral code
- `GET /api/referrals/stats` - Get referral statistics

### Leaderboard
- `GET /api/leaderboard/balance` - Top users by balance
- `GET /api/leaderboard/level` - Top users by level
- `GET /api/leaderboard/referrals` - Top referrers
- `GET /api/leaderboard/rank` - Get user's rank

### Transactions
- `GET /api/transactions` - Get transaction history
- `POST /api/transactions/withdraw` - Request withdrawal

## 🎯 Usage Guide

### For Users

1. **Start the Bot**
   - Open Telegram and find your bot
   - Send `/start` command
   - Click "Open App" button

2. **Complete Tasks**
   - Navigate to "Earn" section
   - Browse available tasks
   - Complete tasks to earn coins and XP

3. **Daily Rewards**
   - Claim daily login rewards
   - Build streak for bonus rewards
   - Spin the wheel for random rewards

4. **Referrals**
   - Get your unique referral link
   - Share with friends
   - Earn rewards when they join

5. **Track Progress**
   - View your level and XP
   - Check leaderboard rankings
   - Monitor your achievements

### For Admins

1. **Create Tasks**
   ```javascript
   POST /api/tasks/admin/create
   {
     "title": "Follow on Twitter",
     "description": "Follow our Twitter account",
     "type": "social",
     "category": "twitter",
     "reward": { "coins": 50, "xp": 10 },
     "requirement": {
       "action": "follow_twitter",
       "link": "https://twitter.com/yourhandle",
       "verificationMethod": "manual"
     }
   }
   ```

2. **Manage Users**
   - View user statistics
   - Ban/unban users
   - Verify task completions
   - Process withdrawals

3. **Monitor System**
   - Check server logs
   - Monitor database performance
   - Track user engagement

## 🔐 Security Features

- JWT authentication for API requests
- Password hashing with bcrypt
- Rate limiting to prevent abuse
- Input validation and sanitization
- CORS protection
- Helmet security headers
- MongoDB injection prevention

## 🎨 Customization

### Adding New Task Types
Edit `Task.model.js` and add to enum:
```javascript
type: {
  type: String,
  enum: ['daily', 'weekly', 'social', 'quiz', 'survey', 'referral', 'special', 'YOUR_NEW_TYPE'],
}
```

### Modifying Reward Amounts
Update `.env` file:
```env
DAILY_LOGIN_REWARD=20
REFERRAL_REWARD_DIRECT=150
```

### Changing XP Requirements
Modify in `User.model.js`:
```javascript
userSchema.methods.addXP = function(xp) {
  this.xp += xp;
  const xpForNextLevel = this.level * 150; // Changed from 100
  // ...
};
```

## 📈 Database Schema

### User Collection
```javascript
{
  telegramId: String,
  username: String,
  balance: Number,
  level: Number,
  xp: Number,
  streak: Number,
  referralCode: String,
  referredBy: ObjectId,
  directReferrals: [ObjectId],
  tasksCompleted: Number,
  achievements: [{achievementId, unlockedAt}],
  // ... more fields
}
```

### Task Collection
```javascript
{
  title: String,
  description: String,
  type: String,
  category: String,
  reward: {coins, xp},
  requirement: {action, link, verificationMethod},
  difficulty: String,
  maxCompletions: Number,
  // ... more fields
}
```

## 🐛 Troubleshooting

### Common Issues

**Bot not responding:**
- Check if bot token is correct in `.env`
- Verify MongoDB connection
- Check server logs for errors

**Tasks not showing:**
- Ensure tasks are marked as active
- Check task start/end dates
- Verify user authentication

**Rewards not credited:**
- Check task verification method
- Review server logs
- Verify database connection

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Contact admin via Telegram
- Check documentation

## 📄 License

MIT License - Feel free to use and modify

## 🙏 Credits

- Telegram Bot API
- Node.js Community
- MongoDB
- Express.js

---

**Version:** 2.0.0  
**Last Updated:** 2025  
**Maintained by:** Your Team
```

# Save README
with open('README.md', 'w') as f:
    f.write(readme_content)

print("✅ Created comprehensive README.md")
print("\nDocumentation includes:")
print("- Complete feature list")
print("- Installation guide")
print("- API endpoints")
print("- Usage instructions")
print("- Configuration guide")
print("- Troubleshooting tips")
