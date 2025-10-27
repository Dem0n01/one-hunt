const mongoose = require('mongoose');

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
