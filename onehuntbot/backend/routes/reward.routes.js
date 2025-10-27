const express = require('express');
const router = express.Router();
const rewardController = require('../controllers/reward.controller');
const auth = require('../middleware/auth.middleware');

// Claim daily reward
router.post('/daily', auth, rewardController.claimDailyReward);

// Spin the wheel
router.post('/spin', auth, rewardController.spinWheel);

// Get reward history
router.get('/history', auth, rewardController.getRewardHistory);

module.exports = router;
