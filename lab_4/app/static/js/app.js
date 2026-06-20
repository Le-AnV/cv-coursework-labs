/**
 * Wavelet Image Retrieval - JavaScript
 * Handles UI interactions and API communication
 */

// Global state
let selectedFile = null;

// DOM Elements
const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const fileInputBtn = document.getElementById("fileInputBtn");
const previewSection = document.getElementById("previewSection");
const previewImage = document.getElementById("previewImage");
const previewFilename = document.getElementById("previewFilename");
const actionButtons = document.getElementById("actionButtons");
const searchBtn = document.getElementById("searchBtn");
const cancelBtn = document.getElementById("cancelBtn");
const removeFileBtn = document.getElementById("removeFileBtn");
const loadingSpinner = document.getElementById("loadingSpinner");
const resultsSection = document.getElementById("resultsSection");
const resultsGrid = document.getElementById("resultsGrid");
const errorSection = document.getElementById("errorSection");
const errorMessage = document.getElementById("errorMessage");
const newSearchBtn = document.getElementById("newSearchBtn");

// Event Listeners
document.addEventListener("DOMContentLoaded", initializeEventListeners);

function initializeEventListeners() {
  // File input click
  fileInputBtn.addEventListener("click", () => fileInput.click());

  // File input change
  fileInput.addEventListener("change", handleFileSelect);

  // Drag and drop
  uploadArea.addEventListener("dragover", handleDragOver);
  uploadArea.addEventListener("dragleave", handleDragLeave);
  uploadArea.addEventListener("drop", handleDrop);
  uploadArea.addEventListener("click", () => fileInput.click());

  // Action buttons
  searchBtn.addEventListener("click", performSearch);
  cancelBtn.addEventListener("click", resetForm);
  removeFileBtn.addEventListener("click", resetForm);
  newSearchBtn.addEventListener("click", resetForm);
}

/**
 * Handle file selection
 */
function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) {
    processFile(file);
  }
}

/**
 * Handle drag over
 */
function handleDragOver(e) {
  e.preventDefault();
  e.stopPropagation();
  uploadArea.classList.add("dragover");
}

/**
 * Handle drag leave
 */
function handleDragLeave(e) {
  e.preventDefault();
  e.stopPropagation();
  uploadArea.classList.remove("dragover");
}

/**
 * Handle drop
 */
function handleDrop(e) {
  e.preventDefault();
  e.stopPropagation();
  uploadArea.classList.remove("dragover");

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    const file = files[0];
    if (isValidFile(file)) {
      processFile(file);
    } else {
      showError(
        `File type not supported. Please use: JPG, JPEG, PNG, BMP, or TIFF`,
      );
    }
  }
}

/**
 * Check if file is valid
 */
function isValidFile(file) {
  const allowedExtensions = ["jpg", "jpeg", "png", "bmp", "tiff", "tif"];
  const fileExtension = file.name.split(".").pop().toLowerCase();
  const maxSize = 10 * 1024 * 1024; // 10MB

  if (!allowedExtensions.includes(fileExtension)) {
    return false;
  }

  if (file.size > maxSize) {
    showError(`File size exceeds 10 MB. Please select a smaller file.`);
    return false;
  }

  return true;
}

/**
 * Process selected file
 */
function processFile(file) {
  if (!isValidFile(file)) {
    showError(
      `File type not supported. Please use: JPG, JPEG, PNG, BMP, or TIFF`,
    );
    return;
  }

  selectedFile = file;

  // Show preview
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.src = e.target.result;
    previewFilename.textContent = file.name;
    document.getElementById("infoFilename").textContent = file.name;
    document.getElementById("infoFileSize").textContent = formatFileSize(
      file.size,
    );
  };
  reader.readAsDataURL(file);

  // Show preview section and action buttons
  uploadArea.style.display = "none";
  previewSection.style.display = "block";
  actionButtons.style.display = "flex";

  // Hide error and results sections
  errorSection.style.display = "none";
  resultsSection.style.display = "none";
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
}

/**
 * Perform search
 */
async function performSearch() {
  if (!selectedFile) {
    showError("Please select a file first");
    return;
  }

  // Show loading spinner
  actionButtons.style.display = "none";
  loadingSpinner.style.display = "block";
  errorSection.style.display = "none";
  resultsSection.style.display = "none";

  try {
    // Create form data
    const formData = new FormData();
    formData.append("file", selectedFile);

    // Send request
    const response = await fetch("/api/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unknown error occurred");
    }

    // Display results
    displayResults(data);
  } catch (error) {
    console.error("Search error:", error);
    showError(error.message || "Failed to search. Please try again.");
  } finally {
    loadingSpinner.style.display = "none";
  }
}

/**
 * Display search results
 */
function displayResults(data) {
  // Display query image
  document.getElementById("resultQueryImage").src = data.query_image.path;
  document.getElementById("resultFilename").textContent =
    data.query_image.filename;
  document.getElementById("resultHashLength").textContent =
    data.query_image.hash_length;

  // Display results grid
  resultsGrid.innerHTML = "";

  if (data.results.length === 0) {
    resultsGrid.innerHTML = `
            <div class="col-12">
                <div class="alert alert-info" role="alert">
                    <h4 class="alert-heading">No Results</h4>
                    <p>No similar images were found in the dataset.</p>
                </div>
            </div>
        `;
  } else {
    data.results.forEach((result, index) => {
      const card = createResultCard(result);
      resultsGrid.innerHTML += card;
    });
  }

  // Show results section
  resultsSection.style.display = "block";

  // Scroll to results
  setTimeout(() => {
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 100);
}

/**
 * Create result card HTML
 */
function createResultCard(result) {
  const similarityPercentage = parseFloat(result.similarity);
  const hamming = result.hamming_distance;
  const totalBits = result.total_bits;
  const imageUrl =
    result.image_url || `/api/image/${encodeURIComponent(result.path)}`;

  return `
        <div class="col-lg-6 col-xl-5">
            <div class="result-card">
                <img src="${imageUrl}" 
                     alt="${result.name}" 
                     class="result-card-image" 
                     onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%22 height=%22100%22%3E%3Crect fill=%22%23ddd%22 width=%22100%22 height=%22100%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22 font-family=%22sans-serif%22 font-size=%2214%22 fill=%22%23999%22%3EImage not found%3C/text%3E%3C/svg%3E'">
                <div class="result-card-body">
                    <span class="result-rank">Rank #${result.rank}</span>
                    <p class="result-name" title="${result.name}">${result.name}</p>
                    <div class="result-metrics">
                        <div class="metric">
                            <span class="metric-label">Hamming Distance:</span>
                            <span class="metric-value">${hamming}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Similarity:</span>
                            <span class="metric-value">${similarityPercentage}%</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Hash Bits:</span>
                            <span class="metric-value">${totalBits}</span>
                        </div>
                        <div class="similarity-bar">
                            <div class="similarity-fill" style="width: ${Math.max(0, Math.min(100, similarityPercentage))}%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Reset form to initial state
 */
function resetForm() {
  selectedFile = null;
  fileInput.value = "";

  // Reset visibility
  uploadArea.style.display = "block";
  previewSection.style.display = "none";
  actionButtons.style.display = "none";
  loadingSpinner.style.display = "none";
  errorSection.style.display = "none";
  resultsSection.style.display = "none";

  // Scroll to top
  setTimeout(() => {
    uploadArea.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 100);
}

/**
 * Show error message
 */
function showError(message) {
  errorMessage.textContent = message;
  errorSection.style.display = "block";

  // Auto-hide after 10 seconds
  setTimeout(() => {
    errorSection.style.display = "none";
  }, 10000);
}

/**
 * Format percentage
 */
function formatPercentage(value) {
  return Math.round(value * 100) / 100;
}
