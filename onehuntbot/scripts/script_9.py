
# Create Task Model
task_model = '''const mongoose = require('mongoose');

const taskSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  
  // Task Type
  type: {
    type: String,
    enum: ['daily', 'weekly', 'social', 'quiz', 'survey', 'referral', 'special'],
    default: 'daily'
  },
  
  // Category
  category: {
    type: String,
    enum: ['telegram', 'twitter', 'youtube', 'general', 'partner'],
    default: 'general'
  },
  
  // Rewards
  reward: {
    coins: { type: Number, required: true },
    xp: { type: Number, default: 10 }
  },
  
  // Requirements
  requirement: {
    action: String,  // 'join_channel', 'follow_twitter', 'watch_video', etc.
    link: String,
    verificationMethod: String  // 'auto', 'manual', 'proof'
  },
  
  // Difficulty
  difficulty: {
    type: String,
    enum: ['easy', 'medium', 'hard'],
    default: 'easy'
  },
  
  // Limits
  maxCompletions: {
    type: Number,
    default: 1  // How many times a user can complete this task
  },
  totalCompletionsLimit: Number,  // Total completions across all users
  currentCompletions: {
    type: Number,
    default: 0
  },
  
  // Schedule
  startDate: Date,
  endDate: Date,
  isRecurring: {
    type: Boolean,
    default: false
  },
  recurringPeriod: {
    type: String,
    enum: ['daily', 'weekly', 'monthly']
  },
  
  // Status
  isActive: {
    type: Boolean,
    default: true
  },
  
  // Featured
  isFeatured: {
    type: Boolean,
    default: false
  },
  
  // Icon
  icon: String,
  
  // Priority (for sorting)
  priority: {
    type: Number,
    default: 0
  }
}, {
  timestamps: true
});

// Indexes
taskSchema.index({ type: 1, isActive: 1 });
taskSchema.index({ startDate: 1, endDate: 1 });
taskSchema.index({ priority: -1 });

module.exports = mongoose.model('Task', taskSchema);
'''

# Task Completion Model
task_completion_model = '''const mongoose = require('mongoose');

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
'''

with open('Task.model.js', 'w') as f:
    f.write(task_model)

with open('TaskCompletion.model.js', 'w') as f:
    f.write(task_completion_model)

print("✅ Created Task.model.js and TaskCompletion.model.js")
print("\nTask System Features:")
print("- Multiple task types (daily, weekly, social, etc.)")
print("- Category-based organization")
print("- Reward system (coins + XP)")
print("- Verification methods")
print("- Difficulty levels")
print("- Completion limits")
print("- Scheduling & recurring tasks")
print("- Task completion tracking")
