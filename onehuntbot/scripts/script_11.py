
# Create Reward and Gamification features

# Reward Model
reward_model = '''const mongoose = require('mongoose');

const rewardSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    index: true
  },
  
  type: {
    type: String,
    enum: ['daily_login', 'task_completion', 'referral', 'achievement', 'spin_wheel', 'bonus', 'level_up'],
    required: true
  },
  
  amount: {
    type: Number,
    required: true
  },
  
  xp: {
    type: Number,
    default: 0
  },
  
  description: String,
  
  relatedTask: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Task'
  },
  
  relatedReferral: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }
}, {
  timestamps: true
});

rewardSchema.index({ user: 1, createdAt: -1 });

module.exports = mongoose.model('Reward', rewardSchema);
'''

# Achievement Model
achievement_model = '''const mongoose = require('mongoose');

const achievementSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    unique: true
  },
  
  description: String,
  
  icon: String,
  
  category: {
    type: String,
    enum: ['tasks', 'referrals', 'earnings', 'social', 'special'],
    default: 'tasks'
  },
  
  requirement: {
    type: String,
    required: true
  },
  
  // Condition to unlock
  condition: {
    type: {
      type: String,
      enum: ['tasks_completed', 'referrals_count', 'balance_reached', 'streak_days', 'level_reached']
    },
    value: Number
  },
  
  reward: {
    coins: Number,
    xp: Number
  },
  
  rarity: {
    type: String,
    enum: ['common', 'rare', 'epic', 'legendary'],
    default: 'common'
  },
  
  isActive: {
    type: Boolean,
    default: true
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Achievement', achievementSchema);
'''

# Leaderboard Controller
leaderboard_controller = '''const User = require('../models/User.model');

// Get top users by balance
exports.getTopByBalance = async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 100;
    
    const topUsers = await User.find({ isActive: true, isBanned: false })
      .select('username firstName balance level xp')
      .sort({ balance: -1 })
      .limit(limit);
    
    // Add rank
    const rankedUsers = topUsers.map((user, index) => ({
      rank: index + 1,
      user: {
        username: user.username,
        firstName: user.firstName,
        balance: user.balance,
        level: user.level
      }
    }));
    
    res.json({ success: true, data: rankedUsers });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get top users by XP/Level
exports.getTopByLevel = async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 100;
    
    const topUsers = await User.find({ isActive: true, isBanned: false })
      .select('username firstName level xp balance')
      .sort({ level: -1, xp: -1 })
      .limit(limit);
    
    const rankedUsers = topUsers.map((user, index) => ({
      rank: index + 1,
      user: {
        username: user.username,
        firstName: user.firstName,
        level: user.level,
        xp: user.xp,
        balance: user.balance
      }
    }));
    
    res.json({ success: true, data: rankedUsers });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get top referrers
exports.getTopReferrers = async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 100;
    
    const topReferrers = await User.aggregate([
      { $match: { isActive: true, isBanned: false } },
      {
        $project: {
          username: 1,
          firstName: 1,
          totalReferrals: {
            $add: [
              { $size: { $ifNull: ['$directReferrals', []] } },
              { $size: { $ifNull: ['$indirectReferrals', []] } }
            ]
          },
          directReferralsCount: { $size: { $ifNull: ['$directReferrals', []] } }
        }
      },
      { $sort: { totalReferrals: -1, directReferralsCount: -1 } },
      { $limit: limit }
    ]);
    
    const rankedUsers = topReferrers.map((user, index) => ({
      rank: index + 1,
      user
    }));
    
    res.json({ success: true, data: rankedUsers });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get user's rank
exports.getUserRank = async (req, res) => {
  try {
    const userId = req.user.id;
    
    const user = await User.findById(userId);
    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }
    
    // Get rank by balance
    const balanceRank = await User.countDocuments({
      isActive: true,
      isBanned: false,
      balance: { $gt: user.balance }
    }) + 1;
    
    // Get rank by level
    const levelRank = await User.countDocuments({
      isActive: true,
      isBanned: false,
      $or: [
        { level: { $gt: user.level } },
        { level: user.level, xp: { $gt: user.xp } }
      ]
    }) + 1;
    
    res.json({
      success: true,
      data: {
        balanceRank,
        levelRank,
        user: {
          balance: user.balance,
          level: user.level,
          xp: user.xp
        }
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};
'''

# Daily Reward Controller
reward_controller = '''const User = require('../models/User.model');
const Reward = require('../models/Reward.model');

// Claim daily login reward
exports.claimDailyReward = async (req, res) => {
  try {
    const userId = req.user.id;
    const user = await User.findById(userId);
    
    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }
    
    // Check if already claimed today
    const today = new Date().setHours(0, 0, 0, 0);
    const lastClaim = user.lastDailyReward ? 
      new Date(user.lastDailyReward).setHours(0, 0, 0, 0) : 0;
    
    if (lastClaim === today) {
      return res.status(400).json({ 
        success: false, 
        message: 'Daily reward already claimed today' 
      });
    }
    
    // Calculate streak
    const yesterday = today - (24 * 60 * 60 * 1000);
    if (lastClaim === yesterday) {
      user.dailyRewardStreak += 1;
    } else if (lastClaim < yesterday) {
      user.dailyRewardStreak = 1;
    }
    
    // Calculate reward based on streak
    const baseReward = parseInt(process.env.DAILY_LOGIN_REWARD) || 10;
    const streakBonus = Math.floor(user.dailyRewardStreak / 7) * 5;
    const totalReward = baseReward + streakBonus;
    
    // Award reward
    await user.addBalance(totalReward);
    await user.addXP(5);
    user.lastDailyReward = new Date();
    await user.save();
    
    // Record reward
    const reward = new Reward({
      user: userId,
      type: 'daily_login',
      amount: totalReward,
      xp: 5,
      description: `Day ${user.dailyRewardStreak} streak reward`
    });
    await reward.save();
    
    res.json({
      success: true,
      message: 'Daily reward claimed!',
      data: {
        reward: totalReward,
        streak: user.dailyRewardStreak,
        nextStreakBonus: Math.floor((user.dailyRewardStreak + 1) / 7) * 5
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Spin the wheel
exports.spinWheel = async (req, res) => {
  try {
    const userId = req.user.id;
    const user = await User.findById(userId);
    
    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }
    
    // Implement spin wheel logic
    // Random reward between 5-100 coins
    const rewards = [5, 10, 15, 20, 25, 50, 75, 100];
    const randomReward = rewards[Math.floor(Math.random() * rewards.length)];
    
    await user.addBalance(randomReward);
    
    const reward = new Reward({
      user: userId,
      type: 'spin_wheel',
      amount: randomReward,
      description: 'Spin wheel reward'
    });
    await reward.save();
    
    res.json({
      success: true,
      message: 'Wheel spun!',
      data: { reward: randomReward }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get reward history
exports.getRewardHistory = async (req, res) => {
  try {
    const userId = req.user.id;
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    
    const rewards = await Reward.find({ user: userId })
      .sort({ createdAt: -1 })
      .skip((page - 1) * limit)
      .limit(limit)
      .populate('relatedTask', 'title')
      .populate('relatedReferral', 'username');
    
    const total = await Reward.countDocuments({ user: userId });
    
    res.json({
      success: true,
      data: {
        rewards,
        pagination: {
          page,
          limit,
          total,
          pages: Math.ceil(total / limit)
        }
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};
'''

with open('Reward.model.js', 'w') as f:
    f.write(reward_model)

with open('Achievement.model.js', 'w') as f:
    f.write(achievement_model)

with open('leaderboard.controller.js', 'w') as f:
    f.write(leaderboard_controller)

with open('reward.controller.js', 'w') as f:
    f.write(reward_controller)

print("✅ Created Reward System Files:")
print("- Reward.model.js")
print("- Achievement.model.js")
print("- leaderboard.controller.js")
print("- reward.controller.js")
print("\nGamification Features:")
print("- Daily login rewards with streak bonuses")
print("- Spin the wheel")
print("- Achievement system")
print("- Leaderboards (Balance, Level, Referrals)")
print("- User ranking system")
print("- Reward history tracking")
