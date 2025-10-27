const mongoose = require('mongoose');

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
