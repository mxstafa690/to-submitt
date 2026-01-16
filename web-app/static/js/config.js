/**
 * Configuration file
 * This file contains all the configuration settings for the app
 */

// API Configuration
const CONFIG = {
    // Backend API URL - Change this if your backend runs on a different port
    API_BASE_URL: 'http://127.0.0.1:5000/api',
    
    // Default values
    DEFAULT_PAGE_SIZE: 20,
    
    // API Endpoints
    ENDPOINTS: {
        MEMBERS: '/members',
        CLASSES: '/classes',
        PLANS: '/plans',
        CHECKINS: '/checkins',
        SUBSCRIPTIONS: '/subscriptions',
        PAYMENTS: '/payments'
    }
};

// Export for use in other files
window.CONFIG = CONFIG;
