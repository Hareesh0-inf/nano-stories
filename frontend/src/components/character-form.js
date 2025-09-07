/**
 * Character Input Form Component
 * Handles character creation and image generation
 */
class CharacterForm {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentCharacter = null;
        this.render();
        this.attachEventListeners();

        // Listen for project events
        window.addEventListener('projectCreated', () => this.enableForm());
        window.addEventListener('projectReset', () => this.resetForm());
    }

    render() {
        this.container.innerHTML = `
            <div class="character-form">
                <h2>Character Creation</h2>
                <p class="form-description">Define the main character for your brand story. This will be used to generate a representative image.</p>

                <form id="characterForm" class="form" style="display: none;">
                    <div class="form-group">
                        <label for="characterDetails">Character Details</label>
                        <textarea
                            id="characterDetails"
                            name="characterDetails"
                            placeholder="Describe your character in detail (e.g., age, appearance, role, clothing style)"
                            required
                            rows="4"
                            maxlength="500"
                        ></textarea>
                        <small class="form-help">Be specific about physical appearance, clothing, and role in your brand story</small>
                    </div>

                    <div class="form-group">
                        <label for="characterPersonality">Personality & Style</label>
                        <select id="characterPersonality" name="characterPersonality">
                            <option value="">Select personality (optional)</option>
                            <option value="professional">Professional & Corporate</option>
                            <option value="approachable">Warm & Approachable</option>
                            <option value="confident">Confident & Authoritative</option>
                            <option value="innovative">Innovative & Creative</option>
                            <option value="trustworthy">Trustworthy & Reliable</option>
                            <option value="youthful">Youthful & Energetic</option>
                            <option value="sophisticated">Sophisticated & Elegant</option>
                        </select>
                        <small class="form-help">Choose a personality that matches your brand's voice</small>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary" id="generateCharacterBtn">
                            <span class="btn-text">Generate Character Image</span>
                            <span class="btn-spinner" style="display: none;">Generating...</span>
                        </button>
                    </div>
                </form>

                <div id="characterPlaceholder" class="placeholder-message">
                    <p>👤 Create a project first to start building your character</p>
                </div>

                <div id="characterStatus" class="status-message" style="display: none;"></div>

                <!-- Generated Character Display -->
                <div id="characterResult" class="result-section" style="display: none;">
                    <h3>Generated Character</h3>
                    <div class="character-display">
                        <div class="image-container">
                            <img id="characterImage" src="" alt="Generated Character" style="max-width: 300px; max-height: 300px;">
                        </div>
                        <div class="character-info">
                            <p><strong>Details:</strong> <span id="characterDetailsDisplay"></span></p>
                            <p><strong>Personality:</strong> <span id="characterPersonalityDisplay"></span></p>
                        </div>
                    </div>
                    <div class="result-actions">
                        <button class="btn btn-secondary" onclick="characterForm.regenerateCharacter()">Regenerate</button>
                        <button class="btn btn-success" onclick="characterForm.approveCharacter()">Approve & Continue</button>
                    </div>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        const form = document.getElementById('characterForm');
        form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    enableForm() {
        document.getElementById('characterForm').style.display = 'block';
        document.getElementById('characterPlaceholder').style.display = 'none';
    }

    resetForm() {
        document.getElementById('characterForm').style.display = 'none';
        document.getElementById('characterPlaceholder').style.display = 'block';
        document.getElementById('characterResult').style.display = 'none';
        document.getElementById('characterStatus').style.display = 'none';
        document.getElementById('characterForm').reset();
        this.currentCharacter = null;
    }

    async handleSubmit(event) {
        event.preventDefault();

        const details = document.getElementById('characterDetails').value.trim();
        const personality = document.getElementById('characterPersonality').value;

        if (!details) {
            this.showStatus('Please provide character details', 'error');
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
            const data = await window.apiClient.createCharacter(projectId, {
                details: details,
                personality: personality || undefined
            });

            this.currentCharacter = {
                id: data.id,
                imageUrl: data.image_url,
                details: details,
                personality: personality
            };

            this.showCharacterResult();
            this.showStatus('Character generated successfully!', 'success');

            // Trigger event for other components
            window.dispatchEvent(new CustomEvent('characterCreated', {
                detail: this.currentCharacter
            }));
        } catch (error) {
            console.error('Error generating character:', error);
            this.showStatus(`Error: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    setLoading(loading) {
        const btn = document.getElementById('generateCharacterBtn');
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
        const statusDiv = document.getElementById('characterStatus');
        statusDiv.textContent = message;
        statusDiv.className = `status-message ${type}`;
        statusDiv.style.display = 'block';

        if (type === 'success') {
            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 5000);
        }
    }

    showCharacterResult() {
        const resultDiv = document.getElementById('characterResult');
        resultDiv.style.display = 'block';

        // Construct full URL for backend images
        const imageUrl = window.apiClient.constructImageUrl(this.currentCharacter.imageUrl);

        document.getElementById('characterImage').src = imageUrl;
        document.getElementById('characterDetailsDisplay').textContent = this.currentCharacter.details;
        document.getElementById('characterPersonalityDisplay').textContent =
            this.currentCharacter.personality || 'Not specified';
    }

    regenerateCharacter() {
        // Reset the result and allow regeneration
        document.getElementById('characterResult').style.display = 'none';
        this.currentCharacter = null;
        // Form remains filled, user can submit again
    }

    approveCharacter() {
        // Mark character as approved and move to next step
        this.showStatus('Character approved! You can now add your product.', 'success');

        // Trigger event for workflow progression
        window.dispatchEvent(new CustomEvent('characterApproved', {
            detail: this.currentCharacter
        }));
    }

    getCurrentCharacter() {
        return this.currentCharacter;
    }
}

// Export for use in other modules
window.CharacterForm = CharacterForm;
