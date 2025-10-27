const express = require('express');
const router = express.Router();
const referralController = require('../controllers/referral.controller');
const auth = require('../middleware/auth.middleware');

// Get referral info
router.get('/info', auth, referralController.getReferralInfo);

// Apply referral code
router.post('/apply', auth, referralController.applyReferralCode);

// Get referral leaderboard
router.get('/leaderboard', auth, referralController.getReferralLeaderboard);

module.exports = router;
