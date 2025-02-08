async function summarizeFile() {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please upload a file to summarize.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    const endpoint = file.name.endsWith('.pdf')
    ? 'http://127.0.0.1:5000/summarize/pdf'
    : file.name.endsWith('.docx')
    ? 'http://127.0.0.1:5000/summarize/word'
    : null;

    if (!endpoint) {
        alert('Unsupported file format. Please upload a PDF or Word file.');
        return;
    }

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error('Failed to summarize the file. Please try again.');
        }

        const data = await response.json();
        document.getElementById('summary-output').innerText = data.summary || 'No summary generated.';
    } catch (error) {
        alert('Error: ' + error.message);
        console.error(error);
    }
}
