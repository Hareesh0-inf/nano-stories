/* Nano Stories Frontend Application */

// API base URL
const API_BASE = 'http://127.0.0.1:8000';

// Current project ID
let currentProjectId = null;

// DOM elements
const projectForm = document.getElementById('project-form');
const characterForm = document.getElementById('character-form');
const projectSection = document.getElementById('project-section');
const characterSection = document.getElementById('character-section');

// Initialize the application
function init() {
    setupEventListeners();
}

// Setup event listeners
function setupEventListeners() {
    projectForm.addEventListener('submit', handleProjectSubmit);
    characterForm.addEventListener('submit', handleCharacterSubmit);
}

// Handle project creation
async function handleProjectSubmit(event) {
    event.preventDefault();
    
    const projectName = document.getElementById('project-name').value;
    
    try {
        const response = await fetch(`${API_BASE}/projects`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: projectName }),
        });
        
        if (response.ok) {
            const project = await response.json();
            currentProjectId = project.id;
            showCharacterSection();
        } else {
            alert('Failed to create project');
        }
    } catch (error) {
        console.error('Error creating project:', error);
        alert('Error creating project');
    }
}

// Handle character generation
async function handleCharacterSubmit(event) {
    event.preventDefault();
    
    const details = document.getElementById('character-details').value;
    const personality = document.getElementById('character-personality').value;
    
    try {
        const response = await fetch(`${API_BASE}/projects/${currentProjectId}/character`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ details, personality }),
        });
        
        if (response.ok) {
            const character = await response.json();
            // Handle character response
            console.log('Character generated:', character);
        } else {
            alert('Failed to generate character');
        }
    } catch (error) {
        console.error('Error generating character:', error);
        alert('Error generating character');
    }
}

// Show character section
function showCharacterSection() {
    projectSection.style.display = 'none';
    characterSection.style.display = 'block';
}

// Initialize on load
document.addEventListener('DOMContentLoaded', init);
