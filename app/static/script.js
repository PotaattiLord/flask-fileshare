// Theme toggle functionality

const toggleButton = document.getElementById('theme-toggle');
const body = document.body;

// Check for saved preference, otherwise use system preference
const savedTheme = localStorage.getItem('theme');
const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
  body.classList.add('dark-theme');
}

// Toggle theme on button click
toggleButton.addEventListener('click', () => {
  body.classList.toggle('dark-theme');
  
  // Save preference to LocalStorage
  if (body.classList.contains('dark-theme')) {
    localStorage.setItem('theme', 'dark');
  } else {
    localStorage.setItem('theme', 'light');
  }
});

document.getElementById('togglePublicFiles').addEventListener('change', function() {
  const publicFiles = document.querySelectorAll('.public-files');
  publicFiles.forEach(file => {
    file.style.display = this.checked ? 'block' : 'none';
  });
});

document.getElementById('togglePrivateFiles').addEventListener('change', function() {
  const privateFiles = document.querySelectorAll('.private-files');
  privateFiles.forEach(file => {
    file.style.display = this.checked ? 'block' : 'none';
  });
});

document.getElementById('downloadSelectedFiles').style.display = 'none';

var fileCheckboxes = document.querySelectorAll('.file-checkbox');
fileCheckboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        var filename = this.getAttribute('data-filename');
        if (this.checked) {
            console.log('Selected file: ' + filename);
        } else {
            console.log('Deselected file: ' + filename);
        }
        if (document.querySelectorAll('.file-checkbox:checked').length > 0) {
            document.getElementById('downloadSelectedFiles').style.display = 'inline-block';
        } else {
            document.getElementById('downloadSelectedFiles').style.display = 'none';
        }
    });
});

document.getElementById('fileNameFilter').addEventListener('input', function() {
    var filterValue = this.value.toLowerCase();
    var files = document.querySelectorAll('.file-item');
    files.forEach(function(file) {
        var fileName = file.querySelector('p').textContent.toLowerCase();
        if (fileName.includes(filterValue)) {
            file.style.display = 'flex';
        } else {
            file.style.display = 'none';
        }
    });
});

document.getElementById('downloadSelectedFiles').addEventListener('click', function() {
    var selectedFiles = [];
    fileCheckboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            selectedFiles.push(checkbox.getAttribute('data-filename'));
        }
    });

    if (selectedFiles.length > 0) {
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = '/download_selected_files';

        selectedFiles.forEach(function(file) {
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'files[]';
            input.value = file;
            form.appendChild(input);
        });

        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
    } else {
        alert('No files selected for download.');
    }
});