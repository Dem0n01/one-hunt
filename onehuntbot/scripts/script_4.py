
# 5. CREATE ALL ROUTE FILES

# Auth Routes
auth_routes = """const express = require('express');
const router = express.Router();
const authController = require('../controllers/auth.controller');
const auth = require('../middleware/auth.middleware');

// Telegram authentication
router.post('/telegram', authController.telegramAuth);

// Get current user
router.get('/me', auth, authController.getCurrentUser);

// Verify token
router.post('/verify', authController.verifyToken);

module.exports = router;
"""

# User Routes
user_routes = """const express = require('express');
const router = express.Router();
const userController = require('../controllers/user.controller');
const auth = require('../middleware/auth.middleware');

// Get user profile
router.get('/profile', auth, userController.getProfile);

// Update profile
router.put('/profile', auth, userController.updateProfile);

// Get user statistics
router.get('/stats', auth, userController.getUserStats);

// Get user by ID (public)
router.get('/:id', auth, userController.getUserById);

// Check and unlock achievements
router.post('/achievements/check', auth, userController.checkAchievements);

module.exports = router;
"""

# Referral Routes
referral_routes = """const express = require('express');
const router = express.Router();
const referralController = require('../controllers/referral.controller');
const auth = require('../middleware/auth.middleware');

// Get referral info
router.get('/info', auth, referralController.getReferralInfo);

// Apply referral code
router.post('/apply', auth, referralController.applyReferralCode);

// Get referral leaderboard
router.get('/leaderboard', auth, referralController.getReferralLeaderboard);

module.exports = router;
"""

# Reward Routes
reward_routes = """const express = require('express');
const router = express.Router();
const rewardController = require('../controllers/reward.controller');
const auth = require('../middleware/auth.middleware');

// Claim daily reward
router.post('/daily', auth, rewardController.claimDailyReward);

// Spin the wheel
router.post('/spin', auth, rewardController.spinWheel);

// Get reward history
router.get('/history', auth, rewardController.getRewardHistory);

module.exports = router;
"""

# Transaction Routes
transaction_routes = """const express = require('express');
const router = express.Router();
const transactionController = require('../controllers/transaction.controller');
const auth = require('../middleware/auth.middleware');

// Get transaction history
router.get('/', auth, transactionController.getTransactionHistory);

// Request withdrawal
router.post('/withdraw', auth, transactionController.requestWithdrawal);

// Get withdrawal status
router.get('/withdraw/:transactionId', auth, transactionController.getWithdrawalStatus);

// Cancel withdrawal
router.delete('/withdraw/:transactionId', auth, transactionController.cancelWithdrawal);

// Admin: Process withdrawal
router.put('/admin/withdraw/:transactionId', auth, transactionController.processWithdrawal);

module.exports = router;
"""

# Leaderboard Routes
leaderboard_routes = """const express = require('express');
const router = express.Router();
const leaderboardController = require('../controllers/leaderboard.controller');
const auth = require('../middleware/auth.middleware');

// Get top users by balance
router.get('/balance', auth, leaderboardController.getTopByBalance);

// Get top users by level
router.get('/level', auth, leaderboardController.getTopByLevel);

// Get top referrers
router.get('/referrals', auth, leaderboardController.getTopReferrers);

// Get user's rank
router.get('/rank', auth, leaderboardController.getUserRank);

module.exports = router;
"""

# Save all route files
with open('auth.routes.js', 'w') as f:
    f.write(auth_routes)
    
with open('user.routes.js', 'w') as f:
    f.write(user_routes)
    
with open('referral.routes.js', 'w') as f:
    f.write(referral_routes)
    
with open('reward.routes.js', 'w') as f:
    f.write(reward_routes)
    
with open('transaction.routes.js', 'w') as f:
    f.write(transaction_routes)
    
with open('leaderboard.routes.js', 'w') as f:
    f.write(leaderboard_routes)

print("✅ Created all route files:")
print("  - auth.routes.js")
print("  - user.routes.js")
print("  - referral.routes.js")
print("  - reward.routes.js")
print("  - transaction.routes.js")
print("  - leaderboard.routes.js")
