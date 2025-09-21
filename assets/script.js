const yearEl=document.getElementById('year');if(yearEl){yearEl.textContent=new Date().getFullYear();}
const toggle=document.querySelector('.nav-toggle');const menu=document.querySelector('.nav-links');if(toggle){toggle.addEventListener('click',()=>menu.classList.toggle('open'));}
