const User = require('../models/User.model');
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
