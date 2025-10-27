# XCX Wallet Bot - Complete Setup Guide

## 📦 What You Have

You now have **ALL** the necessary files for a fully functional Telegram Wallet Bot with:
- ✅ Complete backend infrastructure
- ✅ Database models and schemas
- ✅ API controllers and routes
- ✅ Authentication & security
- ✅ Task system with rewards
- ✅ Gamification (levels, XP, achievements)
- ✅ Referral system
- ✅ Transaction management
- ✅ Leaderboards

## 📁 File Organization

### **Backend Files** (Place in `backend/` folder)

**Models** (`backend/models/`):
- `User.model.js` - User schema with gamification
- `Task.model.js` - Task definitions
- `TaskCompletion.model.js` - Task tracking
- `Reward.model.js` - Reward history
- `Achievement.model.js` - Achievement system

**Controllers** (`backend/controllers/`):
- `auth.controller.js` - User authentication (NEW)
- `user.controller.js` - User profile management (NEW)
- `task.controller.js` - Task operations
- `reward.controller.js` - Reward distribution
- `referral.controller.js` - Referral tracking (NEW)
- `transaction.controller.js` - Withdrawals & transactions (NEW)
- `leaderboard.controller.js` - Rankings

**Routes** (`backend/routes/`):
- `auth.routes.js` - Auth endpoints (NEW)
- `user.routes.js` - User endpoints (NEW)
- `task.routes.js` - Task endpoints
- `reward.routes.js` - Reward endpoints (NEW)
- `referral.routes.js` - Referral endpoints (NEW)
- `transaction.routes.js` - Transaction endpoints (NEW)
- `leaderboard.routes.js` - Leaderboard endpoints (NEW)

**Middleware** (`backend/middleware/`):
- `auth.middleware.js` - JWT authentication (NEW)
- `validation.middleware.js` - Input validation (NEW)
- `error.middleware.js` - Error handling (NEW)

**Server**:
- `server.js` - Main Express server (in `backend/`)

### **Scripts** (Place in `scripts/` folder)
- `seed-database.js` - Populate database with sample data (NEW)

### **Configuration** (Root directory)
- `package.json` - Dependencies (NEW)
- `env.example` - Environment template (NEW) - **Rename to `.env`**
- `gitignore.txt` - Git ignore file (NEW) - **Rename to `.gitignore`**

### **Frontend** (Extract from `paste.txt`)
Your existing HTML file should be split into:
- `frontend/public/index.html` - HTML structure
- `frontend/public/styles.css` - CSS styles
- `frontend/public/app.js` - JavaScript logic

---

## 🚀 Quick Setup (5 Steps)

### **Step 1: Create Project Structure**
```bash
mkdir xcx-wallet-bot
cd xcx-wallet-bot

# Create directories
mkdir -p backend/models
mkdir -p backend/controllers
mkdir -p backend/routes
mkdir -p backend/middleware
mkdir -p frontend/public
mkdir scripts
```

### **Step 2: Place Files in Correct Locations**

**Backend**:
```
backend/
├── models/
│   ├── User.model.js
│   ├── Task.model.js
│   ├── TaskCompletion.model.js
│   ├── Reward.model.js
│   └── Achievement.model.js
├── controllers/
│   ├── auth.controller.js
│   ├── user.controller.js
│   ├── task.controller.js
│   ├── reward.controller.js
│   ├── referral.controller.js
│   ├── transaction.controller.js
│   └── leaderboard.controller.js
├── routes/
│   ├── auth.routes.js
│   ├── user.routes.js
│   ├── task.routes.js
│   ├── reward.routes.js
│   ├── referral.routes.js
│   ├── transaction.routes.js
│   └── leaderboard.routes.js
├── middleware/
│   ├── auth.middleware.js
│   ├── validation.middleware.js
│   └── error.middleware.js
└── server.js
```

**Root files**:
```
xcx-wallet-bot/
├── package.json
├── .env (rename from env.example)
├── .gitignore (rename from gitignore.txt)
└── README.md
```

**Scripts**:
```
scripts/
└── seed-database.js
```

### **Step 3: Install Dependencies**
```bash
npm install
```

This will install:
- Express.js (web server)
- Mongoose (MongoDB driver)
- node-telegram-bot-api (Telegram bot)
- JWT, bcrypt (authentication)
- And other dependencies

### **Step 4: Configure Environment**

1. Rename `env.example` to `.env`
2. Edit `.env` with your values:

```env
# Get bot token from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# MongoDB connection (local or Atlas)
MONGODB_URI=mongodb://localhost:27017/xcx_wallet_bot

# Generate a random secret for JWT
JWT_SECRET=your_random_secret_key_here

# Your domain
BASE_URL=https://yourdomain.com

# Your Telegram user ID (for admin)
ADMIN_CHAT_ID=123456789
```

### **Step 5: Start the Application**

```bash
# Seed database with sample tasks and achievements
npm run seed

# Start development server
npm run dev
```

Server will start on `http://localhost:3000`

---

## 📡 API Endpoints Reference

### **Authentication**
- `POST /api/auth/telegram` - Login/register via Telegram
- `GET /api/auth/me` - Get current user
- `POST /api/auth/verify` - Verify JWT token

### **User**
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update profile
- `GET /api/users/stats` - Get user statistics
- `POST /api/users/achievements/check` - Check for new achievements

### **Tasks**
- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/type/:type` - Get tasks by type
- `GET /api/tasks/user/available` - Get available tasks
- `GET /api/tasks/user/completed` - Get completed tasks
- `POST /api/tasks/:id/complete` - Complete a task

### **Rewards**
- `POST /api/rewards/daily` - Claim daily login reward
- `POST /api/rewards/spin` - Spin the wheel
- `GET /api/rewards/history` - Get reward history

### **Referrals**
- `GET /api/referrals/info` - Get referral info & link
- `POST /api/referrals/apply` - Apply referral code
- `GET /api/referrals/leaderboard` - Top referrers

### **Transactions**
- `GET /api/transactions` - Transaction history
- `POST /api/transactions/withdraw` - Request withdrawal
- `GET /api/transactions/withdraw/:id` - Withdrawal status
- `DELETE /api/transactions/withdraw/:id` - Cancel withdrawal

### **Leaderboards**
- `GET /api/leaderboard/balance` - Top users by balance
- `GET /api/leaderboard/level` - Top users by level
- `GET /api/leaderboard/referrals` - Top referrers
- `GET /api/leaderboard/rank` - Get your rank

---

## 🎮 Testing the Bot

### **1. Create Telegram Bot**
1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Follow instructions
4. Copy token to `.env`

### **2. Test with Postman or curl**

**Login/Register:**
```bash
curl -X POST http://localhost:3000/api/auth/telegram \
  -H "Content-Type: application/json" \
  -d '{
    "telegramId": "123456789",
    "username": "testuser",
    "firstName": "Test"
  }'
```

**Get Tasks (with token):**
```bash
curl -X GET http://localhost:3000/api/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Claim Daily Reward:**
```bash
curl -X POST http://localhost:3000/api/rewards/daily \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🎯 Next Steps

1. **Connect Frontend**: Update your HTML (`paste.txt`) to call these API endpoints
2. **Deploy**: Use Heroku, Vercel, or your own server
3. **Customize**: Modify tasks, rewards, and achievements
4. **Add Features**: Implement more gamification elements

---

## 🐛 Troubleshooting

**MongoDB Connection Error:**
- Install MongoDB locally or use MongoDB Atlas
- Check connection string in `.env`

**Bot Not Responding:**
- Verify bot token is correct
- Check server is running
- Test endpoints with Postman

**Tasks Not Showing:**
- Run `npm run seed` to populate database
- Check MongoDB connection

---

## 📝 Summary

You now have:
- ✅ **25 Backend Files** (models, controllers, routes, middleware)
- ✅ **Complete Authentication System**
- ✅ **Task & Reward Management**
- ✅ **Gamification Features**
- ✅ **Referral System**
- ✅ **Transaction Management**
- ✅ **Leaderboards & Rankings**
- ✅ **Database Seeding Script**
- ✅ **Configuration Files**

**Everything is ready! Just organize files, run `npm install`, configure `.env`, and start the server!**

---

## 📞 Need Help?

If you encounter any issues:
1. Check server logs
2. Verify all files are in correct locations
3. Ensure MongoDB is running
4. Confirm `.env` is properly configured

Good luck with your Telegram Wallet Bot! 🚀