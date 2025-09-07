/**
 * Product Upload Form Component
 * Handles product image uploads
 */
class ProductForm {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentProduct = null;
        this.render();
        this.attachEventListeners();

        // Listen for project events
        window.addEventListener('projectCreated', () => this.enableForm());
        window.addEventListener('projectReset', () => this.resetForm());
    }

    render() {
        this.container.innerHTML = `
            <div class="product-form">
                <h2>Product Image Upload</h2>
                <p class="form-description">Upload an image of your product that will be featured in your brand story.</p>

                <form id="productForm" class="form" style="display: none;">
                    <div class="form-group">
                        <label for="productImage">Product Image</label>
                        <div class="file-upload-area" id="fileUploadArea">
                            <div class="upload-placeholder">
                                <div class="upload-icon">📦</div>
                                <p>Click to select or drag and drop your product image</p>
                                <small>Supported formats: JPEG, PNG, WebP (Max: 10MB)</small>
                            </div>
                            <input
                                type="file"
                                id="productImage"
                                name="productImage"
                                accept="image/jpeg,image/png,image/webp"
                                required
                                style="display: none;"
                            >
                        </div>
                        <div id="fileInfo" class="file-info" style="display: none;">
                            <span id="fileName"></span>
                            <span id="fileSize"></span>
                            <button type="button" class="remove-file" onclick="productForm.removeFile()">×</button>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary" id="uploadProductBtn" disabled>
                            <span class="btn-text">Upload Product</span>
                            <span class="btn-spinner" style="display: none;">Uploading...</span>
                        </button>
                    </div>
                </form>

                <div id="productPlaceholder" class="placeholder-message">
                    <p>📦 Create a project first to upload your product image</p>
                </div>

                <div id="productStatus" class="status-message" style="display: none;"></div>

                <!-- Uploaded Product Display -->
                <div id="productResult" class="result-section" style="display: none;">
                    <h3>Uploaded Product</h3>
                    <div class="product-display">
                        <div class="image-container">
                            <img id="productImageDisplay" src="" alt="Uploaded Product" style="max-width: 300px; max-height: 300px;">
                        </div>
                        <div class="product-info">
                            <p><strong>Status:</strong> <span class="status-success">Uploaded successfully</span></p>
                            <p><strong>Uploaded:</strong> <span id="productUploadDate"></span></p>
                        </div>
                    </div>
                    <div class="result-actions">
                        <button class="btn btn-secondary" onclick="productForm.replaceProduct()">Replace Product</button>
                        <button class="btn btn-success" onclick="productForm.approveProduct()">Approve & Continue</button>
                    </div>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        const form = document.getElementById('productForm');
        form.addEventListener('submit', (e) => this.handleSubmit(e));

        // File upload area interactions
        const uploadArea = document.getElementById('fileUploadArea');
        const fileInput = document.getElementById('productImage');

        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
    }

    enableForm() {
        document.getElementById('productForm').style.display = 'block';
        document.getElementById('productPlaceholder').style.display = 'none';
    }

    resetForm() {
        document.getElementById('productForm').style.display = 'none';
        document.getElementById('productPlaceholder').style.display = 'block';
        document.getElementById('productResult').style.display = 'none';
        document.getElementById('productStatus').style.display = 'none';
        document.getElementById('fileInfo').style.display = 'none';
        document.getElementById('productForm').reset();
        this.currentProduct = null;
        this.selectedFile = null;
    }

    handleDragOver(event) {
        event.preventDefault();
        event.currentTarget.classList.add('drag-over');
    }

    handleDrop(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('drag-over');

        const files = event.dataTransfer.files;
        if (files.length > 0) {
            this.handleFile(files[0]);
        }
    }

    handleFileSelect(event) {
        const files = event.target.files;
        if (files.length > 0) {
            this.handleFile(files[0]);
        }
    }

    handleFile(file) {
        // Validate file type
        const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            this.showStatus('Please select a valid image file (JPEG, PNG, or WebP)', 'error');
            return;
        }

        // Validate file size (10MB max)
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            this.showStatus('File size must be less than 10MB', 'error');
            return;
        }

        this.selectedFile = file;
        this.showFileInfo(file);
        document.getElementById('uploadProductBtn').disabled = false;
    }

    showFileInfo(file) {
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');

        fileName.textContent = file.name;
        fileSize.textContent = `(${this.formatFileSize(file.size)})`;

        fileInfo.style.display = 'flex';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    removeFile() {
        this.selectedFile = null;
        document.getElementById('fileInfo').style.display = 'none';
        document.getElementById('productImage').value = '';
        document.getElementById('uploadProductBtn').disabled = true;
    }

    async handleSubmit(event) {
        event.preventDefault();

        if (!this.selectedFile) {
            this.showStatus('Please select a product image', 'error');
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
            const data = await window.apiClient.uploadProduct(projectId, this.selectedFile);

            this.currentProduct = {
                id: data.id,
                imageUrl: data.image_url || URL.createObjectURL(this.selectedFile), // Use API URL or local preview
                uploadDate: new Date().toLocaleString()
            };

            this.showProductResult();
            this.showStatus('Product uploaded successfully!', 'success');

            // Trigger event for other components
            window.dispatchEvent(new CustomEvent('productUploaded', {
                detail: this.currentProduct
            }));
        } catch (error) {
            console.error('Error uploading product:', error);
            this.showStatus(`Error: ${error.message}`, 'error');
        } finally {
            this.setLoading(false);
        }
    }

    setLoading(loading) {
        const btn = document.getElementById('uploadProductBtn');
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
        const statusDiv = document.getElementById('productStatus');
        statusDiv.textContent = message;
        statusDiv.className = `status-message ${type}`;
        statusDiv.style.display = 'block';

        if (type === 'success') {
            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 5000);
        }
    }

    showProductResult() {
        const resultDiv = document.getElementById('productResult');
        resultDiv.style.display = 'block';

        // Construct full URL for backend images
        const imageUrl = window.apiClient.constructImageUrl(this.currentProduct.imageUrl);

        document.getElementById('productImageDisplay').src = imageUrl;
        document.getElementById('productUploadDate').textContent = this.currentProduct.uploadDate;
    }

    replaceProduct() {
        document.getElementById('productResult').style.display = 'none';
        this.currentProduct = null;
        this.removeFile();
    }

    approveProduct() {
        this.showStatus('Product approved! You can now set up your background.', 'success');

        // Trigger event for workflow progression
        window.dispatchEvent(new CustomEvent('productApproved', {
            detail: this.currentProduct
        }));
    }

    getCurrentProduct() {
        return this.currentProduct;
    }
}

// Export for use in other modules
window.ProductForm = ProductForm;
