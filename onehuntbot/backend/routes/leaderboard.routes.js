const express = require('express');
const router = express.Router();
const leaderboardController = require('../controllers/leaderboard.controller');
const auth = require('../middleware/auth.middleware');

// Get top users by balance
router.get('/balance', auth, leaderboardController.getTopByBalance);

// Get top users by level
router.get('/level', auth, leaderboardController.getTopByLevel);

// Get top referrers
router.get('/referrals', auth, leaderboardController.getTopReferrers);

// Get user's rank
router.get('/rank', auth, leaderboardController.getUserRank);

module.exports = router;
