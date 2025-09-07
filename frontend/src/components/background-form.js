/**
 * Background Input Form Component
 * Handles background scene creation and image generation
 */
class BackgroundForm {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentBackground = null;
        this.render();
        this.attachEventListeners();

        // Listen for project events
        window.addEventListener('projectCreated', () => this.enableForm());
        window.addEventListener('projectReset', () => this.resetForm());
    }

    render() {
        this.container.innerHTML = `
            <div class="background-form">
                <h2>Background Scene</h2>
                <p class="form-description">Define the setting and atmosphere for your brand story. This will create the perfect backdrop for your character and product.</p>

                <form id="backgroundForm" class="form" style="display: none;">
                    <div class="form-group">
                        <label for="sceneDetails">Scene Description</label>
                        <textarea
                            id="sceneDetails"
                            name="sceneDetails"
                            placeholder="Describe the scene and setting (e.g., modern office, outdoor marketplace, elegant showroom)"
                            required
                            rows="4"
                            maxlength="500"
                        ></textarea>
                        <small class="form-help">Be descriptive about the location, time of day, and overall atmosphere</small>
                    </div>

                    <div class="form-group">
                        <label for="lighting">Lighting & Mood</label>
                        <select id="lighting" name="lighting">
                            <option value="">Select lighting (optional)</option>
                            <option value="natural daylight">Natural Daylight</option>
                            <option value="warm indoor">Warm Indoor Lighting</option>
                            <option value="dramatic">Dramatic & Moody</option>
                            <option value="bright and airy">Bright & Airy</option>
                            <option value="golden hour">Golden Hour</option>
                            <option value="studio lighting">Professional Studio</option>
                            <option value="urban night">Urban Night Scene</option>
                        </select>
                        <small class="form-help">Choose lighting that enhances your brand's mood and message</small>
                    </div>

                    <div class="form-group">
                        <label>Style Preferences</label>
                        <div class="checkbox-group">
                            <label class="checkbox-label">
                                <input type="checkbox" id="photorealistic" name="photorealistic" checked>
                                Photorealistic
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" id="professional" name="professional" checked>
                                Professional Quality
                            </label>
                            <label class="checkbox-label">
                                <input type="checkbox" id="brandAppropriate" name="brandAppropriate" checked>
                                Brand Appropriate
                            </label>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary" id="generateBackgroundBtn">
                            <span class="btn-text">Generate Background</span>
                            <span class="btn-spinner" style="display: none;">Generating...</span>
                        </button>
                    </div>
                </form>

                <div id="backgroundPlaceholder" class="placeholder-message">
                    <p>🎨 Create a project first to design your background scene</p>
                </div>

                <div id="backgroundStatus" class="status-message" style="display: none;"></div>

                <!-- Generated Background Display -->
                <div id="backgroundResult" class="result-section" style="display: none;">
                    <h3>Generated Background</h3>
                    <div class="background-display">
                        <div class="image-container">
                            <img id="backgroundImage" src="" alt="Generated Background" style="max-width: 400px; max-height: 300px;">
                        </div>
                        <div class="background-info">
                            <p><strong>Scene:</strong> <span id="backgroundSceneDisplay"></span></p>
                            <p><strong>Lighting:</strong> <span id="backgroundLightingDisplay"></span></p>
                            <p><strong>Style:</strong> <span id="backgroundStyleDisplay"></span></p>
                        </div>
                    </div>
                    <div class="result-actions">
                        <button class="btn btn-secondary" onclick="backgroundForm.regenerateBackground()">Regenerate</button>
                        <button class="btn btn-success" onclick="backgroundForm.approveBackground()">Approve & Continue</button>
                    </div>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        const form = document.getElementById('backgroundForm');
        form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    enableForm() {
        document.getElementById('backgroundForm').style.display = 'block';
        document.getElementById('backgroundPlaceholder').style.display = 'none';
    }

    resetForm() {
        document.getElementById('backgroundForm').style.display = 'none';
        document.getElementById('backgroundPlaceholder').style.display = 'block';
        document.getElementById('backgroundResult').style.display = 'none';
        document.getElementById('backgroundStatus').style.display = 'none';
        document.getElementById('backgroundForm').reset();
        this.currentBackground = null;
    }

    async handleSubmit(event) {
        event.preventDefault();

        const sceneDetails = document.getElementById('sceneDetails').value.trim();
        const lighting = document.getElementById('lighting').value;

        if (!sceneDetails) {
            this.showStatus('Please provide scene details', 'error');
            return;
        }

        // Get project ID from project form
        const projectForm = window.projectForm;
        if (!projectForm || !projectForm.getCurrentProjectId()) {
            this.showStatus('Please create a project first', 'error');
            return;
        }

        const projectId = projectForm.getCurrentProjectId();
        this.setLoading(true);

        try {
            const data = await window.apiClient.createBackground(projectId, {
                scene_details: sceneDetails,
                lighting: lighting || undefined
            });

            // Collect style preferences
            const styles = [];
            if (document.getElementById('photorealistic').checked) styles.push('Photorealistic');
            if (document.getElementById('professional').checked) styles.push('Professional');
            if (document.getElementById('brandAppropriate').checked) styles.push('Brand Appropriate');

            this.currentBackground = {
                id: data.id,
                imageUrl: data.image_url,
                sceneDetails: sceneDetails,
                lighting: lighting,
                styles: styles.join(', ')
            };

            this.showBackgroundResult();
            this.showStatus('Background generated successfully!', 'success');

            // Trigger event for other components
            window.dispatchEvent(new CustomEvent('backgroundCreated', {
                detail: this.currentBackground
            }));
        } catch (error) {
            console.error('Error generating background:', error);
            this.showStatus(`Error: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    setLoading(loading) {
        const btn = document.getElementById('generateBackgroundBtn');
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
        const statusDiv = document.getElementById('backgroundStatus');
        statusDiv.textContent = message;
        statusDiv.className = `status-message ${type}`;
        statusDiv.style.display = 'block';

        if (type === 'success') {
            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 5000);
        }
    }

    showBackgroundResult() {
        const resultDiv = document.getElementById('backgroundResult');
        resultDiv.style.display = 'block';

        // Construct full URL for backend images
        const imageUrl = window.apiClient.constructImageUrl(this.currentBackground.imageUrl);

        document.getElementById('backgroundImage').src = imageUrl;
        document.getElementById('backgroundSceneDisplay').textContent = this.currentBackground.sceneDetails;
        document.getElementById('backgroundLightingDisplay').textContent =
            this.currentBackground.lighting || 'Not specified';
        document.getElementById('backgroundStyleDisplay').textContent = this.currentBackground.styles;
    }

    regenerateBackground() {
        // Reset the result and allow regeneration
        document.getElementById('backgroundResult').style.display = 'none';
        this.currentBackground = null;
        // Form remains filled, user can submit again
    }

    approveBackground() {
        // Mark background as approved and move to next step
        this.showStatus('Background approved! You can now write your story.', 'success');

        // Trigger event for workflow progression
        window.dispatchEvent(new CustomEvent('backgroundApproved', {
            detail: this.currentBackground
        }));
    }

    getCurrentBackground() {
        return this.currentBackground;
    }
}

// Export for use in other modules
window.BackgroundForm = BackgroundForm;
