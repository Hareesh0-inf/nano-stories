/**
 * Story Input Form Component
 * Handles brand story text input and submission
 */
class StoryForm {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentStory = null;
        this.render();
        this.attachEventListeners();

        // Listen for project events
        window.addEventListener('projectCreated', () => this.enableForm());
        window.addEventListener('projectReset', () => this.resetForm());
    }

    render() {
        this.container.innerHTML = `
            <div class="story-form">
                <h2>Brand Story</h2>
                <p class="form-description">Write the compelling narrative that will bring your character, product, and background together into a cohesive brand story.</p>

                <form id="storyForm" class="form" style="display: none;">
                    <div class="form-group">
                        <label for="storyText">Story Narrative</label>
                        <textarea
                            id="storyText"
                            name="storyText"
                            placeholder="Tell your brand story... What is the journey? What makes your product special? How does your character embody your brand values?"
                            required
                            rows="8"
                            maxlength="2000"
                        ></textarea>
                        <div class="character-count">
                            <span id="charCount">0</span>/2000 characters
                        </div>
                        <small class="form-help">Write a compelling narrative that connects your character, product, and brand message</small>
                    </div>

                    <div class="story-examples">
                        <h4>Story Writing Tips:</h4>
                        <ul>
                            <li><strong>Hook:</strong> Start with what makes your brand unique</li>
                            <li><strong>Character:</strong> Show how your character represents your brand values</li>
                            <li><strong>Challenge:</strong> Present the problem your product solves</li>
                            <li><strong>Solution:</strong> Demonstrate how your product delivers value</li>
                            <li><strong>Call to Action:</strong> End with what you want customers to do</li>
                        </ul>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary" id="saveStoryBtn">
                            <span class="btn-text">Save Story</span>
                            <span class="btn-spinner" style="display: none;">Saving...</span>
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="storyForm.clearStory()">Clear</button>
                    </div>
                </form>

                <div id="storyPlaceholder" class="placeholder-message">
                    <p>📖 Create a project first to write your brand story</p>
                </div>

                <div id="storyStatus" class="status-message" style="display: none;"></div>

                <!-- Story Display -->
                <div id="storyResult" class="result-section" style="display: none;">
                    <h3>Your Brand Story</h3>
                    <div class="story-display">
                        <div class="story-content">
                            <p id="storyTextDisplay"></p>
                        </div>
                        <div class="story-meta">
                            <p><strong>Status:</strong> <span class="status-success">Saved successfully</span></p>
                            <p><strong>Length:</strong> <span id="storyLength"></span> characters</p>
                            <p><strong>Saved:</strong> <span id="storySaveDate"></span></p>
                        </div>
                    </div>
                    <div class="result-actions">
                        <button class="btn btn-secondary" onclick="storyForm.editStory()">Edit Story</button>
                        <button class="btn btn-success" onclick="storyForm.approveStory()">Approve & Generate Final Images</button>
                    </div>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        const form = document.getElementById('storyForm');
        form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Character counter
        const storyText = document.getElementById('storyText');
        storyText.addEventListener('input', () => this.updateCharCount());
    }

    enableForm() {
        document.getElementById('storyForm').style.display = 'block';
        document.getElementById('storyPlaceholder').style.display = 'none';
    }

    resetForm() {
        document.getElementById('storyForm').style.display = 'none';
        document.getElementById('storyPlaceholder').style.display = 'block';
        document.getElementById('storyResult').style.display = 'none';
        document.getElementById('storyStatus').style.display = 'none';
        document.getElementById('storyForm').reset();
        this.currentStory = null;
        this.updateCharCount();
    }

    updateCharCount() {
        const storyText = document.getElementById('storyText');
        const charCount = document.getElementById('charCount');
        const count = storyText.value.length;

        charCount.textContent = count;

        // Change color based on length
        if (count > 1800) {
            charCount.style.color = '#e74c3c'; // Red for near limit
        } else if (count > 1500) {
            charCount.style.color = '#f39c12'; // Orange for getting close
        } else {
            charCount.style.color = '#666'; // Normal color
        }
    }

    async handleSubmit(event) {
        event.preventDefault();

        const storyText = document.getElementById('storyText').value.trim();

        if (!storyText) {
            this.showStatus('Please write your brand story', 'error');
            return;
        }

        if (storyText.length < 50) {
            this.showStatus('Please write a more detailed story (at least 50 characters)', 'error');
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
            const data = await window.apiClient.createStory(projectId, {
                story_text: storyText
            });

            this.currentStory = {
                id: data.id,
                text: storyText,
                length: storyText.length,
                saveDate: new Date().toLocaleString()
            };

            this.showStoryResult();
            this.showStatus('Story saved successfully!', 'success');

            // Trigger event for other components
            window.dispatchEvent(new CustomEvent('storyCreated', {
                detail: this.currentStory
            }));
        } catch (error) {
            console.error('Error saving story:', error);
            this.showStatus(`Error: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    setLoading(loading) {
        const btn = document.getElementById('saveStoryBtn');
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
        const statusDiv = document.getElementById('storyStatus');
        statusDiv.textContent = message;
        statusDiv.className = `status-message ${type}`;
        statusDiv.style.display = 'block';

        if (type === 'success') {
            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 5000);
        }
    }

    showStoryResult() {
        const resultDiv = document.getElementById('storyResult');
        resultDiv.style.display = 'block';

        document.getElementById('storyTextDisplay').textContent = this.currentStory.text;
        document.getElementById('storyLength').textContent = this.currentStory.length;
        document.getElementById('storySaveDate').textContent = this.currentStory.saveDate;
    }

    editStory() {
        // Hide result and show form for editing
        document.getElementById('storyResult').style.display = 'none';
        document.getElementById('storyText').value = this.currentStory.text;
        this.updateCharCount();
        // Form remains visible for editing
    }

    clearStory() {
        document.getElementById('storyText').value = '';
        this.updateCharCount();
        this.currentStory = null;
        document.getElementById('storyResult').style.display = 'none';
    }

    approveStory() {
        // Check if all required components are ready
        const projectForm = window.projectForm;
        const characterForm = window.characterForm;
        const productForm = window.productForm;
        const backgroundForm = window.backgroundForm;

        const missingComponents = [];

        if (!projectForm || !projectForm.getCurrentProjectId()) {
            missingComponents.push('Project');
        }
        if (!characterForm || !characterForm.getCurrentCharacter()) {
            missingComponents.push('Character');
        }
        if (!productForm || !productForm.getCurrentProduct()) {
            missingComponents.push('Product');
        }
        if (!backgroundForm || !backgroundForm.getCurrentBackground()) {
            missingComponents.push('Background');
        }

        if (missingComponents.length > 0) {
            this.showStatus(`Please complete the following first: ${missingComponents.join(', ')}`, 'error');
            return;
        }

        this.showStatus('Story approved! Ready to generate final images.', 'success');

        // Trigger event for final image generation
        window.dispatchEvent(new CustomEvent('storyApproved', {
            detail: {
                story: this.currentStory,
                projectId: projectForm.getCurrentProjectId(),
                character: characterForm.getCurrentCharacter(),
                product: productForm.getCurrentProduct(),
                background: backgroundForm.getCurrentBackground()
            }
        }));
    }

    getCurrentStory() {
        return this.currentStory;
    }
}

// Export for use in other modules
window.StoryForm = StoryForm;
