const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const TelegramBot = require('node-telegram-bot-api');
const cron = require('node-cron');

// Import routes
const authRoutes = require('./routes/auth.routes');
const userRoutes = require('./routes/user.routes');
const taskRoutes = require('./routes/task.routes');
const rewardRoutes = require('./routes/reward.routes');
const referralRoutes = require('./routes/referral.routes');
const transactionRoutes = require('./routes/transaction.routes');
const leaderboardRoutes = require('./routes/leaderboard.routes');

// Import middleware
const errorHandler = require('./middleware/error.middleware');

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize Telegram Bot
const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN, { polling: true });

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);

// Serve static files (frontend)
app.use(express.static('public'));

// Database connection
mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('✅ MongoDB Connected'))
.catch(err => console.error('❌ MongoDB Connection Error:', err));

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/tasks', taskRoutes);
app.use('/api/rewards', rewardRoutes);
app.use('/api/referrals', referralRoutes);
app.use('/api/transactions', transactionRoutes);
app.use('/api/leaderboard', leaderboardRoutes);

// Telegram Webhook
app.post('/webhook', (req, res) => {
  bot.processUpdate(req.body);
  res.sendStatus(200);
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date() });
});

// Error handling middleware
app.use(errorHandler);

// Scheduled Tasks
// Daily reward reset
cron.schedule('0 0 * * *', async () => {
  console.log('Running daily reset tasks...');
  // Reset daily tasks, distribute rewards, etc.
});

// Weekly leaderboard update
cron.schedule('0 0 * * 0', async () => {
  console.log('Running weekly leaderboard update...');
});

// Telegram Bot Commands
bot.onText(/\/start/, async (msg) => {
  const chatId = msg.chat.id;
  const userId = msg.from.id;
  const username = msg.from.username || msg.from.first_name;

  bot.sendMessage(chatId, \`Welcome to XCX Wallet Bot, \${username}! 🎉\n\nOpen the app to get started!\`, {
    reply_markup: {
      inline_keyboard: [[
        { text: '🚀 Open App', web_app: { url: process.env.BASE_URL } }
      ]]
    }
  });
});

bot.onText(/\/help/, (msg) => {
  const helpText = \`
🤖 *XCX Wallet Bot Commands*

/start - Start the bot
/help - Show this help message
/balance - Check your balance
/tasks - View available tasks
/referral - Get your referral link
/leaderboard - View top users
/withdraw - Withdraw your earnings
  \`;

  bot.sendMessage(msg.chat.id, helpText, { parse_mode: 'Markdown' });
});

// Start server
app.listen(PORT, () => {
  console.log(\`🚀 Server running on port \${PORT}\`);
  console.log(\`📱 Telegram Bot is active\`);
});

module.exports = { app, bot };
