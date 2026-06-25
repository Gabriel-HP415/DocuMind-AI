// Shared auth utilities
const API_BASE = '/api/v1';

function getToken() {
    return localStorage.getItem('documind_token');
}

function setToken(token, userId, role) {
    localStorage.setItem('documind_token', token);
    localStorage.setItem('documind_user_id', userId);
    localStorage.setItem('documind_role', role);
}

function clearAuth() {
    localStorage.removeItem('documind_token');
    localStorage.removeItem('documind_user_id');
    localStorage.removeItem('documind_role');
}

function isLoggedIn() {
    return !!getToken();
}

function isAdmin() {
    return localStorage.getItem('documind_role') === 'admin';
}

function authHeaders() {
    const token = getToken();
    return token ? { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' };
}

function requireAuth() {
    if (!isLoggedIn()) {
        window.location.href = 'sign_in.html';
        return false;
    }
    return true;
}

function requireAdmin() {
    if (!isAdmin()) {
        window.location.href = 'dashboard.html';
        return false;
    }
    return true;
}

async function apiFetch(path, options = {}) {
    const res = await fetch(API_BASE + path, {
        ...options,
        headers: { ...authHeaders(), ...(options.headers || {}) },
    });
    if (res.status === 401) {
        clearAuth();
        window.location.href = 'sign_in.html';
        return null;
    }
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || 'Request failed');
    }
    if (res.status === 204) return null;
    return res.json();
}

function logout() {
    clearAuth();
    window.location.href = 'landing.html';
}

// Toast notification helper
function showToast(message, type = 'info') {
    const id = 'toast-' + Date.now();
    const colors = {
        success: 'bg-green-600',
        error: 'bg-red-600',
        info: 'bg-primary',
        warning: 'bg-yellow-500',
    };
    const icons = {
        success: 'check_circle',
        error: 'error',
        info: 'info',
        warning: 'warning',
    };
    const bg = colors[type] || colors.info;
    const icon = icons[type] || icons.info;

    const toast = document.createElement('div');
    toast.id = id;
    toast.className = `fixed top-4 right-4 z-[9999] flex items-center gap-3 px-4 py-3 rounded-xl text-white text-sm font-medium shadow-lg transform translate-x-full transition-transform duration-300 ${bg}`;
    toast.innerHTML = `<span class="material-symbols-outlined text-lg">${icon}</span><span>${message}</span>`;
    document.body.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.remove('translate-x-full');
    });

    setTimeout(() => {
        toast.classList.add('translate-x-full');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
