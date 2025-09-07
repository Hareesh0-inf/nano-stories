/**
 * Image Gallery Component
 * Handles display and selection of generated images
 */
class ImageGallery {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.images = [];
        this.selectedImages = new Set();
        this.render();
        this.attachEventListeners();

        // Listen for image generation events
        window.addEventListener('imagesGenerated', (e) => this.displayImages(e.detail));
        window.addEventListener('projectReset', () => this.resetGallery());
    }

    render() {
        this.container.innerHTML = `
            <div class="image-gallery">
                <h2>Generated Images</h2>
                <p class="gallery-description">Review and select your favorite brand storytelling images. You can choose multiple images to save.</p>

                <div id="galleryPlaceholder" class="gallery-placeholder">
                    <div class="placeholder-content">
                        <div class="placeholder-icon">🖼️</div>
                        <h3>No Images Yet</h3>
                        <p>Complete your character, product, background, and story to generate your brand images.</p>
                    </div>
                </div>

                <div id="galleryContent" class="gallery-content" style="display: none;">
                    <div class="gallery-header">
                        <div class="selection-info">
                            <span id="selectedCount">0</span> of <span id="totalCount">0</span> selected
                        </div>
                        <div class="gallery-actions">
                            <button class="btn btn-secondary" onclick="imageGallery.selectAll()">Select All</button>
                            <button class="btn btn-secondary" onclick="imageGallery.clearSelection()">Clear Selection</button>
                            <button class="btn btn-primary" onclick="imageGallery.saveSelected()">Save Selected</button>
                        </div>
                    </div>

                    <div id="imagesGrid" class="images-grid">
                        <!-- Images will be dynamically added here -->
                    </div>

                    <div class="gallery-footer">
                        <div class="generation-info">
                            <p><strong>Generation Complete!</strong></p>
                            <p>Images generated using Nano Banana's fusion technology combining your character, product, background, and story.</p>
                        </div>
                        <div class="final-actions">
                            <button class="btn btn-success" onclick="imageGallery.finishProject()">Finish Project</button>
                            <button class="btn btn-secondary" onclick="imageGallery.generateMore()">Generate More Variations</button>
                        </div>
                    </div>
                </div>

                <div id="galleryStatus" class="status-message" style="display: none;"></div>
            </div>
        `;
    }

    attachEventListeners() {
        // Event listeners are handled through the render method
    }

    displayImages(imageData) {
        this.images = imageData.images || [];
        this.selectedImages.clear();

        const placeholder = document.getElementById('galleryPlaceholder');
        const content = document.getElementById('galleryContent');
        const imagesGrid = document.getElementById('imagesGrid');

        placeholder.style.display = 'none';
        content.style.display = 'block';

        // Update counts
        this.updateSelectionCount();

        // Clear existing images
        imagesGrid.innerHTML = '';

        // Add images to grid
        this.images.forEach((image, index) => {
            const imageCard = this.createImageCard(image, index);
            imagesGrid.appendChild(imageCard);
        });

        this.showStatus(`${this.images.length} images generated successfully!`, 'success');
    }

    createImageCard(image, index) {
        const card = document.createElement('div');
        card.className = 'image-card';
        card.dataset.index = index;

        // Construct full URL for backend images
        const displayUrl = window.apiClient.constructImageUrl(image.image_url);

        card.innerHTML = `
            <div class="image-container">
                <img src="${displayUrl}" alt="Generated Image ${index + 1}" loading="lazy">
                <div class="image-overlay">
                    <div class="image-info">
                        <h4>Fusion Style: ${image.fusion_style || 'Custom'}</h4>
                        <p>${image.prompt.substring(0, 100)}...</p>
                    </div>
                    <div class="image-actions">
                        <button class="select-btn" onclick="imageGallery.toggleSelection(${index})">
                            <span class="select-icon">✓</span>
                            Select
                        </button>
                        <button class="preview-btn" onclick="imageGallery.previewImage(${index})">
                            🔍 Preview
                        </button>
                    </div>
                </div>
                <div class="selection-indicator" style="display: none;">
                    <span class="checkmark">✓</span>
                </div>
            </div>
        `;

        // Add click handler for the entire card
        card.addEventListener('click', (e) => {
            if (!e.target.closest('.select-btn') && !e.target.closest('.preview-btn')) {
                this.toggleSelection(index);
            }
        });

        return card;
    }

    toggleSelection(index) {
        const card = document.querySelector(`.image-card[data-index="${index}"]`);
        const indicator = card.querySelector('.selection-indicator');

        if (this.selectedImages.has(index)) {
            this.selectedImages.delete(index);
            card.classList.remove('selected');
            indicator.style.display = 'none';
        } else {
            this.selectedImages.add(index);
            card.classList.add('selected');
            indicator.style.display = 'flex';
        }

        this.updateSelectionCount();
    }

    selectAll() {
        this.images.forEach((_, index) => {
            if (!this.selectedImages.has(index)) {
                this.toggleSelection(index);
            }
        });
    }

    clearSelection() {
        this.selectedImages.forEach(index => {
            this.toggleSelection(index);
        });
    }

    updateSelectionCount() {
        const selectedCount = document.getElementById('selectedCount');
        const totalCount = document.getElementById('totalCount');

        selectedCount.textContent = this.selectedImages.size;
        totalCount.textContent = this.images.length;
    }

    previewImage(index) {
        const image = this.images[index];
        if (!image) return;

        // Construct full URL for backend images
        const imageUrl = window.apiClient.constructImageUrl(image.image_url);

        // Create modal for image preview
        const modal = document.createElement('div');
        modal.className = 'image-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>Image Preview</h3>
                    <button class="close-btn" onclick="this.closest('.image-modal').remove()">×</button>
                </div>
                <div class="modal-body">
                    <img src="${imageUrl}" alt="Preview" style="max-width: 100%; max-height: 70vh;">
                    <div class="image-details">
                        <h4>Fusion Style: ${image.fusion_style || 'Custom'}</h4>
                        <p><strong>Prompt:</strong> ${image.prompt}</p>
                        <p><strong>Image ID:</strong> ${image.id}</p>
                    </div>
                </div>
            </div>
        `;

        // Add modal styles if not already present
        if (!document.querySelector('#modal-styles')) {
            const styles = document.createElement('style');
            styles.id = 'modal-styles';
            styles.textContent = `
                .image-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.8);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 1000;
                }
                .modal-content {
                    background: white;
                    border-radius: 8px;
                    max-width: 90%;
                    max-height: 90%;
                    overflow: auto;
                }
                .modal-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 20px;
                    border-bottom: 1px solid #eee;
                }
                .modal-body {
                    padding: 20px;
                    text-align: center;
                }
                .close-btn {
                    background: none;
                    border: none;
                    font-size: 24px;
                    cursor: pointer;
                }
            `;
            document.head.appendChild(styles);
        }

        document.body.appendChild(modal);

        // Close modal when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }

    async saveSelected() {
        if (this.selectedImages.size === 0) {
            this.showStatus('Please select at least one image to save.', 'error');
            return;
        }

        const selectedImageData = Array.from(this.selectedImages).map(index => this.images[index]);

        try {
            // Here you would typically save to a backend or download the images
            // For now, we'll simulate saving
            this.showStatus(`Successfully saved ${this.selectedImages.size} image(s)!`, 'success');

            // Trigger save event for other components
            window.dispatchEvent(new CustomEvent('imagesSaved', {
                detail: { savedImages: selectedImageData }
            }));

        } catch (error) {
            console.error('Error saving images:', error);
            this.showStatus('Error saving images. Please try again.', 'error');
        }
    }

    generateMore() {
        // Trigger event to generate more images
        window.dispatchEvent(new CustomEvent('generateMoreImages'));
        this.showStatus('Generating additional image variations...', 'info');
    }

    finishProject() {
        if (this.selectedImages.size === 0) {
            this.showStatus('Please select at least one image before finishing.', 'error');
            return;
        }

        // Show completion message
        this.showStatus('Project completed successfully! Your brand storytelling images are ready.', 'success');

        // Trigger project completion event
        window.dispatchEvent(new CustomEvent('projectCompleted', {
            detail: {
                selectedImages: Array.from(this.selectedImages).map(index => this.images[index]),
                totalImages: this.images.length
            }
        }));
    }

    resetGallery() {
        this.images = [];
        this.selectedImages.clear();

        const placeholder = document.getElementById('galleryPlaceholder');
        const content = document.getElementById('galleryContent');

        placeholder.style.display = 'block';
        content.style.display = 'none';

        document.getElementById('galleryStatus').style.display = 'none';
    }

    showStatus(message, type) {
        const statusDiv = document.getElementById('galleryStatus');
        statusDiv.textContent = message;
        statusDiv.className = `status-message ${type}`;
        statusDiv.style.display = 'block';

        if (type === 'success') {
            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 5000);
        }
    }

    getSelectedImages() {
        return Array.from(this.selectedImages).map(index => this.images[index]);
    }
}

// Export for use in other modules
window.ImageGallery = ImageGallery;
