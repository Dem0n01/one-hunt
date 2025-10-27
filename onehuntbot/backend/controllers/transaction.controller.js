const User = require('../models/User.model');
const mongoose = require('mongoose');

// Transaction Schema
const transactionSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    index: true
  },
  type: {
    type: String,
    enum: ['deposit', 'withdrawal', 'reward', 'refund', 'fee'],
    required: true
  },
  amount: {
    type: Number,
    required: true
  },
  status: {
    type: String,
    enum: ['pending', 'processing', 'completed', 'rejected', 'cancelled'],
    default: 'pending'
  },
  method: String,
  walletAddress: String,
  transactionHash: String,
  fee: Number,
  description: String,
  adminNotes: String,
  processedBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  processedAt: Date
}, {
  timestamps: true
});

transactionSchema.index({ user: 1, createdAt: -1 });
transactionSchema.index({ status: 1 });

const Transaction = mongoose.model('Transaction', transactionSchema);

// Get transaction history
exports.getTransactionHistory = async (req, res) => {
  try {
    const userId = req.user.id;
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const type = req.query.type;

    const query = { user: userId };
    if (type) query.type = type;

    const transactions = await Transaction.find(query)
      .sort({ createdAt: -1 })
      .skip((page - 1) * limit)
      .limit(limit);

    const total = await Transaction.countDocuments(query);

    res.json({
      success: true,
      data: {
        transactions,
        pagination: {
          page,
          limit,
          total,
          pages: Math.ceil(total / limit)
        }
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Request withdrawal
exports.requestWithdrawal = async (req, res) => {
  try {
    const userId = req.user.id;
    const { amount, walletAddress, method } = req.body;

    const user = await User.findById(userId);

    if (!user) {
      return res.status(404).json({ success: false, message: 'User not found' });
    }

    // Validate amount
    const minWithdrawal = parseInt(process.env.MIN_WITHDRAWAL_AMOUNT) || 100;
    if (amount < minWithdrawal) {
      return res.status(400).json({
        success: false,
        message: `Minimum withdrawal amount is ${minWithdrawal} coins`
      });
    }

    // Calculate fee
    const feePercent = parseInt(process.env.WITHDRAWAL_FEE_PERCENT) || 2;
    const fee = (amount * feePercent) / 100;
    const totalDeduction = amount + fee;

    // Check balance
    if (user.balance < totalDeduction) {
      return res.status(400).json({
        success: false,
        message: `Insufficient balance. Required: ${totalDeduction} (including ${fee} fee)`
      });
    }

    // Validate wallet address
    if (!walletAddress) {
      return res.status(400).json({
        success: false,
        message: 'Wallet address is required'
      });
    }

    // Create withdrawal transaction
    const transaction = new Transaction({
      user: userId,
      type: 'withdrawal',
      amount,
      fee,
      method: method || 'crypto',
      walletAddress,
      status: 'pending',
      description: `Withdrawal request: ${amount} coins`
    });

    await transaction.save();

    // Deduct from user balance (hold until processed)
    await user.deductBalance(totalDeduction);

    res.json({
      success: true,
      message: 'Withdrawal request submitted successfully',
      data: {
        transaction,
        newBalance: user.balance
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Get withdrawal status
exports.getWithdrawalStatus = async (req, res) => {
  try {
    const { transactionId } = req.params;
    const userId = req.user.id;

    const transaction = await Transaction.findOne({
      _id: transactionId,
      user: userId,
      type: 'withdrawal'
    });

    if (!transaction) {
      return res.status(404).json({
        success: false,
        message: 'Transaction not found'
      });
    }

    res.json({
      success: true,
      data: transaction
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Cancel pending withdrawal
exports.cancelWithdrawal = async (req, res) => {
  try {
    const { transactionId } = req.params;
    const userId = req.user.id;

    const transaction = await Transaction.findOne({
      _id: transactionId,
      user: userId,
      type: 'withdrawal',
      status: 'pending'
    });

    if (!transaction) {
      return res.status(404).json({
        success: false,
        message: 'Pending withdrawal not found'
      });
    }

    // Refund amount
    const user = await User.findById(userId);
    const refundAmount = transaction.amount + (transaction.fee || 0);
    await user.addBalance(refundAmount);

    // Update transaction
    transaction.status = 'cancelled';
    await transaction.save();

    res.json({
      success: true,
      message: 'Withdrawal cancelled and amount refunded',
      data: {
        refundAmount,
        newBalance: user.balance
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

// Admin: Process withdrawal
exports.processWithdrawal = async (req, res) => {
  try {
    // Check if user is admin
    if (!req.user.isAdmin) {
      return res.status(403).json({ success: false, message: 'Unauthorized' });
    }

    const { transactionId } = req.params;
    const { status, transactionHash, adminNotes } = req.body;

    const transaction = await Transaction.findById(transactionId);

    if (!transaction) {
      return res.status(404).json({
        success: false,
        message: 'Transaction not found'
      });
    }

    if (transaction.status !== 'pending') {
      return res.status(400).json({
        success: false,
        message: 'Transaction is not pending'
      });
    }

    // Update transaction
    transaction.status = status;
    transaction.transactionHash = transactionHash;
    transaction.adminNotes = adminNotes;
    transaction.processedBy = req.user.id;
    transaction.processedAt = new Date();

    await transaction.save();

    // If rejected, refund the amount
    if (status === 'rejected') {
      const user = await User.findById(transaction.user);
      const refundAmount = transaction.amount + (transaction.fee || 0);
      await user.addBalance(refundAmount);
    }

    // If completed, update user's total withdrawn
    if (status === 'completed') {
      const user = await User.findById(transaction.user);
      user.totalWithdrawn += transaction.amount;
      await user.save();
    }

    res.json({
      success: true,
      message: `Withdrawal ${status}`,
      data: transaction
    });
  } catch (error) {
    res.status(500).json({ success: false, message: error.message });
  }
};

module.exports = { ...exports, Transaction };
