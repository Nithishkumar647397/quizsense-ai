/**
 * QuizSense AI - Frontend JavaScript
 * Handles API calls, authentication, and common helpers
 */

// ============================================
// CONFIGURATION
// ============================================

const API_BASE_URL = 'http://127.0.0.1:8000';

// ============================================
// API OBJECT - All API Calls
// ============================================

const api = {

    getHeaders() {
        const token = localStorage.getItem('token');
        return {
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
        };
    },

    async handleResponse(response) {
        let data = null;
        try {
            data = await response.json();
        } catch (e) {
            // no json body
        }

        if (!response.ok) {
            const msg = data && data.detail
                ? (typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail))
                : `Request failed with status ${response.status}`;
            throw new Error(msg);
        }

        return data;
    },

    // ========== AUTH ENDPOINTS ==========

    async register(name, email, password) {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });

        const data = await this.handleResponse(response);

        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));

        return data;
    },

    async login(email, password) {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await this.handleResponse(response);

        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));

        return data;
    },

    // We still keep endpoint, but frontend logout is client-side
    async serverLogout() {
        try {
            await fetch(`${API_BASE_URL}/auth/logout`, {
                method: 'POST',
                headers: this.getHeaders()
            });
        } catch (e) {
            console.log('Server logout failed (can be ignored):', e.message);
        }
    },

    async getMe() {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
            method: 'GET',
            headers: this.getHeaders()
        });

        return await this.handleResponse(response);
    },

    // ========== QUIZ ENDPOINTS ==========

    async generateQuiz(subject, topic, difficulty, numQuestions) {
        const response = await fetch(`${API_BASE_URL}/quiz/generate`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({
                subject,
                topic,
                difficulty,
                num_questions: numQuestions
            })
        });

        return await this.handleResponse(response);
    },

    async generateAutoQuiz(domain, numQuestions) {
        const response = await fetch(`${API_BASE_URL}/quiz/auto`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({
                domain: domain,
                num_questions: numQuestions
            })
        });

        return await this.handleResponse(response);
    },

    async submitQuiz(quizId, answers, totalTimeSeconds) {
        const response = await fetch(`${API_BASE_URL}/quiz/submit`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify({
                quiz_id: quizId,
                answers: answers,
                total_time_seconds: totalTimeSeconds
            })
        });

        return await this.handleResponse(response);
    },

    async getQuizHistory(days = 7, limit = 10) {
        const response = await fetch(
            `${API_BASE_URL}/quiz/history?days=${days}&limit=${limit}`,
            {
                method: 'GET',
                headers: this.getHeaders()
            }
        );

        return await this.handleResponse(response);
    },

    async getTopics(subject = null) {
        let url = `${API_BASE_URL}/quiz/topics`;
        if (subject) {
            url += `?subject=${encodeURIComponent(subject)}`;
        }

        const response = await fetch(url, {
            method: 'GET',
            headers: this.getHeaders()
        });

        return await this.handleResponse(response);
    },

    // ========== REPORTS ENDPOINTS ==========

    async getWeeklyReport() {
        const response = await fetch(`${API_BASE_URL}/reports/weekly`, {
            method: 'GET',
            headers: this.getHeaders()
        });

        return await this.handleResponse(response);
    },

    async getPerformance(days = 7) {
        const response = await fetch(
            `${API_BASE_URL}/reports/performance?days=${days}`,
            {
                method: 'GET',
                headers: this.getHeaders()
            }
        );

        return await this.handleResponse(response);
    },

    async getDashboard() {
        const response = await fetch(`${API_BASE_URL}/reports/dashboard`, {
            method: 'GET',
            headers: this.getHeaders()
        });

        return await this.handleResponse(response);
    },

    async getWeakTopics() {
        const response = await fetch(`${API_BASE_URL}/reports/topics/weak`, {
            method: 'GET',
            headers: this.getHeaders()
        });

        return await this.handleResponse(response);
    },

    async getReportHistory(limit = 4) {
        const response = await fetch(
            `${API_BASE_URL}/reports/history?limit=${limit}`,
            {
                method: 'GET',
                headers: this.getHeaders()
            }
        );

        return await this.handleResponse(response);
    }
};

// ============================================
// AUTH HELPERS
// ============================================

function checkAuth() {
    const token = localStorage.getItem('token');
    const path = window.location.pathname.toLowerCase();

    if (!token) {
        if (!path.endsWith('signin.html') && !path.endsWith('signup.html')) {
            window.location.href = 'signin.html';
        }
        return false;
    }
    return true;
}

function logout() {
    // pure client-side logout (safe even if server down)
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'signin.html';
}

// Get current user from localStorage
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            return JSON.parse(userStr);
        } catch {
            return null;
        }
    }
    return null;
}

// ============================================
// UTILS
// ============================================

function formatDate(dateStr) {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatTime(seconds) {
    if (!seconds || seconds < 0) seconds = 0;
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function getPerformanceClass(accuracy) {
    if (accuracy >= 80) return 'excellent';
    if (accuracy >= 60) return 'good';
    return 'needs-work';
}

function showLoading(elementId) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = '<div class="spinner"></div>';
    }
}

function showError(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = `<div class="error-state">${message}</div>`;
    }
}

function showEmpty(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = `<div class="empty-state">${message}</div>`;
    }
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function () {
    const profileNameEl = document.getElementById('profileName');
    if (profileNameEl) {
        const user = getCurrentUser();
        profileNameEl.textContent = user && user.name ? user.name : 'User';
    }
});

// expose to HTML inline scripts
window.api = api;
window.checkAuth = checkAuth;
window.logout = logout;
window.getCurrentUser = getCurrentUser;
window.formatDate = formatDate;
window.formatTime = formatTime;
window.getPerformanceClass = getPerformanceClass;
window.showLoading = showLoading;
window.showError = showError;
window.showEmpty = showEmpty;