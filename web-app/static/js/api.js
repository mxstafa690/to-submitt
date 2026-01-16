/**
 * API Service
 * This file handles all API calls to the backend
 */

class ApiService {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    /**
     * Make a GET request
     */
    async get(endpoint) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('GET request failed:', error);
            throw error;
        }
    }

    /**
     * Make a POST request
     */
    async post(endpoint, data) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorMessage = errorData.error || errorData.message || `HTTP error! status: ${response.status}`;
                const error = new Error(errorMessage);
                error.status = response.status;
                error.details = errorData;
                throw error;
            }
            return await response.json();
        } catch (error) {
            console.error('POST request failed:', error);
            throw error;
        }
    }

    /**
     * Make a PUT request
     */
    async put(endpoint, data) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('PUT request failed:', error);
            throw error;
        }
    }

    /**
     * Make a DELETE request
     */
    async delete(endpoint) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                method: 'DELETE'
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('DELETE request failed:', error);
            throw error;
        }
    }

    // Specific API methods

    /**
     * Get all members
     */
    async getMembers() {
        return this.get(CONFIG.ENDPOINTS.MEMBERS);
    }

    /**
     * Get a specific member
     */
    async getMember(id) {
        return this.get(`${CONFIG.ENDPOINTS.MEMBERS}/${id}`);
    }

    /**
     * Create a new member
     */
    async createMember(memberData) {
        return this.post(CONFIG.ENDPOINTS.MEMBERS, memberData);
    }

    /**
     * Get all classes
     */
    async getClasses() {
        return this.get(CONFIG.ENDPOINTS.CLASSES);
    }

    /**
     * Create a new class
     */
    async createClass(classData) {
        return this.post(CONFIG.ENDPOINTS.CLASSES, classData);
    }

    /**
     * Get all plans
     */
    async getPlans() {
        return this.get(CONFIG.ENDPOINTS.PLANS);
    }

    /**
     * Create a new plan
     */
    async createPlan(planData) {
        return this.post(CONFIG.ENDPOINTS.PLANS, planData);
    }

    /**
     * Get all check-ins
     */
    async getCheckins() {
        return this.get(CONFIG.ENDPOINTS.CHECKINS);
    }
}

// Create a global API instance
window.api = new ApiService(CONFIG.API_BASE_URL);
