const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");

menuBtn.addEventListener('click',()=> {
    sideMenu.style.display = 'block';
});

closeBtn.addEventListener('click',()=>{
    sideMenu.style.display = 'none';
})

themeToggler.addEventListener('click',()=>{
    document.body.classList.toggle('dark-theme-variables');
    
    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');

})

function updateCounts() {
    // Get the current counts
    var count1 = parseInt(document.getElementById("count1").innerText);
    var count2 = parseInt(document.getElementById("count2").innerText);
    var count3 = parseInt(document.getElementById("count3").innerText);

    // Update the counts
    document.getElementById("count1").innerText = count1 + 1;
    document.getElementById("count2").innerText = count2 + 1;
    document.getElementById("count3").innerText = count3 + 1;
}

// Update counts every 10 seconds
setInterval(updateCounts, 10000);