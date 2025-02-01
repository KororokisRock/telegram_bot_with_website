const mainArray = document.querySelectorAll("main");
const navA = document.querySelectorAll(".nav-a");
const mainWord = document.querySelector(".main-word");
const answerMake = document.querySelectorAll(".answer-make");
const menu = document.getElementById("menu");


let currentSlogan;
let isAdmin = false;

//массив со слоганами
const slogans = [
  "Задай вопрос — получи ответ!",
  "Твоя помощь — твой успех!",
  "Вместе легче учиться!",
  "Задавай, учись,  помогай!",
  "Учись, делясь знаниями!",
  "Поделись опытом — стань мастером!",
  "Вместе к успеху в учебе!",
  "Твоя помощь — наш общий успех!",
  "Где есть вопросы, там есть и ответы!",
  "Помогай другим — учись сам!",
  "Учеба с друзьями — проще и интереснее!",
  "Знания в обмен на помощь!",
  "Поддержка друг друга— залог успеха!",
  "Сложные задачи? Вместе решим!",
  "Учись, помогая другим расти!",
  "Твои знания — твой капитал!",
  "Соберем команду для учебных побед!",
  "Помощь в учебе — это просто!",
  "Делись знаниями, получай поддержку!",
  "Задавай вопросы, находи друзей!",
  "Учеба без стресса — помогай и получай!",
  "Обмен знаниями — путь к успеху!",
  "Помоги другому — вырасти сам!",
];

//навигация
navA.forEach((link, index) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();

    navA.forEach((navA) => {
      navA.classList.remove("active");
    });
    mainArray.forEach((main) => {
      main.classList.remove("show");
      main.classList.remove("fade-in");
    });

    if (navA[index]) {
      navA[index].classList.add("active");
    }
    if (mainArray[index]) {
      mainArray[index].classList.add("show");
      setTimeout(() => {
        mainArray[index].classList.add("fade-in");
      }, 10);
    }
  });
});


if (isAdmin) {
  // Если админ, показываем диву
  document.querySelector('.admin').classList.remove('hidden'); 
}


//функция смены слоганов
function changeSlogan() {
  currentSlogan = mainWord.innerHTML;

  const randomIndex = Math.floor(Math.random() * slogans.length);
  const newSlogan = slogans[randomIndex];

  // Проверяем, равен ли новый слоган текущему
  if (newSlogan === currentSlogan) {
    return; // Если равны, выходим из функции
  }

  mainWord.style.opacity = 0;
  setTimeout(() => {
    mainWord.innerHTML = newSlogan;
    currentSlogan = newSlogan; // Обновляем текущий слоган
    mainWord.style.opacity = 1;
  }, 500);
}

menu.addEventListener("click", () => {
  if (menu.parentElement.classList.contains("responsive")) {
    menu.parentElement.classList.remove("responsive");
  } else {
    menu.parentElement.classList.add("responsive");
  }
});


setInterval(changeSlogan, 4000);
