const express = require('express');
const router = express.Router();
const authController = require('../controllers/auth.controller');
const auth = require('../middleware/auth.middleware');

// Telegram authentication
router.post('/telegram', authController.telegramAuth);

// Get current user
router.get('/me', auth, authController.getCurrentUser);

// Verify token
router.post('/verify', authController.verifyToken);

module.exports = router;
