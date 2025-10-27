const express = require('express');
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
