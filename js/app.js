const map = L.map('map', {
    crs: L.CRS.Simple,
    minZoom: 0,
    maxZoom: 4, // Expanded to allow deep street-level zooming
    zoomControl: false
});

L.tileLayer('tiles/{z}/{x}/{y}.png', {
    tileSize: 200,
    noWrap: true,
    tms: true,
    minZoom: 0,
    maxZoom: 4
}).addTo(map);

// Center precisely on Hexham town center coordinates for your grid
map.setView([400, 600], 1);

// --- BOTTOM SHEET UI ELEMENTS ---
const bottomSheet = document.getElementById('bottomSheet');
const sheetContent = document.getElementById('sheetContent');
const closeSheetBtn = document.getElementById('closeSheet');

function openSheet(item) {
    sheetContent.innerHTML = `
        <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold px-2.5 py-1 bg-blue-50 text-blue-600 rounded-full">${item.category}</span>
            <span class="text-xs text-gray-500 font-medium">${item.openingHours}</span>
        </div>
        <h2 class="text-xl font-bold text-gray-900 mb-1">${item.name}</h2>
        <p class="text-sm text-gray-600 mb-4">${item.address}</p>
        
        <p class="text-sm text-gray-700 leading-relaxed mb-6">${item.fullDescription}</p>
        
        <div class="flex gap-3">
            ${item.website ? `<a href="${item.website}" target="_blank" class="flex-1 bg-blue-600 text-white text-center py-2.5 px-4 rounded-xl font-medium text-sm shadow-sm hover:bg-blue-700 transition-colors">Visit Website</a>` : ''}
            ${item.menuUrl ? `<a href="${item.menuUrl}" target="_blank" class="flex-1 bg-gray-100 text-gray-800 text-center py-2.5 px-4 rounded-xl font-medium text-sm hover:bg-gray-200 transition-colors">View Menu</a>` : ''}
        </div>
    `;
    bottomSheet.classList.remove('translate-y-full');
}

function closeSheet() {
    bottomSheet.classList.add('translate-y-full');
}

closeSheetBtn.addEventListener('click', closeSheet);

// Close sheet when tapping on the map background
map.on('click', closeSheet);

// --- RENDER PINS FROM DATA ---
const markersLayer = L.layerGroup().addTo(map);

function renderPins(dataToRender) {
    markersLayer.clearLayers();

    dataToRender.forEach(item => {
        const marker = L.marker(item.coords);

        // Bind click event to open bottom sheet instead of a popup
        marker.on('click', (e) => {
            L.DomEvent.stopPropagation(e); // Prevent map click from closing it instantly
            openSheet(item);
            map.setView(item.coords, 1); // Center map slightly on pin
        });

        markersLayer.addLayer(marker);
    });
}

renderPins(touristData);

// --- SEARCH & FILTER LOGIC ---
const searchInput = document.getElementById('searchInput');
const filterButtons = document.querySelectorAll('.filter-btn');

let currentCategory = 'all';
let searchQuery = '';

function filterAndRender() {
    const filtered = touristData.filter(item => {
        // Check category match
        const matchesCategory = currentCategory === 'all' || item.category === currentCategory;
        
        // Check search query match (name, description, or category)
        const query = searchQuery.toLowerCase();
        const matchesSearch = item.name.toLowerCase().includes(query) ||
                              item.shortDescription.toLowerCase().includes(query) ||
                              item.category.toLowerCase().includes(query);

        return matchesCategory && matchesSearch;
    });

    renderPins(filtered);
}

// Search input listener
searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value;
    filterAndRender();
});

// Category filter button listeners
filterButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        // Update active styling on pills
        filterButtons.forEach(btn => {
            btn.classList.remove('bg-blue-600', 'text-white');
            btn.classList.add('bg-white/90', 'text-gray-700', 'border', 'border-gray-200');
        });
        e.target.classList.remove('bg-white/90', 'text-gray-700', 'border', 'border-gray-200');
        e.target.classList.add('bg-blue-600', 'text-white');

        // Apply filter category
        currentCategory = e.target.getAttribute('data-category');
        filterAndRender();
    });
});