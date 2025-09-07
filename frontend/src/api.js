/**
 * API Client for Brand Storytelling Frontend
 * Centralized API communication with error handling
 */

class ApiClient {
    constructor(baseURL = 'http://localhost:8000/api/v1') {
        this.baseURL = baseURL;
        this.backendBaseURL = 'http://localhost:8000';
    }

    // Utility function to construct full image URLs
    constructImageUrl(imageUrl) {
        if (!imageUrl) return '';
        if (imageUrl.startsWith('http') || imageUrl.startsWith('blob:')) {
            return imageUrl;
        }
        return `${this.backendBaseURL}${imageUrl}`;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API request failed: ${endpoint}`, error);
            throw error;
        }
    }

    // Project endpoints
    async createProject(name) {
        return this.request('/projects', {
            method: 'POST',
            body: JSON.stringify({ name })
        });
    }

    async getProject(projectId) {
        return this.request(`/projects/${projectId}`);
    }

    // Character endpoints
    async createCharacter(projectId, characterData) {
        return this.request(`/projects/${projectId}/character`, {
            method: 'POST',
            body: JSON.stringify(characterData)
        });
    }

    // Product endpoints
    async generateProduct(projectId, productData) {
        return this.request(`/projects/${projectId}/product/generate`, {
            method: 'POST',
            body: JSON.stringify(productData)
        });
    }

    async uploadProduct(projectId, file) {
        const formData = new FormData();
        formData.append('image', file);

        return this.request(`/projects/${projectId}/product/upload`, {
            method: 'POST',
            headers: {}, // Let browser set content-type for FormData
            body: formData
        });
    }

    // Background endpoints
    async createBackground(projectId, backgroundData) {
        return this.request(`/projects/${projectId}/background`, {
            method: 'POST',
            body: JSON.stringify(backgroundData)
        });
    }

    // Story endpoints
    async createStory(projectId, storyData) {
        return this.request(`/projects/${projectId}/story`, {
            method: 'POST',
            body: JSON.stringify(storyData)
        });
    }

    // Generate endpoints
    async generateImages(projectId) {
        return this.request(`/projects/${projectId}/generate`, {
            method: 'POST'
        });
    }
}

// Create global API client instance
const apiClient = new ApiClient();

// Export for use in other modules
window.ApiClient = ApiClient;
window.apiClient = apiClient;
