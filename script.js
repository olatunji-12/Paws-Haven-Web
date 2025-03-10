function openModal(name) {
    document.getElementById('dog-name').textContent = name;
    new bootstrap.Modal(document.getElementById('modal')).show();
}