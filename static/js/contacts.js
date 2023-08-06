    const csrfToken = '{{ csrf_token }}';

    // Функция для обновления списка пользователей
    function updateUsersList() {
        fetch('/chat/chats_list/', {
            method: 'POST',  // Используем метод POST для получения данных
            headers: {
                'Content-Type': 'application/json',  // Устанавливаем заголовок Content-Type для JSON данных
                'X-CSRFToken': '{{ csrf_token }}'  // Если используется CSRF защита, передайте CSRF токен
            },
            body: JSON.stringify({})  // Пустой объект, если не требуется передача данных
        })
        .then(response => response.json())
        .then(data => {
            // Обработка успешного ответа от сервера

            // Очищаем текущий список пользователей
            $("#chat-list").empty();

            // Добавляем новые данные в список
            data.users_with_common_chats.forEach(function(user) {
                var listItem = '<li>' +
                    '<a href="/chat/room/' + user.username + '">' +
                    '<div class="chat-user">' +
                    '<img class="avatar" src="' + (user.avatar_url ? user.avatar_url : '{% static "img/def.jpg" %}') + '" alt="Avatar">' +
                    '<div class="user-info">' +
                    '<div class="username">' + user.username + '</div>';

                if (user.has_both_permissions) {
                    listItem += '<div class="username">' + user.first_name + ' ' + user.last_name + '</div>';
                }

                if (user.last_message) {
                    listItem += '<div class="last-message">' + user.last_message + '</div>';
                }

                listItem += '</div>' +
                    '</div>' +
                    '</a>' +
                    '</li>';

                $("#chat-list").prepend(listItem);
            });
        })
        .catch(error => {
            // Обработка ошибки
            console.error("Error:", error);
        });
    }

    // Вызываем функцию для обновления списка пользователей при загрузке страницы
    updateUsersList();

    // Выполняем обновление списка пользователей через определенный интервал времени (например, каждые 10 секунд)
    setInterval(updateUsersList, 10000);