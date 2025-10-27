
# Create Database Models

# User Model
user_model = '''const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  telegramId: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  username: {
    type: String,
    required: true
  },
  firstName: String,
  lastName: String,
  
  // Wallet
  balance: {
    type: Number,
    default: 0
  },
  totalEarned: {
    type: Number,
    default: 0
  },
  totalWithdrawn: {
    type: Number,
    default: 0
  },
  walletAddress: String,
  
  // Gamification
  level: {
    type: Number,
    default: 1
  },
  xp: {
    type: Number,
    default: 0
  },
  streak: {
    type: Number,
    default: 0
  },
  lastLoginDate: Date,
  
  // Referrals
  referralCode: {
    type: String,
    unique: true,
    index: true
  },
  referredBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  directReferrals: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }],
  indirectReferrals: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }],
  
  // Stats
  tasksCompleted: {
    type: Number,
    default: 0
  },
  dailyTasksCompleted: {
    type: Number,
    default: 0
  },
  
  // Achievements
  achievements: [{
    achievementId: String,
    unlockedAt: Date
  }],
  
  // Daily Rewards
  lastDailyReward: Date,
  dailyRewardStreak: {
    type: Number,
    default: 0
  },
  
  // Premium
  isPremium: {
    type: Boolean,
    default: false
  },
  premiumExpiry: Date,
  
  // Status
  isActive: {
    type: Boolean,
    default: true
  },
  isBanned: {
    type: Boolean,
    default: false
  }
}, {
  timestamps: true
});

// Indexes
userSchema.index({ balance: -1 });
userSchema.index({ xp: -1 });
userSchema.index({ level: -1 });

// Methods
userSchema.methods.addBalance = function(amount) {
  this.balance += amount;
  this.totalEarned += amount;
  return this.save();
};

userSchema.methods.deductBalance = function(amount) {
  if (this.balance < amount) {
    throw new Error('Insufficient balance');
  }
  this.balance -= amount;
  return this.save();
};

userSchema.methods.addXP = function(xp) {
  this.xp += xp;
  // Level up logic
  const xpForNextLevel = this.level * 100;
  if (this.xp >= xpForNextLevel) {
    this.level += 1;
    this.xp -= xpForNextLevel;
  }
  return this.save();
};

userSchema.methods.updateStreak = function() {
  const today = new Date().setHours(0, 0, 0, 0);
  const lastLogin = this.lastLoginDate ? new Date(this.lastLoginDate).setHours(0, 0, 0, 0) : 0;
  const dayDiff = (today - lastLogin) / (1000 * 60 * 60 * 24);
  
  if (dayDiff === 1) {
    this.streak += 1;
  } else if (dayDiff > 1) {
    this.streak = 1;
  }
  
  this.lastLoginDate = new Date();
  return this.save();
};

module.exports = mongoose.model('User', userSchema);
'''

with open('User.model.js', 'w') as f:
    f.write(user_model)

print("✅ Created User.model.js")
print("\nUser Model Features:")
print("- Telegram integration")
print("- Wallet management")
print("- Gamification (level, XP, streak)")
print("- Referral system")
print("- Achievement tracking")
print("- Daily rewards")
print("- Premium membership")
