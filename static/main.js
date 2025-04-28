// main.js - handles UI logic for research system
async function submitQuery() {
    const query = document.getElementById('queryInput').value;
    if (!query) return;

    // Show loading
    document.querySelector('.loading').classList.add('active');
    document.getElementById('results').innerHTML = '';

    try {
        const response = await fetch('/research', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });

        const data = await response.json();
        if (data.error) {
            showError(data.error);
        } else {
            showResults(data);
        }
    } catch (error) {
        showError('An error occurred while processing your request.');
    } finally {
        document.querySelector('.loading').classList.remove('active');
    }
}

function showError(message) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `
        <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded">
            <p>${message}</p>
        </div>
    `;
}

function showResults(data) {
    const resultsDiv = document.getElementById('results');
    let html = '';
    data.sections.forEach(section => {
        html += `
            <div class="bg-white rounded-lg shadow-lg p-6">
                <h2 class="text-2xl font-semibold mb-4 text-gray-800">${section.title}</h2>
                <div class="prose max-w-none">
                    ${formatContent(section.content)}
                </div>
            </div>
        `;
    });
    if (data.conclusion) {
        html += `
            <div class="bg-blue-50 rounded-lg shadow-lg p-6">
                <h2 class="text-2xl font-semibold mb-4 text-blue-800">Conclusion</h2>
                <div class="prose max-w-none text-blue-900">
                    ${formatContent(data.conclusion)}
                </div>
            </div>
        `;
    }
    if (data.analysis) {
        html += `
            <div class="bg-green-50 rounded-lg shadow-lg p-6">
                <h2 class="text-2xl font-semibold mb-4 text-green-800">Analysis (Stub)</h2>
                <div class="prose max-w-none text-green-900">
                    ${data.analysis.map(a => `<p>${a}</p>`).join('')}
                </div>
            </div>
        `;
    }
    if (data.communications) {
        html += `
            <div class="bg-yellow-50 rounded-lg shadow-lg p-6">
                <h2 class="text-2xl font-semibold mb-4 text-yellow-800">Communications (Stub)</h2>
                <div class="prose max-w-none text-yellow-900">
                    ${data.communications.map(c => `<p>${c}</p>`).join('')}
                </div>
            </div>
        `;
    }
    resultsDiv.innerHTML = html;
}

function formatContent(content) {
    return content.split('\n\n').map(para => 
        `<p>${para.replace(/\n/g, '<br>')}</p>`
    ).join('');
}

document.getElementById('queryInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        submitQuery();
    }
});
