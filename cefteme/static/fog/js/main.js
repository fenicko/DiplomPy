// window.onload = function() {
//   var paragraphs = document.getElementsByClassName('card-text');
//   for (var i = 0; i < paragraphs.length; i++) {
//     var paragraph = paragraphs[i];
//     var text = paragraph.innerText;
//     var newText = text.slice(0, -1) + '.';
//     paragraph.innerText = newText;
//   }
// };

function reloadPage() {
  setTimeout(function() {
     location.reload();
  }, 10);
}

// Загрузка jQuery из CDN
var script = document.createElement('script');
script.src = 'https://code.jquery.com/jquery-3.6.0.min.js';
document.head.appendChild(script);

// Получение CSRF-токена из cookie
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Имя cookie начинается с "csrftoken="
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Ожидание загрузки документа
document.addEventListener('DOMContentLoaded', function() {
  // Назначение обработчика события на изменение поля ввода с именем "basketID"
  var inputFields = document.getElementsByName('basketID');
  for (var i = 0; i < inputFields.length; i++) {
    inputFields[i].addEventListener('change', function() {
      var basketId = this.dataset.id;
      var quantity = this.value;

      // Получение CSRF-токена
      var csrftoken = getCookie('csrftoken');

      // Отправка AJAX-запроса
      var xhr = new XMLHttpRequest();
      xhr.open('POST', basketUpdateURL, true);
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
      xhr.onload = function() {
        if (xhr.status === 200) {
          // Обработка успешного ответа от сервера
          location.reload();
          var response = JSON.parse(xhr.responseText);
          if (response && response.basketSum) {
            basket.sum = response.basketSum;

            // Дополнительные действия после успешного обновления basket.sum
          }
        } else {
          // Обработка ошибки, если необходимо
        }
      };
      xhr.onerror = function() {
        // Обработка ошибки, если необходимо
      };
      xhr.send('basketId=' + encodeURIComponent(basketId) + '&quantity=' + encodeURIComponent(quantity));
    });
  }
});
