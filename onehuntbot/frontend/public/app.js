// One Hunt Bot - Main Application JavaScript

// Configuration
const API_BASE_URL = 'http://localhost:3000/api';
let currentUser = null;

// Initialize Telegram Web App
const tg = window.Telegram?.WebApp;
if (tg) {
    tg.ready();
    tg.expand();
}

// Utility Functions
function showLoading() {
    document.getElementById('loadingOverlay').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('active');
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function formatNumber(num) {
    return new Intl.NumberFormat().format(num);
}

// Navigation
function showView(viewId) {
    // Hide all views
    document.querySelectorAll('.view').forEach(view => {
        view.classList.remove('active');
    });

    // Remove active class from all nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });

    // Show selected view
    document.getElementById(viewId).classList.add('active');

    // Add active class to corresponding nav item
    const navItem = document.querySelector(`[data-view="${viewId}"]`);
    if (navItem) {
        navItem.classList.add('active');
    }

    // Load data for the view
    loadViewData(viewId);
}

// Setup navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
        const viewId = item.getAttribute('data-view');
        showView(viewId);
    });
});

// API Functions
async function authenticateUser() {
    try {
        showLoading();

        // Get user data from Telegram
        const telegramUser = tg?.initDataUnsafe?.user || {
            id: 123456789,
            first_name: 'Demo',
            username: 'demo_user'
        };

        const response = await fetch(`${API_BASE_URL}/auth/telegram`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                telegramId: telegramUser.id,
                username: telegramUser.username || '',
                firstName: telegramUser.first_name || 'User'
            })
        });

        const data = await response.json();

        if (data.success) {
            currentUser = data.user;
            localStorage.setItem('authToken', data.token);
            updateUI();
            showToast('Welcome to One Hunt! 🎯');
        }
    } catch (error) {
        console.error('Authentication error:', error);
        showToast('Connection error. Please try again.');
    } finally {
        hideLoading();
    }
}

async function fetchWithAuth(url, options = {}) {
    const token = localStorage.getItem('authToken');

    return fetch(url, {
        ...options,
        headers: {
            ...options.headers,
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
}

async function getUserProfile() {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/users/profile`);
        const data = await response.json();

        if (data.success) {
            currentUser = data.user;
            updateUI();
        }
    } catch (error) {
        console.error('Error fetching profile:', error);
    }
}

async function claimDailyReward() {
    try {
        showLoading();

        const response = await fetchWithAuth(`${API_BASE_URL}/rewards/daily`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showToast(`Claimed ${data.reward} coins! 🎉`);
            getUserProfile();
        } else {
            showToast(data.message || 'Already claimed today!');
        }
    } catch (error) {
        console.error('Error claiming reward:', error);
        showToast('Failed to claim reward');
    } finally {
        hideLoading();
    }
}

async function loadTasks(filter = 'all') {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/tasks?type=${filter}`);
        const data = await response.json();

        if (data.success) {
            displayTasks(data.tasks, 'allTasks');
            displayTasks(data.tasks.slice(0, 3), 'featuredTasks');
        }
    } catch (error) {
        console.error('Error loading tasks:', error);
    }
}

function displayTasks(tasks, containerId) {
    const container = document.getElementById(containerId);

    if (tasks.length === 0) {
        container.innerHTML = '<p class="empty-state">No tasks available</p>';
        return;
    }

    container.innerHTML = tasks.map(task => `
        <div class="task-card" data-task-id="${task._id}">
            <div class="task-info">
                <h4 class="task-title">${task.title}</h4>
                <p class="task-desc">${task.description}</p>
                <span class="task-reward">🪙 +${task.reward}</span>
            </div>
            <button class="btn btn-sm btn-primary" onclick="completeTask('${task._id}')">
                ${task.completed ? 'Completed ✓' : 'Start'}
            </button>
        </div>
    `).join('');
}

async function completeTask(taskId) {
    try {
        showLoading();

        const response = await fetchWithAuth(`${API_BASE_URL}/tasks/${taskId}/complete`, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            showToast(`Task completed! Earned ${data.reward} coins! 🎯`);
            getUserProfile();
            loadTasks();
        } else {
            showToast(data.message || 'Task already completed!');
        }
    } catch (error) {
        console.error('Error completing task:', error);
        showToast('Failed to complete task');
    } finally {
        hideLoading();
    }
}

async function loadLeaderboard(type = 'balance') {
    try {
        const response = await fetchWithAuth(`${API_BASE_URL}/leaderboard?type=${type}`);
        const data = await response.json();

        if (data.success) {
            displayLeaderboard(data.leaderboard);
        }
    } catch (error) {
        console.error('Error loading leaderboard:', error);
    }
}

function displayLeaderboard(users) {
    const container = document.getElementById('leaderboardList');

    container.innerHTML = users.map((user, index) => `
        <div class="leaderboard-item">
            <span class="rank">#${index + 1}</span>
            <span class="username">${user.username || user.firstName}</span>
            <span class="score">${formatNumber(user.balance || user.level || user.referralCount)}</span>
        </div>
    `).join('');
}

function updateUI() {
    if (!currentUser) return;

    // Update balance
    document.getElementById('userBalance').textContent = formatNumber(currentUser.balance || 0);
    document.getElementById('profileBalance').textContent = formatNumber(currentUser.balance || 0);

    // Update level
    document.getElementById('userLevel').textContent = currentUser.level || 1;
    document.getElementById('profileLevel').textContent = currentUser.level || 1;

    // Update streak
    document.getElementById('userStreak').textContent = currentUser.streak || 0;

    // Update tasks completed
    document.getElementById('tasksCompleted').textContent = currentUser.tasksCompleted || 0;

    // Update profile info
    document.getElementById('userName').textContent = currentUser.firstName || 'User';
    document.getElementById('userUsername').textContent = `@${currentUser.username || 'anonymous'}`;
    document.getElementById('userInitial').textContent = (currentUser.firstName || 'U')[0].toUpperCase();
    document.getElementById('profileReferrals').textContent = currentUser.referralCount || 0;

    // Update referral link
    const referralLink = `https://t.me/YourBotUsername?start=${currentUser.telegramId}`;
    document.getElementById('referralLink').value = referralLink;
}

function loadViewData(viewId) {
    switch(viewId) {
        case 'tasksView':
            loadTasks();
            break;
        case 'leaderboardView':
            loadLeaderboard();
            break;
        case 'profileView':
            getUserProfile();
            break;
    }
}

// Event Listeners
document.getElementById('claimDailyBtn')?.addEventListener('click', claimDailyReward);

document.getElementById('copyLinkBtn')?.addEventListener('click', () => {
    const input = document.getElementById('referralLink');
    input.select();
    document.execCommand('copy');
    showToast('Link copied to clipboard! 📋');
});

document.getElementById('shareBtn')?.addEventListener('click', () => {
    const referralLink = document.getElementById('referralLink').value;
    if (tg) {
        tg.openTelegramLink(referralLink);
    } else {
        showToast('Share link: ' + referralLink);
    }
});

// Task filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.getAttribute('data-filter');
        loadTasks(filter);
    });
});

// Leaderboard tabs
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const type = btn.getAttribute('data-tab');
        loadLeaderboard(type);
    });
});

// Initialize app
window.addEventListener('DOMContentLoaded', () => {
    authenticateUser();
    loadTasks();
});

// Make functions global for inline onclick handlers
window.showView = showView;
window.completeTask = completeTask;
