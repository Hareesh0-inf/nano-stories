/**
 * Main Application Logic
 * Coordinates all components and manages the application workflow
 */
class BrandStorytellingApp {
    constructor() {
        this.components = {};
        this.currentStep = 0;
        this.workflowSteps = [
            'project',     // Step 0: Create project
            'character',   // Step 1: Generate character
            'product',     // Step 2: Upload product
            'background',  // Step 3: Generate background
            'story',       // Step 4: Write story
            'generate',    // Step 5: Generate final images
            'gallery'      // Step 6: Review and select images
        ];

        this.init();
    }

    async init() {
        console.log('Initializing Brand Storytelling App...');

        try {
            // Initialize all components
            await this.initializeComponents();

            // Set up event listeners
            this.setupEventListeners();

            // Initialize workflow
            this.updateWorkflowUI();

            console.log('App initialized successfully');
        } catch (error) {
            console.error('Error initializing app:', error);
            this.showGlobalError('Failed to initialize application. Please refresh the page.');
        }
    }

    async initializeComponents() {
        // Initialize form components
        this.components.projectForm = new ProjectForm('project-section');
        this.components.characterForm = new CharacterForm('character-section');
        this.components.productForm = new ProductForm('product-section');
        this.components.backgroundForm = new BackgroundForm('background-section');
        this.components.storyForm = new StoryForm('story-section');

        // Initialize image gallery
        this.components.imageGallery = new ImageGallery('gallery-section');

        // Store references globally for easy access
        window.projectForm = this.components.projectForm;
        window.characterForm = this.components.characterForm;
        window.productForm = this.components.productForm;
        window.backgroundForm = this.components.backgroundForm;
        window.storyForm = this.components.storyForm;
        window.imageGallery = this.components.imageGallery;
    }

    setupEventListeners() {
        // Project events
        window.addEventListener('projectCreated', (e) => this.handleProjectCreated(e));
        window.addEventListener('projectReset', () => this.handleProjectReset());

        // Component approval events
        window.addEventListener('characterApproved', () => this.advanceToStep(2));
        window.addEventListener('productApproved', () => this.advanceToStep(3));
        window.addEventListener('backgroundApproved', () => this.advanceToStep(4));
        window.addEventListener('storyApproved', (e) => this.handleStoryApproved(e));

        // Image generation events
        window.addEventListener('imagesGenerated', (e) => this.handleImagesGenerated(e));
        window.addEventListener('generateMoreImages', () => this.generateMoreImages());

        // Project completion
        window.addEventListener('projectCompleted', (e) => this.handleProjectCompleted(e));

        // Keyboard accessibility
        this.setupKeyboardAccessibility();
    }

    setupKeyboardAccessibility() {
        // Navigation keyboard support
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach((item, index) => {
            item.setAttribute('tabindex', '0');
            item.setAttribute('role', 'button');
            item.setAttribute('aria-label', `${this.workflowSteps[index]} step`);

            item.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.handleNavItemClick(index);
                }
            });

            item.addEventListener('click', () => this.handleNavItemClick(index));
        });

        // Skip link functionality
        const skipLink = document.querySelector('.skip-link');
        if (skipLink) {
            skipLink.addEventListener('click', (e) => {
                e.preventDefault();
                const mainContent = document.getElementById('main-content');
                if (mainContent) {
                    mainContent.focus();
                    mainContent.scrollIntoView();
                }
            });
        }

        // Global keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Alt + N: New project
            if (e.altKey && e.key === 'n') {
                e.preventDefault();
                this.handleProjectReset();
            }

            // Alt + Left/Right: Navigate between steps
            if (e.altKey && e.key === 'ArrowLeft') {
                e.preventDefault();
                this.navigateToPreviousStep();
            }

            if (e.altKey && e.key === 'ArrowRight') {
                e.preventDefault();
                this.navigateToNextStep();
            }

            // Escape: Close modals or return to current step
            if (e.key === 'Escape') {
                this.handleEscapeKey();
            }
        });

        // Form accessibility enhancements
        this.setupFormAccessibility();
    }

    setupFormAccessibility() {
        // Add ARIA labels and descriptions to form elements
        document.querySelectorAll('input, textarea, select').forEach(element => {
            const label = document.querySelector(`label[for="${element.id}"]`);
            if (label && !element.getAttribute('aria-labelledby')) {
                element.setAttribute('aria-labelledby', label.id || `label-${element.id}`);
                if (!label.id) {
                    label.id = `label-${element.id}`;
                }
            }

            // Add ARIA descriptions for help text
            const helpText = element.parentElement?.querySelector('.form-help');
            if (helpText && !element.getAttribute('aria-describedby')) {
                helpText.id = helpText.id || `help-${element.id}`;
                element.setAttribute('aria-describedby', helpText.id);
            }
        });

        // Button accessibility
        document.querySelectorAll('.btn').forEach(button => {
            if (!button.getAttribute('aria-label') && !button.textContent.trim()) {
                button.setAttribute('aria-label', 'Button');
            }
        });
    }

    handleNavItemClick(stepIndex) {
        if (this.isStepAvailable(stepIndex)) {
            this.advanceToStep(stepIndex);
        } else {
            // Announce to screen readers that step is not available
            const navItem = document.querySelectorAll('.nav-item')[stepIndex];
            if (navItem) {
                navItem.setAttribute('aria-label', `${this.workflowSteps[stepIndex]} step - not available yet`);
                setTimeout(() => {
                    navItem.setAttribute('aria-label', `${this.workflowSteps[stepIndex]} step`);
                }, 1000);
            }
        }
    }

    navigateToPreviousStep() {
        const prevStep = this.currentStep - 1;
        if (prevStep >= 0) {
            this.advanceToStep(prevStep);
        }
    }

    navigateToNextStep() {
        const nextStep = this.currentStep + 1;
        if (nextStep < this.workflowSteps.length && this.isStepAvailable(nextStep)) {
            this.advanceToStep(nextStep);
        }
    }

    handleEscapeKey() {
        // Close any open modals or overlays
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay && loadingOverlay.style.display !== 'none') {
            this.hideLoading();
            return;
        }

        const globalError = document.getElementById('globalError');
        if (globalError && globalError.style.display !== 'none') {
            globalError.style.display = 'none';
            return;
        }

        // Return focus to current navigation item
        const currentNavItem = document.querySelectorAll('.nav-item')[this.currentStep];
        if (currentNavItem) {
            currentNavItem.focus();
        }
    }

    handleProjectCreated(event) {
        console.log('Project created:', event.detail);
        this.advanceToStep(1);
        this.updateProgressIndicator();
    }

    handleProjectReset() {
        console.log('Project reset');
        this.currentStep = 0;
        this.updateWorkflowUI();
        this.updateProgressIndicator();
    }

    handleStoryApproved(event) {
        console.log('Story approved, ready for image generation');
        this.storyData = event.detail;
        this.advanceToStep(5);
        this.generateFinalImages();
    }

    async generateFinalImages() {
        try {
            this.showLoading('Generating your brand storytelling images...');

            const projectId = this.components.projectForm.getCurrentProjectId();

            const data = await window.apiClient.generateImages(projectId);

            this.hideLoading();
            this.advanceToStep(6);

            // Trigger images generated event
            window.dispatchEvent(new CustomEvent('imagesGenerated', {
                detail: data
            }));
        } catch (error) {
            console.error('Error generating images:', error);
            this.hideLoading();
            this.showGlobalError(`Failed to generate images: ${error.message}`);
        }
    }

    generateMoreImages() {
        // Regenerate images with potentially different parameters
        this.generateFinalImages();
    }

    handleImagesGenerated(event) {
        console.log('Images generated:', event.detail);
        this.updateProgressIndicator();
    }

    handleProjectCompleted(event) {
        console.log('Project completed:', event.detail);
        this.showCompletionMessage(event.detail);
    }

    advanceToStep(stepIndex) {
        if (stepIndex < 0 || stepIndex >= this.workflowSteps.length) {
            console.warn('Invalid step index:', stepIndex);
            return;
        }

        this.currentStep = stepIndex;
        this.updateWorkflowUI();
        this.updateProgressIndicator();
        this.scrollToCurrentStep();
    }

    updateWorkflowUI() {
        // Hide all sections
        document.querySelectorAll('.workflow-section').forEach(section => {
            section.style.display = 'none';
            section.setAttribute('aria-hidden', 'true');
        });

        // Show current section
        const currentSectionId = `${this.workflowSteps[this.currentStep]}-section`;
        const currentSection = document.getElementById(currentSectionId);
        if (currentSection) {
            currentSection.style.display = 'block';
            currentSection.setAttribute('aria-hidden', 'false');
        }

        // Update section navigation
        this.updateSectionNavigation();

        // Announce current step to screen readers
        this.announceCurrentStep();
    }

    updateSectionNavigation() {
        const navItems = document.querySelectorAll('.nav-item');

        navItems.forEach((item, index) => {
            item.classList.remove('active', 'completed', 'available');

            if (index === this.currentStep) {
                item.classList.add('active');
                item.setAttribute('aria-current', 'step');
            } else {
                item.removeAttribute('aria-current');
            }

            if (index < this.currentStep) {
                item.classList.add('completed');
                item.setAttribute('aria-label', `${this.workflowSteps[index]} step - completed`);
            } else if (this.isStepAvailable(index)) {
                item.classList.add('available');
                item.setAttribute('aria-label', `${this.workflowSteps[index]} step - available`);
            } else {
                item.setAttribute('aria-label', `${this.workflowSteps[index]} step - not available`);
            }
        });
    }

    announceCurrentStep() {
        const progressText = document.getElementById('progressText');
        if (progressText) {
            const announcement = `Current step: ${this.workflowSteps[this.currentStep]}. ${progressText.textContent}`;
            progressText.setAttribute('aria-live', 'polite');

            // Update the live region
            setTimeout(() => {
                progressText.textContent = announcement;
                setTimeout(() => {
                    const progress = ((this.currentStep + 1) / this.workflowSteps.length) * 100;
                    progressText.textContent = `${Math.round(progress)}% Complete`;
                }, 1000);
            }, 100);
        }
    }

    isStepAvailable(stepIndex) {
        // Define which steps are available based on completion of previous steps
        switch (stepIndex) {
            case 0: return true; // Project creation always available
            case 1: return this.currentStep >= 0; // Character after project
            case 2: return this.currentStep >= 1; // Product after character
            case 3: return this.currentStep >= 2; // Background after product
            case 4: return this.currentStep >= 3; // Story after background
            case 5: return this.currentStep >= 4; // Generate after story
            case 6: return this.currentStep >= 5; // Gallery after generation
            default: return false;
        }
    }

    updateProgressIndicator() {
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');

        if (progressBar && progressText) {
            const progress = ((this.currentStep + 1) / this.workflowSteps.length) * 100;
            progressBar.style.width = `${progress}%`;
            progressText.textContent = `${Math.round(progress)}% Complete`;
        }
    }

    scrollToCurrentStep() {
        const currentSection = document.getElementById(`${this.workflowSteps[this.currentStep]}-section`);
        if (currentSection) {
            currentSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }

    showLoading(message) {
        let loadingOverlay = document.getElementById('loadingOverlay');
        if (!loadingOverlay) {
            loadingOverlay = document.createElement('div');
            loadingOverlay.id = 'loadingOverlay';
            loadingOverlay.className = 'loading-overlay';
            loadingOverlay.innerHTML = `
                <div class="loading-content">
                    <div class="loading-spinner"></div>
                    <p id="loadingMessage">${message}</p>
                </div>
            `;
            document.body.appendChild(loadingOverlay);
        } else {
            document.getElementById('loadingMessage').textContent = message;
        }

        loadingOverlay.style.display = 'flex';
    }

    hideLoading() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }

    showGlobalError(message) {
        // Create or update error message
        let errorDiv = document.getElementById('globalError');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'globalError';
            errorDiv.className = 'global-error';
            document.body.insertBefore(errorDiv, document.body.firstChild);
        }

        errorDiv.innerHTML = `
            <div class="error-content">
                <span class="error-icon">⚠️</span>
                <span class="error-message">${message}</span>
                <button class="error-close" onclick="this.parentElement.parentElement.style.display='none'">×</button>
            </div>
        `;
        errorDiv.style.display = 'block';

        // Auto-hide after 10 seconds
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 10000);
    }

    showCompletionMessage(data) {
        const completionDiv = document.createElement('div');
        completionDiv.className = 'completion-message';
        completionDiv.innerHTML = `
            <div class="completion-content">
                <h2>🎉 Project Completed!</h2>
                <p>You've successfully created ${data.selectedImages.length} brand storytelling images.</p>
                <div class="completion-stats">
                    <div class="stat">
                        <span class="stat-number">${data.totalImages}</span>
                        <span class="stat-label">Total Generated</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">${data.selectedImages.length}</span>
                        <span class="stat-label">Selected</span>
                    </div>
                </div>
                <div class="completion-actions">
                    <button class="btn btn-primary" onclick="location.reload()">Start New Project</button>
                    <button class="btn btn-secondary" onclick="window.print()">Print Summary</button>
                </div>
            </div>
        `;

        document.body.appendChild(completionDiv);
    }

    // Utility methods
    getCurrentProjectId() {
        return this.components.projectForm?.getCurrentProjectId();
    }

    isStepCompleted(stepName) {
        const stepIndex = this.workflowSteps.indexOf(stepName);
        return this.currentStep > stepIndex;
    }

    canAdvanceToStep(stepName) {
        const stepIndex = this.workflowSteps.indexOf(stepName);
        return this.isStepAvailable(stepIndex);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new BrandStorytellingApp();
});

// Export for use in other modules
window.BrandStorytellingApp = BrandStorytellingApp;
