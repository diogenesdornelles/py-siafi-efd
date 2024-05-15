const loading = document.getElementById('loading');
addEventListener('py:ready', () => loading.close());
loading.showModal();
