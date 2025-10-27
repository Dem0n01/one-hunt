const express = require('express');
const router = express.Router();
const transactionController = require('../controllers/transaction.controller');
const auth = require('../middleware/auth.middleware');

// Get transaction history
router.get('/', auth, transactionController.getTransactionHistory);

// Request withdrawal
router.post('/withdraw', auth, transactionController.requestWithdrawal);

// Get withdrawal status
router.get('/withdraw/:transactionId', auth, transactionController.getWithdrawalStatus);

// Cancel withdrawal
router.delete('/withdraw/:transactionId', auth, transactionController.cancelWithdrawal);

// Admin: Process withdrawal
router.put('/admin/withdraw/:transactionId', auth, transactionController.processWithdrawal);

module.exports = router;
