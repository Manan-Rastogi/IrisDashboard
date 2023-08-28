// Function to handle login form submission
document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("login-form");
    
    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault();
            
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.token) {
                    sessionStorage.setItem('jwtToken', data.token);
                    window.location.href = '/index';
                } else {
                    document.getElementById("error-message").innerText = "Invalid Credentials";
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    }
});

// Function to fetch data and render histogram
function renderHistogram() {
    const species = document.getElementById("species").value;
    const feature = document.getElementById("feature").value;
    const bins = 10;
    
    fetch(`/get_histogram?species=${species}&feature=${feature}&bins=${bins}`)
    .then(response => response.json())
    .then(data => {
        // Render histogram using Plotly
        Plotly.newPlot('histogram-plot', data.histogramData).then(function(gd) {
            gd.on('plotly_click', function(data) {
                const point = data.points[0];
                const bin_start = point.x;
                const bin_end = bin_start + point.xbins.size;
                
                // Trigger CSV download
                window.location.href = `/download_csv?species=${species}&feature=${feature}&bin_start=${bin_start}&bin_end=${bin_end}`;
            });
        });
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Function to fetch data and render line chart
function renderLineChart() {
    const species = document.getElementById("species").value;
    const feature = document.getElementById("feature").value;
    
    fetch(`/get_line_chart?species=${species}&feature=${feature}`)
    .then(response => response.json())
    .then(data => {
        // Render line chart using Plotly
        Plotly.newPlot('line-chart', data.lineChartData);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Attach event listener to form submit
const mainForm = document.getElementById("iris-form");
if (mainForm) {
    mainForm.addEventListener("submit", function(event) {
        event.preventDefault();
        renderHistogram();
        renderLineChart();
    });
}
