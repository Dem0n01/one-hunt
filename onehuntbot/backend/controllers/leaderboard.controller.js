const User = require('../models/User.model');

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
