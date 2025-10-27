
# Create comprehensive API routes and controllers

# Task Routes
task_routes = '''const express = require('express');
const router = express.Router();
const taskController = require('../controllers/task.controller');
const auth = require('../middleware/auth.middleware');

// Get all tasks
router.get('/', auth, taskController.getAllTasks);

// Get task by ID
router.get('/:id', auth, taskController.getTaskById);

// Get tasks by type
router.get('/type/:type', auth, taskController.getTasksByType);

// Complete task
router.post('/:id/complete', auth, taskController.completeTask);

// Get user's completed tasks
router.get('/user/completed', auth, taskController.getUserCompletedTasks);

// Get user's available tasks
router.get('/user/available', auth, taskController.getUserAvailableTasks);

// Admin routes
router.post('/admin/create', auth, taskController.createTask);
router.put('/admin/:id', auth, taskController.updateTask);
router.delete('/admin/:id', auth, taskController.deleteTask);

module.exports = router;
'''

# Task Controller
task_controller = '''const Task = require('../models/Task.model');
const TaskCompletion = require('../models/TaskCompletion.model');
const User = require('../models/User.model');
const { bot } = require('../server');

// Get all active tasks
exports.getAllTasks = async (req, res) => {
  try {
    const tasks = await Task.find({ 
      isActive: true,
      $or: [
        { endDate: { $gte: new Date() } },
        { endDate: null }
      ]
    }).sort({ priority: -1, createdAt: -1 });
    
    res.json({ success: true, data: tasks });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get tasks by type
exports.getTasksByType = async (req, res) => {
  try {
    const { type } = req.params;
    const tasks = await Task.find({ 
      type, 
      isActive: true 
    }).sort({ priority: -1 });
    
    res.json({ success: true, data: tasks });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get user's available tasks
exports.getUserAvailableTasks = async (req, res) => {
  try {
    const userId = req.user.id;
    
    // Get all active tasks
    const allTasks = await Task.find({ isActive: true });
    
    // Get completed tasks
    const completedTasks = await TaskCompletion.find({ 
      user: userId,
      status: 'verified'
    }).select('task');
    
    const completedTaskIds = completedTasks.map(ct => ct.task.toString());
    
    // Filter out completed tasks (if maxCompletions = 1)
    const availableTasks = allTasks.filter(task => {
      if (task.maxCompletions === 1) {
        return !completedTaskIds.includes(task._id.toString());
      }
      return true;
    });
    
    res.json({ success: true, data: availableTasks });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Complete task
exports.completeTask = async (req, res) => {
  try {
    const { id } = req.params;
    const userId = req.user.id;
    const { proof } = req.body;
    
    const task = await Task.findById(id);
    if (!task) {
      return res.status(404).json({ success: false, message: 'Task not found' });
    }
    
    // Check if already completed
    const existingCompletion = await TaskCompletion.findOne({
      user: userId,
      task: id,
      status: 'verified'
    });
    
    if (existingCompletion && task.maxCompletions === 1) {
      return res.status(400).json({ 
        success: false, 
        message: 'Task already completed' 
      });
    }
    
    // Create completion record
    const completion = new TaskCompletion({
      user: userId,
      task: id,
      proof,
      rewardGiven: task.reward
    });
    
    // Auto-verify or manual verify based on task
    if (task.requirement.verificationMethod === 'auto') {
      completion.status = 'verified';
      completion.verifiedAt = new Date();
      
      // Award rewards
      const user = await User.findById(userId);
      await user.addBalance(task.reward.coins);
      await user.addXP(task.reward.xp);
      user.tasksCompleted += 1;
      await user.save();
      
      // Update task completion count
      task.currentCompletions += 1;
      await task.save();
    }
    
    await completion.save();
    
    res.json({ 
      success: true, 
      message: completion.status === 'verified' ? 
        'Task completed! Rewards added to your account.' : 
        'Task submitted for verification.',
      data: completion 
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get user's completed tasks
exports.getUserCompletedTasks = async (req, res) => {
  try {
    const userId = req.user.id;
    
    const completions = await TaskCompletion.find({ user: userId })
      .populate('task')
      .sort({ completedAt: -1 });
    
    res.json({ success: true, data: completions });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Admin: Create task
exports.createTask = async (req, res) => {
  try {
    // Check if user is admin
    if (!req.user.isAdmin) {
      return res.status(403).json({ success: false, message: 'Unauthorized' });
    }
    
    const task = new Task(req.body);
    await task.save();
    
    res.status(201).json({ success: true, data: task });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Admin: Update task
exports.updateTask = async (req, res) => {
  try {
    if (!req.user.isAdmin) {
      return res.status(403).json({ success: false, message: 'Unauthorized' });
    }
    
    const task = await Task.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true, runValidators: true }
    );
    
    if (!task) {
      return res.status(404).json({ success: false, message: 'Task not found' });
    }
    
    res.json({ success: true, data: task });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Admin: Delete task
exports.deleteTask = async (req, res) => {
  try {
    if (!req.user.isAdmin) {
      return res.status(403).json({ success: false, message: 'Unauthorized' });
    }
    
    const task = await Task.findByIdAndDelete(req.params.id);
    
    if (!task) {
      return res.status(404).json({ success: false, message: 'Task not found' });
    }
    
    res.json({ success: true, message: 'Task deleted successfully' });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

exports.getTaskById = async (req, res) => {
  try {
    const task = await Task.findById(req.params.id);
    if (!task) {
      return res.status(404).json({ success: false, message: 'Task not found' });
    }
    res.json({ success: true, data: task });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};
'''

with open('task.routes.js', 'w') as f:
    f.write(task_routes)

with open('task.controller.js', 'w') as f:
    f.write(task_controller)

print("✅ Created task.routes.js and task.controller.js")
print("\nTask API Endpoints:")
print("- GET /api/tasks - Get all tasks")
print("- GET /api/tasks/type/:type - Get tasks by type")
print("- GET /api/tasks/user/available - Get available tasks for user")
print("- GET /api/tasks/user/completed - Get completed tasks")
print("- POST /api/tasks/:id/complete - Complete a task")
print("- POST /api/tasks/admin/create - Create task (admin)")
print("- PUT /api/tasks/admin/:id - Update task (admin)")
print("- DELETE /api/tasks/admin/:id - Delete task (admin)")
