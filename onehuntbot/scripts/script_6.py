
# 7. CREATE SEED DATABASE SCRIPT
seed_script = """const mongoose = require('mongoose');
require('dotenv').config();

// Import models
const User = require('../backend/models/User.model');
const Task = require('../backend/models/Task.model');
const Achievement = require('../backend/models/Achievement.model');

const sampleTasks = [
  {
    title: "Join Telegram Channel",
    description: "Join our official Telegram channel for updates and announcements",
    type: "social",
    category: "telegram",
    reward: { coins: 50, xp: 10 },
    requirement: {
      action: "join_channel",
      link: "https://t.me/yourchannel",
      verificationMethod: "manual"
    },
    difficulty: "easy",
    isActive: true,
    isFeatured: true,
    priority: 10
  },
  {
    title: "Daily Check-in",
    description: "Check in daily to earn rewards",
    type: "daily",
    category: "general",
    reward: { coins: 10, xp: 5 },
    requirement: {
      action: "daily_checkin",
      verificationMethod: "auto"
    },
    difficulty: "easy",
    isActive: true,
    isRecurring: true,
    recurringPeriod: "daily",
    priority: 20
  },
  {
    title: "Follow on Twitter",
    description: "Follow our Twitter account @yourhandle",
    type: "social",
    category: "twitter",
    reward: { coins: 75, xp: 15 },
    requirement: {
      action: "follow_twitter",
      link: "https://twitter.com/yourhandle",
      verificationMethod: "manual"
    },
    difficulty: "easy",
    isActive: true,
    priority: 15
  },
  {
    title: "Subscribe on YouTube",
    description: "Subscribe to our YouTube channel",
    type: "social",
    category: "youtube",
    reward: { coins: 100, xp: 20 },
    requirement: {
      action: "subscribe_youtube",
      link: "https://youtube.com/@yourchannel",
      verificationMethod: "manual"
    },
    difficulty: "easy",
    isActive: true,
    priority: 12
  },
  {
    title: "Refer 5 Friends",
    description: "Invite 5 friends to join the bot",
    type: "referral",
    category: "general",
    reward: { coins: 200, xp: 50 },
    requirement: {
      action: "refer_friends",
      verificationMethod: "auto"
    },
    difficulty: "medium",
    isActive: true,
    priority: 5
  },
  {
    title: "Complete 10 Tasks",
    description: "Complete any 10 tasks to earn bonus",
    type: "special",
    category: "general",
    reward: { coins: 150, xp: 30 },
    requirement: {
      action: "complete_tasks",
      verificationMethod: "auto"
    },
    difficulty: "medium",
    isActive: true,
    priority: 8
  },
  {
    title: "Weekly Challenge",
    description: "Complete all daily tasks for 7 consecutive days",
    type: "weekly",
    category: "general",
    reward: { coins: 300, xp: 75 },
    requirement: {
      action: "weekly_streak",
      verificationMethod: "auto"
    },
    difficulty: "hard",
    isActive: true,
    isRecurring: true,
    recurringPeriod: "weekly",
    priority: 3
  }
];

const sampleAchievements = [
  {
    name: "First Steps",
    description: "Complete your first task",
    icon: "🎯",
    category: "tasks",
    requirement: "Complete 1 task",
    condition: { type: "tasks_completed", value: 1 },
    reward: { coins: 20, xp: 10 },
    rarity: "common",
    isActive: true
  },
  {
    name: "Task Warrior",
    description: "Complete 10 tasks",
    icon: "⚔️",
    category: "tasks",
    requirement: "Complete 10 tasks",
    condition: { type: "tasks_completed", value: 10 },
    reward: { coins: 100, xp: 50 },
    rarity: "rare",
    isActive: true
  },
  {
    name: "Task Master",
    description: "Complete 50 tasks",
    icon: "👑",
    category: "tasks",
    requirement: "Complete 50 tasks",
    condition: { type: "tasks_completed", value: 50 },
    reward: { coins: 500, xp: 200 },
    rarity: "epic",
    isActive: true
  },
  {
    name: "Social Butterfly",
    description: "Refer your first friend",
    icon: "🦋",
    category: "referrals",
    requirement: "Refer 1 user",
    condition: { type: "referrals_count", value: 1 },
    reward: { coins: 50, xp: 15 },
    rarity: "common",
    isActive: true
  },
  {
    name: "Referral King",
    description: "Refer 10 friends",
    icon: "👑",
    category: "referrals",
    requirement: "Refer 10 users",
    condition: { type: "referrals_count", value: 10 },
    reward: { coins: 500, xp: 100 },
    rarity: "epic",
    isActive: true
  },
  {
    name: "Referral Legend",
    description: "Refer 50 friends",
    icon: "🌟",
    category: "referrals",
    requirement: "Refer 50 users",
    condition: { type: "referrals_count", value: 50 },
    reward: { coins: 2000, xp: 500 },
    rarity: "legendary",
    isActive: true
  },
  {
    name: "Rich Beginner",
    description: "Reach 100 coins balance",
    icon: "💰",
    category: "earnings",
    requirement: "Accumulate 100 coins",
    condition: { type: "balance_reached", value: 100 },
    reward: { coins: 50, xp: 25 },
    rarity: "common",
    isActive: true
  },
  {
    name: "High Roller",
    description: "Reach 1000 coins balance",
    icon: "💎",
    category: "earnings",
    requirement: "Accumulate 1000 coins",
    condition: { type: "balance_reached", value: 1000 },
    reward: { coins: 200, xp: 75 },
    rarity: "rare",
    isActive: true
  },
  {
    name: "Millionaire",
    description: "Reach 10000 coins balance",
    icon: "🏆",
    category: "earnings",
    requirement: "Accumulate 10000 coins",
    condition: { type: "balance_reached", value: 10000 },
    reward: { coins: 1000, xp: 300 },
    rarity: "legendary",
    isActive: true
  },
  {
    name: "Streak Starter",
    description: "Login for 3 consecutive days",
    icon: "🔥",
    category: "special",
    requirement: "3-day login streak",
    condition: { type: "streak_days", value: 3 },
    reward: { coins: 50, xp: 15 },
    rarity: "common",
    isActive: true
  },
  {
    name: "Streak Warrior",
    description: "Login for 7 consecutive days",
    icon: "🔥🔥",
    category: "special",
    requirement: "7-day login streak",
    condition: { type: "streak_days", value: 7 },
    reward: { coins: 150, xp: 30 },
    rarity: "rare",
    isActive: true
  },
  {
    name: "Streak Legend",
    description: "Login for 30 consecutive days",
    icon: "🔥🔥🔥",
    category: "special",
    requirement: "30-day login streak",
    condition: { type: "streak_days", value: 30 },
    reward: { coins: 1000, xp: 200 },
    rarity: "legendary",
    isActive: true
  },
  {
    name: "Level Up",
    description: "Reach level 5",
    icon: "⬆️",
    category: "special",
    requirement: "Reach level 5",
    condition: { type: "level_reached", value: 5 },
    reward: { coins: 100, xp: 0 },
    rarity: "common",
    isActive: true
  },
  {
    name: "Power User",
    description: "Reach level 10",
    icon: "⚡",
    category: "special",
    requirement: "Reach level 10",
    condition: { type: "level_reached", value: 10 },
    reward: { coins: 300, xp: 0 },
    rarity: "rare",
    isActive: true
  },
  {
    name: "Elite",
    description: "Reach level 20",
    icon: "🌟",
    category: "special",
    requirement: "Reach level 20",
    condition: { type: "level_reached", value: 20 },
    reward: { coins: 1000, xp: 0 },
    rarity: "epic",
    isActive: true
  }
];

async function seedDatabase() {
  try {
    // Connect to MongoDB
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('📦 Connected to MongoDB');

    // Clear existing data (optional - comment out to keep existing data)
    await Task.deleteMany({});
    await Achievement.deleteMany({});
    console.log('🗑️  Cleared existing tasks and achievements');

    // Insert sample tasks
    const tasks = await Task.insertMany(sampleTasks);
    console.log(`✅ Inserted ${tasks.length} sample tasks`);

    // Insert sample achievements
    const achievements = await Achievement.insertMany(sampleAchievements);
    console.log(`✅ Inserted ${achievements.length} sample achievements`);

    console.log('\\n🎉 Database seeded successfully!');
    console.log('\\nYou can now:');
    console.log('- Start the server: npm run dev');
    console.log('- Check tasks in the app');
    console.log('- Complete tasks to earn rewards');
    
    process.exit(0);
  } catch (error) {
    console.error('❌ Error seeding database:', error);
    process.exit(1);
  }
}

seedDatabase();
"""

with open('seed-database.js', 'w') as f:
    f.write(seed_script)

print("✅ Created seed-database.js")
