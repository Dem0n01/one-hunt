const mongoose = require('mongoose');

const taskCompletionSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    index: true
  },
  task: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Task',
    required: true,
    index: true
  },

  // Verification
  status: {
    type: String,
    enum: ['pending', 'verified', 'rejected'],
    default: 'pending'
  },
  proof: String,  // Screenshot URL or proof of completion
  verifiedBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  verifiedAt: Date,

  // Rewards given
  rewardGiven: {
    coins: Number,
    xp: Number
  },

  // Completion details
  completedAt: {
    type: Date,
    default: Date.now
  },

  // Notes
  notes: String
}, {
  timestamps: true
});

// Compound index to prevent duplicate completions
taskCompletionSchema.index({ user: 1, task: 1 }, { unique: false });

module.exports = mongoose.model('TaskCompletion', taskCompletionSchema);
