const User = require('../models/User.model');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const crypto = require('crypto');

// Generate JWT Token
const generateToken = (userId) => {
  return jwt.sign({ id: userId }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRE || '7d'
  });
};

// Generate unique referral code
const generateReferralCode = () => {
  return crypto.randomBytes(4).toString('hex').toUpperCase();
};

// Register/Login user via Telegram
exports.telegramAuth = async (req, res) => {
  try {
    const { telegramId, username, firstName, lastName, referralCode } = req.body;

    if (!telegramId || !username) {
      return res.status(400).json({ 
        success: false, 
        message: 'Telegram ID and username are required' 
      });
    }

    // Check if user exists
    let user = await User.findOne({ telegramId });

    if (user) {
      // Existing user - login
      user.lastLoginDate = new Date();
      await user.updateStreak();
      await user.save();

      const token = generateToken(user._id);

      return res.json({
        success: true,
        message: 'Login successful',
        data: {
          token,
          user: {
            id: user._id,
            username: user.username,
            balance: user.balance,
            level: user.level,
            xp: user.xp,
            streak: user.streak,
            referralCode: user.referralCode
          }
        }
      });
    }

    // New user - register
    const newReferralCode = generateReferralCode();

    user = new User({
      telegramId,
      username,
      firstName,
      lastName,
      referralCode: newReferralCode,
      lastLoginDate: new Date()
    });

    // Handle referral if code provided
    if (referralCode) {
      const referrer = await User.findOne({ referralCode });
      if (referrer) {
        user.referredBy = referrer._id;
        referrer.directReferrals.push(user._id);

        // Award referral bonus
        const referralBonus = parseInt(process.env.REFERRAL_REWARD_DIRECT) || 100;
        await referrer.addBalance(referralBonus);
        await referrer.save();

        // Check if referrer was also referred (indirect referral)
        if (referrer.referredBy) {
          const indirectReferrer = await User.findById(referrer.referredBy);
          if (indirectReferrer) {
            indirectReferrer.indirectReferrals.push(user._id);
            const indirectBonus = parseInt(process.env.REFERRAL_REWARD_INDIRECT) || 50;
            await indirectReferrer.addBalance(indirectBonus);
            await indirectReferrer.save();
          }
        }
      }
    }

    await user.save();

    const token = generateToken(user._id);

    res.status(201).json({
      success: true,
      message: 'Registration successful',
      data: {
        token,
        user: {
          id: user._id,
          username: user.username,
          balance: user.balance,
          level: user.level,
          xp: user.xp,
          referralCode: user.referralCode
        }
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get current user
exports.getCurrentUser = async (req, res) => {
  try {
    const user = await User.findById(req.user.id)
      .select('-__v')
      .populate('referredBy', 'username')
      .populate('directReferrals', 'username level')
      .populate('indirectReferrals', 'username');

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

// Verify JWT token
exports.verifyToken = async (req, res) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({ success: false, message: 'No token provided' });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await User.findById(decoded.id);

    if (!user) {
      return res.status(401).json({ success: false, message: 'Invalid token' });
    }

    res.json({
      success: true,
      data: {
        userId: user._id,
        username: user.username,
        isValid: true
      }
    });
  } catch (error) {
    res.status(401).json({ success: false, message: 'Invalid token' });
  }
};

module.exports = exports;
