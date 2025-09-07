/**
 * Project Form Component
 * Handles project creation and management
 */
class ProjectForm {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentProjectId = null;
        this.render();
        this.attachEventListeners();
    }

    render() {
        this.container.innerHTML = `
            <div class="project-form">
                <h2>Create New Brand Story Project</h2>
                <form id="projectForm" class="form">
                    <div class="form-group">
                        <label for="projectName">Project Name</label>
                        <input
                            type="text"
                            id="projectName"
                            name="projectName"
                            placeholder="Enter your brand story project name"
                            required
                            maxlength="100"
                        >
                        <small class="form-help">Give your project a descriptive name that reflects your brand story</small>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary" id="createProjectBtn">
                            <span class="btn-text">Create Project</span>
                            <span class="btn-spinner" style="display: none;">Creating...</span>
                        </button>
                    </div>
                </form>

                <div id="projectStatus" class="status-message" style="display: none;"></div>

                <!-- Current Project Display -->
                <div id="currentProject" class="current-project" style="display: none;">
                    <h3>Current Project</h3>
                    <div class="project-info">
                        <p><strong>Name:</strong> <span id="currentProjectName"></span></p>
                        <p><strong>ID:</strong> <span id="currentProjectId"></span></p>
                        <p><strong>Created:</strong> <span id="currentProjectDate"></span></p>
                    </div>
                    <button class="btn btn-secondary" onclick="projectForm.resetProject()">Start New Project</button>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        const form = document.getElementById('projectForm');
        form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    async handleSubmit(event) {
        event.preventDefault();

        const projectName = document.getElementById('projectName').value.trim();
        if (!projectName) {
            this.showStatus('Please enter a project name', 'error');
            return;
        }

        this.setLoading(true);

        try {
            const data = await window.apiClient.createProject(projectName);

            this.currentProjectId = data.id;
            this.showProjectInfo(data);
            this.showStatus('Project created successfully!', 'success');

            // Trigger event for other components to know project was created
            window.dispatchEvent(new CustomEvent('projectCreated', {
                detail: { projectId: data.id, projectName: data.name }
            }));
        } catch (error) {
            console.error('Error creating project:', error);
            this.showStatus(`Error: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    setLoading(loading) {
        const btn = document.getElementById('createProjectBtn');
        const btnText = btn.querySelector('.btn-text');
        const btnSpinner = btn.querySelector('.btn-spinner');

        if (loading) {
            btn.disabled = true;
            btnText.style.display = 'none';
            btnSpinner.style.display = 'inline';
        } else {
            btn.disabled = false;
            btnText.style.display = 'inline';
            btnSpinner.style.display = 'none';
        }
    }

    showStatus(message, type) {
        const statusDiv = document.getElementById('projectStatus');
        statusDiv.textContent = message;
        statusDiv.className = `status-message ${type}`;
        statusDiv.style.display = 'block';

        // Auto-hide success messages after 5 seconds
        if (type === 'success') {
            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 5000);
        }
    }

    showProjectInfo(projectData) {
        const currentProjectDiv = document.getElementById('currentProject');
        const form = document.getElementById('projectForm');

        // Hide form, show project info
        form.style.display = 'none';
        currentProjectDiv.style.display = 'block';

        // Fill project info
        document.getElementById('currentProjectName').textContent = projectData.name;
        document.getElementById('currentProjectId').textContent = projectData.id;
        document.getElementById('currentProjectDate').textContent = new Date(projectData.created_at).toLocaleString();
    }

    resetProject() {
        this.currentProjectId = null;
        const form = document.getElementById('projectForm');
        const currentProjectDiv = document.getElementById('currentProject');
        const statusDiv = document.getElementById('projectStatus');

        // Reset form
        form.reset();
        form.style.display = 'block';
        currentProjectDiv.style.display = 'none';
        statusDiv.style.display = 'none';

        // Trigger event for other components
        window.dispatchEvent(new CustomEvent('projectReset'));
    }

    getCurrentProjectId() {
        return this.currentProjectId;
    }
}

// Export for use in other modules
window.ProjectForm = ProjectForm;
