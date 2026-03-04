document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('async-search-form');
    const resultsContainer = document.getElementById('quick-results');
    const searchBar = document.getElementById('q');
    let timeout;

    if (!form || !resultsContainer || !searchBar) return;

    const apiUrl = form.dataset.apiUrl;
    if (!apiUrl) return;

    async function fetchAndRender(url) {
        try {
            const resp = await fetch(url, { headers: { 'Accept': 'application/json' } });
            if (!resp.ok) throw new Error(`Network response was not ok: ${resp.status}`);
            const data = await resp.json();
            renderResults(data);
        } catch (err) {
            resultsContainer.innerHTML = '<p>Error fetching results</p>';
            console.error(err);
        }
    }

    function renderResults(data){
        if(!data || !data.genres || data.genres.length === 0){
            resultsContainer.innerHTML = '<p>No results</p>';
            return;
        }

        resultsContainer.innerHTML = '';
        const genreBox = document.createElement('div');
        const ul = document.createElement('ul');

        data.genres.forEach(genre => {
            const genreItem = document.createElement('li');
            genreItem.className = 'quick-result-item';
            genreItem.textContent = genre;
            ul.appendChild(genreItem);
        });
        genreBox.appendChild(ul);
        resultsContainer.appendChild(genreBox);
    }

/*
FOR FULL RESULTS (WITH BOOKS):
    function renderResults(data) {
        resultsContainer.innerHTML = '';
        if (!data || !data.genres || data.genres.length === 0) {
            resultsContainer.innerHTML = '<p>No results</p>';
            return;
        }

        data.genres.forEach(genre => {
            const genreBox = document.createElement('div');
            genreBox.className = 'result-item';
            const h3 = document.createElement('h3');
            h3.textContent = genre.genre_name;
            genreBox.appendChild(h3);

            const ul = document.createElement('ul');
            genre.books.forEach(book => {
                const li = document.createElement('li');
                li.textContent = `${book.name} — ${book.author}`;
                ul.appendChild(li);
            });

            genreBox.appendChild(ul);
            resultsContainer.appendChild(genreBox);
        });
    }
*/
    searchBar.addEventListener('input', (e) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            const currentValue = (e.target.value || '').trim();

            if (currentValue === '') {
                resultsContainer.innerHTML = '';
                return;
            }

            const url = new URL(apiUrl, window.location.origin);
            url.search = new URLSearchParams({ q: currentValue }).toString();
            fetchAndRender(url.toString());
        }, 100);
    })

    // Once the genres appear, they should be clickable -> sends user to genre page

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const q = document.getElementById('q').value || '';
        const typeInput = document.querySelector('input[name="type"]:checked');
        const type = typeInput ? typeInput.value : '';

        const url = new URL(apiUrl, window.location.origin);
        const params = new URLSearchParams();
        params.set('q', q);
        if (type) params.set('type', type);
        url.search = params.toString();
        fetchAndRender(url.toString());
    });
});
