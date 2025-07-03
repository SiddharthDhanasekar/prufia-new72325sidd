
document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.menu-item');
    const contentArea = document.getElementById('teacher-content');
    
    function loadContent(contentType) {
        contentArea.innerHTML = '<div class="loading">Loading...</div>';
        
        fetch(`/${contentType}-content`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.text();
            })
            .then(html => {
                contentArea.innerHTML = html;
                
                // Initialize scripts for the loaded content
                if (contentType === 'matches') {
                    initMatchesPage();
                }
            })
            .catch(error => {
                contentArea.innerHTML = `<div class="error">Error loading content: ${error.message}</div>`;
                console.error('Error:', error);
            });
    }
    function initMatchesPage() {
        // Load matches.js dynamically
        const script = document.createElement('script');
        script.src = "{{ url_for('static', filename='js/teacher/matches.js') }}";
        script.onload = function() {
            console.log('Matches script loaded successfully');
        };
        document.body.appendChild(script);
    }


    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            menuItems.forEach(menuItem => menuItem.classList.remove('active'));
            this.classList.add('active');
            loadContent(this.dataset.content);
        });
    });
    
    // Load initial content
    document.querySelector('.menu-item[data-content="matches"]').click();
});
    
    
   
        function displayUploadResults(data) {
            const resultsDiv = document.getElementById('uploadResults');
            resultsDiv.innerHTML = '<h4><i class="fas fa-check-circle"></i> Uploaded successfully</h4>';           
        }

  
        function populateFilterOptions(data, property, selectElement) {
            const uniqueValues = [...new Set(data.map(item => item[property]))];
            uniqueValues.forEach(value => {
                const option = document.createElement('option');
                option.value = value;
                option.textContent = value;
                selectElement.appendChild(option);
            });
        }
        