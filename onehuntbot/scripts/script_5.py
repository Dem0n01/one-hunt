
# 6. CREATE MIDDLEWARE FILES

# Auth Middleware
auth_middleware = """const jwt = require('jsonwebtoken');
const User = require('../models/User.model');

const auth = async (req, res, next) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');
    
    if (!token) {
      return res.status(401).json({ 
        success: false, 
        message: 'Access denied. No token provided.' 
      });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await User.findById(decoded.id);
    
    if (!user) {
      return res.status(401).json({ 
        success: false, 
        message: 'Invalid token. User not found.' 
      });
    }

    if (user.isBanned) {
      return res.status(403).json({ 
        success: false, 
        message: 'Account is banned.' 
      });
    }

    req.user = user;
    next();
  } catch (error) {
    res.status(401).json({ 
      success: false, 
      message: 'Invalid token.' 
    });
  }
};

module.exports = auth;
"""

# Validation Middleware
validation_middleware = """const { validationResult } = require('express-validator');

const validate = (req, res, next) => {
  const errors = validationResult(req);
  
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      message: 'Validation failed',
      errors: errors.array()
    });
  }
  
  next();
};

module.exports = validate;
"""

# Error Middleware
error_middleware = """const errorHandler = (err, req, res, next) => {
  console.error('❌ Error:', err);

  // Mongoose validation error
  if (err.name === 'ValidationError') {
    const errors = Object.values(err.errors).map(val => val.message);
    return res.status(400).json({
      success: false,
      message: 'Validation Error',
      errors
    });
  }

  // Mongoose duplicate key error
  if (err.code === 11000) {
    const field = Object.keys(err.keyValue)[0];
    return res.status(400).json({
      success: false,
      message: `${field} already exists`
    });
  }

  // JWT errors
  if (err.name === 'JsonWebTokenError') {
    return res.status(401).json({
      success: false,
      message: 'Invalid token'
    });
  }

  if (err.name === 'TokenExpiredError') {
    return res.status(401).json({
      success: false,
      message: 'Token expired'
    });
  }

  // Default error
  res.status(err.statusCode || 500).json({
    success: false,
    message: err.message || 'Internal Server Error'
  });
};

module.exports = errorHandler;
"""

# Save middleware files
with open('auth.middleware.js', 'w') as f:
    f.write(auth_middleware)
    
with open('validation.middleware.js', 'w') as f:
    f.write(validation_middleware)
    
with open('error.middleware.js', 'w') as f:
    f.write(error_middleware)

print("✅ Created all middleware files:")
print("  - auth.middleware.js")
print("  - validation.middleware.js")
print("  - error.middleware.js")
