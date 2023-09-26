
// turn on and off based on chosen option
function toggleDropdowns() {
    const regionDropdown = document.getElementById('search by');
    const countriesDropdown = document.getElementById('flavors');
    const continentsDropdown = document.getElementById('producents');

    if (regionDropdown.value === 'flavors') {
        countriesDropdown.disabled = false;
        continentsDropdown.disabled = true;
        continentsDropdown.selectedIndex = 0;
    } else if (regionDropdown.value === 'producents') {
        countriesDropdown.disabled = true;
        countriesDropdown.selectedIndex = 0;
        continentsDropdown.disabled = false;
    } else {
        countriesDropdown.disabled = true;
        continentsDropdown.disabled = true;
        countriesDropdown.selectedIndex = 0;
        continentsDropdown.selectedIndex = 0;
    }
}

window.addEventListener('load', (event) => {
    const countriesDropdown = document.getElementById('flavors');
    const continentsDropdown = document.getElementById('producents');

    countriesDropdown.disabled = true;
    continentsDropdown.disabled = true;
});


const btn = document.querySelector("button");
btn.onclik = ()=>{
    widget.style.display = "none";
}