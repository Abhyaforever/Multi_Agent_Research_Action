// main.js - improved UI logic for styled research output
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
    data.sections.forEach((section, idx) => {
        html += `
            <div class="card">
                <h2 class="section-title">Subtask ${idx + 1}: ${section.title}</h2>
                <div class="prose max-w-none">
                    ${formatContent(section.content)}
                </div>
            </div>
        `;
    });
    if (data.conclusion) {
        html += `
            <div class="card border-t-4 border-blue-500">
                <h2 class="section-title text-blue-700">Conclusion</h2>
                <div class="prose max-w-none">
                    ${formatContent(data.conclusion)}
                </div>
            </div>
        `;
    }
    resultsDiv.innerHTML = html;
}

function formatContent(content) {
    return content
        .split('\n\n')
        .map(para => {
            const withLinks = para.replace(/(https?:\/\/[^\s]+)/g, url =>
                `<a href="${url}" target="_blank">${url}</a>`
            );
            return `<p>${withLinks}</p>`;
        })
        .join('');
}

document.getElementById('queryInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        submitQuery();
    }
});
