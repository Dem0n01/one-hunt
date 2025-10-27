
# 2. USER CONTROLLER - User Profile Management
user_controller = """const User = require('../models/User.model');
const Reward = require('../models/Reward.model');
const TaskCompletion = require('../models/TaskCompletion.model');

// Get user profile
exports.getProfile = async (req, res) => {
  try {
    const user = await User.findById(req.user.id)
      .populate('referredBy', 'username firstName')
      .populate('directReferrals', 'username firstName level balance')
      .populate('indirectReferrals', 'username firstName');

    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }

    res.json({
      success: true,
      data: user
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Update user profile
exports.updateProfile = async (req, res) => {
  try {
    const { walletAddress, firstName, lastName } = req.body;
    
    const user = await User.findById(req.user.id);
    
    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }

    if (walletAddress) user.walletAddress = walletAddress;
    if (firstName) user.firstName = firstName;
    if (lastName) user.lastName = lastName;

    await user.save();

    res.json({
      success: true,
      message: 'Profile updated successfully',
      data: user
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get user statistics
exports.getUserStats = async (req, res) => {
  try {
    const userId = req.user.id;
    const user = await User.findById(userId);

    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }

    // Get total rewards earned
    const totalRewards = await Reward.aggregate([
      { $match: { user: user._id } },
      { $group: { _id: null, total: { $sum: '$amount' } } }
    ]);

    // Get task completion stats
    const taskStats = await TaskCompletion.aggregate([
      { $match: { user: user._id, status: 'verified' } },
      { $group: { _id: '$status', count: { $sum: 1 } } }
    ]);

    // Referral stats
    const referralStats = {
      directCount: user.directReferrals.length,
      indirectCount: user.indirectReferrals.length,
      totalReferrals: user.directReferrals.length + user.indirectReferrals.length
    };

    res.json({
      success: true,
      data: {
        user: {
          username: user.username,
          level: user.level,
          xp: user.xp,
          balance: user.balance,
          totalEarned: user.totalEarned,
          totalWithdrawn: user.totalWithdrawn,
          streak: user.streak
        },
        rewards: {
          total: totalRewards[0]?.total || 0,
          lifetime: user.totalEarned
        },
        tasks: {
          completed: user.tasksCompleted,
          dailyCompleted: user.dailyTasksCompleted
        },
        referrals: referralStats,
        achievements: {
          total: user.achievements.length,
          unlocked: user.achievements
        }
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get user by ID (public profile)
exports.getUserById = async (req, res) => {
  try {
    const user = await User.findById(req.params.id)
      .select('username firstName level xp tasksCompleted achievements');

    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }

    res.json({
      success: true,
      data: user
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Check user achievements
exports.checkAchievements = async (req, res) => {
  try {
    const userId = req.user.id;
    const user = await User.findById(userId);
    const Achievement = require('../models/Achievement.model');

    const allAchievements = await Achievement.find({ isActive: true });
    const newlyUnlocked = [];

    for (const achievement of allAchievements) {
      // Check if already unlocked
      const alreadyHas = user.achievements.some(
        a => a.achievementId === achievement._id.toString()
      );

      if (alreadyHas) continue;

      // Check conditions
      let unlocked = false;
      switch (achievement.condition.type) {
        case 'tasks_completed':
          unlocked = user.tasksCompleted >= achievement.condition.value;
          break;
        case 'referrals_count':
          unlocked = user.directReferrals.length >= achievement.condition.value;
          break;
        case 'balance_reached':
          unlocked = user.balance >= achievement.condition.value;
          break;
        case 'streak_days':
          unlocked = user.streak >= achievement.condition.value;
          break;
        case 'level_reached':
          unlocked = user.level >= achievement.condition.value;
          break;
      }

      if (unlocked) {
        user.achievements.push({
          achievementId: achievement._id,
          unlockedAt: new Date()
        });
        
        // Award achievement rewards
        if (achievement.reward.coins) {
          await user.addBalance(achievement.reward.coins);
        }
        if (achievement.reward.xp) {
          await user.addXP(achievement.reward.xp);
        }

        newlyUnlocked.push(achievement);
      }
    }

    if (newlyUnlocked.length > 0) {
      await user.save();
    }

    res.json({
      success: true,
      message: newlyUnlocked.length > 0 ? 'New achievements unlocked!' : 'No new achievements',
      data: {
        newlyUnlocked,
        totalAchievements: user.achievements.length
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

module.exports = exports;
"""

with open('user.controller.js', 'w') as f:
    f.write(user_controller)

print("✅ Created user.controller.js")
