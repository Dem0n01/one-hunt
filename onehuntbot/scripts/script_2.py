
# 3. REFERRAL CONTROLLER
referral_controller = """const User = require('../models/User.model');
const Reward = require('../models/Reward.model');

// Get referral information
exports.getReferralInfo = async (req, res) => {
  try {
    const user = await User.findById(req.user.id)
      .populate('directReferrals', 'username firstName level balance createdAt')
      .populate('indirectReferrals', 'username firstName level');

    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }

    // Calculate total earnings from referrals
    const referralRewards = await Reward.find({
      user: user._id,
      type: 'referral'
    });

    const totalReferralEarnings = referralRewards.reduce((sum, r) => sum + r.amount, 0);

    res.json({
      success: true,
      data: {
        referralCode: user.referralCode,
        referralLink: `${process.env.BASE_URL}?ref=${user.referralCode}`,
        stats: {
          directCount: user.directReferrals.length,
          indirectCount: user.indirectReferrals.length,
          totalEarnings: totalReferralEarnings
        },
        directReferrals: user.directReferrals,
        indirectReferrals: user.indirectReferrals,
        rewards: {
          perDirectReferral: process.env.REFERRAL_REWARD_DIRECT || 100,
          perIndirectReferral: process.env.REFERRAL_REWARD_INDIRECT || 50
        }
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Apply referral code (for new users)
exports.applyReferralCode = async (req, res) => {
  try {
    const { referralCode } = req.body;
    const userId = req.user.id;

    const user = await User.findById(userId);
    
    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }

    // Check if user already has a referrer
    if (user.referredBy) {
      return res.status(400).json({
        success: false,
        message: 'You have already used a referral code'
      });
    }

    // Find referrer
    const referrer = await User.findOne({ referralCode });
    
    if (!referrer) {
      return res.status(404).json({
        success: false,
        message: 'Invalid referral code'
      });
    }

    // Can't refer yourself
    if (referrer._id.toString() === userId.toString()) {
      return res.status(400).json({
        success: false,
        message: 'You cannot use your own referral code'
      });
    }

    // Update user
    user.referredBy = referrer._id;
    await user.save();

    // Update referrer
    referrer.directReferrals.push(user._id);
    const directBonus = parseInt(process.env.REFERRAL_REWARD_DIRECT) || 100;
    await referrer.addBalance(directBonus);
    await referrer.save();

    // Create reward record
    const reward = new Reward({
      user: referrer._id,
      type: 'referral',
      amount: directBonus,
      xp: 20,
      description: `Direct referral: ${user.username}`,
      relatedReferral: user._id
    });
    await reward.save();

    // Check for indirect referral
    if (referrer.referredBy) {
      const indirectReferrer = await User.findById(referrer.referredBy);
      if (indirectReferrer) {
        indirectReferrer.indirectReferrals.push(user._id);
        const indirectBonus = parseInt(process.env.REFERRAL_REWARD_INDIRECT) || 50;
        await indirectReferrer.addBalance(indirectBonus);
        await indirectReferrer.save();

        const indirectReward = new Reward({
          user: indirectReferrer._id,
          type: 'referral',
          amount: indirectBonus,
          xp: 10,
          description: `Indirect referral: ${user.username}`,
          relatedReferral: user._id
        });
        await indirectReward.save();
      }
    }

    res.json({
      success: true,
      message: 'Referral code applied successfully',
      data: {
        referrer: {
          username: referrer.username,
          bonus: directBonus
        }
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get referral leaderboard
exports.getReferralLeaderboard = async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 50;

    const topReferrers = await User.aggregate([
      { $match: { isActive: true, isBanned: false } },
      {
        $project: {
          username: 1,
          firstName: 1,
          directCount: { $size: { $ifNull: ['$directReferrals', []] } },
          indirectCount: { $size: { $ifNull: ['$indirectReferrals', []] } },
          totalReferrals: {
            $add: [
              { $size: { $ifNull: ['$directReferrals', []] } },
              { $size: { $ifNull: ['$indirectReferrals', []] } }
            ]
          }
        }
      },
      { $sort: { directCount: -1, totalReferrals: -1 } },
      { $limit: limit }
    ]);

    const rankedReferrers = topReferrers.map((user, index) => ({
      rank: index + 1,
      ...user
    }));

    res.json({
      success: true,
      data: rankedReferrers
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

module.exports = exports;
"""

with open('referral.controller.js', 'w') as f:
    f.write(referral_controller)

print("✅ Created referral.controller.js")
