document.addEventListener('DOMContentLoaded', () => {
    const predictionResult = document.getElementById('predictionResult');
    const accuracyResult = document.getElementById('accuracyResult');
    const accuracyFill = document.getElementById('accuracyFill');

    // Get submitted URL from sessionStorage
    const url = sessionStorage.getItem('submittedURL');
    
    if (!url) {
        showError('Please provide a URL');
        return;
    }

    // Check if URL is from trusted sources
    const isTrustedSource = url.toLowerCase().includes('amazon.') || 
                          url.toLowerCase().includes('flipkart.') || 
                          url.toLowerCase().includes('meesho.');

    // Get visit count for this URL from localStorage
    let urlVisits = JSON.parse(localStorage.getItem('urlVisits') || '{}');
    const currentCount = urlVisits[url] || 0;
    urlVisits[url] = currentCount + 1;
    localStorage.setItem('urlVisits', JSON.stringify(urlVisits));

    // Determine if it's fake based on visit count
    const isFakeByVisits = urlVisits[url] >= 4;

    // Show analyzing state briefly
    predictionResult.textContent = 'Analyzing...';
    accuracyResult.textContent = 'Calculating...';

    // Simulate analysis with setTimeout
    setTimeout(() => {
        // Determine final prediction
        let isFake = !isTrustedSource || isFakeByVisits;
        
        // Update prediction display
        if (isFake) {
            predictionResult.textContent = '❌ FAKE';
            predictionResult.className = 'prediction-value fake';
            predictionResult.style.color = '#f44336';
            predictionResult.style.textShadow = '0 0 15px rgba(244, 67, 54, 0.3)';
        } else {
            predictionResult.textContent = '✅ REAL';
            predictionResult.className = 'prediction-value real';
            predictionResult.style.color = '#4CAF50';
            predictionResult.style.textShadow = '0 0 15px rgba(76, 175, 80, 0.3)';
        }

        // Generate accuracy based on condition
        let accuracy;
        if (isFake) {
            // Lower accuracy for fake predictions
            accuracy = Math.floor(Math.random() * (85 - 70 + 1)) + 70;
        } else {
            // Higher accuracy for real predictions
            accuracy = Math.floor(Math.random() * (99 - 90 + 1)) + 90;
        }

        // Animate accuracy
        let currentAccuracy = 0;
        const duration = 1500;
        const interval = 10;
        const steps = duration / interval;
        const increment = accuracy / steps;

        const accuracyAnimation = setInterval(() => {
            currentAccuracy += increment;
            if (currentAccuracy >= accuracy) {
                currentAccuracy = accuracy;
                clearInterval(accuracyAnimation);
            }

            // Update accuracy display
            accuracyResult.textContent = currentAccuracy.toFixed(1) + '%';
            accuracyFill.style.width = currentAccuracy + '%';

            // Update color based on accuracy
            if (currentAccuracy > 90) {
                accuracyFill.style.background = 'linear-gradient(90deg, #4CAF50, #45a049)';
            } else if (currentAccuracy > 75) {
                accuracyFill.style.background = 'linear-gradient(90deg, #2196F3, #1976D2)';
            } else {
                accuracyFill.style.background = 'linear-gradient(90deg, #FFC107, #FFA000)';
            }
        }, interval);

        // Add source information
        let source = "Unknown Source";
        if (url.toLowerCase().includes('amazon.')) source = "Amazon";
        else if (url.toLowerCase().includes('flipkart.')) source = "Flipkart";
        else if (url.toLowerCase().includes('meesho.')) source = "Meesho";

        // Show visit count warning if needed
       
    }, 1500); // 1.5 second delay for analysis simulation
});

function showError(message) {
    const predictionResult = document.getElementById('predictionResult');
    const accuracyResult = document.getElementById('accuracyResult');
    const accuracyFill = document.getElementById('accuracyFill');
    
    predictionResult.textContent = '❌ ' + message;
    predictionResult.style.color = '#f44336';
    accuracyResult.textContent = 'N/A';
    accuracyFill.style.width = '0%';
} 