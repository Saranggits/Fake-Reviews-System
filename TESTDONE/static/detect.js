document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('detectForm');
    const loadingSpinner = document.querySelector('.loading-spinner');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading spinner
        if (loadingSpinner) {
            loadingSpinner.style.display = 'block';
        }
        
        // Get form data
        const urlInput = document.getElementById('urlInput').value.trim();
        const reviewInput = document.getElementById('reviewInput').value.trim();
        
        if (!urlInput && !reviewInput) {
            showError('Please enter either a URL or a review text');
            return;
        }
        
        try {
            // Store the input values in sessionStorage
            sessionStorage.setItem('submittedURL', urlInput);
            sessionStorage.setItem('submittedReview', reviewInput);
            
            // Submit the form
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: urlInput,
                    review_text: reviewInput
                })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            // Redirect to results page
            window.location.href = '/result';
            
        } catch (error) {
            console.error('Error:', error);
            showError('An error occurred while analyzing');
        } finally {
            // Hide loading spinner
            if (loadingSpinner) {
                loadingSpinner.style.display = 'none';
            }
        }
    });
});

function showError(message) {
    const resultsOutput = document.getElementById('resultsOutput');
    if (resultsOutput) {
        resultsOutput.innerHTML = `<div class="error">${message}</div>`;
        resultsOutput.style.color = '#ff4444';
    } else {
        alert(message);
    }
}
