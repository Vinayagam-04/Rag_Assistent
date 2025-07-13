document.getElementById('upload-form').addEventListener('submit', function(e) {
    const fileInput = document.getElementById('document');
    if (!fileInput.files.length) {
        e.preventDefault();
        alert('Please select a file to upload.');
    }
});

document.getElementById('query-form').addEventListener('submit', function(e) {
    const queryInput = document.getElementById('query');
    if (!queryInput.value.trim()) {
        e.preventDefault();
        alert('Please enter a query.');
    }
});