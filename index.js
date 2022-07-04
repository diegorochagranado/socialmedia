document.querySelector("#login").addEventListener("click",function(){
    document.querySelector(".popup").classList.add("active");
})

document.querySelector(".popup .close-btn").addEventListener("click",function(){
    document.querySelector(".popup").classList.remove("active");
})

document.querySelector("#signup").addEventListener("click",function(){
    document.querySelector(".popup-signup").classList.add("active");
})

document.querySelector(".popup-signup .close-btn").addEventListener("click",function(){
    document.querySelector(".popup-signup").classList.remove("active");
})
