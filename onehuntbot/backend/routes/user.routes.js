const express = require('express');
const router = express.Router();
const userController = require('../controllers/user.controller');
const auth = require('../middleware/auth.middleware');

// Get user profile
router.get('/profile', auth, userController.getProfile);

// Update profile
router.put('/profile', auth, userController.updateProfile);

// Get user statistics
router.get('/stats', auth, userController.getUserStats);

// Get user by ID (public)
router.get('/:id', auth, userController.getUserById);

// Check and unlock achievements
router.post('/achievements/check', auth, userController.checkAchievements);

module.exports = router;
