


document.addEventListener('DOMContentLoaded', function () {
    const regionsList = document.getElementById('regionsList');
    const modalBody = document.getElementById('locationModalBody');
    const selectedLabel = document.getElementById('selectedLocationLabel');
    const allBtn = document.getElementById('allUzbekistanBtn');

   
    

    // Клик по области — грузим районы
    regionsList.addEventListener('click', function (e) {
        const btn = e.target.closest('.region-btn');
        if (!btn) return;

        const regionId = btn.dataset.id;
        const regionName = btn.dataset.name;

        fetch(`/locations/get-children/?parent_id=${regionId}`)
            .then(response => response.json())
            .then(districts => {
                showDistricts(regionId, regionName, districts);
            });
    });

    function showDistricts(regionId, regionName, districts) {
        let html = `
            <button type="button" class="btn btn-link mb-2" id="backToRegionsBtn">&larr; Назад к областям</button>
            <button type="button" class="list-group-item list-group-item-action mb-2 select-location-btn" data-id="${regionId}" data-name="${regionName}">
                Весь ${regionName}
            </button>
            <div class="list-group">
        `;
        districts.forEach(d => {
            html += `<button type="button" class="list-group-item list-group-item-action select-location-btn" data-id="${d.id}" data-name="${d.name}">${d.name}</button>`;
        });
        html += `</div>`;

        modalBody.innerHTML = html;

        document.getElementById('backToRegionsBtn').addEventListener('click', resetModal);

        document.querySelectorAll('.select-location-btn').forEach(b => {
            b.addEventListener('click', function () {
                selectLocation(this.dataset.id, this.dataset.name);
            });
        });
    }

    function resetModal() {
        location.reload(); // проще всего — просто перезагрузить модалку в исходное состояние
    }

    function selectLocation(id, name) {
        selectedLabel.textContent = name;
        window.location.href = `/?location=${id}`;
    }

    allBtn.addEventListener('click', function () {
        window.location.href = `/`;
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // ... существующий код ...

    const searchInput = document.getElementById('locationSearchInput');

    searchInput.addEventListener('input', function () {
        const query = this.value.toLowerCase();
        const items = modalBody.querySelectorAll('.list-group-item');
        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(query) ? '' : 'none';
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('shopsContainer');
    const trigger = document.getElementById('scrollTrigger');
    if (!container || !trigger) return;

    let loading = false;

    const observer = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting && !loading) {
            loadMore();
        }
    });
    observer.observe(trigger);

    function loadMore() {
        loading = true;
        const page = container.dataset.nextPage;
        const location = container.dataset.location;

        fetch(`/?page=${page}&location=${location}&ajax=1`, {
            
        })
            .then(response => {
                if (response.redirected || !response.ok) {
                    trigger.remove();
                    return null;
                }
                return response.text();
            })
            .then(html => {
                if (!html || html.trim() === '') {
                    trigger.remove();
                    return;
                }
                container.insertAdjacentHTML('beforeend', html);
                container.dataset.nextPage = parseInt(page) + 1;
                loading = false;
            });
    }
});